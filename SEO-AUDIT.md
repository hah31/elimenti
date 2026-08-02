# Elimenti — Full SEO Audit

**Date:** 2026-08-02
**Repo state audited:** commit `7139d48`, branch `claude/elimenti-seo-audit-r40jff`
**Method:** every file in the repo was opened and read. Claims below cite file and line. Nothing is inferred from a filename.

**Total repo contents — this is the entire site:**

```
CNAME                     12 B
index.html             5,843 B
portfolio.html        18,766 B
assets/css/style.css  13,947 B
assets/js/main.js      2,852 B
assets/img/logo.png  231,146 B   (1080 x 1080 PNG)
```

Six files. Two HTML pages. One image.

---

## What I could NOT verify (and how you check it yourself)

This sandbox's network policy blocks outbound connections to `elimenti.com` at the gateway (confirmed: `connect_rejected — gateway answered 403 to CONNECT, host www.elimenti.com:443`). I could not fetch the live site. I am **not** guessing at any of the following — verify them manually:

| Unknown | Command to run locally |
|---|---|
| Does `www` → apex redirect, or apex → `www`? | `curl -sSI https://elimenti.com/ \| head -20` then the same for `https://www.elimenti.com/` |
| Does a bad URL return a real `404` status? | `curl -sS -o /dev/null -w "%{http_code}\n" https://www.elimenti.com/no-such-page` |
| Live response/cache headers | `curl -sSI https://www.elimenti.com/assets/css/style.css` |
| Trailing-slash behavior | `curl -sSI https://www.elimenti.com/portfolio` (does it 200, 301, or 404?) |
| Core Web Vitals **field** data | PageSpeed Insights → look for "Discover what your real users are experiencing". If absent, you have no field data yet (likely — traffic is too low) |
| Whether GSC is verified | See §6.3 |

Everything else in this document was read directly out of the repo.

---

## 1. Page Inventory — actual current state

| # | File | `<title>` | len | Meta description | len | `<h1>` | Body words |
|---|---|---|---|---|---|---|---|
| 1 | `index.html` | `Elimenti — Premium Web Design` | **29** | `Elimenti designs websites for high-end businesses that compete on quality.` | **74** | `Built for businesses that compete on quality.` | **182** |
| 2 | `portfolio.html` | `Our Work — Elimenti` | **19** | `Selected projects by Elimenti — premium web design for businesses that compete on quality.` | **90** | `Our Work` | **104** |

**Total indexable words on the entire site: 286.**

### Heading hierarchy (verified by parsing the DOM order)

**`index.html`** — hierarchy is clean, no skipped levels:
```
h1  Built for businesses that compete on quality.
h2  Services
  h3  Web Design
  h3  Visual Identity
  h3  Site Care
h2  Process
  h3  Discover
  h3  Design
  h3  Build
  h3  Launch
h2  What to Expect
h2  Let's build something.
```

**`portfolio.html`** — only two headings on the whole page:
```
h1  Our Work
h2  Let's build something.
```
The four project names are `<span class="card__name">` (lines 309, 325, 341, 357), **not headings**. See HIGH-4.

### Images

There is exactly **one** `<img>` element in the entire site:

- `index.html:45` — `<img src="assets/img/logo.png" alt="Elimenti logo mark">`

`alt` is present and descriptive. No missing-alt problems. No decorative images needing `alt=""`. The four portfolio "images" are actually live `<iframe>` embeds of third-party websites (see HIGH-1).

### Internal link graph

| From | To | Anchor text |
|---|---|---|
| `index.html:33` | `portfolio.html` | "Work" |
| `index.html:31` | `#` | "ELIMENTI" — **dead link, goes nowhere** |
| `portfolio.html:282` | `index.html` | "ELIMENTI" |
| `portfolio.html:286` | `index.html#contact` | "Start a Project" |
| `main.js:58-62` (JS-injected mobile menu) | `portfolio.html`, `#services`, `#process`, `#expect`, `#contact` | descriptive |

**One** crawlable HTML link from home → portfolio, with anchor text "Work". No orphan pages (both pages are reachable), but the link graph is as thin as a two-page site can be. Outbound: 4 external links to client sites, `rel="noopener"`, no `nofollow` — **this is correct, leave it**. Linking to real client work is a legitimate signal, not something to suppress.

---

## CRITICAL

### CRIT-1 — The site contains no geographic signal whatsoever. It cannot rank for a single one of your target keywords.

**Files:** `index.html` (entire file), `portfolio.html` (entire file)

I grepped every file in the repo for `hinsdale|oak brook|naperville|downers|dupage|chicago|illinois|IL|clarendon|western springs|burr ridge`. **One** match exists in the entire codebase:

- `portfolio.html:326` — *"Ongoing site care and content edits for a Chicagoland general contractor."*

That is it. One incidental use of "Chicagoland" buried in a card description on your second page.

Your stated targets are `web design Hinsdale`, `web designer DuPage County`, `custom website design Oak Brook`. The word "Hinsdale" does not appear on your website. Neither does "Oak Brook," "DuPage," "Naperville," or "Downers Grove."

**Why it matters:** this is not a ranking-factor subtlety. A page cannot be returned as relevant for a query whose subject it never mentions. Every other item in this audit is downstream of this one. You could fix all 24 other findings and still rank for nothing local, because there is no local entity on the site to match against.

**The fix** is not to stuff town names into the existing copy. It is to (a) put a geo modifier in the homepage title and meta description, (b) add one honest sentence of location context to the homepage body, and (c) build the service-area and case-study pages in §5. Concrete copy is proposed in §5 — **and I am not changing your copy tone without you approving the wording first.**

---

### CRIT-2 — `og:image` and `twitter:image` are relative paths. Every social share of this site renders with no image.

**Files & lines:**
- `index.html:13` — `<meta property="og:image" content="assets/img/logo.png">`
- `index.html:18` — `<meta name="twitter:image" content="assets/img/logo.png">`
- `portfolio.html:13` — `<meta property="og:image" content="assets/img/logo.png">`
- `portfolio.html:18` — `<meta name="twitter:image" content="assets/img/logo.png">`

**Why it matters:** the Open Graph spec requires an absolute URL. Facebook, LinkedIn, iMessage, Slack, and X do not resolve relative paths against the page URL — they discard the value. Right now, every time anyone shares elimenti.com — including *you*, in a sales email or a DM to a prospect — it renders as a bare text link with no card. For a design agency, a link preview that renders as naked text is an active credibility cost. This is the highest-visibility broken thing on the site.

