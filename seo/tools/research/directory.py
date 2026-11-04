#!/usr/bin/env python3
"""Step 1 of the western suburbs website study: build the sampling frame.

Reads the public online member directories of the Hinsdale Chamber of Commerce and
the Greater Oak Brook Chamber of Commerce (both GrowthZone directories), visits every
category page, then every member page, and records each member's name, categories,
listed city and listed website.

Polite by design: one request at a time, a pause between requests, robots.txt
disallow rules respected (only /list/category/ and /list/member/ pages are read).

Usage:
    python3 seo/tools/research/directory.py OUT_DIR
Writes OUT_DIR/members.json. That file names businesses, so it is kept out of the
public repo (see seo/data/README.md).
"""
import json
import os
import re
import sys
import time
import urllib.robotparser

import requests
from bs4 import BeautifulSoup

DIRECTORIES = {
    'Hinsdale Chamber of Commerce': 'https://business.hinsdalechamber.com',
    'Greater Oak Brook Chamber of Commerce': 'https://business.obchamber.com',
}
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0 Safari/537.36 elimenti-research'
PAUSE = 0.8

session = requests.Session()
session.headers['User-Agent'] = UA


def get(url, rp):
    if not rp.can_fetch(UA, url):
        raise RuntimeError(f'robots.txt disallows {url}')
    for attempt in range(3):
        try:
            r = session.get(url, timeout=30)
            time.sleep(PAUSE)
            if r.status_code == 200:
                return r.text
            if r.status_code == 404:
                return None
        except requests.RequestException:
            pass
        time.sleep(2 ** (attempt + 1))
    return None


def main(out_dir):
    members = {}
    for chamber, base in DIRECTORIES.items():
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(session.get(base + '/robots.txt', timeout=30).text.splitlines())
        index = BeautifulSoup(get(base + '/list', rp), 'lxml')
        cats = sorted({a['href'] for a in index.find_all('a', href=True) if '/list/category/' in a['href']})
        print(f'{chamber}: {len(cats)} categories', flush=True)
        for cat_url in cats:
            html = get(cat_url, rp)
            if not html:
                continue
            soup = BeautifulSoup(html, 'lxml')
            cat_name = soup.find('h1') or soup.find('title')
            cat_name = re.sub(r'\s+', ' ', cat_name.get_text(' ', strip=True)) if cat_name else cat_url
            for card in soup.select('.gz-list-card-wrapper'):
                a = card.select_one('.gz-card-title a')
                if not a:
                    continue
                url = a['href']
                city = card.select_one('.gz-address-city')
                m = members.setdefault(url, {
                    'chamber': chamber, 'member_page': url, 'name': a.get_text(' ', strip=True),
                    'city': city.get_text(strip=True) if city else '', 'categories': []})
                m['categories'].append(cat_url.rsplit('/', 1)[-1])
        print(f'  {sum(1 for m in members.values() if m["chamber"] == chamber)} members so far', flush=True)
        # Member pages: website link
        for url, m in members.items():
            if m['chamber'] != chamber or 'website' in m:
                continue
            html = get(url, rp)
            m['website'] = ''
            if not html:
                continue
            soup = BeautifulSoup(html, 'lxml')
            # Try the website button first; the logo link also carries itemprop="url".
            for sel in ('li.gz-card-website a', '.gz-card-website a', 'a[itemprop="url"]'):
                w = next((a for a in soup.select(sel) if a.get('href', '').startswith('http')), None)
                if w:
                    m['website'] = w['href'].strip()
                    break
            if not m['city']:
                c = soup.select_one('.gz-address-city')
                m['city'] = c.get_text(strip=True) if c else ''
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'members.json'), 'w') as f:
        json.dump(sorted(members.values(), key=lambda m: (m['chamber'], m['name'].lower())), f, indent=1)
    print(f'{len(members)} members written', flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
