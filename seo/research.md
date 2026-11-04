# Elimenti SEO research

Date: 2026-11-04. Branch: `seo-overhaul`, cut from `main` at `53fe2a1`.

## Method and limits

- **No keyword-volume tool.** There's no Ahrefs, Semrush or Keyword Planner here. Keywords are ranked by intent and visible evidence: live search results, Google autocomplete (`suggestqueries.google.com`, US) and what competitors built pages for. **Every priority below is an estimate.**
- **Local terms have almost no autocomplete.** "web design hinsdale", "web designer oak brook", "web design glen ellyn", "web design western springs", "web design burr ridge", "luxury web design chicago" and "custom website design chicago" all returned zero suggestions. That points to low absolute volume (tens of searches a month, not thousands), which is normal for suburb-level service queries. It also means one good page can own them.
- **Autocomplete that did return** (a demand signal, not a count): `luxury web design agency`, `luxury website design examples/ideas`, `high end web design agency`, `boutique web design studio`, `med spa web design agency`, `interior designer website design`, `custom home builder website design`, `best custom home builder websites`, `squarespace vs custom website`, `how much does a website cost for a small business`, `wordpress website care plan`, `website maintenance chicago`.
- **SERP reading** used the search API for the exact queries below, plus direct fetches of the ranking pages. CyberOptik's pages block automated fetches (Cloudflare challenge), so its details come from search snippets.

## 1. Inventory (state of `main` before this branch)

| URL | Title (chars) | Desc | H1 | H2s | Words in `<main>` | Internal links | Page schema | Robots |
|---|---|---|---|---|---|---|---|---|
| `/` | Custom Websites for High-End Businesses \| Elimenti (50) | 132 | Custom websites for high-end businesses. | 7 | 657 | 20 | Service | index |
| `/404.html` | Page not found \| Elimenti (25) | 37 | Page not found | 0 | 14 | 16 | — | noindex |
| `/about/` | About Elimenti \| Hinsdale Web Design Studio (43) | 142 | About Elimenti | 5 | 378 | 17 | AboutPage, BreadcrumbList | index |
| `/boutique-websites/` | Boutique Website Design \| Elimenti (34) | 103 | Websites for independent boutiques and showrooms | 4 | 278 | 17 | BreadcrumbList, Service | index |
| `/car-club-websites/` | Car Club Website Design \| Elimenti (34) | 153 | Car club website design | 4 | 292 | 17 | BreadcrumbList, Service | index |
| `/contact/` | Start a Project \| Elimenti (26) | 110 | Tell us about your business. | 0 | 74 | 16 | BreadcrumbList, ContactPage | index |
| `/custom-home-builder-websites/` | Custom Home Builder Website Design, Hinsdale \| Elimenti (55) | 151 | Custom home builder website design | 6 | 925 | 18 | BreadcrumbList, FAQPage, Service | index |
| `/faq/` | Web Design FAQ: Cost, Timing, Ownership \| Elimenti (50) | 155 | Questions about working with Elimenti | 16 | 1136 | 16 | BreadcrumbList, FAQPage | index |
| `/glen-ellyn-web-design/` | Web Design in Glen Ellyn, IL \| Elimenti (39) | 146 | Web design in Glen Ellyn, IL | 4 | 295 | 17 | BreadcrumbList, Service | index |
| `/guides/website-cost-western-suburbs/` | What a Website Costs in the Western Suburbs \| Elimenti (54) | 154 | What a custom website costs in the western suburbs | 9 | 1077 | 16 | Article, BreadcrumbList | index |
| `/hinsdale-web-design/` | Web Design in Hinsdale, IL \| Custom-Coded Sites \| Elimenti (58) | 143 | Web design in Hinsdale, IL | 5 | 371 | 17 | BreadcrumbList, Service | index |
| `/interior-designer-websites/` | Interior Designer Website Design, Hinsdale \| Elimenti (53) | 146 | Interior designer website design | 6 | 895 | 18 | BreadcrumbList, FAQPage, Service | index |
| `/landscape-design-websites/` | Websites for Landscape Design Firms, Hinsdale \| Elimenti (56) | 152 | Websites for landscape design firms | 6 | 910 | 18 | BreadcrumbList, FAQPage, Service | index |
| `/med-spa-websites/` | Med Spa Website Design in Hinsdale & Oak Brook \| Elimenti (57) | 151 | Med spa website design | 6 | 918 | 17 | BreadcrumbList, FAQPage, Service | index |
| `/portfolio.html` | Web Design Work and Case Studies \| Elimenti (43) | missing | — | 0 | 2 | 1 | — | index |
| `/privacy/` | Privacy Policy \| Elimenti (25) | 153 | Privacy Policy | 12 | 1037 | 16 | BreadcrumbList, WebPage | index |
| `/terms/` | Terms of Service \| Elimenti (27) | 145 | Terms of Service | 13 | 850 | 16 | BreadcrumbList, WebPage | index |
| `/thanks.html` | Thanks \| Elimenti (17) | 58 | Thanks, we got it. | 0 | 16 | 16 | — | noindex |
| `/work/` | Web Design Work and Case Studies \| Elimenti (43) | 155 | Our work | 4 | 104 | 21 | BreadcrumbList, CollectionPage | index |
| `/work/1-of-1-car-club/` | 1 of 1 Car Club Website Case Study \| Elimenti (45) | 140 | 1 of 1 Car Club: website design and build | 4 | 305 | 17 | BreadcrumbList, CreativeWork | index |
| `/work/aamineez-art/` | Aamineez Art Portfolio Website Case Study \| Elimenti (52) | 145 | Aamineez Art: portfolio website | 4 | 230 | 17 | BreadcrumbList, CreativeWork | index |
| `/work/abn-construction-group/` | ABN Construction Website Care, Glen Ellyn IL \| Elimenti (55) | 153 | ABN Construction Group: website care | 4 | 207 | 17 | BreadcrumbList, CreativeWork | index |
| `/work/burdi-clothing/` | Burdi Clothing Site Care, Hinsdale IL \| Elimenti (48) | 148 | Burdi Clothing: Site Care | 4 | 204 | 17 | BreadcrumbList, CreativeWork | index |

