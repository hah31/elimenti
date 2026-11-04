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

@@LIGHTHOUSE@@

## Checks (Phase 4)

@@CHECKS@@

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
