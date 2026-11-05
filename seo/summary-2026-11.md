# SEO pass, November 2026: summary

Branch `seo-pass-nov-2026`, November 5, 2026. Baseline audit: `seo/audit-2026-11.md`.

## Outcome

- **Merged and live.** Every Phase 4 check passed, so `seo-pass-nov-2026` was fast-forwarded into `main` (`da6c438..ba7d969`) and pushed at 09:26 UTC on November 5, 2026. GitHub Pages built it in 38 seconds (run 35, success).
- **Live check.** Fetched from elimenti.com after the deploy: the new guide `/guides/car-club-website-examples/`, `/car-club-websites/`, `/classic-car-club-websites/`, the report, the home page and `/pricing/` all return 200 with the new content. The live sitemap has 38 URLs, including the guide.
- **IndexNow: HTTP 200.** The workflow's first run (Actions run 42002340892) waited for the Pages build of `ba7d969` to finish, then submitted the 16 pages whose HTML changed (home, pricing, the suburbs hub, both car club pages, the 1 of 1 case study, the guide index, the new guide, seven updated guides and the report) and got `IndexNow response: HTTP 200 (16 URLs)`.
- **Car club overlap: 24.2% → 3.2%** of shared 5-word phrases (goal under 15%).
- **Heads-up: `llms.txt`.** PR #34 added it to `main` this morning, which conflicts with hard rule 5. I didn't add it and didn't delete it; I regenerated it so it isn't stale. Your call whether to keep it (decision 10 has the two-step removal).
- **Branches.** `seo-pass-nov-2026` and this session's `claude/loving-shannon-lnsawh` both point at the merged commits.

## What changed, file by file