**Also broken in the same block:**
1. **`og:url` is entirely absent** from both pages. Verified — zero matches for `og:url` in the repo.
2. **The image is the wrong asset and the wrong shape.** `logo.png` is 1080×1080 (verified from the PNG header) and 231 KB. OG cards render at 1.91:1 — a square logo gets center-cropped to a letterboxed sliver of your mark on a transparent background, which most clients composite onto white. Your gold-on-dark mark will likely render as gold-on-white or gold-on-transparent-garbage.

**Exact fix** — replace lines 10–18 in `index.html` with:

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Elimenti">
<meta property="og:url" content="https://www.elimenti.com/">
<meta property="og:title" content="Elimenti — Premium Web Design">
<meta property="og:description" content="Elimenti designs websites for high-end businesses that compete on quality.">
<meta property="og:image" content="https://www.elimenti.com/assets/img/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Elimenti — premium web design">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Elimenti — Premium Web Design">
<meta name="twitter:description" content="Elimenti designs websites for high-end businesses that compete on quality.">
<meta name="twitter:image" content="https://www.elimenti.com/assets/img/og-card.png">
```

Same for `portfolio.html` with `og:url` = `https://www.elimenti.com/portfolio.html` and its own title/description.

**Note the dependency:** `assets/img/og-card.png` does not exist yet. It needs to be designed — 1200×630, dark background matching `--color-bg: #0c0c0b`, wordmark + one line of positioning, exported under 300 KB. That is a design task, not a code task. **Until that file exists, pointing `og:image` at it would be worse than the current state** (a 404 instead of a discarded relative path). So: either you make the card and I wire it up, or I wire it to the absolute URL of the existing logo as a stopgap — `https://www.elimenti.com/assets/img/logo.png` — which at least produces *a* card. Tell me which; I'd do the stopgap now and the designed card this week.

---

### CRIT-3 — No `robots.txt`, no `sitemap.xml`.

**Verified absent.** Neither file exists at the repo root.

**Why it matters:** honestly, for a 2-page site, the sitemap's crawl-discovery value is near zero — Google will find two pages linked from the root without help. Do not let anyone tell you a sitemap is what's holding this site back. The reason to add both is different and specific:

1. **Search Console requires a sitemap** to give you the Sitemaps report and per-URL indexing feedback. That feedback loop is the actual payoff.
2. **A sitemap becomes load-bearing the moment §5 happens.** When you go from 2 pages to 8, you want new URLs discovered the day they ship.
3. **`robots.txt` should exist** so the `Sitemap:` directive has a home, and so you're not serving a 404 to every crawler that asks for it.

**Fix — create `/robots.txt`:**

```
User-agent: *
Allow: /

Sitemap: https://www.elimenti.com/sitemap.xml
```

Do **not** add `Disallow` rules. There is nothing on this site to hide, and every `Disallow` line is a chance to accidentally deindex yourself.

