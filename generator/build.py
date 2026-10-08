#!/usr/bin/env python3
"""Vaelis documentation site generator.

  python3 build.py [--out DIR] [--origin https://docs.example.com] [--facts source-facts.json]

Renders content/**/*.html fragments into a fully static, crawlable site (every page is complete HTML;
JavaScript only enhances it), plus Markdown twins, llms.txt / llms-full.txt, search index, sitemap,
robots.txt and machine-readable API catalogs. Verified against source-facts.json (extract with
tools/extract_source_facts.py <engine_root> source-facts.json)."""
import argparse, json, re, shutil, sys, datetime
from pathlib import Path
from html import escape
from bs4 import BeautifulSoup
from markdownify import markdownify as md
sys.path.insert(0, str(Path(__file__).parent))
from lib.icons import svg, LOGO
from lib.htmlx import process, slugify
from lib import patch

HERE = Path(__file__).parent
ap = argparse.ArgumentParser()
ap.add_argument('--out', default=str(HERE.parent / 'out' / 'vaelis-docs'))
ap.add_argument('--origin', default='')
ap.add_argument('--facts', default=str(HERE / 'source-facts.json'))
args = ap.parse_args()
OUT = Path(args.out); ORIGIN = args.origin.rstrip('/')
VERSION = '1.0.0'; V = f'docs/v{VERSION}'
SITE = 'Vaelis Documentation'
FACTS = json.loads(Path(args.facts).read_text())
CONTENT = HERE / 'content'

# ------------------------------------------------------------------ navigation
NAV = [
 ('Get started', 'rocket', [('Overview','index'),('Installation','getting-started/installation'),('Build your first game','getting-started/first-game'),('Scripting quickstart','getting-started/scripting')]),
 ('Concepts', 'layers', [('Architecture','concepts/architecture'),('Entities & components','concepts/entities-components'),('Game loop & scenes','concepts/game-loop-scenes'),('Coordinate system','reference/coordinate-system')]),
 ('Editor', 'grid', [('Editor overview','editor/overview'),('Controls & exact locations','editor/controls'),('Hierarchy & Inspector','editor/hierarchy-inspector'),('Scenes & projects','editor/scenes-projects'),('Assets & animation','editor/assets-animation'),('Prefab workflow','editor/prefabs'),('Physics authoring','editor/physics'),('Navigation authoring','editor/navigation'),('Lighting, audio & UI','editor/lighting-audio-ui'),('Tilemaps & tilesets','editor/tilemaps'),('Component workflows','editor/component-workflows'),('Complete feature workflows','editor/complete-feature-workflows')]),
 ('Scripting', 'code', [('Lifecycle','scripting/lifecycle'),('Global API','scripting/globals'),('Entity context (this)','scripting/entity-context'),('Entity shortcuts','scripting/entity-shortcuts'),('Finding & spawning','scripting/finding-entities'),('Input','scripting/input'),('Physics scripting','scripting/physics'),('Collisions & triggers','scripting/collisions'),('Pathfinding','scripting/navigation'),('Navigation: complete setup','scripting/navigation-complete'),('State & messaging','scripting/state-messaging'),('Timers, state & messaging','scripting/timers-state'),('Persistence','scripting/persistence'),('Save data','scripting/saving'),('Errors & debugging','scripting/errors'),('API cookbook','scripting/api-cookbook')]),
 ('API reference', 'braces', [('API index','api/index'),('Runtime modules','api/runtime'),('this (EntityContext)','api/this'),('Option schemas (opts)','api/options'),('Requirements & usage map','api/requirements')]),
 ('Export & deploy', 'package', [('Export overview','export/index'),('HTML5 & PWA','export/web'),('Android APK','export/android')]),
 ('Reference', 'book', [('Tuning guide','reference/tuning-guide'),('Scene JSON','reference/scene-format'),('Project format','reference/project-format'),('Engine conventions','reference/rules'),('Debugging','reference/debugging'),('Versioning','reference/versioning'),('Source map','reference/source-map'),('Changelog','reference/changelog')]),
 ('AI & machine access', 'bot', [('AI & crawlers','reference/ai-crawling'),('For AI assistants & LLMs','reference/llm-guide')]),
]
COMPONENT_GROUPS = [
 ('Rendering & UI', ['Transform','SpriteRenderer','ShapeRenderer','TextRenderer','StrokePath','SpeechBubble','ChatLog','TextInput','Joystick']),
 ('Physics & movement', ['Rigidbody2D','Collider2D','Joint2D','CharacterController']),
 ('Animation, camera & audio', ['SpriteAnimation','Camera','AudioSource','AudioListener']),
 ('Lighting', ['Light','ShadowCaster','LightingSettings']),
 ('Navigation & tiles', ['NavAgent2D','NavWorld2D','Tileset','Tilemap']),
 ('Scripting', ['Script']),
]
COMP_NAMES = [c for _, cs in COMPONENT_GROUPS for c in cs]
assert set(COMP_NAMES) == set(FACTS['components']) - {'StrokePathGeometry'}, set(FACTS['components']) ^ set(COMP_NAMES)
COMP_SUMMARY = {}

