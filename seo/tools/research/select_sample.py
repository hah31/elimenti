#!/usr/bin/env python3
"""Step 2 of the western suburbs website study: pick the sample and pseudonymize it.

Usage:
    python3 seo/tools/research/select_sample.py PRIVATE_DIR

Reads PRIVATE_DIR/members.json (from directory.py) and PRIVATE_DIR/exclusions.json (names
excluded on review as chains, franchises, national firms or non-business organizations,
with a reason each). Writes:
  PRIVATE_DIR/sample.json  -> [{id, url}] for the audit scripts
  PRIVATE_DIR/key.csv      -> id, business name, website, town, directory (stays private)
  seo/data/sample-frame.json -> counts at each filtering step (published, no names)

Rules (also stated on the published report):
  * Listed address in Hinsdale, Oak Brook or a neighboring suburb (NEARBY below).
  * Not in a category that is never an independent business (EXCLUDED_CATEGORIES).
  * Has its own website: a listed URL whose domain isn't a national brand's and which
    isn't a location page deep inside a chain's site.
  * Not excluded on name review (exclusions.json).
  * One entry per website domain (some businesses belong to both chambers).
  * If more than CAP sites qualify, a random sample of CAP with a fixed seed.
"""
import csv
import hashlib
import json
import os
import random
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
CAP = 150
SEED = 20261104

NEARBY = {
    'hinsdale': 'Hinsdale', 'oak brook': 'Oak Brook', 'oakbrook': 'Oak Brook', 'oakbrook terrace': 'Oakbrook Terrace',
    'oak brook terrace': 'Oakbrook Terrace', 'clarendon hills': 'Clarendon Hills', 'western springs': 'Western Springs',
    'burr ridge': 'Burr Ridge', 'willowbrook': 'Willowbrook', 'westmont': 'Westmont', 'darien': 'Darien',
    'downers grove': 'Downers Grove', 'la grange': 'La Grange', 'lagrange': 'La Grange', 'la grange park': 'La Grange Park',
    'countryside': 'Countryside', 'elmhurst': 'Elmhurst', 'lombard': 'Lombard', 'villa park': 'Villa Park',
    'lisle': 'Lisle', 'indian head park': 'Indian Head Park',
}

# Directory categories whose members are never independent businesses for this study.
EXCLUDED_CATEGORIES = [
    'government', 'churches', 'library', 'utilities', 'banks', 'banking', 'credit-union', 'hospitals',
    'community-organizations', 'nonprofit', 'family-community-civic', 'religious', 'education',
    'country-clubs', 'symphony', 'theatre', 'cancer-support', 'public-utilities', 'telecommunications',
    'energy', 'manufacturing', 'transportation', 'car-rentals', 'apartments', 'employment', 'press-publications',
]

