"""Accuracy patches applied to content fragments, driven by facts extracted from the engine source."""
import re, json
from bs4 import BeautifulSoup
from html import escape

INTERNAL = re.compile(r'^_')
# component -> script-API module file
API_MODULE = {'Transform':'TransformAPI','SpriteRenderer':'SpriteAPI','ShapeRenderer':'ShapeAPI','TextRenderer':'TextAPI','StrokePath':'StrokePathAPI',
 'SpeechBubble':'SpeechBubbleAPI','ChatLog':'ChatLogAPI','TextInput':'TextInputAPI','Joystick':'JoystickAPI','Rigidbody2D':'RigidbodyAPI','Collider2D':'ColliderAPI',
 'Joint2D':'JointAPI','CharacterController':'ControllerAPI','SpriteAnimation':'AnimatorAPI','Camera':'CameraAPI','AudioSource':'AudioAPI','AudioListener':'AudioListenerAPI',
 'Light':'LightAPI','ShadowCaster':'ShadowCasterAPI','LightingSettings':'LightingSettingsAPI','NavAgent2D':'NavAgentAPI'}

TEXT_FIXES = [
 ('X-Vaelis-Standalone-Export', 'X-ZenEngine-Standalone-Export'),
 ('X-Vaelis-Export-Format', 'X-ZenEngine-Export-Format'),
 ('phyg-updated.zip', 'the Vaelis client distribution'),
 ('standalone runtime directory/', '<code>project/player/</code>'),
 ('standalone runtime directory', '<code>project/player/</code>'),
]

def first_sentence(s, n=170):
    s = re.sub(r'\s+', ' ', s).strip()
    m = re.match(r'(.{20,%d}?[.!?])(\s|$)' % n, s)
    if m: return m.group(1)
    if len(s) <= n: return s
    return s[:n].rsplit(' ', 1)[0].rstrip(',;:( -') + '…'

def fmt_default(f):
    d = f['default']
    if f['kind'] == 'array' or d.startswith('['):
        pts = re.findall(r'\{[^{}]*\}', d)
        return '[' + ', '.join(re.sub(r'\s+', '', p) for p in pts) + ']' if pts else '[]'
    return d

def kind_label(f, enums):
    k = f['kind'] or ''
    if k.startswith('enum:'):
        vals = list(enums[k[5:]].values()); return ' | '.join(vals)
    d = f['default']
    if f['name'] in ('color', 'backgroundColor', 'fillColor', 'barColor') or (k == 'string' and d.startswith('#')): return 'hex string'
    return {'boolean': 'boolean', 'number': 'number', 'string': 'string', 'array': 'array', 'object': 'object', 'null': ('string | null' if re.search(r'(Id|Key)$', f['name']) else 'number | null' if f['name'].startswith(('drive','_script')) else 'value | null')}.get(k, k or 'value')

def patch_component_table(soup, name, facts):
    comp = facts['components'].get(name)
    if not comp: return []
    h = next((x for x in soup.find_all('h2') if x.get_text(strip=True) == 'Component data'), None)
    if not h: return []
    tb = h.find_next('table'); rows = {}
    for tr in tb.find_all('tr')[1:]:
        td = tr.find_all('td')
        if len(td) >= 4: rows[td[0].get_text(strip=True)] = [c.decode_contents() for c in td]
    changes = []; body = []
    for f in comp['fields']:
        if INTERNAL.match(f['name']): continue
        old = rows.get(f['name']); dflt = fmt_default(f)
        typ = kind_label(f, facts['enums'])
        purpose = escape(first_sentence(f['comment'])) if f['comment'] else ''
        if old:
            if BeautifulSoup(old[3], 'html.parser').get_text(strip=True) != dflt: changes.append(f"{name}.{f['name']} default → {dflt}")
            old_type = BeautifulSoup(old[1], 'html.parser').get_text(strip=True)
            # keep hand-written prose; refresh type only if it was a bare enum-type mismatch
            body.append([f"<code>{escape(f['name'])}</code>", old[1], old[2], f'<code>{escape(dflt)}</code>'])
        else:
            changes.append(f"{name}.{f['name']} added")
            engine_managed = f['name'].startswith(('request', 'drive', 'pending', 'resolved')) or f['name'] in ('grounded','x','y','magnitude','angle','active','baseScreenX','baseScreenY','currentPath','currentPathIndex','hideTimer','frameElapsed','focused','justSubmitted')
            tag = ' <em>(engine-managed runtime state)</em>' if engine_managed else ''
            if engine_managed: purpose = 'Written by the engine each frame; not an authored setting.' if not f['name'].startswith(('drive','request')) else 'Set transiently by the engine (controller/navigation input); not an authored setting.'
            body.append([f"<code>{escape(f['name'])}</code>", escape(typ), (purpose or 'See the Inspector field of the same name.') + tag, f'<code>{escape(dflt)}</code>'])
    th = ''.join(f'<th>{c.get_text(strip=True)}</th>' for c in tb.find_all('th'))
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in body)
    new = BeautifulSoup(f'<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>', 'html.parser')
    tb.replace_with(new)
    return changes

def patch_api_table(soup, name, facts):
    mod = API_MODULE.get(name)
    if not mod: return []
    api = facts['api'].get(mod)
    if not api: return []
    h = next((x for x in soup.find_all('h2') if x.get_text(strip=True) == 'Script API'), None)
    if not h: return []
    tb = h.find_next('table')
    have = {re.sub(r'\(.*', '', tr.find('td').get_text(strip=True)) for tr in tb.find_all('tr')[1:]}
    allowed = {m for s in api['member_sets'].values() for m in s}
    add = []
    for m in sorted(allowed):
        if m in have or m not in api['members']: continue
        e = api['members'][m]
        kind = 'Method' if e['method'] else ('Property (read-only)' if e['get'] and not e['set'] else 'Property')
        doc = escape(first_sentence(e['doc'])) if e['doc'] else 'Available on this module.'
        sig = f'{m}(…)' if e['method'] else m
        add.append((sig, kind, doc))
    if name == 'Transform':
        for tr in tb.find_all('tr')[1:]:
            c = tr.find('td').get_text(strip=True)
            if c in ('scaleX', 'scaleY'): tr.decompose()
    if add:
        tbody = tb.find('tbody')
        for sig, kind, doc in add:
            tbody.append(BeautifulSoup(f'<tr><td><code>{escape(sig)}</code></td><td>{kind}</td><td>{doc}</td></tr>', 'html.parser'))
    return [f'{name} script API + {a[0]}' for a in add]

def apply(html, meta, path, facts, log):
    for a, b in TEXT_FIXES:
        if a in html: html = html.replace(a, b); log.append(f'{path}: text fix {a!r}')
    m = re.match(r'api/components/(\w+)$', path)
    if m:
        name = next((c for c in facts['components'] if c.lower() == m.group(1)), None)
        if name:
            soup = BeautifulSoup(html, 'html.parser')
            log += [f'{path}: {c}' for c in patch_component_table(soup, name, facts)]
            log += [f'{path}: {c}' for c in patch_api_table(soup, name, facts)]
            if name == 'Transform':
                s = str(soup)
                s = s.replace('<td><code>scaleX</code></td>', '<td><code>scaleX</code></td>')
                html = s
            else:
                html = str(soup)
    return html