def url_of(key):  # page key -> path relative to site root
    return f'{V}/index.html' if key == 'index' else f'{V}/{key}.html'

# ------------------------------------------------------------------ load + patch content
log = []; PAGES = {}
for f in sorted(CONTENT.rglob('*.html')):
    key = f.relative_to(CONTENT).with_suffix('').as_posix()
    raw = f.read_text(encoding='utf-8')
    m = re.match(r'<!--meta (.*?) -->\n', raw, re.S)
    meta = json.loads(m.group(1)); body = raw[m.end():]
    body = patch.apply(body, meta, key, FACTS, log)
    PAGES[key] = {'key': key, 'meta': meta, 'body': body}

group_of = {}
for gname, gicon, items in NAV:
    for t, k in items: group_of[k] = (gname, t)
for c in COMP_NAMES: group_of[f'api/components/{c.lower()}'] = ('Components', c)
missing = [k for k in PAGES if k not in group_of and k != 'index']
assert not missing, missing
unused = [k for k in group_of if k not in PAGES]
assert not unused, unused

# ------------------------------------------------------------------ rendering pieces
def rel(root, target): return root + target
def sidebar(root, current):
    out = []
    def link(t, key, cls=''):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{root}{url_of(key)}"{cur}>{escape(t)}</a>'
    for gname, gicon, items in NAV:
        open_ = ' open' if any(k == current for _, k in items) or gname == 'Get started' and current == 'index' else ''
        out.append(f'<details class="side-group"{open_}><summary>{svg(gicon)}<span>{escape(gname)}</span>{svg("chevron","icon chev")}</summary><div class="side-links">' + ''.join(link(t, k) for t, k in items) + '</div></details>')
    comp_open = ' open' if current.startswith('api/components/') else ''
    inner = ''
    for gname, cs in COMPONENT_GROUPS:
        inner += f'<div class="side-sub">{escape(gname)}</div>' + ''.join(link(c, f'api/components/{c.lower()}') for c in cs)
    out.append(f'<details class="side-group"{comp_open}><summary>{svg("box")}<span>Components</span>{svg("chevron","icon chev")}</summary><div class="side-links">{inner}</div></details>')
    return '\n'.join(out)

def topbar(root, section):
    def a(label, href, key=None):
        cur = ' aria-current="true"' if key and key == section else ''
        return f'<a href="{root}{href}"{cur}>{label}</a>'
    return f'''<header class="topbar"><div class="topbar-inner">
<button class="icon-btn menu-toggle" type="button" data-menu-toggle aria-label="Toggle navigation" aria-controls="sidebar">{svg("menu")}</button>
<a class="brand" href="{root}index.html">{LOGO}<span>Vaelis</span><small>Docs</small></a>
<nav class="topnav" aria-label="Primary">{a("Guides", V+"/getting-started/installation.html", "guides")}{a("Scripting", V+"/scripting/lifecycle.html", "scripting")}{a("API", V+"/api/index.html", "api")}{a("Reference", V+"/reference/tuning-guide.html", "reference")}{a("For AI", V+"/reference/llm-guide.html", "ai")}</nav>
<div class="top-spacer"></div>
<button class="search-btn" type="button" data-search-open aria-label="Search documentation" aria-keyshortcuts="Control+K Meta+K /">{svg("search")}<span>Search docs…</span><kbd data-mod>Ctrl K</kbd></button>
<span class="ver-pill" title="Documented engine version"><i></i>v{VERSION}</span>
<button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle color theme">{svg("sun","icon i-sun")}{svg("moon","icon i-moon")}</button>
</div></header>'''

def section_of(key):
    if key.startswith('scripting/'): return 'scripting'
    if key.startswith('api/'): return 'api'
    if key.startswith('reference/ai') or key.startswith('reference/llm'): return 'ai'
    if key.startswith('reference/'): return 'reference'
    return 'guides'

THEME_BOOT = "<script>(function(){try{var t=localStorage.getItem('vaelis-docs-theme');if(!t)t=matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';document.documentElement.setAttribute('data-theme',t)}catch(e){document.documentElement.setAttribute('data-theme','dark')}})()</script>"