# Domains of national brands, franchisors and large firms whose local offices list a corporate page.
NATIONAL_DOMAINS = {
    'statefarm.com', 'allstate.com', 'farmers.com', 'agents.farmers.com', 'edwardjones.com', 'ameriprise.com',
    'nm.com', 'northwesternmutual.com', 'massmutual.com', 'primerica.com', 'morganstanley.com', 'ml.com',
    'merrilllynch.com', 'wellsfargo.com', 'wellsfargoadvisors.com', 'chase.com', 'bmo.com', 'pnc.com', 'fifththird.com',
    'usbank.com', 'citi.com', 'raymondjames.com', 'lpl.com', 'coldwellbanker.com', 'coldwellbankerhomes.com',
    'compass.com', 'bairdwarner.com', 'atproperties.com', 'kw.com', 'remax.com', 'century21.com', 'sothebysrealty.com',
    'theupsstore.com', 'locations.theupsstore.com', 'servpro.com', 'orangetheory.com', 'clubpilates.com',
    'massageenvy.com', 'handandstone.com', 'waxcenter.com', 'sportclips.com', 'greatclips.com', 'kumon.com',
    'mathnasium.com', 'sylvanlearning.com', 'goddardschool.com', 'primroseschools.com', 'kiddieacademy.com',
    'starbucks.com', 'panerabread.com', 'chipotle.com', 'potbelly.com', 'jerseymikes.com', 'walgreens.com', 'cvs.com',
    'jewelosco.com', 'wholefoodsmarket.com', 'traderjoes.com', 'marianos.com', 'acehardware.com', 'sherwin-williams.com',
    'marriott.com', 'hilton.com', 'hyatt.com', 'ihg.com', 'wyndhamhotels.com', 'choicehotels.com', 'comcast.com',
    'xfinity.com', 'att.com', 'verizon.com', 'tmobile.com', 't-mobile.com', 'nicor.com', 'nicorgas.com', 'comed.com',
    'enterprise.com', 'hertz.com', 'avis.com', 'advocatehealth.com', 'advocateaurorahealth.org', 'nm.org',
    'uchicagomedicine.org', 'amitahealth.org', 'adventisthealthcare.com', 'aah.org', 'ascension.org', 'hoffmanbeverly.com',
    'fastsigns.com', 'minuteman.com', 'allegramarketingprint.com', 'sir-speedy.com', 'regus.com', 'iwgplc.com',
    'expresspros.com', 'roberthalf.com', 'adp.com', 'paychex.com', 'insperity.com', 'h&rblock.com', 'hrblock.com',
    'jacksonhewitt.com', 'twomenandatruck.com', 'collegehunkshaulingjunk.com', 'molly-maid.com', 'mollymaid.com',
    'merrymaids.com', 'mrhandyman.com', 'mrrooter.com', 'rotorooter.com', 'benjaminfranklinplumbing.com',
    'homeinstead.com', 'comfortkeepers.com', 'visitingangels.com', 'brightstarcare.com', 'rightathome.net',
    'seniorhelpers.com', 'griswoldhomecare.com', 'lifetime.life', 'lifetimefitness.com', 'xsport.com', 'f45training.com',
    'anytimefitness.com', 'snapfitness.com', 'planetfitness.com', 'bodyrok.com', 'solidcore.co', 'corepoweryoga.com',
    'restorationhardware.com', 'rh.com', 'potterybarn.com', 'williams-sonoma.com', 'nordstrom.com', 'macys.com',
    'neimanmarcus.com', 'saksfifthavenue.com', 'apple.com', 'tesla.com', 'mbusa.com', 'dealer.com', 'dealerinspire.com',
    'nothingbundtcakes.com', 'cookiesbyfields.com', 'crumblcookies.com', 'kendrascott.com', 'lululemon.com',
    'shopsimon.com', 'brookfieldproperties.com', 'newyorklife.com', 'cbre.com', 'oakbrookcenter.com', 'gnc.com', 'thejointchiro.com', 'aspendental.com',
    'heartland.com', 'smiledirectclub.com', 'pearlevision.com', 'lenscrafters.com', 'americasbest.com', 'warbyparker.com',
}

SHORTENERS = {'facebook.com', 'm.facebook.com', 'instagram.com', 'linkedin.com', 'business.site', 'yelp.com',
              'google.com', 'goo.gl', 'g.page', 'sites.google.com', 'linktr.ee'}


def clean_url(url):
    """Fix mechanical typos in directory listings: a doubled scheme, a missing or mistyped '.com'."""
    u = url.strip().replace(' ', '')
    u = re.sub(r'^https?://(https?://)', r'\1', u, flags=re.I)
    if '://' not in u:
        u = 'http://' + u
    p = urlparse(u)
    host = p.netloc
    if host and '.' not in host.replace('www.', '', 1):
        host += '.com'
    host = re.sub(r'\.cpm$', '.com', host)
    return f'{p.scheme}://{host}{p.path}'


def domain(url):
    host = urlparse(url if '://' in url else 'http://' + url).netloc.lower().split('@')[-1].split(':')[0]
    return host[4:] if host.startswith('www.') else host


