# Niche pages, concept sites and cost guide: plan

Branch: `claude/adoring-goldberg-ufkmyy` (cut from `main` at `4c97942`). Nothing is merged to `main`.

This file is a working doc. It is **not published**: `_config.yml` excludes `"*.md"` (plus `SEO-AUDIT.md` and `content/` by name), and GitHub Pages runs Jekyll because there is no `.nojekyll`, so the exclude applies. Verified in Phase 5 by checking that `/PLAN.md` is absent from the built output rules (Jekyll `exclude` matches root-level `*.md`).

---

## Phase 0: what the site is today

### Pages (sitemap.xml, 15 URLs, all verified against the repo and the live site)

| URL | H1 | Notes |
|---|---|---|
| `/` | Custom websites for high-end businesses. | `.hero`, services grid, statement, process, pricing line, work grid, quote, areas, inline contact form |
| `/about/` | About Elimenti | first person ("run by me, Hashim") |
| `/faq/` | Questions about working with Elimenti | 15 Q&As, FAQPage JSON-LD mirrors visible text |
| `/contact/` | Tell us about your business. | Web3Forms form (not FormSubmit, despite the brief; left as is) |
| `/work/` | Our work | `CollectionPage` JSON-LD |
| `/work/1-of-1-car-club/` | 1 of 1 Car Club: website design and build | full build |
| `/work/aamineez-art/` | Aamineez Art: portfolio website | pro bono build |
| `/work/burdi-clothing/` | Burdi Clothing: Site Care | WordPress site care |
| `/work/abn-construction-group/` | ABN Construction Group: website care | WordPress site care, Glen Ellyn GC |
| `/hinsdale-web-design/` | Web design in Hinsdale, IL | town page |
| `/glen-ellyn-web-design/` | Web design in Glen Ellyn, IL | town page |
| `/boutique-websites/` | Websites for independent boutiques and showrooms | niche page |
| `/car-club-websites/` | Car club website design | niche page |
| `/privacy/`, `/terms/` | legal | |

Not in sitemap (correctly): `404.html` (noindex), `thanks.html` (noindex), `portfolio.html` (meta-refresh to `/work/`, canonical `/work/`).

Existing niche slugs: `boutique-websites`, `car-club-websites`. Skip both industries.

### Design system (`assets/css/style.css`, one stylesheet, no build step)

- **Color tokens:** `--color-bg #FAF8F5` (warm off-white), `--color-surface #F3EFEA`, `--color-text #171315`, `--color-muted #6A6266`, `--color-faint #A89FA3` (decorative only), `--color-accent #6D1A36` (burgundy), `--color-accent-tint #F5E8ED`, borders `#E8E2E4` / `#CFC6CA` / input `#91888C`.
- **Type:** Cormorant Garamond (display, self-hosted variable 300–700 + italic) and Outfit (body, variable). H1 72px light (52 / 42 on small screens), H2 48px, H3 24px, body 17px / 1.7. Labels and nav are 13–14px Outfit, medium, uppercase, 0.08em tracking.
- **Spacing:** 8 / 16 / 24 / 48 / 80 / 120px (`--space-xs` … `--space-section`). Max width 1120px, prose 68ch, gutter 24px (20px under 540px).
- **Radius:** 4px buttons/inputs, 8px cards.
- **Motion:** `[data-reveal] > *` fade-up, added by JS only for elements below the fold, so everything is visible with JS off. `prefers-reduced-motion` respected.

### Components in use (reuse these, don't reinvent)

`.nav` (fixed, wordmark + Work/About/FAQ + "Start a project" CTA, mobile overlay via `.js`), `.page-hero` + `.lede`, `.prose` > `section` (68ch column, `h2`, `ul` with burgundy dash bullets), `.glance` (`dl` key/value table), `.shots` (desktop + phone screenshot pair), `.work-grid` / `.work-card` (whole-card link), `.faq-list` / `.faq-item` (h2 + p), `.actions` + `.btn--primary` / `.btn--ghost` + `.actions__alt`, `.text-link`, `.quote`, `.areas__list`, `.breadcrumb` (rendered after `</main>`), `.footer`.

### Page template (every subpage)