def head(root, title, desc, path, extra='', md_path=None, jsonld=None, og_type='article'):
    canon = f'<link rel="canonical" href="{ORIGIN}/{path}">' if ORIGIN else ''
    ogurl = f'<meta property="og:url" content="{ORIGIN}/{path}">' if ORIGIN else ''
    mdl = f'<link rel="alternate" type="text/markdown" href="{Path(md_path).name}" title="Markdown version">' if md_path else ''
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False, separators=(",", ":"))}</script>' if jsonld else ''
    return f'''<!doctype html>
<html lang="en" data-theme="dark" data-root="{root or './'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc, quote=True)}">
<meta name="robots" content="index,follow,max-snippet:-1">
<meta name="theme-color" content="#0a0c11">
<meta name="generator" content="Vaelis docs build">
<meta property="og:site_name" content="{SITE}"><meta property="og:type" content="{og_type}"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(desc, quote=True)}">{ogurl}
<meta name="twitter:card" content="summary">
{canon}{mdl}
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
{THEME_BOOT}
<link rel="stylesheet" href="{root}assets/site.css">
{extra}{ld}
</head>'''

def crumbs_html(root, key, title):
    g = group_of.get(key)
    parts = [f'<a href="{root}index.html">Vaelis</a>', f'<a href="{root}{url_of("index")}">Docs</a>']
    if g and key != 'index':
        first = next((k for gn, _, items in NAV if gn == g[0] for _, k in items), None) if g[0] != 'Components' else 'api/index'
        parts.append(f'<a href="{root}{url_of(first)}">{escape(g[0])}</a>')
    parts.append(f'<span aria-current="page">{escape(title)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + '</nav>', parts

def flat_order():
    order = []
    for _, _, items in NAV: order += [k for _, k in items]
    order += [f'api/components/{c.lower()}' for c in COMP_NAMES]
    return order
ORDER = flat_order()

def pager(root, key):
    if key not in ORDER: return ''
    i = ORDER.index(key); out = ''
    if i > 0:
        p = ORDER[i-1]; out += f'<a class="pn prev" href="{root}{url_of(p)}" rel="prev"><small>← Previous</small><b>{escape(PAGES[p]["meta"]["title"])}</b></a>'
    if i < len(ORDER)-1:
        n = ORDER[i+1]; out += f'<a class="pn next" href="{root}{url_of(n)}" rel="next"><small>Next →</small><b>{escape(PAGES[n]["meta"]["title"])}</b></a>'
    return f'<nav class="pager" aria-label="Previous and next pages">{out}</nav>'

def footer(root):
    return f'''<footer class="foot"><span>Vaelis {VERSION} documentation · static, versioned, machine-readable</span><nav aria-label="Footer"><a href="{root}index.html">Home</a><a href="{root}docs/index.html">Versions</a><a href="{root}llms.txt">llms.txt</a><a href="{root}llms-full.txt">llms-full.txt</a><a href="{root}search-index.json">Search index</a><a href="{root}api/v{VERSION}/index.json">API JSON</a><a href="{root}sitemap.html">Site map</a></nav></footer>'''

def toc_html(heads):
    if len(heads) < 2: return ''
    lis = ''.join(f'<li class="l{lv}"><a href="#{i}">{escape(t)}</a></li>' for lv, t, i in heads)
    return f'<aside class="toc" aria-label="On this page"><h2>On this page</h2><ol>{lis}</ol></aside>'

def plain(html):
    s = BeautifulSoup(html, 'html.parser')
    for x in s.select('.anchor, .copy, svg, script, style'): x.decompose()
    return re.sub(r'\s+', ' ', s.get_text(' ', strip=True))

RENDERED = {}
def write(rel_path, content):
    p = OUT / rel_path; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8'); return p

def render_doc(key, title, desc, lede, body_html, page_path, kind='Guide', jsonld_type='TechArticle', md_source=True):
    depth = len(Path(page_path).parts) - 1; root = '../' * depth
    body, heads = process(body_html, key, root)
    gname = group_of.get(key, ('Docs', title))[0]
    crumb, crumb_parts = crumbs_html(root, key, title)
    md_name = Path(page_path).with_suffix('.md').as_posix()
    tools = ''
    if md_source:
        tools = f'<div class="page-tools"><button class="chip-btn" type="button" data-copy-md>{svg("copy")}Copy page as Markdown</button><a class="chip-btn" href="{Path(md_name).name}">{svg("filecode")}View as Markdown</a><a class="chip-btn" href="{root}llms.txt">{svg("bot")}llms.txt</a></div>'
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'TechArticle', 'headline': title, 'description': desc, 'inLanguage': 'en', 'version': VERSION, 'isPartOf': {'@type': 'WebSite', 'name': SITE}, 'about': 'Vaelis 2D game engine', **({'url': f'{ORIGIN}/{page_path}'} if ORIGIN else {})},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i+1, 'name': re.sub('<[^>]+>', '', c)} for i, c in enumerate(crumb_parts)]}]}
    cur = key
    html = (head(root, f'{title} · {SITE} v{VERSION}' if key != 'index' else f'{SITE} · v{VERSION}', desc, page_path, md_path=md_name if md_source else None, jsonld=ld) +
      f'''\n<body data-layout="docs" data-page="{escape(key)}"><a class="skip" href="#main">Skip to content</a><div id="nav-progress"></div>
{topbar(root, section_of(key))}
<div class="shell"><aside class="sidebar" id="sidebar" aria-label="Documentation navigation">{sidebar(root, cur)}</aside>
<main id="main" class="main"><div class="doc-grid"><article class="doc">{crumb}<div class="eyebrow">{escape(gname)} · v{VERSION}</div><h1>{escape(title)}</h1><p class="lede">{escape(lede)}</p>{tools}{body}{pager(root, key)}{footer(root)}</article>{toc_html(heads)}</div></main></div>
<script src="{root}assets/site.js" defer></script></body></html>''')
    write(page_path, html)
    # markdown twin
    mdsoup = BeautifulSoup(body, 'html.parser')
    for x in mdsoup.select('.anchor, .copy, svg, header'): x.decompose()
    for c in mdsoup.select('div.callout'):
        t = c.select_one('.ctitle'); label = (t.get_text(strip=True) if t else 'Note')
        if t: t.decompose()
        c.replace_with(BeautifulSoup('<blockquote><strong>' + escape(label) + ':</strong> ' + c.get_text(' ', strip=True) + '</blockquote>', 'html.parser'))
    for cb in mdsoup.select('div.codeblock'):
        lang = cb.get('data-lang', '')
        cb.replace_with(BeautifulSoup('<pre><code class="language-' + lang + '">' + escape(cb.find('pre').get_text()) + '</code></pre>', 'html.parser'))
    md_body = md(str(mdsoup), heading_style='ATX', code_language_callback=lambda el: (el.get('class') or [''])[0].replace('language-', ''), bullets='-')
    md_body = re.sub(r'\n{3,}', '\n\n', md_body).strip()
    md_url = (ORIGIN + '/' if ORIGIN else '') + page_path
    md_text = f'# {title}\n\n> {desc}\n\n- Source: {md_url}\n- Engine version: Vaelis {VERSION}\n\n{md_body}\n'
    write(md_name, md_text)
    toks = []
    for cel in BeautifulSoup(body, 'html.parser').select('code'):
        for t in re.findall(r'[A-Za-z_$][\w$]{2,}', cel.get_text()):
            if t not in toks: toks.append(t)
    RENDERED[key] = {'code': ' '.join(toks[:320]), 'title': title, 'desc': desc, 'url': page_path, 'group': gname, 'heads': heads, 'text': plain(body), 'md': md_body}
    return root