**Fix — create `/sitemap.xml`** (both real pages, no others — do not list URLs that don't exist):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.elimenti.com/</loc>
    <lastmod>2026-08-02</lastmod>
  </url>
  <url>
    <loc>https://www.elimenti.com/portfolio.html</loc>
    <lastmod>2026-08-02</lastmod>
  </url>
</urlset>
```

I've deliberately omitted `<priority>` and `<changefreq>`. Google has publicly stated it ignores both. Including them is cargo cult.

---

### CRIT-4 — No canonical tags on either page, and the repo disagrees with you about which domain is canonical.

**Verified:** zero matches for `canonical` in the repo.

**The domain conflict:** `CNAME` (line 1) contains:
```
elimenti.com
```
That is the **non-www apex**. You described the site to me as `https://www.elimenti.com`. These are two different canonical hosts and something has to give.

Also worth noting: a root `CNAME` file is a **GitHub Pages** convention. Cloudflare Pages ignores it entirely — it would just be served as a downloadable text file at `/CNAME`. Combined with `git log` showing `Delete wrangler.jsonc` (commit `830c18a`) followed later by `Create CNAME` (commit `269b7ca`), I can't tell from the repo alone which host is actually serving traffic today. **This is the one thing I need you to confirm before I write canonicals**, because a canonical pointing at the wrong host is worse than no canonical at all — it tells Google to index a URL you don't serve.

**Why canonicals matter here:** Cloudflare Pages serves your site on `*.pages.dev` **as well as** your custom domain, and both are crawlable unless you tell Google otherwise. Right now `elimenti.pages.dev` (or whatever your project subdomain is) can be indexed as a full duplicate of your site. A self-referencing canonical on every page collapses that duplication to one URL.

**Fix — add to `<head>` of each page, after the `<title>`:**

```html
<!-- index.html -->
<link rel="canonical" href="https://www.elimenti.com/">

<!-- portfolio.html -->
<link rel="canonical" href="https://www.elimenti.com/portfolio.html">
```

**And add a `_redirects` file** at the repo root to force one host. Cloudflare Pages reads this. Assuming `www` wins:

```
https://elimenti.com/*  https://www.elimenti.com/:splat  301
```

Cloudflare Pages does **not** automatically redirect apex→www or vice versa when both are attached to the project. If you have both hostnames on the project and no redirect, you are currently serving the entire site on two hosts with no canonical — the textbook duplicate-content setup.

---

## HIGH

### HIGH-1 — `portfolio.html` loads four complete third-party websites in iframes. This is the worst performance decision on the site, and it puts zero crawlable content on the page.

**File:** `portfolio.html:305, 321, 337, 353`

```html
<iframe src="https://1of1carclub.pages.dev" ... loading="lazy" ...></iframe>
<iframe src="https://abnconstruction.com/" ... loading="lazy" ...></iframe>
<iframe src="https://burdiclothing.com/" ... loading="lazy" ...></iframe>
<iframe src="https://aamineez.art" ... loading="lazy" ...></iframe>
```

**Why it matters — four separate problems:**

1. **Loading your portfolio page loads four entire other websites.** Every stylesheet, font, script, and image on each client site. One of them (`abnconstruction.com`) is a WordPress/Elementor build — those routinely ship 2–4 MB. You have no control over any of this, and it can change without warning when a client edits their site. Your portfolio page's weight is effectively unbounded.

2. **It's fragile by design, and your own code admits it.** `portfolio.html:376-382` contains a comment explaining the `X-Frame-Options` / `frame-ancestors` detection hack, and lines 383-418 implement a `try/catch` on `contentDocument` plus an 8-second timeout fallback. You wrote a fallback because you already know these embeds break. Any client who adds `X-Frame-Options: DENY` — which is standard hardening, and which many WordPress security plugins enable by default — silently turns their card into a text placeholder.

3. **It contributes nothing to SEO.** Iframe content is attributed to the framed origin, never to the framing page. Google indexes zero words from these embeds. Your portfolio page's crawlable text is 104 words, and the iframes add none of it.

4. **`loading="lazy"` is on all four, including the top two**, which are above the fold on a desktop viewport (grid is `repeat(2, 1fr)`, `portfolio.html:74`). Lazy-loading an above-fold element delays it. Minor next to problems 1–3, but it's there.

**The fix:** replace the iframes with static screenshots — WebP, ~1040×650 (2× the 520px column), with explicit `width`/`height`, `loading="lazy"` on cards 3–4 only, and `alt` text naming the client and the work. This deletes ~120 lines of CSS and ~45 lines of JS, makes the page 10× faster, and removes the entire failure mode.

**This changes how the cards look** (a static shot rather than a live render). It's a visual change, so I'm not doing it without you saying yes. If you want to keep the live-preview effect, the compromise is: screenshot by default, and keep the "Visit Site →" link — which you already have.

---

### HIGH-2 — `portfolio.html`'s `<h1>` starts at `opacity: 0` in the served HTML, delaying Largest Contentful Paint until JavaScript executes.

**Files:** `portfolio.html:289` + `assets/css/style.css:474-480`

```html
<section class="portfolio-hero fade-in">   <!-- line 289 -->
```
```css
.fade-in {                                  /* style.css:474 */
    opacity: 0;
    transform: translateY(var(--reveal-translate));
    ...
}
```

The `fade-in` class is **hardcoded into the HTML** on `portfolio.html` (lines 289, 299, 315, 331, 347, 366, 367, 368). So the browser receives a page whose above-fold hero — including the `<h1>` — is `opacity: 0`. It only becomes visible after the inline script at line 371 parses, constructs an `IntersectionObserver` (line 425), and fires a callback.

**An element at `opacity: 0` is not painted, and does not count for LCP.** Your LCP on this page is therefore gated on JS parse + execute + observer callback, rather than on first paint.

**Note the contrast:** `index.html` does **not** have this problem. There, `fade-in` is added *by* JavaScript (`main.js:21` — `fadeTargets.forEach(el => el.classList.add('fade-in'))`), so the hero paints immediately in the initial HTML and only then gets the animation class. The homepage is fine. Only the portfolio page has the hardcoded-hidden hero.

(Side effect on `index.html`: because JS *adds* the hidden class after paint, there's a potential flash-of-visible-then-hidden on the hero. Cosmetic, not an SEO issue — flagging it as a thing you may or may not be seeing.)

**Fix:** remove `fade-in` from `portfolio.html:289` only — the above-fold hero. Leave it on the cards and contact section below the fold. One-word change, no visual difference below the fold, and the hero simply appears immediately instead of fading.

**This alters the entrance animation on that one element,** so per your instruction I'm asking before touching it.

---

### HIGH-3 — Titles and meta descriptions contain no keywords, no geography, and waste 60–70% of available pixels.

**Files:** `index.html:7-8`, `portfolio.html:7-8`

| Page | Current | Length | Problem |
|---|---|---|---|
| index | `Elimenti — Premium Web Design` | 29 | Uses 29 of ~60 usable chars. No geo. Leads with a brand nobody is searching for. |
| portfolio | `Our Work — Elimenti` | 19 | Uses 19 of ~60. "Our Work" is not a query any human types. |

**Why it matters:** your brand name has no search volume — nobody types "Elimenti." Leading with it spends your most valuable ranking real estate on a term you already win by default. Meanwhile "web design" appears once and "Hinsdale"/"DuPage" appear zero times.

The `portfolio.html` title is the weaker of the two. "Our Work" describes the page's *position in your nav*, not its *content*. The content is a web design portfolio for Chicago-area businesses.

**Proposed replacements** — these are close to your existing voice, but they *are* copy, so approve them before I write them in:

```html
<!-- index.html:7-8 -->
<title>Premium Web Design in Hinsdale & DuPage County | Elimenti</title>
<meta name="description" content="Custom websites for high-end businesses in Hinsdale, Oak Brook, Naperville and Downers Grove. No templates — every site designed from scratch. Start a project.">

<!-- portfolio.html:7-8 -->
<title>Web Design Portfolio — Chicago-Area Client Work | Elimenti</title>
<meta name="description" content="Selected websites designed and built by Elimenti for automotive, construction, apparel and arts businesses across DuPage County and Chicagoland. See the work.">
```

Both descriptions land at 155–160 chars, lead with the offer, name the towns, and end with a CTA — which the current ones don't (they're descriptive statements, not ad copy). Meta descriptions aren't a ranking factor, but they are the ad. Yours currently read like an About paragraph.

---

### HIGH-4 — Portfolio project names are `<span>`s, not headings. The page has no content structure.

**File:** `portfolio.html:309, 325, 341, 357` (and the fallback names at 302, 318, 334, 350)

```html
<span class="card__name">1 of 1 Car Club</span>
```

`portfolio.html` has exactly two headings on the entire page: the `h1` and one `h2`. The four client names — the actual content of the page, and the only proper nouns on it — are semantically invisible.

**The good news: this is a free fix with zero visual change.** I checked the CSS specificity. Global `h3` styling (`style.css:142-145`) sets `font-size`, `letter-spacing: -0.01em`. `.card__name` (`portfolio.html:208-218`) sets `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing: var(--track-display)`, `color`, `display: block`, `margin-bottom`. A class selector (0,1,0) beats a type selector (0,0,1) on every overlapping property. **Changing `<span class="card__name">` to `<h3 class="card__name">` renders pixel-identically.**

**Fix:** `span` → `h3` on lines 309, 325, 341, 357 only. Leave the `.card__fallback-name` spans alone (they're duplicate text inside the preview area — promoting those would create duplicate headings).

---

### HIGH-5 — Both pages are far below any reasonable content threshold. 286 words total.

**Files:** `index.html` (182 words), `portfolio.html` (104 words)

There is no magic word count, and I'm not going to tell you to pad pages to hit 300. But 104 words on a portfolio page is not a thin-content *risk* — it's an absence of content. There is nothing on that page for Google to understand except four client names and a tagline.

**Specifically what each page needs:**

- **`index.html` (182 → ~600):** the "What to Expect" section (lines 89-94) is three sentences and one of them repeats the other ("Every engagement is scoped to the project" at line 93 restates "Scoped to your project" at line 92 — that's a genuine copy duplication bug, not just an SEO note). The Services cards (lines 52-63) are one sentence each. Each service needs 2–3 sentences describing what's actually delivered. Add one short section establishing where you work and who you work with.

- **`portfolio.html` (104 → ~400):** each card's `<p class="card__desc">` is a single sentence. Two of them ("An exquisite calligraphy portfolio page." line 358; "A digital flagship for a Porsche-exclusive car club." line 310) say nothing about what you actually did. Each needs 2–3 sentences: what the client needed, what you built, what changed. This also feeds directly into the case-study pages in §5.

---

## MEDIUM

### MED-1 — No structured data anywhere. See §3 for ready-to-paste blocks.
Verified: zero matches for `ld+json` or `schema.org` in the repo.

### MED-2 — `index.html:31` — the wordmark links to `#`, which is a dead link.

```html
<a href="#" class="nav__wordmark">ELIMENTI</a>
```

`portfolio.html:282` correctly uses `href="index.html"`. The homepage version points at `#`, which jumps to the top of the page and appends a bare `#` to the URL. **Fix:** change to `href="/"`. One character of value, but it's a broken link in your primary nav.

### MED-3 — No `404.html`.

**Verified absent.** Cloudflare Pages will serve its own default 404 page with a correct `404` status code, so this is **not** a soft-404 problem and won't hurt indexing. The cost is purely brand: a visitor who mistypes a URL lands on a generic Cloudflare page with no way back to your site.

**Fix:** create `404.html` reusing your existing nav + a short message + a link home. Low effort, low SEO value, real brand value for a design agency. Cloudflare Pages picks it up automatically with no config.

### MED-4 — Favicon is a 231 KB, 1080×1080 PNG. There's no apple-touch-icon.

**File:** `index.html:20`, `portfolio.html:20`
```html
<link rel="icon" type="image/png" href="assets/img/logo.png">
```

Every visitor downloads **231 KB** to render a 16×16 tab icon. That single file is larger than all your HTML, CSS, and JS combined (41 KB). It's also the hero image (`index.html:45`), so it's not a wasted request — but it *is* a wasted 231 KB, because a 360px-wide hero display does not need a 1080px source, and a favicon needs 32px.

**Verified absent:** `favicon.ico`, `apple-touch-icon.png`, `site.webmanifest`.

**Fix:** generate from the existing logo — `favicon-32.png` (32×32), `apple-touch-icon.png` (180×180), and a `logo-720.webp` for the hero. Then:
```html
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
```
Expected saving: ~200 KB per page load, which on a mobile connection is most of your load time.

### MED-5 — The hero image has no `width`/`height`, causing layout shift.

**File:** `index.html:45`
```html
<img src="assets/img/logo.png" alt="Elimenti logo mark">
```

`style.css:80` sets `height: auto` and `style.css:317-320` sets `width: 100%; max-width: 360px`. With no intrinsic dimensions in the HTML, the browser cannot reserve space before the 231 KB PNG downloads — the layout reflows when it lands. That's Cumulative Layout Shift.

**Fix:** add `width="1080" height="1080"`. The CSS `max-width`/`height: auto` still control rendered size; the attributes only supply the aspect ratio for space reservation. **No visual change.**

Also add `fetchpriority="high"` — this is the LCP candidate on mobile (`style.css:600` sets `order: -1`, putting the image above the headline). And confirmed: it correctly does **not** have `loading="lazy"`. That's right, don't add it.

### MED-6 — No `_headers` file; static assets get no long-lived cache.

**Verified absent.** Your CSS and JS filenames are unhashed (`style.css`, `main.js`), so Cloudflare Pages serves them with a short/revalidating cache by default. Every repeat visitor re-validates.

**Fix — create `/_headers`:**

```
/assets/*
  Cache-Control: public, max-age=31536000, immutable

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

**One caveat you must understand before shipping this:** `immutable` + 1-year on unhashed filenames means when you edit `style.css`, returning visitors keep the old file for up to a year. If you adopt this, you must either add a query string (`style.css?v=2`) or rename the file on every CSS change. If that discipline sounds like a trap, use `max-age=86400` instead — a day of caching, no footgun. **For a site you edit weekly, I'd recommend the 86400 version.** I'd rather tell you that than hand you a config that silently breaks your next deploy.

I've deliberately omitted CSP and HSTS headers. They're good practice but they're security, not SEO, and a misconfigured CSP would break your Google Fonts. Out of scope here.

### MED-7 — Google Fonts loads 10 weights; the CSS uses 4.

**File:** `index.html:24`, `portfolio.html:24`
```
family=Cormorant+Garamond:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700
```

That's 5 weights × 2 families = 10 font files. I grepped the CSS: `--weight-semibold: 600` (`style.css:20`) and `--weight-bold: 700` (`style.css:21`) are **declared but never referenced anywhere**. The only weights actually used are 300, 400, 500.

**Fix:** change both `<link>` tags to `:wght@300;400;500`. Drops 4 font files. **No visual change** — you can't lose a weight you never used.

What's already correct, and should be left alone: `display=swap` is present (line 24), and both `preconnect` hints are present and correctly formed, including `crossorigin` on the `gstatic` one (lines 22-23). That's the right setup. **Self-hosting the fonts would shave another ~100 ms** by removing a third-party connection entirely, but it's a bigger change and the current setup is not broken — I'd put it well below everything else on this list.

### MED-8 — CTA behavior is inconsistent between pages.

- `index.html:35` nav CTA → `mailto:` with a long pre-filled body
- `portfolio.html:286` nav CTA → `index.html#contact`
- `index.html:98` contact CTA → `mailto:` with pre-filled body
- `portfolio.html:367` contact CTA → bare `mailto:hello@elimenti.com`, **no pre-filled subject or body**

Four CTAs, three different behaviors. The portfolio page's contact CTA drops the pre-filled draft that you clearly put effort into building on the homepage. See §6 for the broader mailto question.

---

## LOW

### LOW-1 — `portfolio.html` carries 250 lines of inline `<style>` (lines 28-277).

This duplicates what would normally live in `style.css`. I want to be straight with you: **inline critical CSS is faster, not slower** — it avoids a render-blocking round trip. This is a maintainability issue, not a performance or SEO one. If someone tells you to move it to the stylesheet "for SEO," they're wrong. Leave it unless it starts costing you edit time.

### LOW-2 — Dead CSS rule.

`style.css:300-304` styles `.hero__text h1 em`. There is no `<em>` element anywhere in either HTML file (verified). Five dead lines. Also `--weight-semibold` and `--weight-bold` (lines 20-21) are unreferenced.

**This is trivia.** Total unused CSS here is well under 1 KB in a 14 KB file that gzips to ~3 KB. "Remove unused CSS" is a Lighthouse checkbox that does nothing for you at this scale. I'm listing it for completeness, not because you should spend time on it.

### LOW-3 — Copy duplication in "What to Expect."

`index.html:92` — "Scoped to your project. We don't sell packages..."
`index.html:93` — "Every engagement is scoped to the project — get in touch..."

Two consecutive paragraphs make the same point. Reads like an editing artifact. Copy change — your call.

### LOW-4 — `CNAME` is a GitHub Pages file sitting in a Cloudflare Pages repo.

If you're fully on Cloudflare Pages, this file does nothing except get served as a public text file at `/CNAME`. Harmless, but it's also the thing creating the www/apex ambiguity in CRIT-4. Worth resolving one way or the other.

---

## 3. Structured Data — ready to paste

Before the blocks, an honest ranking of what these are actually worth, because they are not equal:

| Schema | Real-world value | Verdict |
|---|---|---|
| `ProfessionalService` / `LocalBusiness` | Moderate. Helps Google resolve you as a business entity, feeds local understanding. | **Worth it.** |
| `Organization` | Moderate. `logo` can feed a knowledge panel. | **Worth it** — merge into the block above. |
| `WebSite` + `SearchAction` | **Near zero.** Google retired the sitelinks search box in late 2024, which was this schema's only rich result. | Included below since you asked, minus the dead `SearchAction`. |
| `BreadcrumbList` | Low now, real later. Breadcrumbs *do* render in SERPs, but `Home > Work` on a flat 2-page site is marginal. Becomes genuinely useful once case-study pages exist. | **Add it** — it's free and forward-compatible. |
| `Service` | **Effectively zero.** `Service` has no associated rich result in Google Search. It won't change how you appear in SERPs at all. | Included because you asked. Do it last. |

**Nothing here will move your rankings by itself.** Structured data is an eligibility mechanism for SERP features, not a ranking factor. It is worth 20 minutes; it is not worth 3 hours.

**⚠️ Placeholders you must fill before shipping:** I have used `REPLACE_ME` markers below. **Do not invent a street address.** If you don't have a public commercial address, omit `address` entirely — `areaServed` is enough for a service-area business, and a fabricated address is a real liability if you ever claim a Google Business Profile.

### Block A — Organization + ProfessionalService (combined)

**Where:** `index.html`, immediately before `</head>` (i.e. before line 27).

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["Organization", "ProfessionalService"],
      "@id": "https://www.elimenti.com/#organization",
      "name": "Elimenti",
      "url": "https://www.elimenti.com/",
      "email": "hello@elimenti.com",
      "description": "Elimenti designs and builds custom websites for high-end businesses in Hinsdale, Oak Brook, Naperville, Downers Grove and the greater Chicago area.",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.elimenti.com/assets/img/logo.png",
        "width": 1080,
        "height": 1080
      },
      "image": "https://www.elimenti.com/assets/img/logo.png",
      "priceRange": "$$$",
      "areaServed": [
        { "@type": "AdministrativeArea", "name": "DuPage County, Illinois" },
        { "@type": "City", "name": "Hinsdale, Illinois" },
        { "@type": "City", "name": "Oak Brook, Illinois" },
        { "@type": "City", "name": "Naperville, Illinois" },
        { "@type": "City", "name": "Downers Grove, Illinois" },
        { "@type": "City", "name": "Chicago, Illinois" }
      ],
      "knowsAbout": [
        "Web Design",
        "Web Development",
        "Visual Identity",
        "Brand Design",
        "Website Maintenance"
      ],
      "sameAs": [
        "REPLACE_ME_INSTAGRAM_URL",
        "REPLACE_ME_LINKEDIN_URL"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.elimenti.com/#website",
      "url": "https://www.elimenti.com/",
      "name": "Elimenti",
      "publisher": { "@id": "https://www.elimenti.com/#organization" },
      "inLanguage": "en-US"
    }
  ]
}
</script>
```

**Before shipping:** replace the two `sameAs` entries with your real profile URLs, **or delete the `sameAs` array entirely**. An array of placeholder strings is worse than no array. `priceRange: "$$$"` is a positioning claim — adjust or remove it if you'd rather not signal a tier.

### Block B — BreadcrumbList

**Where:** `portfolio.html`, immediately before `</head>` (before line 278, after the closing `</style>`).

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.elimenti.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Work",
      "item": "https://www.elimenti.com/portfolio.html"
    }
  ]
}
</script>
```

