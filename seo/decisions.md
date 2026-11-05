# Decisions made during the November 2026 SEO pass

Each one is a point where I'd normally have asked. The brief said to take the safest option it allows and keep going.

## Phase 0

1. **PageSpeed Insights API returned HTTP 429** (keyless daily quota exhausted for this machine, same as the v2 pass). I ran Lighthouse 13.6.0 locally with its default mobile settings instead. That is the engine and the lab settings PSI's mobile test uses (emulated Moto G Power, simulated slow 4G, 4x CPU slowdown), median of three runs. The PSI page also shows field data from real Chrome users, which a local run can't. The before and after numbers were measured the same way, so they compare fairly.
2. **"Internal links pointing to it" counted two ways.** With the nav and footer included, every footer page has 36 referring pages and no page has fewer than 3, so that count can't find a weak page. I report both and treat a page as under-linked when it has 0 or 1 links from inside other pages' content. That flagged `/guides/` (0), `/terms/` (0) and `/privacy/` (1). The legal pages are meant to be reached from the footer, so I left them alone and fixed `/guides/`.
3. **Overlap metric.** "Share of 5-word phrases" can mean two things. The audit's figures (car club pair about a quarter, every other pair 14% or less) match *containment*: the share of the smaller page's distinct 5-word phrases that also appear on the other page. That gives 24.2% and 13.9% here. I used it for before and after (`seo/tools/overlap.py`).

## Phase 1

4. **IndexNow key: reused the existing one instead of generating a new one.** `68d89061c779808cf9a3a0092f52b061.txt` was already at the site root, live, and accepted by IndexNow on November 4 (36 URLs, HTTP 200). A second key file would break `seo/tools/indexnow.py`, which expects exactly one, and buys nothing: the key is public by design. The workflow reads the key from that file.
5. **`sameAs` left empty.** No Elimenti profile URL (Google Business Profile, LinkedIn, Instagram, Clutch, Yelp, Bing Places) appears anywhere in the repo; the only Instagram mention is an option in the contact form's "How did you find us?" menu. The brief allows a URL only if it's in the repo, so none was added. I added a `SAME_AS` list to `seo/tools/build.py` that puts `sameAs` into the shared LocalBusiness block on every page as soon as a URL is added. The profiles to send are in `seo/todo-hashim.md`.
6. **IndexNow "first run" behavior.** The workflow submits the URLs whose HTML changed in the push that triggers it. The merge of this branch is that first push, so its first run submits every page this pass changed. If the merge reaches `main` as several pushes, each push submits its own changes. There is no schedule or cron trigger, and a manual "run" button wasn't added either, so the only trigger is a push to `main`.
7. **Med spa page has no case study to link to.** No med spa client exists, so the industry-to-case-study rule can't apply to it. I didn't link it to an unrelated case study to fill the slot.

## Phase 2

8. **Industry pages with no case study (med spa, interior designer, custom home builder, landscape design): no change.** The report's downloadable CSV (`western-suburbs-2026-findings.csv`) has no breakdown by business type. The private site-level data has only broad sectors ("Health, wellness and beauty", "Home and building", "Professional services"), and none of them is a med spa, interior designer, home builder or landscape firm. Quoting a sector figure as if it were the industry's would be a made-up stat, and the sector figures aren't on the report page to cite anyway. All four are in `seo/todo-hashim.md`.

## Shipping

10. **`main` moved during the pass, and it now has an `llms.txt`.** PR #34 merged this morning (after the audit the brief describes) and added `/llms.txt`, its generator `seo/tools/llms.py`, CLAUDE.md lines saying to rebuild it after every change, and `seo/cloudflare-redirects.md`. Hard rule 5 says not to add an llms.txt. I didn't add one, and I didn't delete the one you merged either: removing a file you approved a few hours ago is your call, not mine. Leaving it stale was the worst option (it would publish the old classic-club description and miss the new guide, and `llms.py --check` would fail), so I merged `main` into the branch and regenerated it. The only change is those two lines. To remove it: delete `llms.txt` and `seo/tools/llms.py` and the two `llms.py` lines in CLAUDE.md.
11. **Glen Ellyn redirect steps vs `seo/cloudflare-redirects.md`.** That file's Rule 2 is the same redirect. My steps in `seo/todo-hashim.md` use the same expression and say to skip them if that file has been followed, so the rule isn't created twice. The target is `/chicago-suburbs-web-design/` as the brief asked; that file adds `#glen-ellyn`, which makes no difference to search.

9. **Branch.** This session's tooling assigned the branch `claude/loving-shannon-lnsawh`; the brief named `seo-pass-nov-2026`. I did the work on `seo-pass-nov-2026` as the brief says and pushed the same commits to both branch names, so neither points at stale work. Only `seo-pass-nov-2026` is merged into `main`.