def registrable(host):
    parts = host.split('.')
    return '.'.join(parts[-2:]) if len(parts) >= 2 else host


def main(private_dir):
    members = json.load(open(os.path.join(private_dir, 'members.json')))
    excl_path = os.path.join(private_dir, 'exclusions.json')
    exclusions = json.load(open(excl_path)) if os.path.exists(excl_path) else {}
    steps = {'directory_listings': len(members)}

    def town_of(m):
        return NEARBY.get(re.sub(r'\s+', ' ', (m.get('city') or '').strip().lower()))

    rows = [m for m in members if town_of(m)]
    steps['listed_address_in_study_area'] = len(rows)
    rows = [m for m in rows if not any(any(x in c for x in EXCLUDED_CATEGORIES) for c in m['categories'])]
    steps['after_category_exclusions'] = len(rows)
    for m in rows:
        if m.get('website'):
            m['website'] = clean_url(m['website'])
    with_site = [m for m in rows if m.get('website')]
    steps['with_a_listed_website'] = len(with_site)
    own = []
    for m in with_site:
        u = m['website'].strip()
        host = domain(u)
        reg = registrable(host)
        if not host or reg in SHORTENERS or host in SHORTENERS:
            continue
        if reg in NATIONAL_DOMAINS or host in NATIONAL_DOMAINS:
            continue
        path = urlparse(u if '://' in u else 'http://' + u).path.strip('/')
        if path.count('/') >= 1:  # deep location page inside a larger site
            continue
        own.append(m)
    steps['own_domain_not_a_national_brand'] = len(own)
    own = [m for m in own if m['name'] not in exclusions]
    steps['after_name_review'] = len(own)
    seen, unique = set(), []
    for m in sorted(own, key=lambda m: (m['chamber'] != 'Hinsdale Chamber of Commerce', m['name'].lower())):
        reg = registrable(domain(m['website']))
        if reg in seen:
            continue
        seen.add(reg)
        unique.append(m)
    steps['unique_websites'] = len(unique)
    rng = random.Random(SEED)
    sample = unique if len(unique) <= CAP else rng.sample(unique, CAP)
    steps['sample'] = len(sample)

    def sid(m):
        return 's' + hashlib.sha256(f"{SEED}|{domain(m['website'])}".encode()).hexdigest()[:8]

    out_sample, key = [], []
    for m in sorted(sample, key=sid):
        url = m['website'].strip()
        if '://' not in url:
            url = 'http://' + url
        p = urlparse(url)
        url = f'{p.scheme}://{p.netloc}/'
        out_sample.append({'id': sid(m), 'url': url, 'town': town_of(m), 'chamber': m['chamber'],
                           'categories': m['categories']})
        key.append([sid(m), m['name'], url, town_of(m), m['chamber'], ';'.join(m['categories'])])
    json.dump(out_sample, open(os.path.join(private_dir, 'sample.json'), 'w'), indent=1)
    with open(os.path.join(private_dir, 'key.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id', 'business', 'website', 'town', 'directory', 'directory_categories'])
        w.writerows(key)
    frame = {'collected': '2026-11-04', 'directories': {
        'Hinsdale Chamber of Commerce': 'https://business.hinsdalechamber.com/list',
        'Greater Oak Brook Chamber of Commerce': 'https://business.obchamber.com/list'},
        'steps': steps, 'cap': CAP, 'seed': SEED, 'study_area': sorted(set(NEARBY.values())),
        'excluded_categories': EXCLUDED_CATEGORIES,
        'name_review_exclusions_by_reason': {r: sum(1 for v in exclusions.values() if v == r) for r in sorted(set(exclusions.values()))}}
    os.makedirs(os.path.join(ROOT, 'seo', 'data'), exist_ok=True)
    json.dump(frame, open(os.path.join(ROOT, 'seo', 'data', 'sample-frame.json'), 'w'), indent=1)
    print(json.dumps(steps, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
