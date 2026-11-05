#!/usr/bin/env python3
"""Measure how much visible copy two or more pages share, as 5-word phrases (shingles).

Usage (from the repo root):
    python3 seo/tools/overlap.py car-club-websites classic-car-club-websites
    python3 seo/tools/overlap.py --all          # every pair of industry and location pages

Text is the page's <main>, lowercased, with punctuation removed. For each pair it prints
the share of the smaller page's distinct 5-word phrases that also appear on the other page
(containment), and the Jaccard share of all distinct phrases across both pages.
"""
import itertools
import os
import re
import sys

from bs4 import BeautifulSoup

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
N = 5
GROUP = ['hinsdale-web-design', 'oak-brook-web-design', 'chicago-suburbs-web-design', 'med-spa-websites',
         'interior-designer-websites', 'custom-home-builder-websites', 'landscape-design-websites',
         'boutique-websites', 'car-club-websites', 'classic-car-club-websites']


def shingles(slug):
    soup = BeautifulSoup(open(os.path.join(ROOT, slug, 'index.html'), encoding='utf-8').read(), 'lxml')
    text = soup.find('main').get_text(' ', strip=True).lower().replace('’', "'")
    words = re.findall(r"[a-z0-9$']+", text)
    return {' '.join(words[i:i + N]) for i in range(len(words) - N + 1)}


def compare(a, b):
    sa, sb = shingles(a), shingles(b)
    inter = len(sa & sb)
    return inter / min(len(sa), len(sb)), inter / len(sa | sb), inter


if __name__ == '__main__':
    slugs = GROUP if '--all' in sys.argv else sys.argv[1:]
    rows = []
    for a, b in itertools.combinations(slugs, 2):
        c, j, n = compare(a, b)
        rows.append((c, j, n, a, b))
    for c, j, n, a, b in sorted(rows, reverse=True):
        print(f'{c * 100:5.1f}% containment  {j * 100:5.1f}% Jaccard  {n:4d} shared  {a} / {b}')
