# Western suburbs website study, 2026: data

Raw and aggregate data behind `/research/western-suburbs-website-report-2026/`. Collected 2026-11-04 with the scripts in `seo/tools/research/`.

## Privacy: why there are no names or URLs here

This repository is public, and so is the `elimenti.pages.dev` copy of it. The brief was to never name or shame an individual business, so nothing committed here identifies one:

- Every site has a random ID (`s` + 8 hex characters), derived from a hash of its domain and a fixed seed.
- No business names, URLs, page titles, phone numbers or email addresses are stored. Phone and contact checks are kept as true/false results.
- The key that maps IDs to businesses (`key.csv`) and the raw member list (`members.json`) were delivered privately to the owner and are **never** to be committed.

## Files

| File | What it is |
|---|---|
| `sample-frame.json` | How 759 directory listings became a sample of 150: the count left after each rule, the rules themselves, the random seed and the exclusion reasons by count. |
| `western-suburbs-2026-sites.csv` | One row per sampled site, pseudonymous (columns below). |
| `western-suburbs-2026-summary.json` | Every aggregate the report quotes. Each number on the report page, the guides and the town pages comes from this file. |

The aggregate table offered for download on the site is `research/western-suburbs-website-report-2026/western-suburbs-2026-findings.csv`.

## Columns in `western-suburbs-2026-sites.csv`

| Column | Meaning |
|---|---|
| `id` | Pseudonymous site ID |
| `town`, `area` | Listed town; area group used in the report (Hinsdale / Oak Brook and Oakbrook Terrace / Neighboring suburbs) |
| `directory` | Which chamber directory the listing came from |
| `sector` | Broad sector from the directory category |
| `page_loaded` | The homepage loaded in the phone test (not a bot check, error page or failed connection) |
| `blocked_by_bot_check` | The site showed a bot check instead of the page |
| `platform` | Builder fingerprint found in the page code, or "No builder detected" |
| `lh_runs_ok` | Successful Lighthouse runs (of 3) that returned the page with a success status |
| `lh_benchmark_index` | Lighthouse's CPU benchmark for the machine at the time of the run (median of the site's runs); a check that the test machine wasn't overloaded |
| `lh_performance`, `lh_accessibility`, `lh_best_practices`, `lh_seo` | Lighthouse 13.6.0 mobile category scores, 0 to 100, median of the runs |
| `lcp_s`, `fcp_s`, `tbt_ms`, `cls` | Lab metrics: largest and first contentful paint (seconds), total blocking time (ms), cumulative layout shift |
| `page_weight_kb` | Total bytes downloaded by the homepage, in KB |
| `tap_targets_ok`, `meta_description_ok` | Lighthouse `target-size` and `meta-description` audits passed |
| `https_status` | `works`, `broken` (TLS or certificate failure), `downgrades` (HTTPS sends visitors to plain HTTP) or `unknown` (couldn't be checked) |
| `viewport_tag`, `scrolls_sideways`, `small_text_share` | Mobile layout checks at 390 x 844: a viewport tag, sideways scrolling, share of visible text under 12px |
| `phone_shown`, `tel_links`, `phone_not_tappable`, `phone_partly_tappable`, `tel_link_malformed` | A phone number in the homepage text; number of tap-to-call links; a number shown with no tap-to-call link at all; some shown numbers not linked; a tap-to-call link whose number isn't 10 or 11 digits |
| `email_link`, `contact_link`, `contact_link_broken`, `form_on_homepage` | Contact routes on the homepage, and whether the contact link loads |
| `copyright_year` | Newest year next to a copyright mark or word, footer first |
| `structured_data`, `local_business_markup` | Any JSON-LD; LocalBusiness or one of its subtypes |

Blank cells mean the check couldn't run for that site (it didn't load, or Lighthouse couldn't measure it).

## Reproducing

```
python3 seo/tools/research/directory.py PRIVATE_DIR        # read both directories
python3 seo/tools/research/select_sample.py PRIVATE_DIR    # needs PRIVATE_DIR/exclusions.json (name review)
LH_MODULES=... node seo/tools/research/audit_lighthouse.mjs PRIVATE_DIR/sample.json PRIVATE_DIR/lh_a.jsonl
node seo/tools/research/audit_pages.js PRIVATE_DIR/sample.json PRIVATE_DIR/pages_v2.jsonl
python3 seo/tools/research/analyze.py PRIVATE_DIR
python3 seo/tools/research/report_page.py
node seo/tools/research/summary_pdf.js
```

All requests went through the session's HTTPS proxy. Lighthouse ran two at a time on a 4-core machine, except for a few minutes when three overlapped; the CPU benchmark index is in the site-level CSV, and its range is in the summary.
