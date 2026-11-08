#!/usr/bin/env python3
"""Crawl a built copy of the site and check it before merging.

Usage:
    python3 seo/tools/check.py http://127.0.0.1:8001

Serve the Jekyll output (or the repo, for a rough check) at that address first.
Checks: every internal link and asset resolves; no indexable page has fewer than two
other pages linking to it; no unfilled {{token}} remains; every sitemap URL is reachable,
indexable and canonical; every indexable page is in the sitemap; titles,
descriptions and H1s are present, unique and within length; JSON-LD parses, uses
no Review/AggregateRating, and FAQPage text matches the visible text; visible copy
has no banned terms (plus, outside /concepts/, no Elimenti prices, no "high-end" describing
the client and no "Hinsdale and Oak Brook" location claim). Exits non-zero on any failure.
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

from bs4 import BeautifulSoup

BASE = sys.argv[1].rstrip('/')
SITE = 'https://elimenti.com'
BANNED = [r'\bTODO\b', r'\bTBD\b', r'(?i)lorem', r'(?i)placeholder', r'\[', r'\bXX\b', r'\bAI\b', r'(?i)hand-coded']
# Non-concept pages only: the med spa concept legitimately shows a $175 treatment.
# Elimenti prices live in the written proposal; "high-end" describes the work, never the client;
# Elimenti is based in Hinsdale, and Oak Brook is a town it serves.
BANNED_SITE = [r'\$4,000', r'\$175', r'\$85\b', r'(?i)pro bono', r'(?i)high-end (independent )?business',
               r'(?i)owners of high-end', r'Hinsdale and Oak Brook, IL', r'(?i)(based in|works? out of) Hinsdale and Oak Brook']

failures, notes = [], []
pages, status, seen = {}, {}, set()


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'elimenti-check'})
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return r.status, r.read(), r.headers.get('Content-Type', '')
    except urllib.error.HTTPError as e:
        return e.code, e.read(), ''


def local(url):
    """Map an href/src to a site path, or None for external/special links."""
    if not url or url.startswith(('mailto:', 'tel:', 'data:', 'javascript:')):
        return None
    if url.startswith('#'):
        return None
    if url.startswith(SITE):
        url = url[len(SITE):] or '/'
    if url.startswith(('http://', 'https://', '//')):
        return None
    return urllib.parse.urljoin('/', url.split('#')[0].split('?')[0])


def srcset_urls(srcset):
    """URLs in a srcset. A candidate's URL runs to the next whitespace, so it may contain
    commas (a data: URI does); a comma only separates candidates after a URL or descriptor."""
    return re.findall(r'(\S+?)(?:\s+[\d.]+[wx])?\s*(?:,(?=\s)|,$|$)', srcset.strip())


def crawl(start):
    queue = [start]
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        code, body, ctype = fetch(path)
        status[path] = code
        if code != 200:
            continue
        if 'text/html' in ctype or path.endswith('/') or path.endswith('.html'):
            pages[path] = body.decode('utf-8')
            soup = BeautifulSoup(pages[path], 'lxml')
            refs = [a.get('href') for a in soup.find_all(['a', 'link'], href=True)]
            refs += [t.get('src') for t in soup.find_all(['img', 'script', 'source'], src=True)]
            for t in soup.find_all(['img', 'source'], srcset=True):
                refs += srcset_urls(t['srcset'])
            for t in soup.find_all('link', imagesrcset=True):
                refs += srcset_urls(t['imagesrcset'])
            for r in refs:
                lp = local(r)
                if lp and lp != path:
                    referrers[lp].add(path)  # every referring page, for the orphan check
                if lp and lp not in seen:
                    queue.append(lp)
        elif path.endswith('.css'):
            for u in re.findall(r'url\([\'"]?([^\'")]+)', body.decode('utf-8')):
                lp = local(u)
                if lp and lp not in seen:
                    queue.append(lp)
                    referrers[lp].add(path)


referrers = defaultdict(set)
crawl('/')

# Sitemap
code, body, _ = fetch('/sitemap.xml')
sitemap = [u[len(SITE):] for u in re.findall(r'<loc>([^<]+)</loc>', body.decode())]
for p in sitemap:
    if p not in seen:
        crawl(p)
for p, c in status.items():
    if c != 200:
        failures.append(f'BROKEN {c}: {p} (linked from {sorted(referrers[p])[:3]})')

# llms.txt carries registry titles and descriptions, so the site-only patterns apply to it too.
code, body, _ = fetch('/llms.txt')
if code != 200:
    failures.append(f'llms.txt returned {code}')
else:
    llms = body.decode('utf-8')
    for pat in BANNED_SITE:
        for m in re.finditer(pat, llms):
            failures.append(f'/llms.txt: banned term {pat!r}: ...{llms[max(0, m.start() - 40):m.end() + 40]}...')

code, _, _ = fetch('/no-such-page-check/')
if code != 404:
    failures.append(f'404 handling: unknown URL returned {code}')

titles, descs, h1s = defaultdict(list), defaultdict(list), defaultdict(list)
indexable = set()
for path, html in pages.items():
    soup = BeautifulSoup(html, 'lxml')
    robots = soup.find('meta', attrs={'name': 'robots'})
    noindex = robots and 'noindex' in robots.get('content', '')
    if path.startswith('/concepts/'):
        if not noindex:
            failures.append(f'concept page is indexable: {path}')
        text = BeautifulSoup(html, 'lxml').body.get_text(' ', strip=True)
        for pat in BANNED:
            for m in re.finditer(pat, text):
                failures.append(f'{path}: banned term {pat!r}: ...{text[max(0, m.start() - 40):m.end() + 40]}...')
        continue
    title = soup.title.get_text(strip=True) if soup.title else ''
    desc = (soup.find('meta', attrs={'name': 'description'}) or {}).get('content', '')
    h1 = [h.get_text(' ', strip=True) for h in soup.find_all('h1')]
    if path == '/portfolio.html':
        continue  # meta-refresh stub to /work/, canonical /work/
    if len(h1) != 1:
        failures.append(f'{path}: {len(h1)} H1s')
    if not title or len(title) > 60:
        failures.append(f'{path}: title length {len(title)}: {title}')
    if not desc or len(desc) > 160:
        failures.append(f'{path}: description length {len(desc)}')
    if not noindex:
        indexable.add(path)
        titles[title].append(path)
        descs[desc].append(path)
        h1s[h1[0] if h1 else ''].append(path)
        can = soup.find('link', rel='canonical')
        if not can or can['href'] != SITE + path:
            failures.append(f'{path}: canonical {can["href"] if can else None}')
        for prop in ('og:title', 'og:description', 'og:image', 'og:url'):
            if not soup.find('meta', property=prop):
                failures.append(f'{path}: missing {prop}')
    if '{{' in html or '}}' in html:
        failures.append(f'{path}: unfilled {{{{token}}}} in HTML')
    # alt text
    for img in soup.find_all('img'):
        if img.get('alt') is None:
            failures.append(f'{path}: img without alt {img.get("src")}')
    # JSON-LD
    visible_faq = {}
    for item in soup.select('main .faq-item'):
        q = item.find(['h2', 'h3'])
        visible_faq[q.get_text(' ', strip=True)] = re.sub(r'\s+', ' ', ' '.join(p.get_text(' ', strip=True) for p in item.find_all('p')))
    ld_faq = {}
    for sc in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(sc.string)
        except Exception as e:
            failures.append(f'{path}: JSON-LD parse error {e}')
            continue
        text = json.dumps(data)
        if 'AggregateRating' in text or '"Review"' in text:
            failures.append(f'{path}: Review/AggregateRating markup')
        for node in data.get('@graph', [data]):
            if node.get('@type') == 'FAQPage':
                for q in node['mainEntity']:
                    ld_faq[q['name']] = q['acceptedAnswer']['text']
    if visible_faq != ld_faq and (visible_faq or ld_faq):
        failures.append(f'{path}: FAQPage JSON-LD does not match visible FAQ ({len(ld_faq)} vs {len(visible_faq)})')
    # banned terms in visible copy (body text, alt text and the title/description)
    body = soup.find('body')
    for s in body(['script', 'style']):
        s.decompose()
    visible = ' '.join([body.get_text(' ', strip=True), title, desc] + [i.get('alt', '') for i in body.find_all('img')])
    # JSON-LD and the social tags are checked for the site-only patterns too (no prices in schema).
    hay = ' '.join([visible] + [t.get('content', '') for t in soup.find_all('meta')]
                   + [sc.string or '' for sc in soup.find_all('script', type='application/ld+json')])
    for pat in BANNED_SITE:
        for m in re.finditer(pat, hay):
            failures.append(f'{path}: banned term {pat!r}: ...{hay[max(0, m.start() - 40):m.end() + 40]}...')
    for pat in BANNED:
        for m in re.finditer(pat, visible):
            failures.append(f'{path}: banned term {pat!r}: ...{visible[max(0, m.start() - 40):m.end() + 40]}...')

for label, d in (('title', titles), ('description', descs), ('H1', h1s)):
    for k, v in d.items():
        if len(v) > 1:
            failures.append(f'duplicate {label} on {v}: {k}')

sm = set(sitemap)
for p in indexable - sm:
    failures.append(f'indexable page missing from sitemap: {p}')
for p in sm - indexable:
    failures.append(f'sitemap URL is not an indexable page: {p}')

# Orphans: every indexable page needs at least two other pages linking to it
for p in sorted(indexable):
    refs = {r for r in referrers.get(p, set()) if r != p}
    if p != '/' and len(refs) < 2:
        failures.append(f'orphan: {p} has {len(refs)} referring page(s): {sorted(refs)}')
inbound = sorted((len({r for r in referrers.get(p, set()) if r != p}), p) for p in indexable if p != '/')
notes.append('fewest inbound links: ' + ', '.join(f'{p} ({n})' for n, p in inbound[:5]))

print(f'Crawled {len(seen)} URLs ({len(pages)} HTML pages, {len(indexable)} indexable, {len(sitemap)} in sitemap).')
for n in notes:
    print('note:', n)
if failures:
    print(f'{len(failures)} FAILURES:')
    for f in failures:
        print(' -', f)
    sys.exit(1)
print('All checks passed.')
