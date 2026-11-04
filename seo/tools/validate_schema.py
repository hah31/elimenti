#!/usr/bin/env python3
"""Validate every page's JSON-LD with the official Schema Markup Validator (validator.schema.org).

Usage (from the repo root):
    python3 seo/tools/validate_schema.py
Prints each page's top-level types and any errors or warnings; exits non-zero on errors.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from build import PAGES, ROOT  # noqa: E402


def walk(node, out):
    if isinstance(node, dict):
        for key in ('errors', 'warnings'):
            for e in node.get(key) or []:
                out[key].append(e.get('args') or e.get('ownerSet') or e)
        for v in node.values():
            walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


total_errors = 0
for p in PAGES:
    html = open(os.path.join(ROOT, p['file']), encoding='utf-8').read()
    data = urllib.parse.urlencode({'html': html}).encode()
    for attempt in range(3):
        try:
            raw = urllib.request.urlopen('https://validator.schema.org/validate', data=data, timeout=60).read().decode()
            break
        except Exception as e:  # network hiccup: retry
            if attempt == 2:
                sys.exit(f'{p["path"]}: validator unreachable: {e}')
            time.sleep(2 ** attempt)
    res = json.loads(raw.split('\n', 1)[1])
    out = {'errors': [], 'warnings': []}
    walk(res, out)
    types = set()

    def collect(n):
        if isinstance(n, dict):
            if n.get('typeGroup'):
                types.add(n['typeGroup'])
            for v in n.values():
                collect(v)
        elif isinstance(n, list):
            for v in n:
                collect(v)
    collect(res.get('tripleGroups'))
    types = sorted(types - {'Thing', 'ListItem', 'Answer', 'Question', 'City', 'Country', 'PostalAddress', 'Offer', 'AdministrativeArea'})
    out['errors'] += [None] * max(0, res.get('totalNumErrors', 0) - len(out['errors']))
    total_errors += len(out['errors'])
    flag = 'OK ' if not out['errors'] else 'ERR'
    print(f'{flag} {p["path"]:48} {len(out["errors"])} errors, {len(out["warnings"])} warnings  [{", ".join(types)}]')
    for e in out['errors'] + out['warnings']:
        print('      ', e)
    time.sleep(0.5)

sys.exit(1 if total_errors else 0)