### Block C — Services

**Where:** `index.html`, immediately before `</head>`, after Block A.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "name": "Web Design",
      "serviceType": "Custom Website Design",
      "provider": { "@id": "https://www.elimenti.com/#organization" },
      "description": "A site that reflects the standard of your business. Designed from scratch, built to last.",
      "areaServed": { "@type": "AdministrativeArea", "name": "DuPage County, Illinois" }
    },
    {
      "@type": "Service",
      "name": "Visual Identity",
      "serviceType": "Brand Identity Design",
      "provider": { "@id": "https://www.elimenti.com/#organization" },
      "description": "Marks, type, and color systems for brands that want to be remembered.",
      "areaServed": { "@type": "AdministrativeArea", "name": "DuPage County, Illinois" }
    },
    {
      "@type": "Service",
      "name": "Site Care",
      "serviceType": "Website Maintenance and Support",
      "provider": { "@id": "https://www.elimenti.com/#organization" },
      "description": "Ongoing updates, performance, and support. Your site stays current so you don't have to think about it.",
      "areaServed": { "@type": "AdministrativeArea", "name": "DuPage County, Illinois" }
    }
  ]
}
</script>
```

**Syntax validation:** all three blocks were parsed with a strict JSON parser and are valid JSON. The `@id` cross-references between Block C's `provider` and Block A's `#organization` node resolve correctly. **Validate the rendered pages** at https://validator.schema.org/ and https://search.google.com/test/rich-results after deploying — a syntax check here can't catch a typo introduced during paste.

