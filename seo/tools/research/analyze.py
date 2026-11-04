#!/usr/bin/env python3
"""Step 4 of the western suburbs website study: merge, pseudonymize and aggregate.

Usage:
    python3 seo/tools/research/analyze.py PRIVATE_DIR

Reads PRIVATE_DIR/sample.json, pages_v2.jsonl and lh_*.jsonl. Writes:
  seo/data/western-suburbs-2026-sites.csv   one row per site, no names, URLs, phone numbers
                                             or email addresses (pseudonymous id only)
  seo/data/western-suburbs-2026-summary.json every aggregate the published report uses
  research/western-suburbs-website-report-2026/western-suburbs-2026-findings.csv
                                             the aggregate table offered for download
Every number on the report page should trace to summary.json.
"""
import csv
import glob
import json
import os
import re
import statistics as st
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
CURRENT_YEAR = 2026

# schema.org types that are LocalBusiness or one of its common subtypes
LOCAL_TYPES = {
    'LocalBusiness', 'ProfessionalService', 'Store', 'ClothingStore', 'JewelryStore', 'FurnitureStore', 'HomeGoodsStore',
    'BookStore', 'GardenStore', 'PetStore', 'SportingGoodsStore', 'ShoeStore', 'GroceryStore', 'Restaurant', 'FoodEstablishment',
    'CafeOrCoffeeShop', 'Bakery', 'BarOrPub', 'Dentist', 'MedicalBusiness', 'MedicalClinic', 'Physician', 'MedicalSpa',
    'HealthAndBeautyBusiness', 'BeautySalon', 'DaySpa', 'HairSalon', 'NailSalon', 'HealthClub', 'ExerciseGym',
    'SportsActivityLocation', 'LegalService', 'Attorney', 'Notary', 'AccountingService', 'FinancialService',
    'InsuranceAgency', 'RealEstateAgent', 'HomeAndConstructionBusiness', 'GeneralContractor', 'RoofingContractor',
    'Plumber', 'Electrician', 'HVACBusiness', 'HousePainter', 'Locksmith', 'MovingCompany', 'AutomotiveBusiness',
    'AutoDealer', 'AutoRepair', 'VeterinaryCare', 'AnimalShelter', 'ChildCare', 'DryCleaningOrLaundry',
    'EmploymentAgency', 'EntertainmentBusiness', 'FuneralHome' , 'LodgingBusiness', 'TravelAgency', 'Optician',
    'Pharmacy', 'MedicalOrganization', 'Hospital', 'EventVenue', 'ShoppingCenter', 'TattooParlor', 'Florist',
}

SECTORS = [  # broad sector from the directory category slug (first match wins)
    ('Food and drink', ['restaurant', 'food', 'gourmet', 'grocery', 'catering', 'bakery']),
    ('Health, wellness and beauty', ['health', 'dental', 'medical', 'salon', 'spa', 'counseling', 'fitness', 'beauty', 'veterinar', 'pets', 'senior']),
    ('Shops and showrooms', ['clothing', 'jewel', 'gift', 'retail', 'furnish', 'books', 'sporting', 'consumer-products', 'interior', 'windows']),
    ('Home and building', ['contractor', 'construction', 'architect', 'landscap', 'building', 'remodel', 'cleaning', 'moving']),
    ('Professional services', ['legal', 'attorney', 'account', 'financial', 'insurance', 'consult', 'real-estate', 'tax', 'business', 'technology', 'information', 'advertis', 'marketing', 'photograph', 'publishing', 'office']),
    ('Events, travel and leisure', ['event', 'travel', 'entertain', 'hospitality', 'sports', 'golf', 'art', 'theatre']),
]


def sector(cats):
    for name, keys in SECTORS:
        if any(k in c for c in cats for k in keys):
            return name
    return 'Other'


def load_jsonl(paths):
    rows = {}
    for p in paths:
        if os.path.exists(p):
            for line in open(p):
                if line.strip():
                    d = json.loads(line)
                    rows.setdefault(d['id'], d)  # first result wins if a site was run twice
    return rows


def digits(s):
    return re.sub(r'\D', '', s or '')


def tel_ok(href):
    d = digits(href.split(',')[0].split(';')[0])
    return len(d) == 10 or (len(d) == 11 and d.startswith('1'))


