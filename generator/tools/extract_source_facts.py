#!/usr/bin/env python3
"""Extract ground-truth facts (component fields/defaults, enums, script-API member sets)
from the Vaelis engine source so the documentation can be generated and verified from code.
Usage: extract_source_facts.py <engine_root> <out.json>"""
import re, json, sys
from pathlib import Path

def strip_comments(s):
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    return re.sub(r'(?<!:)//[^\n]*', '', s)

def parse_enums(text):
    enums = {}
    for m in re.finditer(r'export const (\w+)\s*=\s*(?:Object\.freeze\()?\{(.*?)\}\)?;', text, re.S):
        vals = {k: v for k, v in re.findall(r'(\w+)\s*:\s*"([^"]*)"', strip_comments(m.group(2)))}
        enums[m.group(1)] = vals
    return enums

def split_top(body):
    depth = 0; cur = ''; parts = []; instr = None
    for ch in body:
        if instr:
            cur += ch
            if ch == instr: instr = None
            continue
        if ch in '"\'`': instr = ch; cur += ch; continue
        if ch in '([{': depth += 1
        if ch in ')]}': depth -= 1
        if ch == ',' and depth == 0: parts.append(cur); cur = ''
        else: cur += ch
    parts.append(cur)
    return parts

def field_comments(raw_body):
    """Map field name -> nearby comment text (preceding // block or trailing // comment)."""
    comments = {}; pending = []
    for line in raw_body.split('\n'):
        s = line.strip()
        if s.startswith('//'): pending.append(s.lstrip('/ ').strip()); continue
        if s.startswith('/*') or s.startswith('*') or s.endswith('*/'):
            t = s.strip('/* ').strip()
            if t: pending.append(t)
            continue
        m = re.match(r'(\w+)\s*=', s)
        if m:
            trailing = re.search(r'//\s*(.*)$', s)
            txt = ' '.join(pending + ([trailing.group(1)] if trailing else []))
            if txt: comments[m.group(1)] = re.sub(r'\s+', ' ', txt).strip()
            pending = []
        elif not s: pending = []
    return comments

def main(root, out):
    root = Path(root); comp_dir = root / 'project/runtime/components'
    enums = {}
    for f in list(comp_dir.glob('*.js')) + list((root / 'project/runtime/systems').glob('*.js')): enums.update(parse_enums(f.read_text()))
    components = {}
    for f in sorted(comp_dir.glob('*.js')):
        t = f.read_text()
        m = re.search(r'constructor\s*\(\s*\{(.*?)\}\s*=\s*\{\}\s*\)', t, re.S)
        if not m: continue
        raw = m.group(1); comments = field_comments(raw)
        body = strip_comments(raw); fields = []
        for p in split_top(body):
            p = p.strip()
            if not p: continue
            k, _, v = p.partition('=')
            k = k.strip(); v = re.sub(r'\s+', ' ', v.strip())
            resolved = v; kind = None
            em = re.fullmatch(r'(\w+)\.(\w+)', v)
            if em and em.group(1) in enums and em.group(2) in enums[em.group(1)]:
                resolved = enums[em.group(1)][em.group(2)]; kind = 'enum:' + em.group(1)
            elif v in ('true', 'false'): kind = 'boolean'
            elif re.fullmatch(r'-?\d+(\.\d+)?', v): kind = 'number'
            elif re.fullmatch(r'"[^"]*"|\'[^\']*\'', v): resolved = v[1:-1]; kind = 'string'
            elif v == 'null': kind = 'null'
            elif v.startswith('['): kind = 'array'
            elif v.startswith('{'): kind = 'object'
            fields.append({'name': k, 'default': resolved, 'kind': kind, 'comment': comments.get(k, '')})
        cls = re.search(r'export class (\w+)', t)
        head = re.search(r'/\*\*(.*?)\*/', t, re.S)
        summary = ''
        if head:
            lines = [re.sub(r'^\s*\*\s?', '', l) for l in head.group(1).split('\n')]
            summary = re.sub(r'\s+', ' ', ' '.join(l for l in lines[2:] if l.strip() and 'RUNTIME-ONLY' not in l)).strip()
        components[cls.group(1) if cls else f.stem] = {'file': str(f.relative_to(root)), 'fields': fields, 'header': summary}
    api = {}
    for f in sorted((root / 'project/runtime/scripting/components').glob('*.js')):
        text = f.read_text()
        sets = {n: re.findall(r'"([^"]+)"', b) for n, b in re.findall(r'const\s+([A-Z_0-9]*MEMBERS[A-Z_0-9]*)\s*=\s*new Set\(\[(.*?)\]\)', text, re.S)}
        # per-member JSDoc + kind (getter/setter/method) so docs can be generated from source comments
        members = {}
        for m in re.finditer(r'(?:/\*\*(.*?)\*/\s*)?(?:^|\n)\s*(get|set)?\s*(\w+)\s*(?:\([^)]*\)\s*\{|:\s*function\s*\()', text, re.S):
            doc, acc, name = m.group(1), m.group(2), m.group(3)
            if name in ('if', 'for', 'while', 'switch', 'function', 'catch', 'return'): continue
            e = members.setdefault(name, {'get': False, 'set': False, 'method': False, 'doc': ''})
            if acc == 'get': e['get'] = True
            elif acc == 'set': e['set'] = True
            else: e['method'] = True
            if doc and not e['doc']:
                lines = [re.sub(r'^\s*\*\s?', '', l) for l in doc.split('\n')]
                e['doc'] = re.sub(r'\s+', ' ', ' '.join(l for l in lines if l.strip())).strip()
        api[f.stem] = {'file': str(f.relative_to(root)), 'member_sets': sets, 'members': members}
    Path(out).write_text(json.dumps({'enums': enums, 'components': components, 'api': api}, indent=1))
    print('components', len(components), 'enums', len(enums), 'api modules', len(api))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