# ------------------------------------------------------------------ pages
for key, p in PAGES.items():
    if key == 'index': continue
    m = p['meta']
    render_doc(key, m['title'], m['description'] or m['lede'], m['lede'] or m['description'], p['body'], url_of(key))

# component summaries (from patched pages) for cards
for c in COMP_NAMES:
    soup = BeautifulSoup(PAGES[f'api/components/{c.lower()}']['body'], 'html.parser')
    h = next((x for x in soup.find_all('h2') if x.get_text(strip=True) == 'What it does'), None)
    COMP_SUMMARY[c] = h.find_next('p').get_text(' ', strip=True) if h else ''

# docs home
def home_body():
    n_comp = len(COMP_NAMES); n_pages = len(PAGES) + 1
    cards = ''
    icons = {'Get started':'rocket','Concepts':'layers','Editor':'grid','Scripting':'code','API reference':'braces','Export & deploy':'package','Reference':'book','AI & machine access':'bot'}
    blurb = {'Get started':'Run the editor, build a first game and learn the scripting model.','Concepts':'Architecture, the entity–component model, the game loop and coordinates.','Editor':'Every panel, menu path, shortcut and authoring workflow.','Scripting':'Lifecycle, globals, input, physics, navigation, saving and debugging.','API reference':'Component fields, script members, option shapes and prerequisites.','Export & deploy':'HTML5, installable PWA and Android APK builds.','Reference':'Tuning rules, scene and project formats, versioning and source map.','AI & machine access':'llms.txt, Markdown twins, JSON catalogs and guidance for assistants.'}
    for gname, gicon, items in NAV:
        first = next(k for _, k in items if k != 'index') if gname != 'Get started' else 'getting-started/installation'
        cards += f'<div class="card"><h3><a href="{url_of(first).replace(V+"/","")}">{escape(gname)}</a></h3><p>{escape(blurb[gname])}</p><p class="muted">{len(items)} pages</p></div>'
    comp_chips = ''.join(f'<a class="api-card" href="api/components/{c.lower()}.html"><strong>{c}</strong><span>{escape(first_line(COMP_SUMMARY[c]))}</span></a>' for c in COMP_NAMES)
    return f'''<div class="callout info"><strong>What is Vaelis?</strong><div>A browser-based 2D game engine with a Unity-style visual editor, an entity–component runtime built on PixiJS (rendering) and Rapier2D (physics), and a JavaScript scripting API. The editor, runtime and exporter ship as a static site — no build server is needed to make or play games.</div></div>
<h2 id="start-here">Start here</h2>
<div class="cards"><div class="card"><h3><a href="getting-started/installation.html">Install &amp; run</a></h3><p>Use the hosted editor or serve the static distribution yourself.</p></div><div class="card"><h3><a href="getting-started/first-game.html">Build your first game</a></h3><p>Entities, components and a first script in a few steps.</p></div><div class="card"><h3><a href="getting-started/scripting.html">Scripting quickstart</a></h3><p>onStart, onUpdate, <code>this</code> and the component modules.</p></div><div class="card"><h3><a href="editor/controls.html">Editor controls</a></h3><p>Exact menu paths, panels and keyboard shortcuts.</p></div></div>
<h2 id="browse-by-topic">Browse by topic</h2><div class="cards">{cards}</div>
<h2 id="component-reference">Component reference</h2><p>{n_comp} components, each documented with serialized fields, defaults, script API and editor location.</p><div class="api-list">{comp_chips}</div>
<h2 id="for-automated-systems">For automated systems</h2><p>Every page is complete static HTML with a Markdown twin (same URL, <code>.md</code>). Machine entry points: <a href="../../llms.txt">llms.txt</a>, <a href="../../llms-full.txt">llms-full.txt</a> (all documentation in one file), <a href="../../search-index.json">search-index.json</a>, <a href="../../api/v{VERSION}/index.json">api/v{VERSION}/index.json</a>, <a href="../../sitemap.xml">sitemap.xml</a> and <a href="../../robots.txt">robots.txt</a>. See <a href="reference/ai-crawling.html">AI &amp; crawlers</a>.</p>'''
def first_line(s, n=120):
    s = re.sub(r'\s+', ' ', s).strip(); return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + '…'