def platform(pg):
    p = pg.get('platforms') or []
    order = ['Wix', 'Squarespace', 'Shopify', 'GoDaddy Website Builder', 'Duda', 'Webflow', 'Weebly', 'Showit',
             'HubSpot CMS', 'Framer', 'Drupal', 'Joomla', 'Hibu or other hosted builder', 'WordPress']
    for name in order:  # hosted builders win over WordPress when both fingerprints appear
        if name in p:
            return name
    return 'No builder detected'


def https_status(pg, loaded, challenge):
    """works / broken / downgrades / unknown, for the site's https:// address."""
    if pg.get('httpsExit') in (35, 51, 58, 60) or pg.get('httpsCode') in (525, 526):
        return 'broken'  # TLS handshake or certificate failure
    if pg.get('downgradesToHttp') or (pg.get('status') == 405 and str(pg.get('finalUrl', '')).startswith('http://')):
        return 'downgrades'  # https sends visitors back to plain http
    if loaded:
        return 'works'
    if pg.get('httpsCode') is not None and 200 <= pg['httpsCode'] < 400 and not challenge:
        return 'works'
    return 'unknown'  # bot check, no response or a server error


def pct(n, d):
    return round(100 * n / d, 1) if d else None


def main(private_dir):
    sample = {s['id']: s for s in json.load(open(os.path.join(private_dir, 'sample.json')))}
    pages = load_jsonl([os.path.join(private_dir, 'pages_v2.jsonl')])
    lh = load_jsonl(sorted(glob.glob(os.path.join(private_dir, 'lh_*.jsonl'))))

    rows = []
    for sid, s in sorted(sample.items()):
        pg, l = pages.get(sid, {}), lh.get(sid, {})
        challenge = bool(pg.get('challenge'))
        loaded = bool(pg.get('loaded')) and not challenge and (pg.get('status') or 0) < 400
        # A Lighthouse result only counts if the main document came back with a success status;
        # otherwise it measured an error page or a bot check, not the site.
        lh_valid = bool(l.get('median')) and (l.get('checks') or {}).get('http-status-code') == 1
        med = (l.get('median') or {}) if lh_valid else {}
        tel_links = pg.get('telLinks') or []
        shown = set(pg.get('phonesShown') or [])
        linked = {digits(t)[-10:] for t in tel_links}
        unlinked = [n for n in shown if n not in linked]
        cs = pg.get('contactStatus')
        year = pg.get('copyrightYear')
        types = set(pg.get('jsonLdTypes') or [])
        row = {
            'id': sid,
            'town': s['town'],
            'area': 'Hinsdale' if s['town'] == 'Hinsdale' else ('Oak Brook and Oakbrook Terrace' if s['town'] in ('Oak Brook', 'Oakbrook Terrace') else 'Neighboring suburbs'),
            'directory': 'Hinsdale' if s['chamber'].startswith('Hinsdale') else 'Greater Oak Brook',
            'sector': sector(s['categories']),
            'page_loaded': loaded,
            'blocked_by_bot_check': challenge,
            'platform': platform(pg) if loaded else '',
            'lh_runs_ok': l.get('okRuns', 0) if lh_valid else 0,
            'lh_benchmark_index': round(l['benchmarkIndex']) if lh_valid and l.get('benchmarkIndex') else '',
            'lh_performance': round(100 * med['performance']) if med.get('performance') is not None else '',
            'lh_accessibility': round(100 * med['accessibility']) if med.get('accessibility') is not None else '',
            'lh_best_practices': round(100 * med['bestPractices']) if med.get('bestPractices') is not None else '',
            'lh_seo': round(100 * med['seo']) if med.get('seo') is not None else '',
            'lcp_s': round(med['largest-contentful-paint'] / 1000, 2) if med.get('largest-contentful-paint') else '',
            'fcp_s': round(med['first-contentful-paint'] / 1000, 2) if med.get('first-contentful-paint') else '',
            'tbt_ms': round(med['total-blocking-time']) if med.get('total-blocking-time') is not None else '',
            'cls': round(med['cumulative-layout-shift'], 3) if med.get('cumulative-layout-shift') is not None else '',
            'page_weight_kb': round(med['total-byte-weight'] / 1024) if med.get('total-byte-weight') else '',
            'tap_targets_ok': (l.get('checks') or {}).get('target-size') == 1 if lh_valid else '',
            'meta_description_ok': (l.get('checks') or {}).get('meta-description') == 1 if lh_valid else '',
            'https_status': https_status(pg, loaded, challenge),
            'viewport_tag': bool(pg.get('viewportMeta')) if loaded else '',
            'scrolls_sideways': (pg.get('scrollWidth', 0) > pg.get('innerWidth', 0) + 1) if loaded else '',
            'small_text_share': round(pg['smallTextShare'], 3) if loaded and pg.get('smallTextShare') is not None else '',
            'phone_shown': bool(shown) if loaded else '',
            'tel_links': len(tel_links) if loaded else '',
            'phone_not_tappable': (bool(shown) and len(tel_links) == 0) if loaded else '',
            'phone_partly_tappable': (bool(shown) and len(tel_links) > 0 and bool(unlinked)) if loaded else '',
            'tel_link_malformed': any(not tel_ok(t) for t in tel_links) if loaded else '',
            'email_link': bool(pg.get('mailtoLinks')) if loaded else '',
            'contact_link': bool(pg.get('contactHref')) if loaded else '',
            'contact_link_broken': (cs == 'ERROR' or (isinstance(cs, int) and cs >= 400)) if loaded and pg.get('contactHref') else '',
            'form_on_homepage': bool(pg.get('hasForm')) if loaded else '',
            'copyright_year': year if loaded and year else '',
            'structured_data': bool(types - {'INVALID_JSON'}) if loaded else '',
            'local_business_markup': bool(types & LOCAL_TYPES) if loaded else '',
        }
        rows.append(row)

    os.makedirs(os.path.join(ROOT, 'seo', 'data'), exist_ok=True)
    with open(os.path.join(ROOT, 'seo', 'data', 'western-suburbs-2026-sites.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    S = {'sample_size': len(rows), 'collected': '2026-11-04'}
    loaded = [r for r in rows if r['page_loaded']]
    lhok = [r for r in rows if r['lh_performance'] != '']
    S['loaded'] = len(loaded)
    S['blocked_by_bot_check'] = sum(1 for r in rows if r['blocked_by_bot_check'])
    S['lighthouse_measured'] = len(lhok)
    S['lighthouse_failed'] = len(rows) - len(lhok)
    bi = [r['lh_benchmark_index'] for r in lhok if r['lh_benchmark_index'] != '']
    S['benchmark_index'] = {'min': min(bi) if bi else None, 'median': st.median(bi) if bi else None, 'max': max(bi) if bi else None}

    def summary_scores(rs, key):
        v = [r[key] for r in rs if r[key] != '']
        return {'n': len(v), 'median': st.median(v) if v else None,
                'good_90_plus': pct(sum(1 for x in v if x >= 90), len(v)),
                'needs_improvement_50_89': pct(sum(1 for x in v if 50 <= x < 90), len(v)),
                'poor_under_50': pct(sum(1 for x in v if x < 50), len(v))}

    for k in ('lh_performance', 'lh_accessibility', 'lh_best_practices', 'lh_seo'):
        S[k] = summary_scores(lhok, k)
    lcp = [r['lcp_s'] for r in lhok if r['lcp_s'] != '']
    S['lcp'] = {'n': len(lcp), 'median_s': round(st.median(lcp), 1) if lcp else None,
                'within_2_5s': pct(sum(1 for x in lcp if x <= 2.5), len(lcp)),
                'over_4s': pct(sum(1 for x in lcp if x > 4), len(lcp))}
    wt = [r['page_weight_kb'] for r in lhok if r['page_weight_kb'] != '']
    S['page_weight'] = {'n': len(wt), 'median_kb': st.median(wt) if wt else None,
                        'over_3mb': pct(sum(1 for x in wt if x > 3072), len(wt))}
    tap = [r for r in lhok if r['tap_targets_ok'] != '']
    S['tap_targets_fail'] = {'n': len(tap), 'pct': pct(sum(1 for r in tap if not r['tap_targets_ok']), len(tap))}
    md = [r for r in lhok if r['meta_description_ok'] != '']
    S['meta_description_missing'] = {'n': len(md), 'pct': pct(sum(1 for r in md if not r['meta_description_ok']), len(md))}

    # Platforms (sites that loaded)
    pc = Counter(r['platform'] for r in loaded)
    S['platforms'] = {k: {'n': v, 'pct': pct(v, len(loaded))} for k, v in pc.most_common()}
    S['performance_by_platform'] = {}
    for name, cnt in pc.most_common():
        v = [r['lh_performance'] for r in loaded if r['platform'] == name and r['lh_performance'] != '']
        if len(v) >= 8:
            S['performance_by_platform'][name] = {'n': len(v), 'median': st.median(v),
                                                  'good_90_plus': pct(sum(1 for x in v if x >= 90), len(v))}

    n = len(loaded)
    known = [r for r in rows if r['https_status'] != 'unknown']
    S['https'] = {'n_known': len(known), 'unknown': sum(1 for r in rows if r['https_status'] == 'unknown'),
                  'works': pct(sum(1 for r in known if r['https_status'] == 'works'), len(known)),
                  'broken': pct(sum(1 for r in known if r['https_status'] == 'broken'), len(known)),
                  'downgrades': pct(sum(1 for r in known if r['https_status'] == 'downgrades'), len(known)),
                  'problem_count': sum(1 for r in known if r['https_status'] in ('broken', 'downgrades'))}
    S['mobile'] = {'n': n,
                   'no_viewport_tag': pct(sum(1 for r in loaded if r['viewport_tag'] is False), n),
                   'scrolls_sideways': pct(sum(1 for r in loaded if r['scrolls_sideways'] is True), n),
                   'over_25pct_small_text': pct(sum(1 for r in loaded if r['small_text_share'] != '' and r['small_text_share'] > 0.25), n)}
    mob_issue = [r for r in loaded if r['viewport_tag'] is False or r['scrolls_sideways'] is True
                 or (r['small_text_share'] != '' and r['small_text_share'] > 0.25) or r['tap_targets_ok'] is False]
    S['mobile']['any_mobile_issue'] = pct(len(mob_issue), n)
    shown = [r for r in loaded if r['phone_shown']]
    S['phone'] = {'n': n, 'phone_shown': pct(len(shown), n), 'phone_shown_count': len(shown),
                  'not_tappable_of_shown': pct(sum(1 for r in shown if r['phone_not_tappable']), len(shown)),
                  'not_tappable_count': sum(1 for r in shown if r['phone_not_tappable']),
                  'partly_tappable_of_shown': pct(sum(1 for r in shown if r['phone_partly_tappable']), len(shown)),
                  'malformed_tel_link': pct(sum(1 for r in loaded if r['tel_link_malformed'] is True), n),
                  'malformed_tel_link_count': sum(1 for r in loaded if r['tel_link_malformed'] is True)}
    withc = [r for r in loaded if r['contact_link']]
    S['contact'] = {'n': n, 'contact_link': pct(len(withc), n),
                    'contact_link_broken_of_linked': pct(sum(1 for r in withc if r['contact_link_broken'] is True), len(withc)),
                    'contact_link_broken_count': sum(1 for r in withc if r['contact_link_broken'] is True),
                    'email_link': pct(sum(1 for r in loaded if r['email_link']), n),
                    'no_way_to_reach_on_homepage': pct(sum(1 for r in loaded if not r['contact_link'] and not r['phone_shown'] and not r['email_link'] and not r['form_on_homepage']), n)}
    years = [r['copyright_year'] for r in loaded if r['copyright_year'] != '']
    S['copyright'] = {'n': n, 'year_found': pct(len(years), n), 'year_found_count': len(years),
                      'current_year_of_found': pct(sum(1 for y in years if y == CURRENT_YEAR), len(years)),
                      'last_year_of_found': pct(sum(1 for y in years if y == CURRENT_YEAR - 1), len(years)),
                      'two_plus_years_old_of_found': pct(sum(1 for y in years if y <= CURRENT_YEAR - 2), len(years)),
                      'two_plus_years_old_count': sum(1 for y in years if y <= CURRENT_YEAR - 2),
                      'five_plus_years_old_of_found': pct(sum(1 for y in years if y <= CURRENT_YEAR - 5), len(years)),
                      'oldest': min(years) if years else None,
                      'by_year': dict(sorted(Counter(years).items()))}
    S['structured_data'] = {'n': n, 'any': pct(sum(1 for r in loaded if r['structured_data']), n),
                            'local_business': pct(sum(1 for r in loaded if r['local_business_markup']), n)}

    # Areas with enough sites to report separately
    S['by_area'] = {}
    for area in ('Hinsdale', 'Oak Brook and Oakbrook Terrace', 'Neighboring suburbs'):
        ar = [r for r in rows if r['area'] == area]
        al = [r for r in ar if r['page_loaded']]
        ap = [r['lh_performance'] for r in ar if r['lh_performance'] != '']
        ash = [r for r in al if r['phone_shown']]
        ay = [r['copyright_year'] for r in al if r['copyright_year'] != '']
        S['by_area'][area] = {'sites': len(ar), 'loaded': len(al), 'lighthouse_measured': len(ap),
                              'median_performance': st.median(ap) if ap else None,
                              'performance_90_plus': pct(sum(1 for x in ap if x >= 90), len(ap)),
                              'phone_not_tappable_of_shown': pct(sum(1 for r in ash if r['phone_not_tappable']), len(ash)),
                              'copyright_two_plus_years_old_of_found': pct(sum(1 for y in ay if y <= CURRENT_YEAR - 2), len(ay)),
                              'wordpress_share': pct(sum(1 for r in al if r['platform'] == 'WordPress'), len(al))}
    S['by_sector'] = {}
    for sec in sorted({r['sector'] for r in rows}):
        sr = [r for r in rows if r['sector'] == sec]
        sp = [r['lh_performance'] for r in sr if r['lh_performance'] != '']
        S['by_sector'][sec] = {'sites': len(sr), 'median_performance': st.median(sp) if sp else None}

    json.dump(S, open(os.path.join(ROOT, 'seo', 'data', 'western-suburbs-2026-summary.json'), 'w'), indent=1)

    # Aggregate table offered for download on the report page
    out = os.path.join(ROOT, 'research', 'western-suburbs-website-report-2026')
    os.makedirs(out, exist_ok=True)
    lines = [['measure', 'value', 'base', 'unit']]
    lines += [['Sites in sample', S['sample_size'], '', 'sites'],
              ['Sites measured with Lighthouse', S['lighthouse_measured'], S['sample_size'], 'sites'],
              ['Median mobile performance score', S['lh_performance']['median'], S['lh_performance']['n'], 'score 0-100'],
              ['Mobile performance 90 or higher', S['lh_performance']['good_90_plus'], S['lh_performance']['n'], 'percent'],
              ['Mobile performance under 50', S['lh_performance']['poor_under_50'], S['lh_performance']['n'], 'percent'],
              ['Median accessibility score', S['lh_accessibility']['median'], S['lh_accessibility']['n'], 'score 0-100'],
              ['Median SEO score', S['lh_seo']['median'], S['lh_seo']['n'], 'score 0-100'],
              ['Median largest contentful paint (lab, mobile)', S['lcp']['median_s'], S['lcp']['n'], 'seconds'],
              ['Largest contentful paint within 2.5 s', S['lcp']['within_2_5s'], S['lcp']['n'], 'percent'],
              ['Phone number shown on homepage', S['phone']['phone_shown'], S['phone']['n'], 'percent'],
              ['Phone shown but not tappable', S['phone']['not_tappable_of_shown'], S['phone']['phone_shown_count'], 'percent of sites showing a phone'],
              ['Contact link that fails to load', S['contact']['contact_link_broken_of_linked'], '', 'percent of sites with a contact link'],
              ['Copyright year two or more years old', S['copyright']['two_plus_years_old_of_found'], S['copyright']['year_found_count'], 'percent of sites showing a year'],
              ['HTTPS works', S['https']['works'], S['https']['n_known'], 'percent of sites that could be checked'],
              ['HTTPS broken or downgraded to HTTP', round(S['https']['broken'] + S['https']['downgrades'], 1), S['https']['n_known'], 'percent of sites that could be checked'],
              ['Any mobile usability issue', S['mobile']['any_mobile_issue'], S['mobile']['n'], 'percent'],
              ['LocalBusiness structured data', S['structured_data']['local_business'], S['structured_data']['n'], 'percent']]
    for name, v in S['platforms'].items():
        lines.append([f'Platform: {name}', v['pct'], S['loaded'], 'percent of sites that loaded'])
    for name, v in S['performance_by_platform'].items():
        lines.append([f'Median performance: {name}', v['median'], v['n'], 'score 0-100'])
    with open(os.path.join(out, 'western-suburbs-2026-findings.csv'), 'w', newline='') as f:
        csv.writer(f).writerows(lines)
    print(json.dumps({k: S[k] for k in ('sample_size', 'loaded', 'lighthouse_measured', 'lh_performance', 'platforms', 'phone', 'copyright', 'contact', 'https', 'mobile')}, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
