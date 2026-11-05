#!/usr/bin/env python3
"""Static audit of the built site, read straight from the repo's HTML files.

Usage (from the repo root, after build.py):
    python3 seo/tools/audit.py              # print the per-page table and every problem found
    python3 seo/tools/audit.py --json OUT   # also write the raw numbers to OUT

Per sitemap URL: title and length, description and length, H1, words in <main>,
JSON-LD @types, internal links in (distinct referring pages, all links and links
inside <main> only) and internal links out (distinct target pages).
Site-wide: repo pages not in the sitemap and sitemap URLs with no file; JSON-LD that
doesn't parse; @id references with no definition anywhere on the site; internal
links (and #fragments) that don't resolve; <img> without alt, width or height.
Exits non-zero if any problem is found.
"""
import json
import os
import re
import sys
import urllib.parse
from collections import defaultdict

from bs4 import BeautifulSoup

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SITE = 'https://elimenti.com'
SKIP_DIRS = {'.git', 'seo', 'node_modules', '.github'}


def path_for(rel):
    rel = rel.replace(os.sep, '/')
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel


def file_for(path):
    """Site path -> repo file, or None."""
    p = urllib.parse.unquote(path).lstrip('/')
    cands = [os.path.join(ROOT, p, 'index.html')] if (p == '' or p.endswith('/')) else [os.path.join(ROOT, p), os.path.join(ROOT, p, 'index.html')]
    for c in cands:
        if os.path.isfile(c):
            return c
    return None


def local(url, base):
    if not url or url.startswith(('mailto:', 'tel:', 'data:', 'javascript:', 'sms:')):
        return None, None
    if url.startswith(SITE):
        url = url[len(SITE):] or '/'
    if url.startswith(('http://', 'https://', '//')):
        return None, None
    full = urllib.parse.urljoin(base, url)
    parsed = urllib.parse.urlparse(full)
    return parsed.path or base, parsed.fragment or None


def words(el):
    return len(re.findall(r"[A-Za-z0-9$%][A-Za-z0-9$%'’.,\-]*", el.get_text(' ', strip=True))) if el else 0


def walk_ld(node, defs, refs, types, top=True):
    if isinstance(node, dict):
        if '@id' in node:
            if set(node) - {'@id'}:
                defs.add(node['@id'])
            else:
                refs.add(node['@id'])
        if top and '@type' in node:
            types.append(node['@type'] if isinstance(node['@type'], str) else '/'.join(node['@type']))
        for k, v in node.items():
            if k == '@graph':
                walk_ld(v, defs, refs, types, True)
            elif k not in ('@id', '@type', '@context'):
                walk_ld(v, defs, refs, types, False)
    elif isinstance(node, list):
        for v in node:
            walk_ld(v, defs, refs, types, top)


