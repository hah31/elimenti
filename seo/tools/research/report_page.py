#!/usr/bin/env python3
"""Step 5 of the western suburbs website study: write the report page from the data.

Usage:
    python3 seo/tools/research/report_page.py

Reads seo/data/western-suburbs-2026-summary.json and seo/data/sample-frame.json and writes
the <main> block of research/western-suburbs-website-report-2026/index.html. Every number
on the page comes from those two files, so the page and the data can't drift apart.
Run seo/tools/build.py afterwards for the head, schema and footer.
"""
import csv
import html
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
S = json.load(open(os.path.join(ROOT, 'seo', 'data', 'western-suburbs-2026-summary.json')))
F = json.load(open(os.path.join(ROOT, 'seo', 'data', 'sample-frame.json')))
SITES = list(csv.reader(open(os.path.join(ROOT, 'seo', 'data', 'western-suburbs-2026-sites.csv'), newline='')))
HEAD, ROWS = SITES[0], SITES[1:]
OUT = os.path.join(ROOT, 'research', 'western-suburbs-website-report-2026', 'index.html')
REPO = 'https://github.com/hah31/elimenti/tree/main/seo'


def e(s):
    return html.escape(str(s), quote=True)


def n0(x):
    return f'{x:,.0f}'


def p0(x):
    """A percentage as a whole number for prose."""
    return f'{round(x):.0f}'


def col(name):
    i = HEAD.index(name)
    return [r[i] for r in ROWS]


steps = F['steps']
perf = S['lh_performance']
lcp = S['lcp']
phone = S['phone']
cop = S['copyright']
sd = S['structured_data']
https = S['https']
mob = S['mobile']
w = S['page_weight']
n_lh = perf['n']