---

## 4. Performance

**Repo-side facts (verified):**

| Asset | Size | Notes |
|---|---|---|
| `assets/img/logo.png` | **231,146 B** | 1080×1080 PNG, RGBA. Displayed at max 360px desktop / 200px mobile. **~9× oversized.** Also serving as the favicon. |
| `portfolio.html` | 18,766 B | includes 250 lines inline CSS |
| `assets/css/style.css` | 13,947 B | |
| `index.html` | 5,843 B | |
| `assets/js/main.js` | 2,852 B | |

**The single image is 85% of your site's total byte weight**, and it isn't even displayed at a size that needs it. Converting to WebP at 720px wide should land around 25–35 KB — roughly a **200 KB saving**, or about 87% of the file.

**Summary of performance findings** (details in the sections above):

| Finding | Where | Section |
|---|---|---|
| 4 third-party sites loaded in iframes | `portfolio.html:305,321,337,353` | HIGH-1 |
| Above-fold `h1` hidden at `opacity:0` pre-JS | `portfolio.html:289` | HIGH-2 |
| 231 KB PNG for a 360px slot + 32px favicon | `index.html:20,45` | MED-4 |
| No `width`/`height` → CLS | `index.html:45` | MED-5 |
| No `_headers` / no asset caching | root | MED-6 |
| 10 font weights loaded, 4 used | `index.html:24` | MED-7 |
| Unused CSS | `style.css:300` | LOW-2 (ignorable) |