1. `<head>`: charset, viewport, `<title>` "X | Elimenti", meta description, canonical (absolute `https://elimenti.com/...` with trailing slash), OG (`type`, `site_name`, `locale`, `url`, `title`, `description`, `og-image.png?v=4` 1200×630 + alt), Twitter `summary_large_image` mirror, `theme-color`, favicon + apple-touch-icon `?v=3`, two font preloads, `style.css`, inline `document.documentElement.classList.add('js')`, `main.js` deferred.
2. The TODO comment about `sameAs`, then JSON-LD block 1: the shared `@graph` of `ProfessionalService` (`#business`) + `WebSite` (`#website`), identical on every page.
3. JSON-LD block 2: page-specific `@graph` (Service / CreativeWork / FAQPage / AboutPage …) + `BreadcrumbList`.
4. `<body>`: skip link, header nav (with `aria-current="page"` on the active item), `<main id="main">` with `.page-hero` then `.prose`, breadcrumb `nav`, footer.

**Footer:** NAP line, "Based in Hinsdale and Oak Brook…", footer nav (`Work, About, FAQ, Contact, Hinsdale, Glen Ellyn, Boutique websites, Car club websites`), legal links.

**Voice:** short declarative sentences, "we" for the studio (first person singular only on About), every claim checkable, scope stated exactly ("We didn't build Burdi's site").

**Head quirk worth copying exactly:** apostrophes are `&#x27;` in HTML text and raw `'` inside JSON-LD.

### robots.txt / sitemap / config

- `robots.txt`: `User-agent: * / Allow: /` + sitemap line. Keep as is.
- `sitemap.xml`: `<loc>` + `<lastmod>` only, no priority/changefreq. Add new indexable URLs with `lastmod` 2026-10-25; bump `lastmod` on every existing page whose content changes.
- `_config.yml`: excludes `*.md`. Concept pages are plain HTML with no front matter, so Jekyll copies them untouched. No file or folder may start with `_` (Jekyll would drop it).

---

## Phase 1: niche selection

### Method and its limits (read this)

- **Evidence sources:** web search results, the businesses' own sites, Houzz/Yelp/OpenTable/BBB/Knot listings, the Greater Oak Brook Chamber directory, The Hinsdalean, and Google autocomplete (`suggestqueries.google.com`) as a demand proxy.
- **What I could not do:** this sandbox has no keyword-volume tool (no Ahrefs/Semrush/GKP), and fetching Google or Bing SERP HTML directly returns bot walls or junk (Bing returned generic "Med" results; DuckDuckGo returned a captcha). SERP weakness was judged from the search API results for the exact queries in the brief. Treat criteria 3 and 4 as directional, not measured. **Verify the four chosen queries yourself in an incognito Google and Bing window before spending money against them.**
- Scores are 1–5. A **fit gate** sits on top: an industry fails if winning it would require something Elimenti doesn't sell (online stores) or would imply experience Elimenti doesn't have.

### Scores

| Industry | 1 Density | 2 Pays for premium | 3 SERP weakness | 4 Demand | Total | Fit gate | Decision |
|---|---|---|---|---|---|---|---|
| **Med spas** | 5 | 5 | 4 | 4 | **18** | pass | **Pick** |
| **Custom home builders** | 5 | 4 | 5 | 4 | **18** | pass (ABN case study is real contractor work) | **Pick** |
| **Interior designers** | 5 | 3 | 5 | 3 | **16** | pass | **Pick** |
| **Landscape design-build** | 5 | 4 | 4 | 2 | **15** | pass | **Pick** |
| Cosmetic / boutique dental | 4 | 5 | 2 | 5 | 16 | weak | Defer to batch 2 |
| Salons | 5 | 2 | 3 | 4 | 14 | pass | Reject for now |
| Jewelers | 3 | 4 | 3 | 2 | 12 | **fail** (they want e-commerce catalogs) | Reject |
| Fine dining | 2 | 2 | 3 | 4 | 11 | pass | Reject |
| Specialty automotive (PPF, wrap, restoration) | 2 | 3 | 2 | 3 | 10 | pass | Reject for now |
| Galleries | 1 | 2 | 3 | 1 | 7 | pass | Reject |

### Evidence per industry

