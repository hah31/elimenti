#!/usr/bin/env python3
"""Generate /llms.txt from the PAGES registry in build.py.

Every indexable page (the same set that goes into sitemap.xml) is listed once,
using its registry title and meta description, so the file can't drift from the
site. The summary and key facts come from the registry's business data. No prices: every
project is scoped individually and priced in a written proposal.
Format follows https://llmstxt.org/: H1, blockquote summary, notes, then H2 link lists.

Run from the repo root after build.py:
    python3 seo/tools/llms.py           # write llms.txt
    python3 seo/tools/llms.py --check   # exit 1 if llms.txt is out of date

Google Search ignores llms.txt (Search Central, AI optimization guide), so this
file is for other tools that read it; it has no effect on Google rankings.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402  (importing runs nothing; build.py's work is under __main__)

SITE = build.SITE
OUT = os.path.join(build.ROOT, 'llms.txt')
RESEARCH = build.RESEARCH_PATH

# Section order, and which pages go in each. A page lands in the first section that claims it.
FOOTER = {label: [href for href, _ in links] for label, links in build.FOOTER_GROUPS}
SECTIONS = [
    ('Services', lambda p: p == '/' or (p in FOOTER['Services'] and not p.startswith('/work/'))),
    ('Industries', lambda p: p in FOOTER['Industries']),
    ('Areas', lambda p: p in FOOTER['Areas']),
    ('Work', lambda p: p.startswith('/work/')),
    ('Guides', lambda p: p.startswith('/guides/')),
    ('Research', lambda p: p.startswith('/research/')),
    ('Studio', lambda p: p in ('/about/', '/faq/', '/contact/')),
]
OPTIONAL = ('/privacy/', '/terms/')
DOWNLOADS = [
    (f'{RESEARCH}western-suburbs-website-report-2026.pdf', 'The western suburbs website report, 2026 (PDF)',
     'The research report as a printable PDF.'),
    (f'{RESEARCH}western-suburbs-2026-findings.csv', 'Study findings (CSV)',
     'Aggregate figures from the research report. No business is named.'),
]


def indexable():
    return [p for p in build.PAGES
            if p.get('sitemap', True) and not p.get('robots') and os.path.exists(os.path.join(build.ROOT, p['file']))]


def name(p):
    return p['title'].split(' | ')[0]


def line(path, title, desc):
    return f'- [{title}]({SITE}{path}): {desc}'


def render():
    pages = indexable()
    biz = build.BUSINESS

    out = [
        f"# {biz['name']}",
        '',
        f"> {biz['description']}",
        '',
        'Key facts:',
        '',
        '- Every project, on WordPress or custom-coded, is scoped individually. The exact price and timeline come in a written proposal before any work starts.',
        '- Site Care: a monthly plan or hourly edits, with a five-business-day turnaround.',
        f"- Founder: {biz['founder']['name']}",
        f'- Contact: {build.PHONE_DISPLAY}, {build.EMAIL}, or {SITE}/contact/',
    ]

    placed = set()
    for label, claims in SECTIONS:
        items = [p for p in pages if p['path'] not in placed and p['path'] not in OPTIONAL and claims(p['path'])]
        if not items:
            continue
        out += ['', f'## {label}', '']
        for p in items:
            placed.add(p['path'])
            out.append(line(p['path'], name(p), p['description']))

    optional = [p for p in pages if p['path'] in OPTIONAL]
    out += ['', '## Optional', '']
    for p in optional:
        placed.add(p['path'])
        out.append(line(p['path'], name(p), p['description']))
    for path, title, desc in DOWNLOADS:
        if not os.path.exists(os.path.join(build.ROOT, path.lstrip('/'))):
            sys.exit(f'Missing download {path}')
        out.append(line(path, title, desc))

    missing = [p['path'] for p in pages if p['path'] not in placed]
    if missing:
        sys.exit(f'Pages not assigned to any llms.txt section: {missing}')
    return '\n'.join(out) + '\n', len(placed)


if __name__ == '__main__':
    text, n = render()
    current = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else None
    if '--check' in sys.argv:
        if text != current:
            sys.exit('llms.txt is out of date: run python3 seo/tools/llms.py')
        print(f'llms.txt up to date ({n} pages)')
    else:
        if text != current:
            open(OUT, 'w', encoding='utf-8').write(text)
        print(f'llms.txt {"written" if text != current else "unchanged"} ({n} pages)')