**Render-blocking analysis:**
- `style.css` — render-blocking, but it's 14 KB and it's your only stylesheet. Correct as-is.
- Google Fonts stylesheet (line 24) — render-blocking third-party request. `preconnect` + `display=swap` are both correctly configured, which is the right mitigation short of self-hosting.
- `main.js` (`index.html:102`) — loaded at end of `<body>`, so not render-blocking. Adding `defer` would be marginally cleaner but changes nothing measurable.
- **No `loading="lazy"` on the hero image.** Correct. Do not add it.

**Field data:** unknown from here. Run PageSpeed Insights on both URLs. Expect no field data (CrUX requires meaningful traffic volume) — if so, use the lab scores and don't read too much into them.

---

## 5. Content Gap Analysis

### First, the honest framing

You asked me to be blunt about location pages, so: **the highest-leverage thing available to you is not on this list, and it's the Google Business Profile you've set aside.** For `web design Hinsdale`-class queries, the local pack renders above organic results. A GBP with a verified address, correct category, and 5–10 real reviews will out-produce every page below. I'd genuinely rather you spend this week on GBP than on any page in this section. You said you'd handle it separately — you asked me to flag it if it was #1, and it is.

**On location pages specifically — my honest recommendation is to build one, not four.**

Four pages titled "Web Design in Hinsdale," "Web Design in Oak Brook," "Web Design in Naperville," and "Web Design in Downers Grove," differing only by town name, are a doorway page cluster. Google's guidance names this pattern explicitly, and with 286 words of existing site content there's no way you fill four town pages with genuinely distinct material. You'd be shipping four near-duplicates on a site with two real pages. That's a bad ratio and a bad look.

Location pages *are* legitimate when they carry real local substance — a client in that town, local specifics, something true that could only be written about that place. **You have one real geographic asset right now: ABN Construction, a Chicagoland general contractor.** So build one service-area page covering DuPage County that names all four towns honestly, and earn per-town pages later by doing per-town work. When you have a Hinsdale client with a case study, *then* a Hinsdale page writes itself and deserves to exist.

### Recommended pages, ranked by expected inbound leads (not traffic)

---

**#1 — Case study: 1 of 1 Car Club** → `/work/1of1-car-club.html`

- **Target query:** `[client name]`, `car club website design`, `automotive web design chicago` — **volumes unknown, verify in a keyword tool.**
- **Intent:** evaluative. Someone already considering you wants proof you can execute. This is a *conversion* asset first and a ranking asset second — which is exactly why it's #1 on a list ranked by leads.
- **Why first:** high-end buyers don't hire from a grid of thumbnails. They read one case study end to end and then email. You currently give them one sentence: "A digital flagship for a Porsche-exclusive car club." That sentence cannot close anyone.
- **Title:** `1 of 1 Car Club — Website Design Case Study | Elimenti`
- **Meta:** `How Elimenti designed and built a digital flagship for a Porsche-exclusive car club — the brief, the design decisions, and the result. See the full case study.`
- **H2 outline:**
  - The brief — what the club needed and why
  - Who this site had to speak to
  - Design direction — type, color, and restraint
  - Building it — stack, performance, what we optimized for
  - The result
  - Start a project

---

**#2 — Service-area page** → `/web-design-dupage-county.html`