- `.github/workflows/indexnow.yml`: New. On every push to `main`: diffs the push, waits for the Pages build, posts the changed HTML pages to IndexNow, logs the response code. Push trigger only.
- `seo/tools/indexnow.py`: Adds `--changed BEFORE AFTER --wait-for-pages`, used by the workflow; the old modes are unchanged.
- `seo/tools/build.py`: Registry: the new guide, `SAME_AS` list (empty), lastmod/dateModified moved to Nov 5 only on pages whose content changed, classic club description and service text updated.
- `seo/tools/audit.py`: New. Static audit of every page: titles, descriptions, H1s, words, JSON-LD types and @id references, links and fragments, image attributes, sitemap vs files, inbound links with and without nav/footer.
- `seo/tools/overlap.py`: New. Shared 5-word phrases between pages.
- `seo/tools/research/report_page.py`: Report generator: "Findings you can quote" section, "Press and reuse" note, links to the Hinsdale and Oak Brook pages.
- `guides/car-club-website-examples/index.html`: New guide: seven real club sites checked on Nov 5 plus 1 of 1 Car Club, what each does well and one miss, grouped not ranked.
- `assets/img/og/guides-car-club-website-examples.png`: New OG card for the guide.
- `car-club-websites/index.html`: Now about modern and private clubs: applications that screen, member cars, what stays private. Title and H1 unchanged. Links the new guide.
- `classic-car-club-websites/index.html`: Rebuilt for clubs with long histories: chapters, archives, member directory, club history, step-by-step move off Joomla, Drupal or a custom-built site. New description.
- `work/1-of-1-car-club/index.html`: Links the new guide.
- `guides/index.html`: New "car club" group linking the guide; listed in the CollectionPage schema.
- `guides/squarespace-vs-custom-website/index.html`: Links med spa and interior designer pages.
- `guides/wix-squarespace-wordpress-or-custom/index.html`: Links Hinsdale and Oak Brook pages (per-town study figures).
- `guides/questions-to-ask-a-web-designer/index.html`: Links the Chicago suburbs hub.
- `guides/web-designer-disappeared/index.html`: Links the classic club page (volunteer webmaster handover).
- `guides/website-redesign-vs-refresh/index.html`: Links boutique and home builder pages.
- `guides/how-long-does-a-website-take/index.html`: Links home builder and landscape pages.
- `guides/what-makes-a-website-look-high-end/index.html`: Links boutique and interior designer pages.
- `index.html`: One sentence: we work with Chicago-area businesses, city and suburbs. Link to the guide index.
- `chicago-suburbs-web-design/index.html`: Chicago-area sentence; new short section linking the report.
- `pricing/index.html`: Bruce Hodes testimonial, verbatim, same markup as home; link to the guide index.
- `research/western-suburbs-website-report-2026/index.html`: Regenerated: 13 quotable one-figure sentences, "Press and reuse", links to Hinsdale and Oak Brook.
- `assets/css/style.css`: Spacing for an h3 after a paragraph or list in prose (new guide; also fixes a tight heading in the redesign guide).
- `sitemap.xml`: Regenerated: 38 URLs (adds the guide); lastmod 2026-11-05 only on changed pages.
- `llms.txt`: Regenerated (it arrived with `main`, PR #34): new guide line, new classic description. See decision 10.
- `seo/audit-2026-11.md`: New. Baseline audit.
- `seo/decisions.md`: New. Calls made without asking.
- `seo/todo-hashim.md`: New. What only Hashim can do.
- `seo/request-indexing.md`: New. URLs for Search Console, in priority order.
- `seo/ai-prompts.md`: New. Monthly AI visibility log, 16 prompts.
- `seo/summary-2026-11.md`: This file.

## Audit, before and after

| Check | Before | After |
|---|---|---|
| Sitemap URLs | 37 | 38 (the new guide) |
| Broken internal links, assets or #fragments | 0 | 0 |
| Images missing alt, width or height | 0 | 0 |
| JSON-LD blocks that don't parse | 0 | 0 |
| @id references never defined | 0 | 0 |
| Sitemap URLs with no file / indexable pages missing from sitemap | 0 / 0 | 0 / 0 |
| Pages with fewer than 2 referring pages (all links) | 0 | 0 |
| Pages with 0 or 1 links from page content | 3 (`/guides/`, `/terms/`, `/privacy/`) | 2 (`/terms/`, `/privacy/`, legal pages, footer-only by design) |
| Guides linking to an industry or location page | 3 of 10 | 11 of 11 |
| Report links to Hinsdale and Oak Brook pages | No | Yes |
| Suburbs hub links to the report | No | Yes |
| `check.py` crawl (local server) | Pass | Pass |
| Schema Markup Validator (validator.schema.org) | 37 of 37 valid (v2 report) | 28 of 40 checked so far, 0 errors, 0 warnings, including every page whose JSON-LD changed in this pass; the other 12 have JSON-LD byte-identical to the version already live and were still in the validator's throttled queue when this was written |
| New pages other than the car club guide | | None |
| Banned phrasing in added lines ("hand-coded", AI, knocks on platforms) | | None found |

## Mobile PageSpeed, before and after

The PageSpeed Insights API returned HTTP 429 (keyless quota exhausted), so both columns are Lighthouse 13.6.0 with its default mobile settings, the lab engine and settings PSI uses. Median of three runs against the live site.

| Page | Before: perf / LCP / CLS / TBT | After: perf / LCP / CLS / TBT |
|---|---|---|
| / | 100 / 1.00 s / 0 / 0 ms | 100 / 1.02 s / 0 / 0 ms |
| /car-club-websites/ | 100 / 0.96 s / 0 / 0 ms | 100 / 1.02 s / 0 / 0 ms |
| /guides/what-makes-a-website-look-high-end/ | 100 / 0.89 s / 0 / 0 ms | 100 / 0.80 s / 0 / 0 ms |
| /research/western-suburbs-website-report-2026/ | 100 / 1.02 s / 0 / 0 ms | 100 / 1.02 s / 0 / 0 ms |
| /guides/car-club-website-examples/ (new) | | 100 / 1.08 s / 0 / 0 ms |

Accessibility, Best Practices and SEO: 100 on every page, before and after. No page got worse: performance stayed at 100 with CLS 0 and TBT 0, and LCP moved by 0.06 s or less in either direction, within normal run-to-run variation. Before merging, main and the branch were also compared side by side on a local server: identical scores.

## Car club page overlap

Share of the smaller page's distinct 5-word phrases that also appear on the other page (`python3 seo/tools/overlap.py car-club-websites classic-car-club-websites`):

- Before: **24.2%** (161 shared phrases)
- After: **3.2%** (37 shared phrases). Goal was under 15%.
- Every other industry and location pair is unchanged; the highest is still Hinsdale vs Oak Brook at 13.9%.

## To do (`seo/todo-hashim.md`)

From the November 2026 SEO pass. Each item is something I couldn't do or verify from the repo or the web.

### 1. Send your profile URLs for `sameAs`

No Elimenti profile URL appears anywhere in the repo, so the LocalBusiness schema has no `sameAs` yet. Search engines use `sameAs` to connect the website to the same business elsewhere. Send whichever of these exist, as the public URL a stranger would open:

- [ ] Google Business Profile: in the profile, **Share profile** → copy the link (looks like `https://share.google/...` or `https://maps.app.goo.gl/...`)
- [ ] LinkedIn company page (`https://www.linkedin.com/company/...`)
- [ ] Instagram (`https://www.instagram.com/...`)
- [ ] Clutch (`https://clutch.co/profile/...`)
- [ ] Yelp (`https://www.yelp.com/biz/...`)
- [ ] Bing Places (the public Bing Maps link to the listing)

Each one goes in the `SAME_AS` list near the top of `seo/tools/build.py`; then run `python3 seo/tools/build.py`. Only add a profile that's live, public and clearly Elimenti's.

### 2. Turn the Glen Ellyn redirect into a real 301 (Cloudflare)

`/glen-ellyn-web-design/` redirects with a meta refresh because GitHub Pages can't send a 301. Cloudflare can, because elimenti.com runs through it: on November 5, 2026 the site answered with `server: cloudflare`, so the domain is proxied (orange cloud), which a Redirect Rule needs. Leave the stub file in the repo as a fallback.

**Check first:** `seo/cloudflare-redirects.md` (merged in PR #34 this morning) sets up three redirect rules, and its Rule 2 is this same Glen Ellyn redirect. If you've already followed that file, this is done; don't add it twice. If you're doing that file now, follow it instead of the steps below, because there the rule order matters (first match wins). The steps below are for this one rule on its own, using the same expression as that file.

1. Log in at **dash.cloudflare.com** and click the **elimenti.com** domain.
2. In the left sidebar, open **Rules** → **Overview**.
3. Click **Create rule**, then choose **Redirect Rule**.
4. **Rule name:** `Glen Ellyn page to suburbs hub`
5. Under **If incoming requests match…**, choose **Custom filter expression**.
6. Click **Edit expression** and paste:
   ```
   (http.host in {"elimenti.com" "www.elimenti.com"} and http.request.uri.path in {"/glen-ellyn-web-design/" "/glen-ellyn-web-design" "/glen-ellyn-web-design/index.html"})
   ```
7. Under **Then…**: **Type** `Static`, **URL** `https://elimenti.com/chicago-suburbs-web-design/`, **Status code** `301`. Leave **Preserve query string** off.
8. Click **Deploy**. If you later add other redirect rules, keep this one above any catch-all www/http rule.
9. Check it from any terminal (on Windows PowerShell, type `curl.exe` instead of `curl`):
   ```
   curl -sI https://elimenti.com/glen-ellyn-web-design/
   ```
   You want `HTTP/2 301` and `location: https://elimenti.com/chicago-suburbs-web-design/`.

The click path follows Cloudflare's "Create a redirect rule in the dashboard" page (last updated May 5, 2026). `seo/cloudflare-redirects.md` sends this URL to the `#glen-ellyn` section of the same page instead; either target works for search, since Google ignores the part after `#`.

### 3. Industry pages that need a real project or first-hand detail

The brief allowed one sentence from the report on each of these if the report broke results out by business type with at least five businesses of that type. It doesn't: the downloadable CSV has no business-type breakdown, and the site-level data only has broad sectors ("Health, wellness and beauty", "Home and building", "Professional services"), none of which is one of these. So none of these pages changed. Each needs a real project, or something you've seen first-hand working with that kind of business:

- [ ] `/med-spa-websites/`: no med spa client or case study yet
- [ ] `/interior-designer-websites/`: no interior designer client (it links the Aamineez portfolio case study, which is the closest work)
- [ ] `/custom-home-builder-websites/`: no home builder client (links ABN Construction Group, a general contractor)
- [ ] `/landscape-design-websites/`: no landscape client (also links ABN)

The fastest real fix is one project, even small, in any of these, written up the way the 1 of 1 case study is.

### 4. Ask Google to index the new and changed pages

Paste each URL in `seo/request-indexing.md` into Search Console's URL Inspection, in order, and click **Request indexing**.

### 5. Optional

- [ ] If Bing Webmaster Tools isn't verified yet, verify it (it can import from Search Console). The IndexNow submissions this pass sets up show there under **IndexNow**.

## Decisions (`seo/decisions.md`)

Each one is a point where I'd normally have asked. The brief said to take the safest option it allows and keep going.

### Phase 0

1. **PageSpeed Insights API returned HTTP 429** (keyless daily quota exhausted for this machine, same as the v2 pass). I ran Lighthouse 13.6.0 locally with its default mobile settings instead. That is the engine and the lab settings PSI's mobile test uses (emulated Moto G Power, simulated slow 4G, 4x CPU slowdown), median of three runs. The PSI page also shows field data from real Chrome users, which a local run can't. The before and after numbers were measured the same way, so they compare fairly.
2. **"Internal links pointing to it" counted two ways.** With the nav and footer included, every footer page has 36 referring pages and no page has fewer than 3, so that count can't find a weak page. I report both and treat a page as under-linked when it has 0 or 1 links from inside other pages' content. That flagged `/guides/` (0), `/terms/` (0) and `/privacy/` (1). The legal pages are meant to be reached from the footer, so I left them alone and fixed `/guides/`.
3. **Overlap metric.** "Share of 5-word phrases" can mean two things. The audit's figures (car club pair about a quarter, every other pair 14% or less) match *containment*: the share of the smaller page's distinct 5-word phrases that also appear on the other page. That gives 24.2% and 13.9% here. I used it for before and after (`seo/tools/overlap.py`).

### Phase 1

4. **IndexNow key: reused the existing one instead of generating a new one.** `68d89061c779808cf9a3a0092f52b061.txt` was already at the site root, live, and accepted by IndexNow on November 4 (36 URLs, HTTP 200). A second key file would break `seo/tools/indexnow.py`, which expects exactly one, and buys nothing: the key is public by design. The workflow reads the key from that file.
5. **`sameAs` left empty.** No Elimenti profile URL (Google Business Profile, LinkedIn, Instagram, Clutch, Yelp, Bing Places) appears anywhere in the repo; the only Instagram mention is an option in the contact form's "How did you find us?" menu. The brief allows a URL only if it's in the repo, so none was added. I added a `SAME_AS` list to `seo/tools/build.py` that puts `sameAs` into the shared LocalBusiness block on every page as soon as a URL is added. The profiles to send are in `seo/todo-hashim.md`.
6. **IndexNow "first run" behavior.** The workflow submits the URLs whose HTML changed in the push that triggers it. The merge of this branch is that first push, so its first run submits every page this pass changed. If the merge reaches `main` as several pushes, each push submits its own changes. There is no schedule or cron trigger, and a manual "run" button wasn't added either, so the only trigger is a push to `main`.
7. **Med spa page has no case study to link to.** No med spa client exists, so the industry-to-case-study rule can't apply to it. I didn't link it to an unrelated case study to fill the slot.

### Phase 2

8. **Industry pages with no case study (med spa, interior designer, custom home builder, landscape design): no change.** The report's downloadable CSV (`western-suburbs-2026-findings.csv`) has no breakdown by business type. The private site-level data has only broad sectors ("Health, wellness and beauty", "Home and building", "Professional services"), and none of them is a med spa, interior designer, home builder or landscape firm. Quoting a sector figure as if it were the industry's would be a made-up stat, and the sector figures aren't on the report page to cite anyway. All four are in `seo/todo-hashim.md`.

### Shipping

9. **Branch.** This session's tooling assigned the branch `claude/loving-shannon-lnsawh`; the brief named `seo-pass-nov-2026`. I did the work on `seo-pass-nov-2026` as the brief says and pushed the same commits to both branch names, so neither points at stale work. Only `seo-pass-nov-2026` is merged into `main`.
10. **`main` moved during the pass, and it now has an `llms.txt`.** PR #34 merged this morning (after the audit the brief describes) and added `/llms.txt`, its generator `seo/tools/llms.py`, CLAUDE.md lines saying to rebuild it after every change, and `seo/cloudflare-redirects.md`. Hard rule 5 says not to add an llms.txt. I didn't add one, and I didn't delete the one you merged either: removing a file you approved a few hours ago is your call, not mine. Leaving it stale was the worst option (it would publish the old classic-club description and miss the new guide, and `llms.py --check` would fail), so I merged `main` into the branch and regenerated it. The only change is those two lines. To remove it: delete `llms.txt` and `seo/tools/llms.py` and the two `llms.py` lines in CLAUDE.md.
11. **Glen Ellyn redirect steps vs `seo/cloudflare-redirects.md`.** That file's Rule 2 is the same redirect. My steps in `seo/todo-hashim.md` use the same expression and say to skip them if that file has been followed, so the rule isn't created twice. The target is `/chicago-suburbs-web-design/` as the brief asked; that file adds `#glen-ellyn`, which makes no difference to search.