def main():
    files = []
    for d, dirs, fs in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in fs:
            if f.endswith('.html'):
                files.append(os.path.relpath(os.path.join(d, f), ROOT))
    sitemap = [u[len(SITE):] for u in re.findall(r'<loc>([^<]+)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read())]

    problems = defaultdict(list)
    pages, ids_on_page = {}, {}
    for rel in sorted(files):
        path = path_for(rel)
        soup = BeautifulSoup(open(os.path.join(ROOT, rel), encoding='utf-8').read(), 'lxml')
        robots = soup.find('meta', attrs={'name': 'robots'})
        refresh = soup.find('meta', attrs={'http-equiv': re.compile('refresh', re.I)})
        kind = 'redirect stub' if refresh else ('noindex' if robots and 'noindex' in robots.get('content', '') else 'indexable')
        pages[path] = dict(file=rel, soup=soup, kind=kind)
        ids_on_page[path] = {t['id'] for t in soup.find_all(id=True)} | {t['name'] for t in soup.find_all('a', attrs={'name': True})}

    indexable = {p for p, v in pages.items() if v['kind'] == 'indexable'}
    links_out, links_out_main = defaultdict(set), defaultdict(set)
    ld_defs, ld_refs_by_page = set(), {}
    rows = {}
    for path, v in pages.items():
        soup, rel = v['soup'], v['file']
        main_el = soup.find('main')
        # Links and assets
        for tag, attr in (('a', 'href'), ('link', 'href'), ('img', 'src'), ('script', 'src'), ('source', 'src')):
            for t in soup.find_all(tag, attrs={attr: True}):
                target, frag = local(t[attr], path)
                if target is None:
                    continue
                if tag == 'link' and t.get('rel') and set(t['rel']) & {'canonical'}:
                    continue
                if not file_for(target):
                    problems['broken internal link or asset'].append(f'{path} -> {t[attr]}')
                    continue
                if tag == 'a':
                    tp = path_for(os.path.relpath(file_for(target), ROOT))
                    if frag and tp in ids_on_page and frag not in ids_on_page[tp]:
                        problems['link to a #fragment that does not exist'].append(f'{path} -> {t[attr]}')
                    if tp != path:
                        links_out[path].add(tp)
                        if main_el and main_el in t.parents:
                            links_out_main[path].add(tp)
        for t in soup.find_all(['img', 'source'], srcset=True):
            for c in t['srcset'].split(','):
                u = c.strip().split(' ')[0]
                target, _ = local(u, path)
                if target and not file_for(target):
                    problems['broken internal link or asset'].append(f'{path} -> {u} (srcset)')
        # Images
        if v['kind'] != 'redirect stub':
            for img in soup.find_all('img'):
                miss = [a for a in ('alt', 'width', 'height') if img.get(a) is None]
                if miss:
                    problems['image missing ' + '/'.join(miss)].append(f'{path}: {img.get("src")}')
        # JSON-LD
        types, refs, defs = [], set(), set()
        for sc in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(sc.string)
            except Exception as e:  # noqa: BLE001
                problems['JSON-LD does not parse'].append(f'{path}: {e}')
                continue
            walk_ld(data, defs, refs, types)
        ld_defs |= defs
        ld_refs_by_page[path] = refs
        title = soup.title.get_text(strip=True) if soup.title else ''
        desc = (soup.find('meta', attrs={'name': 'description'}) or {}).get('content', '')
        h1 = ' / '.join(h.get_text(' ', strip=True) for h in soup.find_all('h1'))
        rows[path] = dict(title=title, title_len=len(title), desc=desc, desc_len=len(desc), h1=h1,
                          words=words(main_el), types=sorted(set(types), key=types.index))

    for path, refs in ld_refs_by_page.items():
        for r in sorted(refs - ld_defs):
            problems['JSON-LD @id referenced but never defined'].append(f'{path}: {r}')

    referrers, referrers_main = defaultdict(set), defaultdict(set)
    for src in indexable:
        for t in links_out[src]:
            referrers[t].add(src)
        for t in links_out_main[src]:
            referrers_main[t].add(src)

    for p in sitemap:
        if p not in pages:
            problems['sitemap URL with no file'].append(p)
        elif pages[p]['kind'] != 'indexable':
            problems['sitemap URL that is not indexable'].append(f'{p} ({pages[p]["kind"]})')
    if len(sitemap) != len(set(sitemap)):
        problems['sitemap URL listed twice'] += sorted({p for p in sitemap if sitemap.count(p) > 1})
    not_in_sitemap = sorted(p for p in pages if p not in sitemap)
    for p in not_in_sitemap:
        if pages[p]['kind'] == 'indexable':
            problems['indexable page missing from sitemap'].append(p)

    for p in sitemap:
        if p in rows:
            rows[p].update(inbound=len(referrers[p]), inbound_main=len(referrers_main[p]),
                           outbound=len(links_out[p]), outbound_main=len(links_out_main[p]))
    under = [(p, rows[p]['inbound'], rows[p]['inbound_main']) for p in sitemap if p in rows and p != '/' and rows[p]['inbound_main'] <= 1]
    for p, n, m in under:
        if n <= 1:
            problems['page with fewer than two referring pages'].append(p)

    # Report
    out = []
    out.append('| URL | Title (len) | Description (len) | H1 | Words in main | JSON-LD @types | In: pages (in main) | Out: pages (in main) |')
    out.append('|---|---|---|---|---|---|---|---|')
    for p in sitemap:
        r = rows.get(p)
        if not r:
            out.append(f'| `{p}` | missing file | | | | | | |')
            continue
        esc = lambda s: s.replace('|', '\\|')  # noqa: E731
        out.append(f'| `{p}` | {esc(r["title"])} ({r["title_len"]}) | {esc(r["desc"])} ({r["desc_len"]}) | {esc(r["h1"])} | {r["words"]} | '
                   f'{", ".join(r["types"])} | {r["inbound"]} ({r["inbound_main"]}) | {r["outbound"]} ({r["outbound_main"]}) |')
    print('\n'.join(out))
    print()
    print('Pages with 0 or 1 referring pages from links inside <main> (footer/nav links excluded):')
    for p, n, m in sorted(under, key=lambda x: (x[2], x[0])):
        print(f'  {p}: {m} in main, {n} counting nav/footer')
    print()
    print('Repo pages not in sitemap.xml:')
    for p in not_in_sitemap:
        print(f'  {p} ({pages[p]["kind"]})')
    print()
    total = sum(len(v) for v in problems.values())
    print(f'{total} problem(s)')
    for k, v in problems.items():
        print(f'- {k}: {len(v)}')
        for x in v:
            print('    ', x)
    if '--json' in sys.argv:
        json.dump(dict(rows=rows, sitemap=sitemap, problems=problems, under=under, not_in_sitemap=not_in_sitemap,
                       referrers_main={k: sorted(v) for k, v in referrers_main.items()}),
                  open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1, default=list)
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
