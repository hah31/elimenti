#!/usr/bin/env python3
"""Print the OG card list (slug, H1, kicker) for og.js, read from the registry and built pages."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build import PAGES, ROOT, slug_for  # noqa: E402

KICKERS = [
    ('/work/', 'Case study'), ('/guides/', 'Guide'), ('-web-design/', 'Where we work'),
    ('-websites/', 'Websites by industry'),
]

out = []
for p in PAGES:
    if p.get('og_image'):
        continue  # these pages reuse another page's card
    fp = os.path.join(ROOT, p['file'])
    if not os.path.exists(fp):
        continue
    m = re.search(r'<h1[^>]*>(.*?)</h1>', open(fp, encoding='utf-8').read(), re.S)
    h1 = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else p['title'].split(' | ')[0]
    h1 = h1.replace('&#x27;', '’').replace('&amp;', '&').replace("'", '’')
    kicker = 'Elimenti'
    for frag, k in KICKERS:
        if frag in p['path']:
            kicker = k
            break
    if p['path'] in ('/work/', '/guides/'):
        kicker = 'Elimenti'
    if p['path'] == '/':
        kicker = 'Web design for the Chicago suburbs'
    if p['path'] == '/custom-websites/':
        kicker = 'Custom websites'
    out.append({'slug': slug_for(p['path']), 'h1': h1, 'kicker': kicker})
print(json.dumps(out))