- **Target query:** `web design dupage county`, `web designer hinsdale`, `custom website design oak brook` — **volumes unknown, verify in a keyword tool.**
- **Intent:** commercial, local, high purchase intent. Somebody typing this is shopping right now.
- **Why second:** this is the page that actually targets your stated keywords. Nothing on your site currently does. But it's #2 rather than #1 because it needs real substance to be worth publishing, and that substance partly comes from #1.
- **Honest caveat:** a service-area page without a Google Business Profile is fighting with one hand tied. Local pack results dominate these queries. This page catches the organic remainder — real, but secondary to GBP.
- **Title:** `Web Design in Hinsdale, Oak Brook & DuPage County | Elimenti`
- **Meta:** `Custom website design for businesses across DuPage County — Hinsdale, Oak Brook, Naperville and Downers Grove. No templates, no packages. See the work and start a project.`
- **H2 outline:**
  - Web design for DuPage County businesses
  - Where we work — Hinsdale, Oak Brook, Naperville, Downers Grove *(one honest paragraph, not four stuffed ones)*
  - What working with a local designer actually changes
  - Recent work in the Chicago area *(link to case studies — this is where #1 pays off)*
  - What a project looks like
  - Start a conversation

---

**#3 — Contact page with a real form** → `/contact.html`

- **Target query:** navigational — `elimenti contact`, plus catching `web designer near me` traffic.
- **Intent:** transactional. This is the bottom of your funnel and it currently doesn't exist as a URL.
- **Why third:** it isn't really an SEO page, it's the conversion fix from §6. But every page you build should link somewhere, and right now every CTA on your site opens a mail client and hopes. See §6.1 for the full argument.
- **Title:** `Start a Project — Contact Elimenti | Web Design, DuPage County`
- **Meta:** `Tell us about your project. Elimenti designs custom websites for high-end businesses in Hinsdale, Oak Brook and across the Chicago area. Get in touch.`
- **H2 outline:**
  - Tell us about your project *(the form)*
  - What happens next
  - Prefer email? *(keep `hello@elimenti.com` visible as a fallback)*

---

**#4 — About page** → `/about.html`

- **Target query:** `elimenti`, brand + trust queries. Low direct search value.
- **Intent:** evaluative. Fires *after* someone likes the work and before they email.
- **Why fourth:** for a young agency this is a genuine trust signal — high-end local buyers want to know who they're actually hiring. It also gives your `Organization` schema something to point at. Ranks for almost nothing on its own, which is why it's not higher.
- **One honest caution:** an About page that reveals a very small or solo operation can cut both ways with premium buyers. That's not a reason to skip it — buyers find out regardless, and finding out on your terms is better. But write it deliberately.
- **Title:** `About Elimenti — Web Design Studio, DuPage County, IL`
- **Meta:** `Elimenti is a web design studio serving high-end businesses in Hinsdale, Oak Brook and the greater Chicago area. No templates, no packages. Here's how we work.`
- **H2 outline:**
  - Why Elimenti exists
  - How we work
  - Who we work with
  - Where we are

---

**#5 — Remaining case studies** → `/work/abn-construction.html`, `/work/burdi-clothing.html`, `/work/aamineez-art.html`

Same template as #1. Build them **after** #1 proves the format. Prioritize **ABN Construction** among these — it's your only named Chicago-area client and therefore your only real local proof point.

**Be careful with scope honesty on two of these.** Your own copy says Burdi was "targeted edits and refinements to an existing e-commerce storefront" (`portfolio.html:342`) and ABN was "ongoing site care and content edits" (`portfolio.html:326`). Those are maintenance engagements, not builds. Write them as maintenance case studies — "how we keep a contractor's site current" is a legitimate and sellable story, and inflating it into a build is the kind of thing a prospective client checks.

---

**Not recommended: separate per-service pages.**

You asked. My answer is no, not yet. Three service pages (Web Design / Visual Identity / Site Care) split across a site with 286 words of content would produce three thin pages competing with your own homepage for the same terms. Your homepage Services section (`index.html:49-65`) already covers these. **Expand those three cards to 2–3 sentences each** and revisit standalone service pages when you have enough to say to fill one properly. When that day comes, `/web-design/` is the only one worth building — it's the money service.

---

## 6. Conversion & Tracking

### 6.1 — mailto: CTAs

**Every CTA on the site is a `mailto:` link:** `index.html:35`, `index.html:42`, `index.html:98`, `portfolio.html:367`.

**SEO cost: essentially zero.** `mailto:` links don't hurt rankings. Anyone who tells you otherwise is inventing a mechanism. Let's be precise about the real problem.

**Conversion cost: substantial.** Four specific failures:

1. **On desktop, `mailto:` frequently does nothing.** Users on Gmail-in-a-browser with no OS mail handler configured click your primary CTA and get *nothing* — no error, no window, no feedback. They assume the site is broken. You will never know this happened.
2. **You cannot measure it.** A `mailto:` click is not a trackable conversion. You currently have zero visibility into how many people try to contact you and fail. That's the worst kind of blind spot: silent.
3. **The pre-filled body is clever but brittle.** The `body=` parameter on lines 35/42/98 is a well-constructed template — and it gets truncated or dropped entirely by several webmail handlers and some iOS mail clients. When it works it's great; when it doesn't the user gets a blank compose window with a mystery subject line.
4. **It leaks your address to scrapers.** `hello@elimenti.com` appears in plain text at `index.html:99` and `portfolio.html:368` plus four `href`s. That's spam surface.

**Recommendation: add a form, keep the email.** With FormSubmit, this is genuinely ~15 lines and no backend:

```html
<form action="https://formsubmit.co/hello@elimenti.com" method="POST">
  <input type="hidden" name="_subject" value="New Project Inquiry — elimenti.com">
  <input type="hidden" name="_captcha" value="true">
  <input type="hidden" name="_next" value="https://www.elimenti.com/thank-you.html">
  <input type="text"  name="name"    placeholder="Your name" required>
  <input type="email" name="email"   placeholder="Your email" required>
  <input type="text"  name="company" placeholder="Business or website">
  <textarea name="project" placeholder="What are you looking to build?" rows="5" required></textarea>
  <input type="text" name="_honey" style="display:none">
  <button type="submit" class="btn btn--primary">Start a Project</button>
</form>
```

Three things to know about FormSubmit before you commit:
- The **first** submission triggers a confirmation email to `hello@elimenti.com` to activate the endpoint. Do this before launch or your first real lead vanishes.
- `_next` needs a `thank-you.html` to exist. **That page is also your conversion-tracking trigger** — a pageview on `/thank-you.html` is a lead, which is how you finally get measurement.
- `_honey` is a honeypot field; keep it hidden and keep `_captcha` on.

**Keep `hello@elimenti.com` visible somewhere.** Some buyers — particularly the higher-end ones — prefer email to a form. Form as primary, email as fallback, is the right shape.

### 6.2 — Analytics

**Verified: none installed.** Zero matches for `gtag`, `googletagmanager`, `plausible`, `cloudflareinsights`, or `analytics` across the repo. You are running completely blind.

**Recommendation: Cloudflare Web Analytics.** Reasons, in order:

1. **Free, and you're already on Cloudflare** — enable it in the dashboard for the Pages project, paste one script tag.
2. **No cookie banner required.** It's cookieless, so no GDPR/CCPA consent UI cluttering a design-agency site.
3. **~5 KB and no third-party performance penalty** — meaningful when you're pitching yourself on craft.
4. **You don't need what GA4 does.** GA4 is built for funnels, cohorts, and ecommerce. You have two pages. Its complexity would cost you hours and tell you nothing extra.

**Plausible** is the better product (cleaner UI, better goal tracking) but it's ~$9/mo. Worth it *later*, once you have forms and case studies to measure. Not now.

**If you want GA4 anyway** — the only real argument is that Google Ads integration requires it. If paid search is on your roadmap, install GA4 from the start rather than migrating historical data later.

**Whichever you choose, the thing that actually matters is tracking the form submission**, not pageviews. Pageviews on a 2-page site are vanity. Lead count is the number.

### 6.3 — Google Search Console

**I cannot verify this from the repo.** There's no verification file (`google*.html` — checked, absent) and no `google-site-verification` meta tag in either page. But GSC verification is commonly done via DNS TXT record, which wouldn't appear in the repo at all. **So: absence of evidence here is not evidence of absence.**

**How to confirm:** go to https://search.google.com/search-console. If `elimenti.com` appears in the property dropdown, you're verified. If not, you aren't.

**If not verified, do this:**
1. Add a **Domain property** (not URL-prefix) for `elimenti.com`. Domain properties cover `www`, apex, `http`, and `https` in one property — which matters given the CRIT-4 ambiguity.
2. Verify via **DNS TXT record**. Since Cloudflare manages your DNS, this is a two-minute change in the Cloudflare dashboard and it survives redeploys — unlike an HTML file, which a bad deploy can wipe.

**What to submit first, in order:**
1. **Submit `sitemap.xml`** (after CRIT-3 ships) — Sitemaps → enter `sitemap.xml` → Submit.
2. **URL Inspection on both live URLs** → "Request Indexing." Forces a recrawl rather than waiting.
3. **Check Page Indexing report** for pages excluded as "Duplicate without user-selected canonical" — this is exactly where the www/apex problem in CRIT-4 will surface if it's real.
4. **Set up the Performance report** and check it in 30 days. It'll be sparse. That's the baseline you measure the rest of this work against.

**One expectation to set:** GSC data lags 2–3 days, and with your current traffic the Performance report will be near-empty for weeks. Don't read that as failure. It's the baseline.

---

## 7. Prioritized Action List — by impact ÷ effort

**#0 — Google Business Profile. Out of scope per your instruction, but it is the highest-leverage item available to you and nothing below outranks it.** Claim it, pick "Website designer" as primary category, set the DuPage service area, get 5+ real reviews. For local commercial queries this beats every on-page change on this list.

| # | Action | Impact | Effort | Files |
|---|---|---|---|---|
| 1 | **Fix `og:image`/`twitter:image` to absolute URLs, add `og:url`.** Every share of your site currently renders imageless. Immediate, visible, 10 minutes. | High | 10 min | `index.html:13,18` · `portfolio.html:13,18` |
| 2 | **Add geo to both titles + meta descriptions.** Cheapest possible move toward your actual target keywords. Needs your copy approval. | High | 15 min | `index.html:7-8` · `portfolio.html:7-8` |
| 3 | **Install Cloudflare Web Analytics.** You cannot evaluate anything else on this list without measurement. One script tag. | High | 10 min | both `</body>` |
| 4 | **Add canonicals + `_redirects`, and settle www vs apex.** Blocked on your answer re: `CNAME`. | High | 20 min | both `<head>` · new `_redirects` |
| 5 | **Create `robots.txt` + `sitemap.xml`, submit to GSC.** Low intrinsic value at 2 pages; unlocks the GSC feedback loop and pays off as §5 ships. | Med | 15 min | new files |
| 6 | **Compress the logo → WebP, add `width`/`height`, add real favicon + apple-touch-icon.** ~200 KB saved, CLS fixed, no visual change. | Med-High | 30 min | `index.html:20,45` · new images |
| 7 | **Build case study #1 (1 of 1 Car Club).** Highest lead impact of any new page; also the biggest single effort here. | High | 3-4 hrs | new `/work/1of1-car-club.html` |
| 8 | **Replace mailto with a FormSubmit form + `thank-you.html`.** Fixes silent desktop CTA failures and finally makes leads measurable. | High | 1-2 hrs | new `/contact.html`, `/thank-you.html` |
| 9 | **Paste JSON-LD Blocks A + B.** Twenty minutes, no ranking change, correct entity understanding. Don't oversell it to yourself. | Low-Med | 20 min | `index.html` · `portfolio.html` |
| 10 | **Build the DuPage service-area page.** Targets your money keywords — but do it after #7 so it has real work to link to. | High | 2-3 hrs | new `/web-design-dupage-county.html` |

**Quick wins bundled into the above, no separate line needed:** `span`→`h3` on portfolio cards (HIGH-4, zero visual change), `href="#"`→`href="/"` (MED-2), trimming font weights to 3 (MED-7, zero visual change), removing `fade-in` from the portfolio hero (HIGH-2).

**Deliberately NOT on this list, and why:**
- **Per-town location pages** — doorway-page pattern at your current content depth. See §5.
- **Separate service pages** — would cannibalize your own homepage. See §5.
- **Removing unused CSS** — under 1 KB. Lighthouse theater.
- **Self-hosting fonts** — real but small (~100 ms); your `preconnect` + `display=swap` setup is already correct.
- **Moving portfolio inline CSS to the stylesheet** — inline is *faster*. This is a maintainability preference, not an SEO fix.
- **`Service` schema** — included in §3 because you asked, but it produces no rich result. Do it last or not at all.
- **The portfolio iframes (HIGH-1)** — genuinely important, but it's a visual change and I'm not making it unilaterally.

---

## Open questions I need answered before implementing

1. **www or apex?** `CNAME` says `elimenti.com`; you said `www.elimenti.com`. Every canonical, the sitemap, `_redirects`, and all the JSON-LD depend on this. **This one blocks items 1, 4, 5, and 9.**
2. **GitHub Pages or Cloudflare Pages?** A root `CNAME` file suggests GH Pages. `_redirects` and `_headers` only work on Cloudflare Pages.
3. **`og:image`** — do you want me to design a proper 1200×630 card, or wire the absolute URL of the existing logo as a stopgap today?
4. **Copy changes** — items 2, HIGH-5, LOW-3 and all of §5 involve writing. Approve wording first, or want me to draft and you edit?
5. **Portfolio iframes (HIGH-1)** — replace with static screenshots, or leave as-is?
