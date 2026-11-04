# SEO overhaul: report

Branch `seo-overhaul` → merged to `main` on 2026-11-04. Research: `seo/research.md`. Off-site steps: `seo/off-site-kit.md`.

## Three things you should know first

1. **Your site isn't hosted on Cloudflare Pages.** `elimenti.com` is served by **GitHub Pages** (Cloudflare is only your DNS). A Cloudflare Pages project *also* publishes a full copy at `elimenti.pages.dev`, which was indexable and served `PLAN.md` publicly. Fixed with a `_headers` noindex. Cloudflare-only files (`_headers`, `_redirects`) only affect that copy.
2. **Burdi's scope was wrong on the live site.** It said "Site Care for a WordPress site"; it now says "targeted edits to an existing site" everywhere, with the legal name (Burdi European Boutique Inc.). Two "AI" mentions are gone, and the public name is "Hashim H." everywhere.
3. **No `sameAs` profiles could be verified** (no findable GBP, Instagram or LinkedIn for Elimenti), so none were added. The kit shows the one line to add once they exist.

## What changed, page by page

| Page | Change | Target keyword (estimate) |
|---|---|---|
| `/` | New title/description; studio + price in hero; service cards link to service pages; Oak Brook and suburbs links; guides block; Burdi scope fixed; "AI" removed from form | high end web design Chicago suburbs |
| `/custom-websites/` **new** | Custom build service page: inclusions, why custom-coded, who it's for, redesigns, real builds | custom website design Chicago |
| `/site-care/` **new** | Site Care: pricing, coverage, existing WordPress sites, request flow, FAQ | website maintenance Chicago suburbs |
| `/pricing/` **new** | "Projects start at $3,000", inclusions, what moves price, 5-step process, Stripe or check, ownership | web design pricing (Chicago) |
| `/oak-brook-web-design/` **new** | Oak Brook's own landscape (HQs, professional firms, Oakbrook Center), what Oak Brook clients check | web designer Oak Brook IL |
| `/chicago-suburbs-web-design/` **new** | Hub with distinct sections: Burr Ridge, Western Springs, Clarendon Hills, Elmhurst, Naperville | web design western suburbs Chicago |
| `/hinsdale-web-design/` | Burdi scope fixed; new "How Hinsdale does business" section; links | web design Hinsdale IL |
| `/glen-ellyn-web-design/` | Links to pricing, Site Care, suburbs | web design Glen Ellyn |
| 6 industry pages | "Where templates fall short" section on each; boutique + car club pages doubled with visible FAQs | med spa / interior designer / custom home builder / landscape design / boutique / car club website design |
| `/guides/` **new** | Guide hub | — |
| `/guides/website-cost-western-suburbs/` | Retargeted to Chicago; cited Chicago agency ranges; links | how much does a website cost Chicago |
| `/guides/squarespace-vs-custom-website/` **new** | Honest comparison, 3-year cost table, sourced export limits | squarespace vs custom website |
| `/guides/what-makes-a-website-look-high-end/` **new** | Seven factors, template tells, five-minute test | what makes a website look high end |
| Case studies (4) | Burdi rewritten as targeted edits; 1 of 1 now links its live site; "takeaway" section on each | client name + website |
| `/faq/` | "Where is Elimenti based?", "How do I pay?", links, scope and name fixes | web design questions (long tail) |
| `/about/`, `/work/`, `/404.html` | Name and scope fixes; 404 TODO and placeholder copy replaced | — |
| Every page | Rebuilt head: `LocalBusiness` (schema.org deprecated `ProfessionalService`), Wikipedia-linked service towns, offer catalog, Service per offering, FAQPage only where a FAQ is visible, breadcrumbs, per-page OG cards; grouped footer; nav adds Pricing | — |
| Site files | `sitemap.xml` (20 → 28 URLs), IndexNow key file, `_headers`/`_redirects`, `seo/` excluded from build | — |

**Deliberately not done:** no law-firm page (SERP owned by legal-marketing specialists; no related work); only 3 town pages, not 4–6 (only Hinsdale, Oak Brook and Glen Ellyn have genuinely distinct content; the rest are sections on the hub); no `llms.txt` (Google says it's not needed; no AI company's own docs confirm using it); `robots.txt` unchanged (already allows every crawler, including AI search bots).

**Existing terms I reused but couldn't verify from your brief:** 4–6 week timeline, Site Care's "up to four updates a month", $85/hr photography, visual identity. They were already published on your site. Correct them if any changed.

## Lighthouse (local Jekyll build; scores are Performance/Accessibility/Best practices/SEO)