render_doc('index', 'Vaelis documentation', f'Complete, source-verified documentation for Vaelis {VERSION}: editor workflows, scripting API, components, physics, navigation and export.', f'Everything you need to build 2D games with Vaelis {VERSION}, verified against the engine source.', home_body(), url_of('index'))

# ------------------------------------------------------------------ site-level pages
def simple_page(page_path, title, desc, body, section='guides', layout='docs', extra_head=''):
    depth = len(Path(page_path).parts) - 1; root = '../' * depth
    html = (head(root, f'{title} · {SITE}', desc, page_path) + f'''\n<body data-layout="{layout}" data-page=""><a class="skip" href="#main">Skip to content</a><div id="nav-progress"></div>{topbar(root, section)}
<div class="shell"><aside class="sidebar" id="sidebar" aria-label="Documentation navigation">{sidebar(root, '')}</aside><main id="main" class="main"><div class="doc-grid"><article class="doc">{body}{footer(root)}</article></div></main></div><script src="{root}assets/site.js" defer></script></body></html>''')
    write(page_path, html)

simple_page('docs/index.html', 'Choose a documentation version', 'Select the Vaelis engine version whose documentation you want to read.',
  f'<div class="eyebrow">Versions</div><h1>Documentation versions</h1><p class="lede">Each engine version has its own permanent URL. Older versions are never overwritten.</p><div class="version-list"><div class="version-item"><div><strong>Vaelis {VERSION}</strong> <span class="badge">Current</span><div class="muted">Stable path <code>/docs/v{VERSION}/</code> · alias <code>/docs/latest/</code></div></div><a class="button" href="v{VERSION}/index.html">Open →</a></div></div>')
