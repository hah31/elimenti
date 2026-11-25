# To do: things only Hashim can do

Updated November 25, 2026. Ordered by how much each one moves Google and AI answers, going by what was measured that day (`seo/baseline-2026-11-25.md`). Items 1, 2 and 5 need accounts only you can create or sign in to.

## 1. Finish and verify the Google Business Profile, then ask for reviews

Google's map results, Gemini and Google's AI answers lean on Business Profile data. On November 25 the Hinsdale and Oak Brook pages sat on page 2 of Google (#14 to #17), every one of those searches showed a map pack without Elimenti, and Gemini named four other firms for "best web designers in Hinsdale". No page change substitutes for a verified profile with reviews. It's also the strongest fix for the name: on November 25 the search "elimenti web design" didn't return elimenti.com in Google's top 10, because Google reads "elimenti" as a misspelling of "element". A verified profile under the exact name is how Google learns Elimenti is a business, which matters most for referrals who search the name they heard.

- Copy for the profile: `seo/off-site-kit.md` section 1. **It was rewritten on November 25**: the earlier version listed prices and said "high-end businesses" and "no page builders". Use the current file.
- Review requests: section 2 of the same file, in the order listed.

## 2. The listings ChatGPT reads: Bing Places, Yelp, then Apple

On November 25 ChatGPT named Elimenti first for Hinsdale, car clubs and med spas, but its map panel never showed Elimenti, and for Oak Brook it named only firms with map listings and reviews. Yelp now licenses its business data to OpenAI (Axios, July 23, 2026), and Bing's results feed ChatGPT's search.

Steps are in `seo/off-site-kit.md` section 3: Bing Places (row 1, import from the Business Profile once it's verified), Yelp (row 3, hide the address), Apple Business Connect (conditional row). Add each profile URL to `SAME_AS` in `seo/tools/build.py` when it's live.

## 3. Done: steponesites.com points at elimenti.com

Done November 25 with Hashim's approval (hah31/steponesites PR #7): `/`, `/portfolio.html` and `/pricing.html` redirect to elimenti.com's home, Work and Pricing pages, the broken sitemap is gone, and `Step One Sites` is now an `alternateName` in the schema. `demos/` was left as is.

## 4. Done: hashim-hassan.com describes Elimenti correctly

Done November 25 (hah31/hashim-hassan.com PR #3): the Elimenti entry now says "I design and build websites for local businesses that compete on quality and design, on WordPress or custom-coded, and I maintain existing WordPress sites for others."

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