| Page | Mobile before | Mobile after | Desktop before | Desktop after |
|---|---|---|---|---|
| `/` | 99/100/100/100 | 99–100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/custom-websites/` | new | 100/100/100/100 | new | 100/100/100/100 |
| `/site-care/` | new | 100/100/100/100 | new | 100/100/100/100 |
| `/pricing/` | new | 100/100/100/100 | new | 100/100/100/100 |
| `/chicago-suburbs-web-design/` | new | 100/100/100/100 | new | 100/100/100/100 |
| `/hinsdale-web-design/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/oak-brook-web-design/` | new | 100/100/100/100 | new | 100/100/100/100 |
| `/glen-ellyn-web-design/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/med-spa-websites/` | 99/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/interior-designer-websites/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/custom-home-builder-websites/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/landscape-design-websites/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/boutique-websites/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/car-club-websites/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/guides/` | new | 100/100/100/100 | new | 100/100/100/100 |
| `/guides/website-cost-western-suburbs/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/guides/squarespace-vs-custom-website/` | new | 100/100/100/100 | new | 100/100/100/100 |
| `/guides/what-makes-a-website-look-high-end/` | new | 100/100/100/100 | new | 100/100/100/100 |
| `/work/` | 99/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/work/1-of-1-car-club/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/work/aamineez-art/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/work/burdi-clothing/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/work/abn-construction-group/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/about/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/faq/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/contact/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/privacy/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/terms/` | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 | 100/100/100/100 |
| `/404.html` | 100/100/100/63 | 100/100/100/63 | 100/100/100/63 | 100/100/100/63 |

Every page is 100/100/100/100 on both mobile and desktop except: the homepage on mobile varies between 99 and 100 from run to run (its LCP is the hero paragraph at 1.8–2.0 s; the baseline was 99), and the 404 page's SEO score is 63 because it is intentionally `noindex` with a 404 status. Fixes made: `/work/` loaded its first case-study image lazily even though it was the largest paint, and phones downloaded 1200px images where 800px was enough (both fixed, 99 → 100). Lighthouse 12, local Jekyll build. The local server doesn't compress or cache files and GitHub Pages does, so production should score the same or better.

## Checks (Phase 4)

All passed (`seo/tools/check.py`, `seo/tools/validate_schema.py`):

- **Crawl** of the Jekyll-built site: 162 URLs (40 HTML pages, 28 indexable), **0 broken** links or assets; unknown URLs return a real 404; sitemap = exactly the 28 indexable pages; every page has one H1 and a unique title (≤ 58 chars), description (≤ 155) and H1; canonicals and OG tags correct; every image has alt text; all 12 concept pages `noindex`.
- **Schema:** 30/30 pages, **0 errors, 0 warnings** on the official Schema Markup Validator (validator.schema.org). FAQPage text equals the visible text on all 5 FAQ pages. No `Review`/`AggregateRating`.
- **Grep** for TODO, TBD, lorem, placeholder, `[`, XX, AI and "hand-coded" in visible copy (including concept pages) and raw HTML/CSS/JS: 0 hits.
- **Outbound links:** all 200, except Business Wire, which blocks bots; the Clutch release it backs was confirmed via search.
- **Rules 3/4/5 re-read** of everything written: cut 7 claims that weren't supported ("most of our projects replace something", "every new member starts" at 1 of 1, "no member list", "mostly locally owned", "most customers are referred", "most custom studios", "most people"). Town pages: 3, each with distinct content; the hub covers the rest.
- **Screenshots** of 18 new and changed pages at 1440 and 390 px, reviewed: on-brand, no horizontal overflow. One copy issue found and fixed.

## Deploy and IndexNow

@@DEPLOY@@

## Off-site actions, ranked by expected impact

1. **Google Business Profile**: categories, services, 750-char description, 8 service areas (kit §1). Highest impact for every local query.
2. **Ask for reviews** in the order given (kit §2). Every competitor shows reviews; you have none on Google. This is the biggest gap.
3. **Search Console + Bing Webmaster Tools**, submit the sitemap, request indexing on the 8 key URLs (kit §4). Bing powers Copilot answers.
4. **Cloudflare: confirm "Block AI bots" is off** (kit §4). If it's on, ChatGPT, Claude and Perplexity can't read the site at all.
5. **Clutch profile + 2 client reviews there** (kit §3). The directory AI assistants cite most for agency queries.
6. **Site credits from 1 of 1 Car Club and aamineez.art** (kit §5, #1–2). Easiest real backlinks you'll get.
7. **Bing Places, Yelp, LinkedIn, Instagram, BBB, Nextdoor** (kit §3). Then add the profile URLs to `sameAs`.
8. **Illinois Startups list + TEC + Daily Illini** (kit §5). Links from illinois.edu domains.
9. **The Hinsdalean / Patch Hinsdale** (kit §5). Local press for the Hinsdale query.
10. **Hinsdale Chamber, then Oak Brook Chamber** (paid; kit §3).