Concept sites (`/concepts/*`, 12 pages): all `noindex, follow`, no canonical, not in the sitemap. Correct as they are.

### Technical findings

| Area | Finding | Action |
|---|---|---|
| **Hosting** | `elimenti.com` is served by **GitHub Pages** behind Cloudflare DNS (`x-github-request-id`, Fastly headers). It is *not* Cloudflare Pages. A Cloudflare Pages project also deploys `main` to **`elimenti.pages.dev`**, a full duplicate of the site. | Canonicals already point to `elimenti.com`, so the duplicate is mostly contained. Add `_headers` with Cloudflare's documented `X-Robots-Tag: noindex` rule for `*.pages.dev`. |
| **Leaked working files** | GitHub Pages runs Jekyll and honors `_config.yml` excludes, so `/PLAN.md` returns 404 there. Cloudflare Pages doesn't run Jekyll, so `elimenti.pages.dev/PLAN.md` and `/_config.yml` return **200**. The repo is public, so nothing secret leaks, but they shouldn't be indexable. | `_headers` noindex for `/seo/*` and the `.md` files. `seo/` is added to the Jekyll exclude. |
| `_redirects` / `_headers` | Only Cloudflare Pages reads them. Jekyll drops files that start with `_`, so they never reach `elimenti.com` and can't break it. | Added for the `pages.dev` deployment, and ready if the domain ever moves to Cloudflare Pages. |
| Titles | All unique, all ≤ 60. Homepage title doesn't target a query anyone types. | Retargeted (keyword map below). |
| Descriptions | All present (≤ 155) except `portfolio.html`, which is a redirect stub. | Fine as is. |
| H1 | Exactly one on every page. | — |
| Canonicals | Absolute, trailing slash, correct on all indexable pages. | — |
| `robots.txt` | `User-agent: * / Allow: /` plus sitemap. Live file matches the repo; Cloudflare isn't injecting managed AI-bot rules; GPTBot, ClaudeBot, PerplexityBot and CCBot user agents all get 200. | Keep. Verified guidance below. |
| Sitemap | 20 URLs, `loc` + `lastmod` only. Matches the indexable set. | Regenerated with the new pages. |
| 404 | Real 404 status on both hosts. `404.html` still had a TODO comment and placeholder copy. | Rewritten. |
| Alt text | No `<img>` missing `alt`. | — |
| Schema | `ProfessionalService` + `WebSite` on every page; `Service`, `FAQPage`, `Article`, `CreativeWork`, `BreadcrumbList` per page; no `Review`/`AggregateRating`. Problems: (1) schema.org marks the general `ProfessionalService` type as **deprecated** ("due to confusion with Service"); (2) `postalCode: 60523` is Oak Brook's ZIP on a Hinsdale address; (3) founder name is "Hashim", public name is "Hashim H."; (4) a `TODO sameAs` comment sits in every page's `<head>`. | Switched to `LocalBusiness`, removed the ZIP, fixed the name, removed the TODO, added `hasOfferCatalog` and Wikipedia-linked `areaServed` towns. |
| `sameAs` | Searched for Elimenti's Google Business Profile, Instagram, LinkedIn and Facebook. **None could be confirmed** (the only "Elimenti" hits were unrelated companies). | `sameAs` left out. The off-site kit says where to add the GBP link once it's public. |
| Rule 3 ("AI") hits | FAQ answer: "tells Google and AI tools"; contact form option: "ChatGPT or another AI". | Reworded. |
| Rule 4 (scope) | Burdi's legal name is **Burdi European Boutique Inc.** (site footer, burdiclothing.com). The site called the work "Site Care for a WordPress site"; the agreed scope is **targeted edits to an existing site**. | Reworded everywhere. |
| Thin pages | `/boutique-websites/` (278 words), `/car-club-websites/` (292), `/glen-ellyn-web-design/` (295), `/work/` (104). | Boutique and car club pages expanded; work index gets context. |
| Lighthouse (baseline) | 99–100 on every page, mobile and desktop (see `REPORT.md`). | Small fixes only. |