write('docs/latest/index.html', f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0; url=../v{VERSION}/index.html">{("<link rel=canonical href=" + ORIGIN + "/docs/v" + VERSION + "/index.html>") if ORIGIN else ""}<title>Vaelis documentation (latest)</title></head><body><p>Redirecting to <a href="../v{VERSION}/index.html">Vaelis {VERSION} documentation</a>…</p></body></html>')

# html sitemap
sm = ''
for gname, gicon, items in NAV:
    sm += f'<div><h2>{escape(gname)}</h2><ul>' + ''.join(f'<li><a href="{url_of(k)}">{escape(t)}</a></li>' for t, k in items) + '</ul></div>'
sm += '<div><h2>Components</h2><ul>' + ''.join(f'<li><a href="{V}/api/components/{c.lower()}.html">{c}</a></li>' for c in COMP_NAMES) + '</ul></div>'
simple_page('sitemap.html', 'Site map', 'Every page in the Vaelis documentation.', f'<div class="eyebrow">Docs</div><h1>Site map</h1><p class="lede">All {len(PAGES)} documentation pages, grouped by section.</p><div class="sitemap-grid">{sm}</div>')
write('404.html', head('', 'Page not found · ' + SITE, 'This page does not exist.', '404.html').replace('href="assets/', 'href="/assets/').replace('href="favicon', 'href="/favicon') + f'''\n<body data-layout="static"><div class="notfound"><h1>404</h1><p class="lede" style="margin:12px auto 24px">That page isn't part of the Vaelis documentation.</p><div class="btn-row" style="justify-content:center"><a class="btn primary" href="/index.html">Docs home</a><a class="btn" href="/sitemap.html">Site map</a></div></div></body></html>''')

# ------------------------------------------------------------------ landing page
def landing():
    root = ''
    n_api_members = sum(len(m['members']) for m in FACTS['api'].values())
    stats = [(str(len(COMP_NAMES)), 'documented components'), (str(len(FACTS['api'])), 'script API modules'), (str(len(PAGES)), 'static, crawlable pages'), ('4', 'machine-readable feeds')]
    feats = [('grid','Editor, end to end','Hierarchy, Inspector, viewport tools, prefabs, physics layers and nav areas — with exact menu paths and shortcuts.',f'{V}/editor/overview.html'),
             ('code','JavaScript scripting','Lifecycle hooks, <code>this</code> context, globals, timers, messaging and typed errors.',f'{V}/scripting/lifecycle.html'),
             ('atom','Rapier2D physics','Dynamic, kinematic and static bodies, 16-layer filtering, joints and one-way platforms.',f'{V}/editor/physics.html'),
             ('route','Grid navigation','NavWorld2D bake &amp; paint, 16 areas with costs, NavAgent2D steering and avoidance.',f'{V}/scripting/navigation-complete.html'),
             ('lightning','2D lighting','Six light types, shadow casters and quad or raymarched shadows.',f'{V}/editor/lighting-audio-ui.html'),
             ('package','Ship anywhere','HTML5, installable PWA, and Android APK through your own build server.',f'{V}/export/index.html')]
    fh = ''.join(f'<a href="{u}"><span class="fi">{svg(i)}</span><h3>{t}</h3><p>{d}</p></a>' for i,t,d,u in feats)
    chips = ''.join(f'<a href="{V}/api/components/{c.lower()}.html">{c}</a>' for c in COMP_NAMES)
    hero_code = '''function onStart() {
  this.speed = 220;
}

function onUpdate(dt) {
  if (input.keyDown("ArrowRight")) {
    this.x += this.speed * dt;
  }
  if (input.keyPressed("Space")) {
    this.rigidbody.addImpulse(0, -350);
  }
}'''
    hc = process('<pre><code>' + escape(hero_code) + '</code></pre>', 'landing')[0]
    html = (head('', f'{SITE} — build 2D games in the browser', f'Source-verified documentation for Vaelis {VERSION}, a browser-based 2D game engine: visual editor, JavaScript scripting, Rapier2D physics, navigation, lighting and one-click export.', 'index.html', jsonld={'@context':'https://schema.org','@type':'WebSite','name':SITE,'description':'Documentation for the Vaelis 2D game engine.', **({'url': ORIGIN + '/'} if ORIGIN else {})}, og_type='website') + f'''\n<body class="landing" data-layout="static" data-page="home"><a class="skip" href="#main">Skip to content</a>
{topbar('', '').replace('<button class="icon-btn menu-toggle" type="button" data-menu-toggle aria-label="Toggle navigation" aria-controls="sidebar">'+svg("menu")+'</button>','')}
<main id="main" class="main">
<section class="hero"><div class="hero-in"><div><span class="pill"><b>v{VERSION}</b> Stable · verified against engine source</span><h1>Build 2D games<br>in the <span class="grad">browser</span>.</h1><p class="sub">Vaelis is a 2D game engine with a visual editor, JavaScript scripting, Rapier2D physics, navigation, lighting and one-click export. These docs cover every component, API and editor control.</p><div class="btn-row"><a class="btn primary" href="{V}/getting-started/first-game.html">Build your first game {svg("arrow")}</a><a class="btn" href="{V}/index.html">Browse the docs</a><button class="btn" type="button" data-search-open>{svg("search")}Search <kbd data-mod>Ctrl K</kbd></button></div></div><div class="hero-code">{hc}</div></div></section>
<div class="stats">{''.join(f'<div class="stat"><b>{a}</b><span>{b}</span></div>' for a,b in stats)}</div>
<section class="section"><h2>Everything the engine does, documented</h2><p class="sub">Pages are written from the shipped source: field names, defaults, script members and menu paths are checked, not guessed.</p><div class="feat">{fh}</div></section>
<section class="section"><h2>A clear path in</h2><p class="sub">New to Vaelis? Follow these three pages in order.</p><div class="path"><a href="{V}/getting-started/installation.html"><h3>Open the editor</h3><p>Use the hosted site or serve the static folder yourself — no Node.js required.</p></a><a href="{V}/getting-started/first-game.html"><h3>Make something move</h3><p>Add a sprite, physics and a script, then press Play.</p></a><a href="{V}/export/index.html"><h3>Ship it</h3><p>Export to HTML5 or PWA, or send the package to an APK build server.</p></a></div></section>
<section class="section"><h2>Component reference</h2><p class="sub">{len(COMP_NAMES)} components, each with serialized fields, defaults, script API, tuning rules and the exact editor entry point.</p><div class="chips">{chips}</div></section>
<section class="section"><div class="split"><div class="panel"><h3>For developers</h3><p>Precise, prerequisite-aware API pages.</p><ul>{''.join(f'<li>{svg("check")}<span>{t}</span></li>' for t in ['Every component and script member with types and defaults','Option (<code>opts</code>) shapes for raycasts, spawning and navigation','Editor shortcuts and conditional tools, exactly as implemented'])}</ul></div><div class="panel"><h3>For AI assistants &amp; crawlers</h3><p>Plain HTML, stable URLs, no client-only content.</p><ul>{''.join(f'<li>{svg("check")}<span>{t}</span></li>' for t in ['<a href="llms.txt">llms.txt</a> index and <a href="llms-full.txt">llms-full.txt</a> full text','A Markdown twin of every page (same URL, <code>.md</code>)',f'JSON catalogs: <a href="api/v{VERSION}/index.json">API</a>, <a href="search-index.json">search</a>, <a href="sitemap.xml">sitemap</a>'])}</ul></div></div></section>
<div class="cta"><div class="cta-in"><div><h2>Ready to build?</h2><p>Start with the installation guide, or jump straight into scripting.</p></div><div class="btn-row"><a class="btn primary" href="{V}/getting-started/installation.html">Get started {svg("arrow")}</a><a class="btn" href="{V}/scripting/lifecycle.html">Scripting lifecycle</a></div></div></div>
<div class="landing-foot">{footer('')}</div></main><script src="assets/site.js" defer></script></body></html>''')
    write('index.html', html)
landing()

# ------------------------------------------------------------------ static assets
shutil.copy2(HERE / 'static/css/site.css', OUT / 'assets').__class__ if False else None
(OUT / 'assets').mkdir(parents=True, exist_ok=True)
shutil.copy2(HERE / 'static/css/site.css', OUT / 'assets/site.css')
shutil.copy2(HERE / 'static/js/site.js', OUT / 'assets/site.js')
write('favicon.svg', LOGO.replace('role="img" aria-label="Vaelis" ', '').replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1))