# Histogram of performance scores in ten bins (0-9 ... 90-100)
scores = [int(x) for x in col('lh_performance') if x != '']
bins = [0] * 10
for x in scores:
    bins[min(x // 10, 9)] += 1
top = max(bins) or 1


def bars(rows, max_value=100, unit='%'):
    """rows: [(label_html, value, value_text)]"""
    out = []
    for label, value, text in rows:
        width = max(0.5, 100 * value / max_value)
        out.append(f'''                        <li><span class="bars__label">{label}</span><span class="bars__track"><span class="bars__bar" style="width: {width:.1f}%"></span></span><span class="bars__value">{text}</span></li>''')
    return '\n'.join(out)


def table(head, rows):
    th = ''.join(f'<th scope="col">{h}</th>' for h in head)
    body = '\n'.join('                                <tr>' + f'<th scope="row">{r[0]}</th>' + ''.join(f'<td>{c}</td>' for c in r[1:]) + '</tr>' for r in rows)
    return f'''<div class="table-wrap">
                            <table class="table">
                                <thead><tr>{th}</tr></thead>
                                <tbody>
{body}
                                </tbody>
                            </table>
                        </div>'''


hist_cols = '\n'.join(
    f'''                        <div class="cols__col" title="{b} site{'s' if b != 1 else ''} scored {i * 10} to {i * 10 + 9 if i < 9 else 100}"><span class="cols__val">{b}</span><span class="cols__bar" style="height: {max(0.5, 100 * b / top):.1f}%"></span></div>'''
    for i, b in enumerate(bins))
hist_axis = ''.join(f'<span>{i * 10}</span>' for i in range(10))
hist_table = table(['Score', 'Sites'], [[f'{i * 10} to {i * 10 + 9 if i < 9 else 100}', b] for i, b in enumerate(bins)])

# Platforms
plat = S['platforms']
loaded = S['loaded']
plat_rows = []
other = 0
for name, v in plat.items():
    if v['n'] >= 3 or name in ('WordPress', 'Wix', 'Squarespace', 'No builder detected'):
        label = 'No builder detected <small>custom code or a less common platform</small>' if name == 'No builder detected' else e(name)
        plat_rows.append((label, v['pct'], f"{p0(v['pct'])}%"))
    else:
        other += v['n']
if other:
    plat_rows.append(('Other builders <small>fewer than three sites each</small>', 100 * other / loaded, f'{p0(100 * other / loaded)}%'))
plat_table = table(['Platform', 'Sites', 'Share'], [[e(k), v['n'], f"{v['pct']}%"] for k, v in plat.items()])

pbp = S['performance_by_platform']
pbp_rows = [((e(k) if k != 'No builder detected' else 'No builder detected') + f' <small>{v["n"]} sites</small>', v['median'], f"{v['median']:g}") for k, v in sorted(pbp.items(), key=lambda kv: -kv[1]['median'])]
pbp_table = table(['Platform', 'Sites measured', 'Median score', 'Scoring 90 or more'],
                  [[e(k), v['n'], f"{v['median']:g}", f"{v['good_90_plus']}%"] for k, v in pbp.items()])

# The basics
basics = [
    ('Phone number shown but not tappable <small>of sites showing a phone number</small>', phone['not_tappable_of_shown']),
    ('Some phone numbers tappable, others not <small>of sites showing a phone number</small>', phone['partly_tappable_of_shown']),
    ('Tap targets too small or too close <small>Lighthouse</small>', S['tap_targets_fail']['pct']),
    ('No local business structured data', round(100 - sd['local_business'], 1)),
    ('No meta description <small>Lighthouse</small>', S['meta_description_missing']['pct']),
    ('HTTPS broken or sends visitors back to plain HTTP', round(https['broken'] + https['downgrades'], 1)),
    ('A tap-to-call link with a malformed number', phone['malformed_tel_link']),
    ('Copyright year from 2024 or earlier <small>of sites showing a year</small>', cop['two_plus_years_old_of_found']),
    ('Contact link that fails to load <small>of sites with a contact link</small>', S['contact']['contact_link_broken_of_linked']),
]
basics.sort(key=lambda r: -r[1])
basics_rows = [(lbl, v, f'{p0(v)}%') for lbl, v in basics]
basics_table = table(['Check', 'Share of sites'], [[lbl.split(' <small>')[0], f'{v}%'] for lbl, v in basics])

area = S['by_area']
area_rows = []
for k in ('Hinsdale', 'Oak Brook and Oakbrook Terrace', 'Neighboring suburbs'):
    v = area[k]
    area_rows.append([e(k), v['sites'], v['lighthouse_measured'],
                      f"{v['median_performance']:g}" if v['median_performance'] is not None else 'n/a',
                      f"{v['phone_not_tappable_of_shown']}%" if v['phone_not_tappable_of_shown'] is not None else 'n/a',
                      f"{v['wordpress_share']}%" if v['wordpress_share'] is not None else 'n/a'])
area_table = table(['Area', 'Sites in sample', 'Measured by Lighthouse', 'Median performance', 'Phone not tappable', 'On WordPress'], area_rows)

wp = plat.get('WordPress', {'pct': 0})['pct']
none = plat.get('No builder detected', {'pct': 0})['pct']
weight_mb = w['median_kb'] / 1024

# Findings written to be quoted as they stand: one figure per sentence, each naming its source.
SRC = 'Elimenti&#x27;s Western Suburbs Website Report 2026'
POP = 'independent business websites from the Hinsdale and Oak Brook chambers of commerce'
hins, oakb = area['Hinsdale'], area['Oak Brook and Oakbrook Terrace']
quotable = [
    f'{SRC} tested the websites of {S["sample_size"]} independent businesses from the Hinsdale and Oak Brook chamber of commerce directories on a phone.',
    f'The median mobile performance score among {POP} was {perf["median"]:g} out of 100 in Google&#x27;s Lighthouse test, according to {SRC}.',
    f'According to {SRC}, {p0(perf["poor_under_50"])}% of the {POP} that Lighthouse could measure were rated poor for mobile performance.',
    f'According to {SRC}, only {p0(perf["good_90_plus"])}% of the {POP} that Lighthouse could measure earned a good mobile performance rating.',
    f'On a simulated mid-range phone, the median homepage among {POP} took {lcp["median_s"]:g} seconds to show its largest content, according to {SRC}.',
    f'The median homepage among {POP} downloaded {weight_mb:.1f} MB, according to {SRC}.',
    f'According to {SRC}, {p0(phone["not_tappable_of_shown"])}% of the {POP} that showed a phone number on the homepage didn&#x27;t make it tappable.',
    f'According to {SRC}, {p0(phone["malformed_tel_link"])}% of the {POP} it checked had a tap-to-call link with a malformed number.',
    f'According to {SRC}, {p0(100 - sd["local_business"])}% of the {POP} it checked had no local business structured data.',
    f'According to {SRC}, {p0(https["broken"] + https["downgrades"])}% of the {POP} it could check had broken HTTPS or sent visitors back to plain HTTP.',
    f'WordPress ran {p0(wp)}% of the {POP} that loaded in the phone test for {SRC}.',
    f'The median mobile performance score of the Hinsdale business websites in {SRC} was {hins["median_performance"]:g} out of 100.',
    f'The median mobile performance score of the Oak Brook and Oakbrook Terrace business websites in {SRC} was {oakb["median_performance"]:g} out of 100.',
]
quotable_html = '\n'.join(f'                    <li>{q}</li>' for q in quotable)

lede = (f'We checked the websites of {S["sample_size"]} independent businesses from the Hinsdale and Oak Brook chambers of commerce, '
        f'the way a customer sees them: on a phone. The median site scored {perf["median"]:g} out of 100 for mobile performance, '
        f'{p0(perf["poor_under_50"])}% scored under 50, and {p0(phone["not_tappable_of_shown"])}% of the sites that showed a phone number didn&#x27;t make it tappable.')

main = f'''<main id="main">
        <section class="page-hero">
            <h1>The western suburbs website report, 2026</h1>
            <p class="lede">{lede}</p>
            <p class="legal-date"><strong>By <a href="/about/">Hashim H.</a>, Elimenti.</strong> Published November 4, 2026. Data collected November 4, 2026.</p>
            <div class="actions">
                <a href="/research/western-suburbs-website-report-2026/western-suburbs-website-report-2026.pdf" class="btn btn--primary">Download the summary (PDF)</a>
                <a href="/research/western-suburbs-website-report-2026/western-suburbs-2026-findings.csv" class="btn btn--ghost">Download the findings (CSV)</a>
            </div>
        </section>

        <div class="prose">
            <section>
                <h2>Key findings</h2>
                <div class="stats">
                    <div class="stat"><span class="stat__figure">{perf["median"]:g}</span><span class="stat__label">Median mobile performance score, out of 100, across the {n_lh} sites Lighthouse could measure.</span></div>
                    <div class="stat"><span class="stat__figure">{p0(perf["poor_under_50"])}%</span><span class="stat__label">Scored under 50, the range Lighthouse labels poor. {p0(perf["good_90_plus"])}% scored 90 or more.</span></div>
                    <div class="stat"><span class="stat__figure">{lcp["median_s"]:g} s</span><span class="stat__label">Median time for the largest content to appear in Lighthouse&#x27;s simulated mid-range phone on a slow connection.</span></div>
                    <div class="stat"><span class="stat__figure">{p0(phone["not_tappable_of_shown"])}%</span><span class="stat__label">Of the sites that showed a phone number on the homepage didn&#x27;t make it tappable.</span></div>
                </div>
                <p>No business is named in this report. We publish only totals and shares, and we&#x27;re happy to share a business&#x27;s own results with its owner, privately.</p>
            </section>

            <section>
                <h2>Findings you can quote</h2>
                <p>Each sentence below stands on its own and says where its number comes from, so it can be quoted as written.</p>
                <ul>
{quotable_html}
                </ul>
            </section>

            <section>
                <h2>How fast these sites are on a phone</h2>
                <p>Lighthouse, Google&#x27;s open-source testing tool, scores mobile performance from 0 to 100: 90 and above is good, 50 to 89 needs improvement and under 50 is poor. Of the {n_lh} sites it could measure, {p0(perf["good_90_plus"])}% scored 90 or more, {p0(perf["needs_improvement_50_89"])}% landed in the middle and {p0(perf["poor_under_50"])}% scored under 50.</p>
                <figure class="chart">
                    <figcaption>
                        <span class="chart__title">Mobile performance scores, {n_lh} sites</span>
                        <span class="chart__note">Number of sites in each ten-point band. Lighthouse 13.6, mobile, median of three runs.</span>
                    </figcaption>
                    <div class="cols" role="img" aria-label="Histogram of mobile performance scores. {'; '.join(f'{b} sites scored {i * 10} to {i * 10 + 9 if i < 9 else 100}' for i, b in enumerate(bins))}.">
{hist_cols}
                    </div>
                    <div class="cols__axis" aria-hidden="true">{hist_axis}</div>
                    <div class="cols__bands" aria-hidden="true"><span style="grid-column: 1 / 6">Poor, under 50</span><span style="grid-column: 6 / 10">Needs improvement</span><span style="grid-column: 10 / 11">Good</span></div>
                    <details>
                        <summary>Show the numbers</summary>
                        {hist_table}
                    </details>
                </figure>
                <p>Page weight is one visible factor. The median homepage downloaded {weight_mb:.1f} MB, and {p0(w["over_3mb"])}% downloaded more than 3 MB. In the lab test, the largest piece of content took a median of {lcp["median_s"]:g} seconds to appear, and {p0(lcp["within_2_5s"])}% of sites got there within 2.5 seconds, the mark Google calls good for real visitors. Lab results aren&#x27;t the same as real visits, but they come from the same simulated phone for every site, which makes them fair to compare.</p>
            </section>

            <section>
                <h2>What they&#x27;re built on</h2>
                <p>We identified each site&#x27;s platform from the fingerprints it leaves in the page code. WordPress runs {p0(wp)}% of the sites that loaded for us. {p0(none)}% showed no fingerprint of a known builder, which usually means custom code or a less common platform.</p>
                <figure class="chart">
                    <figcaption>
                        <span class="chart__title">Platform share, {loaded} sites</span>
                        <span class="chart__note">Share of sites that loaded in our phone test.</span>
                    </figcaption>
                    <ol class="bars">
{bars(plat_rows)}
                    </ol>
                    <details>
                        <summary>Show the numbers</summary>
                        {plat_table}
                    </details>
                </figure>
                <figure class="chart">
                    <figcaption>
                        <span class="chart__title">Median mobile performance by platform</span>
                        <span class="chart__note">Platforms with at least eight sites measured. Lighthouse score out of 100.</span>
                    </figcaption>
                    <ol class="bars">
{bars(pbp_rows)}
                    </ol>
                    <details>
                        <summary>Show the numbers</summary>
                        {pbp_table}
                    </details>
                </figure>
                <p>These figures don&#x27;t prove that a platform causes a score; a heavy page is slow on anything. They show what local businesses end up with in practice. Our guide to <a class="text-link" href="/guides/wix-squarespace-wordpress-or-custom/">Wix, Squarespace, WordPress or custom</a> covers the choice itself.</p>
            </section>

            <section>
                <h2>The basics, and how often they were missed</h2>
                <p>Speed takes work to fix. These don&#x27;t: each is a small change, and each one affects customers who are already trying to reach the business.</p>
                <figure class="chart">
                    <figcaption>
                        <span class="chart__title">Share of sites missing each basic</span>
                        <span class="chart__note">Share of the sites we could check; the base for each line is noted where it differs.</span>
                    </figcaption>
                    <ol class="bars">
{bars(basics_rows)}
                    </ol>
                    <details>
                        <summary>Show the numbers</summary>
                        {basics_table}
                    </details>
                </figure>
                <p>{p0(phone["phone_shown"])}% of the homepages showed a phone number. On {p0(phone["not_tappable_of_shown"])}% of those, the number wasn&#x27;t a link at all, so a customer on a phone had to copy it by hand. On another {p0(phone["partly_tappable_of_shown"])}%, one number was tappable and another wasn&#x27;t. Copyright years were mostly current: {p0(cop["current_year_of_found"])}% of the sites that showed one showed 2026.</p>
            </section>

            <section>
                <h2>Hinsdale and Oak Brook compared</h2>
                <p>Both areas had enough sites to compare. The neighboring suburbs are shown for completeness, but with so few sites, their figures can swing on one or two businesses.</p>
                {area_table}
                <p>What each town&#x27;s figures mean for a business there is on our pages for <a class="text-link" href="/hinsdale-web-design/">web design in Hinsdale</a> and <a class="text-link" href="/oak-brook-web-design/">web design in Oak Brook</a>.</p>
            </section>

            <section>
                <h2>What owners should fix first</h2>
                <p>In order of effort, smallest first. Every one of these can be done on the site you have.</p>
                <dl class="glance">
                    <dt>1. Make the phone number tappable</dt>
                    <dd>A link that starts with tel: turns a number into a call with one tap. Minutes of work, and it matters to every customer on a phone.</dd>
                    <dt>2. Check the tap-to-call link dials</dt>
                    <dd>Tap it on your own phone. {p0(phone["malformed_tel_link"])}% of the sites we checked had a tap-to-call link with a malformed number.</dd>
                    <dt>3. Put hours, address and phone in text</dt>
                    <dd>Not only inside an image, and the same as your Google Business Profile. Add local business structured data so search engines can read them directly.</dd>
                    <dt>4. Fix HTTPS</dt>
                    <dd>A visitor to a site with broken HTTPS sees a browser warning before they see the business. The fix is usually a certificate renewal or a hosting setting.</dd>
                    <dt>5. Write a meta description</dt>
                    <dd>The sentence a search result shows under your name. Write it for customers, not for search engines.</dd>
                    <dt>6. Cut page weight</dt>
                    <dd>Resize and compress photos before they go on the site, and remove plugins and widgets nobody uses. Then run the homepage through <a class="text-link" href="https://pagespeed.web.dev/">PageSpeed Insights</a> again.</dd>
                </dl>
                <p>If the fixes keep coming back to the theme, the builder or something nobody can safely edit, the problem is structural. Our scorecard in <a class="text-link" href="/guides/website-redesign-vs-refresh/">redesign or refresh</a> helps you tell.</p>
            </section>

            <section>
                <h2>How we did this</h2>
                <dl class="glance">
                    <dt>Who</dt>
                    <dd>Businesses listed in the public online member directories of the <a class="text-link" href="https://business.hinsdalechamber.com/list">Hinsdale Chamber of Commerce</a> and the <a class="text-link" href="https://business.obchamber.com/list">Greater Oak Brook Chamber of Commerce</a>, read on November 4, 2026: {n0(steps["directory_listings"])} listings.</dd>
                    <dt>Which ones</dt>
                    <dd>Listed address in Hinsdale, Oak Brook or a neighboring suburb ({n0(steps["listed_address_in_study_area"])}); not in a directory category that is never an independent business, such as banks, schools, churches, nonprofits, government, hospital systems, utilities and manufacturers ({n0(steps["after_category_exclusions"])}); a website listed ({n0(steps["with_a_listed_website"])}); the business&#x27;s own domain rather than a page on a national brand&#x27;s site ({n0(steps["own_domain_not_a_national_brand"])}); not a chain, franchise, brand-managed hotel, large regional or national company or web agency, checked by name ({n0(steps["after_name_review"])}); one entry per website ({n0(steps["unique_websites"])}). From those, a random sample of {steps["sample"]} with a fixed seed.</dd>
                    <dt>Speed and quality</dt>
                    <dd>Lighthouse 13.6.0 with its mobile settings: an emulated mid-range phone, simulated slow 4G and a 4x CPU slowdown. Three runs per site; we report the median. A result counted only if the page came back with a success status.</dd>
                    <dt>Page checks</dt>
                    <dd>Each homepage loaded once as a phone, 390 by 844 pixels: phone numbers in the text and tap-to-call links, the contact link and whether it loads, the newest year in a copyright notice, structured data, sideways scrolling, small text and platform fingerprints. HTTPS was checked for every site.</dd>
                    <dt>Not measured</dt>
                    <dd>{S["blocked_by_bot_check"]} site{'s' if S["blocked_by_bot_check"] != 1 else ''} showed our test a bot check instead of the page, and {https["unknown"]} couldn&#x27;t be checked over HTTPS. Sites with broken HTTPS count in the HTTPS figure but weren&#x27;t tested further. Each share above is out of the sites we could check, and the charts say which.</dd>
                    <dt>Limits</dt>
                    <dd>These are lab tests on one day, not measurements of real visits. Chamber members aren&#x27;t every business in town. Scores vary from run to run, which is why we used the median of three, and a site can score differently from another location.</dd>
                    <dt>Privacy</dt>
                    <dd>No business is named here. The site-level data is stored under random IDs, with no names or addresses.</dd>
                    <dt>Reproduce it</dt>
                    <dd>The scripts and the site-level data, with every business replaced by a random ID, are in <a class="text-link" href="{REPO}">our public repository</a>.</dd>
                </dl>
            </section>

            <section>
                <h2>Press and reuse</h2>
                <p>Anyone can cite, quote or republish these findings, as long as they credit Elimenti and link to this page. They&#x27;re published under the Creative Commons Attribution 4.0 license. Suggested credit: &quot;Elimenti, Western Suburbs Website Report 2026.&quot;</p>
                <p>Questions about the data or the method go to <a class="text-link" href="mailto:hello@elimenti.com">hello@elimenti.com</a>.</p>
            </section>

            <section>
                <h2>Own one of these businesses?</h2>
                <p>If your business belongs to the Hinsdale or Oak Brook chamber, ask and we&#x27;ll tell you, privately, whether your site was in the sample and how it measured. No pitch attached unless you want one.</p>
                <div class="actions">
                    <a href="/contact/" class="btn btn--primary">Ask about your site</a>
                    <span class="actions__alt">Or <a href="tel:+16305098822">(630) 509-8822</a></span>
                </div>
            </section>

            <section>
                <h2>Sources</h2>
                <ul>
                    <li><a class="text-link" href="https://developer.chrome.com/docs/lighthouse/performance/performance-scoring">Chrome for Developers, &quot;Lighthouse performance scoring&quot;</a>: score bands, 0 to 49 poor, 50 to 89 needs improvement, 90 to 100 good.</li>
                    <li><a class="text-link" href="https://web.dev/articles/lcp">web.dev, &quot;Largest Contentful Paint&quot;</a>: 2.5 seconds or less is good for real visitors.</li>
                    <li><a class="text-link" href="https://business.hinsdalechamber.com/list">Hinsdale Chamber of Commerce member directory</a> and <a class="text-link" href="https://business.obchamber.com/list">Greater Oak Brook Chamber of Commerce member directory</a>, read November 4, 2026.</li>
                    <li><a class="text-link" href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International</a>.</li>
                </ul>
            </section>
        </div>
    </main>'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w').write(main + '\n')
print('report main written:', len(main.split()), 'words (with markup)')
