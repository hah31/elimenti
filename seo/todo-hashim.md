# To do: things only Hashim can do

Updated November 25, 2026. Ordered by how much each one moves Google and AI answers, going by what was measured that day (`seo/baseline-2026-11-25.md`). Items 1, 2 and 5 need accounts only you can create or sign in to.

## 1. Finish and verify the Google Business Profile, then ask for reviews

Google's map results, Gemini and Google's AI answers lean on Business Profile data. On November 25 the Hinsdale and Oak Brook pages sat on page 2 of Google (#14 to #17), every one of those searches showed a map pack without Elimenti, and Gemini named four other firms for "best web designers in Hinsdale". No page change substitutes for a verified profile with reviews.

- Copy for the profile: `seo/off-site-kit.md` section 1. **It was rewritten on November 25**: the earlier version listed prices and said "high-end businesses" and "no page builders". Use the current file.
- Review requests: section 2 of the same file, in the order listed.

## 2. The listings ChatGPT reads: Bing Places, Yelp, then Apple

On November 25 ChatGPT named Elimenti first for Hinsdale, car clubs and med spas, but its map panel never showed Elimenti, and for Oak Brook it named only firms with map listings and reviews. Yelp now licenses its business data to OpenAI (Axios, July 23, 2026), and Bing's results feed ChatGPT's search.

Steps are in `seo/off-site-kit.md` section 3: Bing Places (row 1, import from the Business Profile once it's verified), Yelp (row 3, hide the address), Apple Business Connect (conditional row). Add each profile URL to `SAME_AS` in `seo/tools/build.py` when it's live.

## 3. Point steponesites.com at elimenti.com

steponesites.com is still live and crawlable. Its title is "Step One Sites — Hand-Coded Websites for DuPage County Small Businesses", it sells sites at $175 a month with a two-week launch, an offer Elimenti doesn't have, and its canonical points at stepone.sites, a domain that doesn't exist. Search engines and AI assistants treat it as a separate, current business.

In the `hah31/steponesites` repo, replace `index.html`, `portfolio.html` and `pricing.html` with the three files below, delete `sitemap.xml` and keep `CNAME`. Each file sends visitors and search engines to the matching elimenti.com page. (Or open a session with that repo attached and ask Claude to do it.)

`index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Step One Sites is now Elimenti</title>
    <link rel="canonical" href="https://elimenti.com/">
    <meta http-equiv="refresh" content="0; url=https://elimenti.com/">
</head>
<body>
    <p>Step One Sites is now Elimenti: <a href="https://elimenti.com/">https://elimenti.com/</a></p>
</body>
</html>
```

`portfolio.html` and `pricing.html`: the same file with `https://elimenti.com/` replaced by `https://elimenti.com/work/` and `https://elimenti.com/pricing/` (three places each).

After it's live, add `'Step One Sites'` to `alternateName` in `BUSINESS` in `seo/tools/build.py` (the comment there explains why it waits) and run the build.

## 4. Change one sentence on hashim-hassan.com

On November 25 ChatGPT described Elimenti's sites as "hand-coded". The one public page that still says that is the Elimenti entry on hashim-hassan.com:

> I hand-code static websites for local businesses that compete on quality and design, and I maintain existing sites for others.

Suggested replacement:

> I design and build websites for local businesses that compete on quality and design, on WordPress or custom-coded, and I maintain existing WordPress sites for others.

## 5. Give the browser's Google account read access to Search Console

Search Console for elimenti.com is on a different Google account from the one signed in to the Claude desktop app's browser, so the November 25 positions come from live searches, which shift with location. In Search Console, as the owner: **Settings → Users and permissions → Add user**, enter the Google account that's signed in to that browser, choose **Restricted** (view-only), **Add**. Future checks can then read real queries, impressions and positions.

## 6. Request indexing for the pages that changed (optional)

The sitemap's dates and the new internal links will get these recrawled anyway; requesting indexing in Search Console's URL Inspection speeds it up. In this order:

1. https://elimenti.com/site-care/
2. https://elimenti.com/guides/taking-over-a-wordpress-site/
3. https://elimenti.com/faq/
4. https://elimenti.com/
5. https://elimenti.com/hinsdale-web-design/
6. https://elimenti.com/chicago-suburbs-web-design/
7. https://elimenti.com/oak-brook-web-design/

## 7. Still open from earlier passes

- **Glen Ellyn 301 (Cloudflare).** On November 25, `/glen-ellyn-web-design/` still answered 200 (the meta-refresh stub). Steps: `seo/cloudflare-redirects.md`, Rule 2.
- **Industry pages that need a real project:** `/med-spa-websites/`, `/interior-designer-websites/`, `/custom-home-builder-websites/`, `/landscape-design-websites/`. One real project in any of them, written up like the 1 of 1 case study, is the fix.