# ------------------------------------------------------------------ machine-readable outputs
featured = {'index','getting-started/installation','getting-started/first-game','getting-started/scripting','scripting/lifecycle','scripting/globals','api/index','editor/controls','scripting/api-cookbook','reference/llm-guide'}
search = []
for key, r in RENDERED.items():
    kw = ' '.join([r['title'], r['group']] + ([FACTS['components'][r['title']]['file'].split('/')[-1]] if r['title'] in FACTS['components'] else []))
    search.append({'t': r['title'], 'd': first_line(r['desc'], 170), 'k': kw, 's': r['group'], 'u': r['url'], 'h': [[t, i] for _, t, i in r['heads']][:40], 'c': r['code'], 'x': r['text'][:2600], **({'f': 1} if key in featured else {})})
search.sort(key=lambda x: x['u'])
write('search-index.json', json.dumps(search, ensure_ascii=False, separators=(',', ':')))

def link_line(r): return f"- [{r['title']}]({r['url']}): {first_line(r['desc'], 160)}"
llms = [f'# Vaelis documentation', '', f'> Vaelis is a browser-based 2D game engine (visual editor, JavaScript scripting, PixiJS rendering, Rapier2D physics). This site documents version {VERSION}. Every page has a Markdown twin at the same URL with a .md extension. Prefer these pages over memory when writing Vaelis code: several APIs differ from Unity/Godot conventions (for example +Y is down).', '']
for gname, gicon, items in NAV:
    llms += [f'## {gname}', ''] + [link_line(RENDERED[k]) for _, k in items] + ['']