**Med spas (pick).**
- Density: Hinsdale has Elase Medical Spa (22 W 1st St), Natural Beauty Med Spa (12 Salt Creek Ln), BU Wellness & Med Spa (201 E Ogden Ave), Renaissance Cosmetic and Duly Aesthetics (not independent). Oak Brook: Charming Skin (2425 W 22nd St), Essex Skin Medical Aesthetics (2044 York Rd), Rejuvenate Med Spa (2021 Midwest Rd). Burr Ridge: MedAndSpa (women-owned, independent). Western Springs: Skinovatio Medical Spa (901 Burlington Ave), Deka Lash & Medspa. Naperville: Blue Seas, V/O Med Spa, Sante, Suburban Healthcare Laser. Sources: [Yelp, Elase](https://www.yelp.com/biz/images-med-spa-hinsdale), [Natural Beauty Hinsdale](https://www.naturalbeautymedspa.com/hinsdale-office.html), [BU Wellness](https://www.buwellness.com/), [PortraitCare Western Springs](https://www.portraitcare.com/directory/united-states/illinois/western-springs/medical-spa/), [Fresha Oakbrook Terrace](https://www.fresha.com/lp/sv/bt/estetik/us-chicago/oakbrook-terrace), [Duly Hinsdale](https://dulyhealthandcare.com/duly-aesthetics-medspa-hinsdale).
- Pays: Natural Beauty's site is "Designed and Maintained by" TNT Dental (a medical-marketing vendor) and has visible typos ("Chigaco", "Mico-Needling") and a dead "Meet Your Injectors" link. Renaissance Cosmetic in Hinsdale hired Metalogic Design for web design and PPC ([case study](https://metalogicdesign.com/med-spa-digital-marketing-renaissance-cosmetic/)). A 2026 roundup counts 18 Chicago-area med spa marketing agencies and notes none publish a starting price ([Web Tonic](https://www.webtonic.io/blog/best-medical-spa-aesthetics-marketing-agencies-chicago)). Money is being spent; the work is generic.
- SERP: "med spa website design Hinsdale IL" returns the med spas themselves plus national agencies (Studio 3, Flamingo, Mila Design Co., Metalogic). No western-suburbs studio.
- Demand: autocomplete offers "med spa web design agency" (commercial intent).
- What top sites have ([AmSpa](https://americanmedspa.org/news/what-every-medspa-needs-to-know-about-website-design), [OnTheMap review of 11 sites](https://www.onthemap.com/med-spa-web-design-company/), [Redefine Web](https://redefineweb.com/industries/med-spa-marketing-agency/med-spa-web-design/)): one page per treatment, booking in the header and on every treatment page (Boulevard, Zenoti, Vagaro, Mindbody), provider credentials and medical director stated plainly, consent-based before/after galleries, a price answer (from-prices, ranges or memberships), real photos of the space.

**Custom home builders (pick).**
- Density: Ross Builders (Hinsdale, typical job $3M–$8M per Houzz), The Walker Group (Clarendon Hills, since 1996, referral-only), MDG Builders, LM Custom Homes (Clarendon Hills), Black Knight Group (Hinsdale), Summit Signature Homes, Tiburon Homes (Hinsdale), Oakley Home Builders (Downers Grove), Greenside Design Build, SG Home Builders, DJK Custom Homes (Naperville), Skycrest, Overstreet Builders (Naperville), CL Design-Build. Sources: [Houzz, Ross](https://www.houzz.com/ideabooks/users/rossbuilders), [Houzz, Walker Group](https://www.houzz.com/pro/thewalkergroup), [Houzz, LM Custom Homes](https://www.houzz.com/professionals/design-build-firms/lm-custom-homes-pfvwus-pf~26574239), [Oakley](https://www.oakleyhomebuilders.com/), [Greenside](https://www.greensidedesignbuild.com/), [The Hinsdalean, Sept 2025](https://www.thehinsdalean.com/story/2025/09/11/news/developments-bring-new-homes-to-hinsdale/9879.html).
- Pays: high-ticket work; agencies do get paid here (Olive Street Design built Martin Design & Build's site). Gap signal: a search for Ross Builders' own website finds only Houzz and directory listings.
- SERP: "home builder website design Hinsdale Naperville" returns only builders. Not one web designer.
- Demand: autocomplete offers "custom home builder website design" and "best custom home builder websites".
- Honest link to real work: ABN Construction Group (Glen Ellyn GC) is ongoing Site Care, and the Glen Ellyn page already says "For a contractor, the project portfolio is the sales pitch."
- What top sites have ([CyberOptik, 20 builder sites](https://cyberoptik.net/blog/20-best-home-builders-website), [FreshySites top 25](https://freshysites.com/web-design-development/top-25-home-builders-websites/)): galleries split by type (custom, spec, renovation), a dedicated process page, "where we build" by town, interiors as well as exteriors, available homes/lots when they exist.

**Interior designers (pick).**
- Density: AXB Interiors (737 S Elm St, Hinsdale), Savvy Interior Design (since 2001), Studio W Interiors (new downtown Hinsdale studio), Violet Grace Interiors (Hinsdale, Oak Brook Chamber), Katharine Andrews Interiors, Linden + Co. (Western Springs, La Grange, Hinsdale), Dara Agruss Design (Elmhurst), JoAnna Baum Interiors (Elmhurst), Debora Lyn (new Elmhurst boutique), Christie Hines, Kristin Petro, Peltier Designs (Naperville). Sources: [Houzz, AXB](https://www.houzz.in/pro/axbdesign/andrea-burridge-interior-design), [Woodworking Network, Savvy](https://www.woodworkingnetwork.com/closets/designer-profile-donna-hall-savvy-interior-design), [Oak Brook Chamber](https://business.obchamber.com/list/ql/architects-26), [Linden + Co.](https://www.lindenandcointeriors.com/), [Dara Agruss](https://daraagrussdesign.com/), [JoAnna Baum](https://www.joannabauminteriors.com/about), [Designers Today, Debora Lyn](https://www.designerstoday.com/designers/debora-lyn-interior-design-marks-20-years-with-new-chicago-suburb-boutique).
- Pays: mixed, which is why this scores 3. Linden + Co. runs on Wix (images on wixstatic.com). Dara Agruss runs a polished WordPress site with room-by-room pages and a client questionnaire. Many lean on Houzz. These owners sell taste, so a design-led studio is a natural fit, but some will choose Squarespace.
- SERP: "interior designer website design western suburbs Chicago" and "…Hinsdale" return the designers themselves and national freelancers. No local studio.
- Demand: autocomplete is mostly "examples / templates / inspiration" (DIY-leaning), so 3.
- What top sites have ([Really Good Designs](https://reallygooddesigns.com/interior-design-portfolio-websites/), [Houzz Pro](https://pro.houzz.co.uk/pro-learn/blog/startup-guide-interior-design-website-inspiration)): portfolio by project with location and scope, a process page, an inquiry form that asks project type, timeline and budget, press.

**Landscape design-build (pick, ahead of dental).**
- Density: King's Landscape Design (Lemont, landscape architects, 65+ years), Fox Landscape (Westmont; "residential focus in Hinsdale is exclusively high-end design-build"), Acorn Design Group (Hinsdale, Western Springs, Clarendon Hills, Burr Ridge, Oak Brook, 24 years), Laslo Landscape Design (Hinsdale), Mariani (dedicated Hinsdale page), Rolling Landscapes, Murphy Landscape & Design, GoldLeaf, Western DuPage Landscaping (Naperville, landscape architects on staff), C B Conlin (Naperville, since 1985), Narnia, Apple Landscape Design, Reveal Design. Sources: [Fox Landscape](https://www.foxlawn.com/landscape-design-hinsdale), [King's](https://kingslandscapedesign.com/landscaping-hinsdale-il/), [Acorn](https://www.acorndesigngroup.net/), [Mariani](https://www.marianilandscape.com/hinsdale-landscaping), [Rolling Landscapes](https://www.rollinglandscapes.com/), [Western DuPage](https://www.westerndupagelandscaping.com/), [Houzz Hinsdale landscape architects](https://www.houzz.com/professionals/landscape-architect/hinsdale-il-us-probr0-bo~t_11788~r_4896012).
- Pays: established firms with landscape architects on staff, buying from contractor-marketing agencies (Straight North and CyberOptik both sell landscaping web design).
- SERP: "landscape company website design Hinsdale western suburbs" returns landscapers and Houzz only.
- Demand: weakest of the four (autocomplete thin), so 2.
- What top sites have ([Moda](https://moda.app/blog/landscaping-website-design), [CyberOptik hardscape sites](https://cyberoptik.net/blog/best-hardscape-design-websites)): portfolio organized by project type with captions that name the site problem and material, design-build kept separate from maintenance with its own intake, the consultation → design → proposal → build → care sequence explained, specific service area.

### Why landscape beat dental for slot four (judgment call)

Dental scores higher on paper (16 vs 15), but it's the most crowded vendor market in the list. "Dental website design Hinsdale Oak Brook" already returns booked.dental's dedicated Oak Brook market pages and TheDocSites' credit on a Hinsdale practice. Practices are often locked into bundled dental-marketing contracts and HIPAA-form vendors. Landscape design-build has the same homeowner, the same towns and the same "the photos sell it" logic as builders and interior designers, so the three pages reinforce each other. Dental is the first candidate for batch two.

### Rejections in one line each

- **Jewelers:** fail the fit gate. Razny's Hinsdale store runs on a store platform (`/pages/` URLs) and Merry Richards in Oakbrook Terrace runs on Build.Shop. They need product catalogs and checkout; Elimenti doesn't build stores.
- **Fine dining:** too few independents. Vistro Prime (Hinsdale) and Petite Vie (Western Springs) share a chef-owner; Oak Brook's upscale rooms are mostly group-owned (Gibsons, Lettuce's VIOLÍ, Eddie Merlot's). Sources: [OpenTable](https://www.opentable.com.au/features/best-restaurants-with-bar-seating-hinsdale-il).
- **Salons:** many in Hinsdale and Clarendon Hills (Studio Giuseppe, Salon Sapphire, Wesley James, The Salon by David and William), but they live on Vagaro/Fresha booking pages and a $3,000 floor is a hard sell. Source: [Vagaro Hinsdale](https://www.vagaro.com/listings/hinsdale--il).
- **Specialty automotive:** the founder's real edge, but thin inside the target towns (XPEL's directory lists Chicago and Naperville installers; Chicago Auto Pros has a Hinsdale location) and the SERP is owned by national detailing-marketing agencies. Revisit as an extension of `/car-club-websites/`.
- **Galleries:** almost none in the target towns.

---

## Phase 2: niche pages

| Slug | H1 | Concept |
|---|---|---|
| `/med-spa-websites/` | Med spa website design | Solenne Aesthetics (Hinsdale) |
| `/custom-home-builder-websites/` | Custom home builder website design | Corbel & Lane Builders (Clarendon Hills) |
| `/interior-designer-websites/` | Interior designer website design | Harrow & Finch Interiors (Western Springs) |
| `/landscape-design-websites/` | Landscape design website design | Wexmoor Landscape Studio (Burr Ridge) |

Slug style matches `boutique-websites` / `car-club-websites`: `[industry]-websites`.

Each page, in order:

1. `.page-hero`: H1 + `.lede` whose first two sentences follow the pattern "Elimenti designs custom websites for [industry] in Hinsdale, Oak Brook and the western suburbs of Chicago. [Who/what]."
2. `What a [industry] website needs to do` (industry-specific list).
3. `The concept` with a `.shots` pair (desktop + phone WebP) captioned "Concept, not a client project." and a link to the live concept.
4. One honest section on real work (or the lack of it): name the relevant case study and say exactly what it was. Never imply prior work in the industry.
5. `Pricing`: "Projects start at $3,000. Most land between $3,500 and $4,500. Every project is scoped individually. Ongoing care is on retainer or hourly."
6. `Questions [industry] owners ask` as `.faq-list` (h3 inside the page, since the page has an H1 and section H2s) with 5–7 Q&As, 40–80 words, first sentence answers outright.
7. `Where we work` linking `/hinsdale-web-design/` and `/glen-ellyn-web-design/` and naming the other towns, then CTA to `/contact/`.
8. Breadcrumb Home / [Industry] websites.

JSON-LD block 2: `Service` (`#service`, with `offers.priceSpecification.minPrice 3000`), `FAQPage` (text identical to the visible copy), `BreadcrumbList`.

Length target 500–900 words of body copy.

**Pricing note (judgment call):** the brief's facts say "ongoing care on retainer or hourly." The live site prices Site Care at $175/month and $85/hour. I keep the existing numbers where Site Care is mentioned because they're already public on the homepage and FAQ, and the brief doesn't say they changed.

**Existing CTA pattern:** existing niche pages link the button to `/#contact`. The brief asks for `/contact/`, so new pages use `/contact/`.

## Phase 3: concept sites

Each lives at `/concepts/[industry]/` with a homepage and two interior pages, its own stylesheet (`/concepts/[industry]/style.css`), its own type and palette (it's the client's brand, not Elimenti's), and a shared banner stylesheet `/concepts/concept.css` for the "Concept by Elimenti, fictional business" strip on every page.

| Concept | Pages |
|---|---|
| `/concepts/med-spa/` Solenne Aesthetics | Home, Treatments, Book |
| `/concepts/custom-home-builder/` Corbel & Lane Builders | Home, Homes, Process |
| `/concepts/interior-designer/` Harrow & Finch Interiors | Home, Projects, Inquire |
| `/concepts/landscape-design/` Wexmoor Landscape Studio | Home, Work, Approach |

Rules: `<meta name="robots" content="noindex, follow">`, canonical omitted (noindex pages shouldn't point canonicals at themselves for indexing), not in sitemap, no fake reviews, testimonials, awards, stats or results (no before/after photos: the med spa gallery is shown as a consent-gated frame, not invented results), phone numbers in the reserved fictional 555-01xx range, no street numbers, forms that don't submit anywhere real (`action` points to the niche page with a note). Photos: Unsplash License (free for commercial use), credited in each concept footer.

**Name checks (searched; no Illinois business found under these names):** "Solenne Aesthetics" (closest: SOLUX Med Spa, Chicago; Solana Aesthetics, Lemont), "Harrow & Finch" (none; closest Marlow & Finch, Australia), "Corbel & Lane" (none; closest Corbel Construction Ltd, UK), "Wexmoor" (none in Illinois).

## Phase 4: guide

`/guides/website-cost-western-suburbs/`: "What a custom website costs in the western suburbs." Sections: the short answer, the four ways to get a site (DIY builder, theme-based WordPress, freelancer/agency custom, custom-coded studio) with what each costs and what you give up, what drives cost, timelines, ongoing costs, questions to ask any designer, Elimenti's numbers. `Article` JSON-LD + Breadcrumb. Market figures cite sources on the page:

- Squarespace plans: [squarespace.com/pricing](https://www.squarespace.com/pricing) (Basic $19 to Advanced $99 a month billed annually, checked 2026-10-25)
- Wix plans: [wix.com/plans](https://www.wix.com/plans) (Light about $17 a month billed yearly; prices vary by location)
- Agency quotes: [Shopify, "How much does a website cost?" (Sep 2026)](https://www.shopify.com/blog/how-much-does-a-website-cost) ("Most (63%) agencies quoted between $1,000 and $15,000")
- Platform share: [Clutch 2025 survey via Business Wire](https://www.businesswire.com/news/home/20250821848152/en/Clutch-Report-No-Code-Tools-Fuel-Website-Growth-Yet-17-of-Small-Businesses-are-Still-Offline) (DIY builders power 41% of small business sites, 34% WordPress or Shopify)

No breadcrumb level for `/guides/` because there's no guides index; a breadcrumb link to a 404 would be worse.

## Phase 5: wiring

- Footer nav (every page, including 404 and thanks): add the four niche pages and "Website cost guide" after "Car club websites". Main nav stays Work / About / FAQ.
- Homepage: a "Websites by industry" line under the services grid's statement section linking all six niche pages, and a link to the cost guide next to "Questions about cost?".
- FAQ: link the cost guide from the first answer's section (visible text and JSON-LD stay identical).
- Case studies: ABN → builder page; Burdi → nothing new (boutique already); Hinsdale page → builder/landscape/interior links in "What we build for Hinsdale businesses".
- `sitemap.xml`: add 5 URLs, bump lastmod on edited pages.

## Verification plan

Local server that mimics GitHub Pages (directory → `index.html`, `/dir` → 301 `/dir/`, unknown → `404.html` with status 404, `.md` not served). Then: status codes for every URL, one H1 each, unique titles (≤60) and descriptions (≤155), canonical correct, lede present in raw HTML, all JSON-LD parses, FAQPage text equals visible text, concept pages noindex and absent from sitemap, sitemap equals the set of indexable pages, no broken internal links, Playwright before/after screenshots of every pre-existing page at 1440 and 390 wide with pixel diff, Lighthouse on home, one niche page, the guide and one concept page (fix anything under 95), banned-phrase grep.