## 2. Verified guidance (checked 2026-11-04)

- **Google, LocalBusiness:** use the most specific subtype; `address` and `name` are required for the rich result; `priceRange` must be under 100 characters. [Docs](https://developers.google.com/search/docs/appearance/structured-data/local-business). The page doesn't cover service-area businesses, and an SAB gets its local knowledge panel from Business Profile anyway, so the markup carries town + state only, no street.
- **schema.org, ProfessionalService:** "The general ProfessionalService type for local businesses was deprecated due to confusion with Service." [schema.org/ProfessionalService](https://schema.org/ProfessionalService). No narrower LocalBusiness subtype fits a web studio, so `LocalBusiness` it is.
- **Google, Organization:** `sameAs` = profile URLs on other sites; markup belongs on the homepage or one page, "don't need to include it on every page." [Docs](https://developers.google.com/search/docs/appearance/structured-data/organization). We keep the full node on every page anyway because every page's `Service` references it by `@id`; this is valid and harmless.
- **Google, FAQ rich results:** "This feature will no longer appear in Google Search starting May 7, 2026." [Search Central changelog](https://developers.google.com/search/updates). Markup is still valid schema.org and still readable by Bing and assistants, so `FAQPage` stays only where a visible FAQ exists, generated from the visible text.
- **Google, AI features:** "You don't need to create new machine readable files, AI text files, or markup to appear in these features"; "no special schema.org structured data that you need to add." [Docs](https://developers.google.com/search/docs/appearance/ai-features)
- **Google-Extended:** controls Gemini training and grounding; "does not impact a site's inclusion in Google Search." Blocking it would cut Gemini grounding, so it stays allowed. [Docs](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)
- **OpenAI:** `OAI-SearchBot` controls ChatGPT search inclusion; `GPTBot` is training; `ChatGPT-User` is user-initiated. [Docs](https://developers.openai.com/api/docs/bots). All allowed by the `*` group.
- **Sitemaps:** Google "ignores `<priority>` and `<changefreq>`" and uses `lastmod` if "consistently and verifiably accurate." [Docs](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap). Bing: list only canonical URLs and include `lastmod`. [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a)
- **Bing and Copilot:** "Bing and Copilot search experiences rely on the same core crawling, indexing, and ranking foundation as traditional search"; use IndexNow when URLs are added, updated or removed; `NOARCHIVE` keeps content out of Copilot answers. [Bing guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a)
- **IndexNow:** POST JSON (`host`, `key`, `keyLocation`, `urlList`) to `https://api.indexnow.org/indexnow`; key 8–128 chars `[a-zA-Z0-9-]`; key file `/{key}.txt` at the root, containing the key. [Docs](https://www.indexnow.org/documentation)
- **llms.txt: not added.** Google: no AI text files needed (above); John Mueller (Google): "no AI system currently uses llms.txt" (June 2025) and "purely speculative" (2026). [Search Engine Roundtable](https://seroundtable.com/google-ai-llms-txt-39607.html). Claims that Perplexity or OpenAI read it come only from SEO blogs, not the companies' own docs. Unverifiable benefit = not worth adding.
- **Spam policies:** doorway abuse includes "multiple domain names or pages targeted at specific regions or cities that funnel users to one page"; scaled content abuse is "many pages… generated for the primary purpose of manipulating search rankings." [Docs](https://developers.google.com/search/docs/essentials/spam-policies)
- **Cloudflare Pages:** `_headers` example `https://:project.pages.dev/*` → `X-Robots-Tag: noindex`; `_redirects` supports 301/302/303/307/308 and 200 rewrites, **not 404**. [Headers](https://developers.cloudflare.com/pages/configuration/headers/), [Redirects](https://developers.cloudflare.com/pages/configuration/redirects/)

## 3. Keyword map

"Premium websites for high-end businesses near Chicago" is positioning. Buyers type the queries below. One primary keyword per page; no two pages share one. Priority = estimated value × winnability.

| Page | Primary keyword (estimate) | Intent | Secondary / supporting | Priority |
|---|---|---|---|---|
| `/` | high end web design Chicago suburbs | Commercial | luxury web design Chicago, high end web design agency | High |
| `/custom-websites/` *(new)* | custom website design Chicago | Commercial | custom-coded website, website redesign | High |
| `/site-care/` *(new)* | website maintenance Chicago suburbs | Commercial | website care plan, WordPress website care | Medium |
| `/pricing/` *(new)* | web design pricing (Chicago) | Commercial | web design process, how much does Elimenti cost | Medium |
| `/hinsdale-web-design/` | web design Hinsdale IL | Local | website designer Hinsdale | High |
| `/oak-brook-web-design/` *(new)* | web designer Oak Brook IL | Local | web design Oak Brook | High |
| `/glen-ellyn-web-design/` | web design Glen Ellyn | Local | — | Low |
| `/chicago-suburbs-web-design/` *(new)* | web design western suburbs Chicago | Local | boutique web design agency Chicago suburbs, web designer Burr Ridge / Western Springs / Clarendon Hills / Elmhurst / Naperville | High |
| `/med-spa-websites/` | med spa website design | Commercial | med spa web design Chicago, Hinsdale, Oak Brook | High |
| `/interior-designer-websites/` | interior designer website design | Commercial | interior design website Chicago | Medium |
| `/custom-home-builder-websites/` | custom home builder website design | Commercial | best custom home builder websites | Medium |
| `/landscape-design-websites/` | landscape design website design | Commercial | landscaping company website Chicago | Low |
| `/boutique-websites/` | boutique website design | Commercial | luxury boutique website, showroom website | Medium |
| `/car-club-websites/` | car club website design | Commercial | private car club website | Low |
| `/guides/website-cost-western-suburbs/` | how much does a website cost Chicago | Informational | website cost western suburbs, small business website cost | High |
| `/guides/squarespace-vs-custom-website/` *(new)* | squarespace vs custom website | Informational | custom website vs website builder for luxury brands | Medium |
| `/guides/what-makes-a-website-look-high-end/` *(new)* | what makes a website look high end | Informational | luxury website design examples/ideas | Medium |
| `/guides/` *(new)* | (hub, no target) | — | — | — |
| `/work/` | web design case studies (brand) | Navigational | — | Low |
| Case studies | client brand + "website" | Navigational | — | Low |
| `/faq/` | web design questions (long tail) | Informational | each question is its own long-tail query | Medium |
| `/about/` | Elimenti (brand) | Navigational | — | Low |

**Not targeted, and why:**
- **Law firm websites.** The SERP for "law firm website design Chicago" belongs to legal-marketing specialists (Hexxen, MileMark Media, The Modern Firm, PaperStreet, CodeWCG, CyberOptik's attorney page), and Elimenti has no legal work to point to. Not winnable now.
- **Luxury retail / e-commerce.** Results are Shopify agencies (Praella, Webtonic, 1Brand). Elimenti doesn't build stores; `/boutique-websites/` covers the non-store side honestly.
- **More town pages.** See section 5.

## 4. Competitor teardown

Who shows up for the strongest queries ("web design Hinsdale", "web designer Oak Brook", "high end web design agency Chicago", "luxury web design Chicago", "boutique web design agency Chicago suburbs"):

| Competitor | Shows for | Structure and depth | Schema | Location pages | Reviews / proof |
|---|---|---|---|---|---|
| **CyberOptik** (Elmhurst, est. 2002) | Hinsdale, Oak Brook, law firms | WordPress agency; city pages for Hinsdale, Oak Brook, Oak Park and more; industry pages | Couldn't fetch (bot wall) | Large city-page network, templated | Reviews and portfolio |
| **RivalMind** | Hinsdale | Hinsdale page ~2,200 words, 12 H2s, generic ("Why Web Design Matters", plan tiers); runs on Duda | `LocalBusiness`, `BreadcrumbList` | 11 `/web-design-services/*-web-design` city pages | "Award-winning", testimonials |
| **Creative Marketing AI** | Hinsdale | ~1,100 words: "About Hinsdale", "Nearby communities", FAQ; a Hinsdale **NY** page on the same template | `Organization` + `LocalBusiness` + `ProfessionalService` | 26 town pages (scaled) | Reviews; builds "from $2,500" |
| **Plego** | Oak Brook | Software/app shop; homepage-led | `Corporation` | No | Testimonials |
| **Dantech IT** | Oak Brook | Managed IT firm with web design as a side service | `Organization`, `WebPage` | No | — |
| **Blacksmith Agency** | high end / Chicago | ~2,150 words: case studies, process, team, industries, FAQ; publishes $20k–$100k+ ranges | `LocalBusiness`, `BreadcrumbList` | Chicago neighborhoods in copy | Clutch reviews, awards |
| **Digital Silk** | luxury / Chicago | ~3,100 words: portfolio, CMS options, process, team, FAQ | `WebPage`, `Service`, `BreadcrumbList` | Chicago page in a national city set | Awards, logos (Paul Stuart) |
| **Solid Digital** | high end / Chicago | ~1,000 words, B2B focus, FAQ | `FAQPage`, `BreadcrumbList` | Chicago only | Testimonials |

**Gaps Elimenti can actually win:**
1. **Nobody local owns "high-end" in the western suburbs.** The suburb results are generalist WordPress shops (CyberOptik, RivalMind), IT firms (Dantech, Plego) and scaled town-page networks. The "luxury/high-end" results are downtown or national agencies at $20k–$100k+. A studio that is local, design-led and **publishes a $3,000 starting price** sits in an empty space.
2. **Town pages in this market are thin templates** (RivalMind's 11, Creative Marketing AI's 26 incl. Hinsdale NY). One honest, specific page per town that has real work or real local knowledge beats them on usefulness, and Google's doorway policy works against them, not us.
3. **Price transparency.** Of the agencies above, only Blacksmith publishes ranges, and those start at $20k. "Projects start at $3,000" is a quotable fact for both buyers and AI assistants.
4. **Industry pages with real substance.** Competitor industry pages are generic. Ours already explain what a med spa or builder site needs; adding "where templates fall short" makes them the most specific pages on the SERP.
5. **Reviews are the gap we can't close on-site.** Every competitor shows reviews. Elimenti has one testimonial and no GBP reviews yet. That is the single biggest off-site lever (see `off-site-kit.md`).

## 5. Location pages: which towns qualify (rule 5)

| Town | Distinct content available? | Decision |
|---|---|---|
| Hinsdale | Yes: GBP service area, real client work (Burdi on Hinsdale Avenue), founder's charity car meet, downtown boutique district | **Own page** (exists, improved) |
| Oak Brook | Yes: GBP service area; a different business base, with corporate HQs (Ace Hardware; McDonald's left in 2018), professional and B2B firms, Oakbrook Center (opened 1962, 160+ stores) | **Own page** (new) |
| Glen Ellyn | Yes: real client work (ABN Construction Group) | **Own page** (exists) |
| Burr Ridge, Western Springs, Clarendon Hills, Elmhurst, Naperville | Each has a few verifiable, distinct facts (Burr Ridge Village Center; Western Springs' Burlington/Hillgrove downtown; Clarendon Hills' downtown plan; Elmhurst's York Theatre district; Naperville's 300+ downtown businesses), but not enough for a full page without padding, and no client work | **Merged** into one `/chicago-suburbs-web-design/` page with a distinct section each |

Three town pages plus one hub. The cap is 4–6; only three towns clear the "genuinely distinct" bar today. A fourth should be added when there's client work in that town.

## 6. AI-assistant citation check

Queries like "best web design agency for luxury brands Chicago suburbs", "best web designers Naperville", "top web design companies DuPage County" and "best boutique web design studio Chicago" return (and assistants cite) these sources:

| Source | Type | How to get in |
|---|---|---|
| [Clutch](https://clutch.co/web-designers/chicago) | Directory with reviews; heavily cited | Free profile; reviews drive rank |
| [DesignRush](https://www.designrush.com/agency/website-design-development/illinois/chicago) | Directory/rankings (some paid) | Free listing via submission form |
| [BrightLocal Agency Directory](https://www.brightlocal.com/agency-directory/usa/illinois/website-design-agencies/) | Directory, town pages (Naperville, Elmhurst, Wheaton) | For BrightLocal customers; skip unless subscribed |
| [The Manifest](https://themanifest.com/web-design/agencies/illinois) | Clutch sister site | Fed by the Clutch profile |
| [ThreeBestRated](https://threebestrated.com/web-designers-in-naperville-il) | "3 best" per town; cited for "best X in [town]" | Free submission, but it has rejected businesses with no physical address |
| [Expertise.com](https://www.expertise.com/business/web-design/illinois/chicago) | Editorial "best" lists | Editorial selection; reviews and site quality matter |
| [Mojo Media: 14 Best Web Design Agencies in Chicago](https://mojo-agency.com/web-design-agencies-in-chicago/) | Agency listicle | Pitch for inclusion |
| [Webtonic: Top 52 Boutique Web Design Agencies](https://www.webtonic.io/blog/top-boutique-web-design-agencies) | Listicle | Pitch for inclusion |
| [Digital Agency Network: Chicago web design](https://digitalagencynetwork.com/agencies/chicago/web-design/) | Directory | Listing request |
| [BBB](https://www.bbb.org/us/il/hinsdale/category/web-design) | Directory; shows for "web design Hinsdale" | Free business profile |
| [Yelp](https://biz.yelp.com) | Cited by assistants for local "best" queries | Free business page |

What the cited agencies have in common: a directory profile with reviews, and a homepage or service page that states plainly who they serve, where and at what price. The on-site work covers the second half. The first half is the off-site kit.

## Sources

Search results consulted 2026-11-04: RivalMind Hinsdale page; CyberOptik Hinsdale/Oak Brook pages (snippets); Creative Marketing AI Hinsdale page and sitemap; Blacksmith, Solid Digital, Digital Silk Chicago pages; Plego; Dantech; Clique Studios cost page (Sept 2024: $5k–$15k basic site); Squarespace pricing ($19–$99/mo billed yearly) and export help article; Oakbrook Center and Discover DuPage; Burr Ridge Village Center coverage; Downtown Naperville Alliance (Feb 2026); City of Elmhurst business districts; Clarendon Hills downtown plan coverage.
