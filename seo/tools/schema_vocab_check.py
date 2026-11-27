#!/usr/bin/env python3
"""Offline schema.org check of every page's JSON-LD: unknown types, unknown properties,
properties used on a type they don't apply to, and values outside a property's range.

The same class of check the Schema Markup Validator runs, for when validate_schema.py
can't reach it (validator.schema.org answered HTTP 405 to its POST on 2026-11-27).
It doesn't check Google's rich-result requirements; the Rich Results Test does that.

Usage (from the repo root):
    python3 seo/tools/schema_vocab_check.py            # every page in sitemap.xml
    python3 seo/tools/schema_vocab_check.py a.html ...  # specific files
Downloads the current schema.org vocabulary once to /tmp. Exits 1 on any problem.
"""
import json, os, re, sys, urllib.request
VOCAB = '/tmp/schemaorg-current-https.jsonld'
if not os.path.exists(VOCAB):
    urllib.request.urlretrieve('https://schema.org/version/latest/schemaorg-current-https.jsonld', VOCAB)
V = json.load(open(VOCAB))['@graph']
def short(x): return x.split(':', 1)[1] if isinstance(x, str) and x.startswith('schema:') else x
def ids(v):
    if v is None: return []
    if isinstance(v, list): return [short(i['@id']) for i in v]
    return [short(v['@id'])]
classes, props, parents = set(), {}, {}
for n in V:
    t = n.get('@type'); t = t if isinstance(t, list) else [t]
    nid = short(n['@id'])
    if 'rdfs:Class' in t:
        classes.add(nid); parents[nid] = ids(n.get('rdfs:subClassOf'))
    if 'rdf:Property' in t:
        props[nid] = {'domain': ids(n.get('schema:domainIncludes')), 'range': ids(n.get('schema:rangeIncludes'))}
# data types are classes too
DATATYPES = {'Text', 'URL', 'Number', 'Integer', 'Boolean', 'Date', 'DateTime', 'Time', 'Float'}
def ancestors(c, seen=None):
    seen = seen or set()
    for p in parents.get(c, []):
        if p not in seen:
            seen.add(p); ancestors(p, seen)
    return seen | {c}
def val_types(v):
    if isinstance(v, dict):
        t = v.get('@type')
        if t is None: return None  # @id reference, can't check
        return t if isinstance(t, list) else [t]
    if isinstance(v, bool): return ['Boolean']
    if isinstance(v, (int, float)): return ['Number']
    if isinstance(v, str):
        if re.match(r'^https?://', v): return ['URL', 'Text']
        if re.match(r'^\d{4}-\d{2}-\d{2}$', v): return ['Date', 'Text', 'DateTime']
        return ['Text']
    return None
def range_ok(prop, vt):
    rng = props[prop]['range']
    if not rng or vt is None: return True
    for t in vt:
        anc = ancestors(t)
        if any(r in anc for r in rng): return True
        if t in ('URL',) and ('Text' in rng or 'URL' in rng): return True
        if t == 'Text' and ('Text' in rng or 'URL' in rng): return True
        if t in ('Date', 'DateTime') and ({'Date', 'DateTime', 'Text'} & set(rng)): return True
        if t == 'Number' and ({'Number', 'Integer', 'Float', 'QuantitativeValue', 'Distance'} & set(rng)): return True
        if t == 'URL' and rng and all(r not in DATATYPES for r in rng): return True  # URL as a reference to a Thing is allowed
    return False
problems = []
def check(node, path):
    if isinstance(node, list):
        for i, n in enumerate(node): check(n, f'{path}[{i}]')
        return
    if not isinstance(node, dict): return
    types = node.get('@type')
    types = types if isinstance(types, list) else ([types] if types else [])
    for t in types:
        if t not in classes: problems.append(f'{path}: unknown type {t}')
    for k, v in node.items():
        if k.startswith('@'): 
            if k == '@graph': check(v, path + '.@graph')
            continue
        if k not in props:
            problems.append(f'{path}: unknown property {k}'); continue
        if types:
            dom = props[k]['domain']
            if dom and not any(d in ancestors(t) for t in types for d in dom):
                problems.append(f'{path} ({"/".join(types)}): property {k} not expected on this type')
        vals = v if isinstance(v, list) else [v]
        for x in vals:
            if not range_ok(k, val_types(x)):
                problems.append(f'{path}.{k}: value type {val_types(x)} outside range {props[k]["range"]}')
            check(x, f'{path}.{k}')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
files = sys.argv[1:] or [os.path.join(ROOT, 'index.html' if u == '/' else u.strip('/') + '/index.html')
                         for u in re.findall(r'<loc>https://elimenti.com(/[^<]*)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read())]
total = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    problems.clear()
    for i, b in enumerate(blocks):
        try: check(json.loads(b), f'block{i}')
        except json.JSONDecodeError as e: problems.append(f'block{i}: invalid JSON {e}')
    total += len(problems)
    if problems:
        print(f'== {f}: {len(problems)} problem(s)')
        for p in problems[:12]: print('   ', p)
print(f'{len(files)} files checked, {total} problems')
sys.exit(1 if total else 0)