llms += ['## Components', ''] + [link_line(RENDERED[f'api/components/{c.lower()}']) for c in COMP_NAMES] + ['']
llms += ['## Optional: machine-readable', '', f'- [Full documentation in one file](llms-full.txt): every page concatenated as Markdown', f'- [API catalog (JSON)](api/v{VERSION}/index.json): component fields, defaults and script members extracted from source', f'- [Search index (JSON)](search-index.json)', f'- [Site map](sitemap.html)', '']
write('llms.txt', '\n'.join(llms))
full = [f'# Vaelis {VERSION} — complete documentation', '', f'Generated {datetime.date.today().isoformat()} from the Vaelis engine source. {len(RENDERED)} pages follow; each starts with a level-1 heading and its canonical path.', '']
for key in ['index'] + ORDER:
    r = RENDERED[key]; full += ['', '---', '', f'<!-- page: {r["url"]} -->', f'# {r["title"]}', '', f'> {r["desc"]}', '', r['md'], '']
write('llms-full.txt', '\n'.join(full))

# API catalog (from source facts + doc summaries)
lifecycle = ['onClone','onStart','onUpdate','onFixedUpdate','onDestroy','onClick','onCollision','onCollisionEnter','onCollisionStay','onCollisionExit','onTriggerEnter','onTriggerExit','onMessage','onStateEnter','onStateExit','onStateUpdate','onHearSound','onLoseSound']
cat = {'engine': 'Vaelis', 'version': VERSION, 'generatedFrom': 'project/runtime/components/*.js and project/runtime/scripting/components/*API.js', 'runtimeEntry': 'project/runtime/index.js', 'componentTypes': COMP_NAMES, 'lifecycle': lifecycle, 'enums': FACTS['enums'], 'components': {}}
for c in COMP_NAMES:
    comp = FACTS['components'][c]; mod = patch.API_MODULE.get(c); api = FACTS['api'].get(mod) if mod else None
    allowed = sorted({m for s in api['member_sets'].values() for m in s}) if api else []
    cat['components'][c] = {'summary': COMP_SUMMARY[c], 'docs': f'{V}/api/components/{c.lower()}.html', 'source': comp['file'], 'sceneFields': [{'name': f['name'], 'default': f['default'], 'type': f['kind'] or 'value'} for f in comp['fields'] if not f['name'].startswith('_')],
        'scriptModule': ('this.' + {'Transform':'transform','SpriteRenderer':'sprite','ShapeRenderer':'shape','TextRenderer':'text','StrokePath':'strokePath','SpeechBubble':'speechBubble','ChatLog':'chat','TextInput':'textInput','Joystick':'joystick','Rigidbody2D':'rigidbody','Collider2D':'collider','Joint2D':'joint','CharacterController':'controller','SpriteAnimation':'animator','Camera':'camera','AudioSource':'audio','AudioListener':'ear','Light':'light','ShadowCaster':'shadowCaster','LightingSettings':'(scene.lighting)','NavAgent2D':'navAgent'}[c]) if mod else None,
        'scriptMembers': [{'name': m, 'kind': ('method' if api['members'][m]['method'] else ('read-only property' if api['members'][m]['get'] and not api['members'][m]['set'] else 'property')), 'doc': first_line(api['members'][m]['doc'], 200)} for m in allowed if m in api['members']] if api else []}
write(f'api/v{VERSION}/index.json', json.dumps(cat, indent=1, ensure_ascii=False))
write(f'api/v{VERSION}/manifest.json', json.dumps({'title': f'Vaelis {VERSION} API catalog', 'engine': 'Vaelis', 'version': VERSION, 'files': {'catalog': f'api/v{VERSION}/index.json', 'searchIndex': 'search-index.json', 'llms': 'llms.txt', 'llmsFull': 'llms-full.txt'}, 'componentCount': len(COMP_NAMES), 'pageCount': len(RENDERED)}, indent=1))
write('versions.json', json.dumps({'current': VERSION, 'versions': [{'version': VERSION, 'status': 'current', 'label': f'Vaelis {VERSION}', 'path': url_of('index')}]}, indent=1))

# sitemap + robots
urls = sorted({r['url'] for r in RENDERED.values()} | {'index.html', 'docs/index.html', 'sitemap.html'})
if ORIGIN:
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + [f'  <url><loc>{escape(ORIGIN + "/" + u)}</loc></url>' for u in urls] + ['</urlset>']
    write('sitemap.xml', '\n'.join(xml) + '\n')
else:
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<!-- Sitemaps require absolute URLs. Rebuild with: python3 build.py --origin https://your-domain.example -->\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>\n')
write('robots.txt', 'User-agent: *\nAllow: /\n\n# AI search and training crawlers are intentionally allowed.\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n' + (f'\nSitemap: {ORIGIN}/sitemap.xml\n' if ORIGIN else '\n# Add "Sitemap: https://your-domain/sitemap.xml" after rebuilding with --origin.\n'))
write('.nojekyll', '')

Path(HERE / 'build.log').write_text('\n'.join(log) + '\n')
print(f'built {len(RENDERED)} pages -> {OUT}; {len(log)} source-driven corrections')
