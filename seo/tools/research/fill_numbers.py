#!/usr/bin/env python3
"""Step 7: put the study's numbers into the guides and town pages.

Usage:
    python3 seo/tools/research/fill_numbers.py PORTFOLIO_LH_JSONL

Pages that quote the study were written with {{TOKENS}}; this replaces each token with
the value from seo/data/western-suburbs-2026-summary.json (and the five-run Lighthouse
measurement of aamineez.art for its case study), then reports any token left unfilled.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
S = json.load(open(os.path.join(ROOT, 'seo', 'data', 'western-suburbs-2026-summary.json')))


def p0(x):
    return f'{round(x):.0f}'


def g(x):
    return f'{x:g}'


pbp = S['performance_by_platform']
plat = S['platforms']


def perf_cell(name):
    if name in pbp:
        v = pbp[name]
        return f'{g(v["median"])} out of 100 ({v["n"]} sites)'
    n = plat.get(name, {}).get('n', 0)
    return f'Too few sites to report ({n} found)'


none = pbp.get('No builder detected')
too_few = [k for k in ('Wix', 'Squarespace') if k not in pbp]
note = ('Medians are shown only where at least eight sites were measured'
        + (f'; {" and ".join(too_few)} had fewer.' if too_few else '.')
        + ' The custom-coded column uses sites that showed no fingerprint of a known builder, a group that includes custom code and less common platforms.')
share = lambda k: p0(plat.get(k, {'pct': 0})['pct'])
platform_sentence = (f'Of the {S["loaded"]} local business websites that loaded in our phone test, {share("WordPress")}% ran on WordPress, '
                     f'{share("Squarespace")}% on Squarespace, {share("Shopify")}% on Shopify and {share("Wix")}% on Wix. '
                     f'{share("No builder detected")}% showed no fingerprint of a known builder, which usually means custom code or a less common platform.')
A = S['by_area']
H, O = A['Hinsdale'], A['Oak Brook and Oakbrook Terrace']
T = {
    'SAMPLE': str(S['sample_size']),
    'COPY_OLD_PCT': p0(S['copyright']['two_plus_years_old_of_found']),
    'PHONE_NOTAP_PCT': p0(S['phone']['not_tappable_of_shown']),
    'HTTPS_FAIL_PCT': p0(S['https']['broken'] + S['https']['downgrades']),
    'PERF_POOR_PCT': p0(S['lh_performance']['poor_under_50']),
    'LOCALBIZ_PCT': p0(S['structured_data']['local_business']),
    'PERF_MEDIAN': g(S['lh_performance']['median']),
    'WP_PCT': p0(plat.get('WordPress', {'pct': 0})['pct']),
    'PERF_WIX': perf_cell('Wix'), 'PERF_SQ': perf_cell('Squarespace'), 'PERF_WP': perf_cell('WordPress'),
    'PERF_NONE': (f'{g(none["median"])} out of 100 for sites with no builder fingerprint ({none["n"]} sites)' if none else 'Too few sites to report'),
    'PERF_NOTE': note,
    'PLATFORM_SENTENCE': platform_sentence,
    'H_SITES': str(H['sites']), 'H_PERF': g(H['median_performance']), 'H_NOTAP': p0(H['phone_not_tappable_of_shown']), 'H_WP': p0(H['wordpress_share']),
    'O_SITES': str(O['sites']), 'O_PERF': g(O['median_performance']), 'O_NOTAP': p0(O['phone_not_tappable_of_shown']), 'O_WP': p0(O['wordpress_share']),
}
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    port = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[1]) if l.strip()}
    a = port.get('p-aamineez', {}).get('median')
    if a:
        T['AAM_LH'] = (f'Measured with Lighthouse 13.6 on mobile, median of five runs on November 4, 2026: '
                       f'{round(100 * a["performance"])} for performance, {round(100 * a["accessibility"])} for accessibility, '
                       f'{round(100 * a["bestPractices"])} for best practices and {round(100 * a["seo"])} for SEO, out of 100. '
                       f'Check it yourself at <a class="text-link" href="https://pagespeed.web.dev/">pagespeed.web.dev</a>.')

files = [f for f in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True) if '/concepts/' not in f]
files += [os.path.join(ROOT, 'seo', n) for n in ('off-site-kit-v2.md', 'REPORT-v2.md') if os.path.exists(os.path.join(ROOT, 'seo', n))]
left = {}
for f in files:
    s = open(f, encoding='utf-8').read()
    if '{{' not in s:
        continue
    new = re.sub(r'\{\{([A-Z_]+)\}\}', lambda m: T.get(m.group(1), m.group(0)), s)
    if new != s:
        open(f, 'w', encoding='utf-8').write(new)
    rest = re.findall(r'\{\{([A-Z_]+)\}\}', new)
    if rest:
        left[os.path.relpath(f, ROOT)] = rest
print(json.dumps(T, indent=1)[:2500])
print('unfilled:', left or 'none')
