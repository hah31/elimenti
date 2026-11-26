# To do: things only Hashim can do

Updated November 25, 2026 (late evening). Ordered by how much each one moves Google and AI answers, going by what was measured that day (`seo/baseline-2026-11-25.md`). Items 1, 2 and 5 need accounts only you can create or sign in to.

**Listing city.** Bing Places, Yelp and Clutch list the city as **Oak Brook, IL 60523**, the business's mailing address, with the street hidden or not shown. The site, schema and OG cards say Hinsdale, IL. Use Oak Brook on every new listing (Google, Apple) so the directories agree with each other, and decide separately whether the site should change.

## 1. Finish and verify the Google Business Profile, then ask for reviews

Google's map results, Gemini and Google's AI answers lean on Business Profile data. On November 25 the Hinsdale and Oak Brook pages sat on page 2 of Google (#14 to #17), every one of those searches showed a map pack without Elimenti, and Gemini named four other firms for "best web designers in Hinsdale". No page change substitutes for a verified profile with reviews. It's also the strongest fix for the name: on November 25 the search "elimenti web design" didn't return elimenti.com in Google's top 10, because Google reads "elimenti" as a misspelling of "element". A verified profile under the exact name is how Google learns Elimenti is a business, which matters most for referrals who search the name they heard.

- Copy for the profile: `seo/off-site-kit.md` section 1. **It was rewritten on November 25**: the earlier version listed prices and said "high-end businesses" and "no page builders". Use the current file.
- Review requests: section 2 of the same file, in the order listed.

## 2. The listings ChatGPT reads: Bing Places, Yelp, Clutch, then Apple

On November 25 ChatGPT named Elimenti first for Hinsdale, car clubs and med spas, but its map panel never showed Elimenti, and for Oak Brook it named only firms with map listings and reviews. Yelp now licenses its business data to OpenAI (Axios, July 23, 2026), and Bing's results feed ChatGPT's search.

Where each one stands (November 25, late evening):

- **Bing Places: created, not verified, not published.** Bing only offers a mailed postcard PIN. Sign in at bing.com/forbusiness, open the Elimenti listing, **Verify now → Mail**, and enter the PIN when it arrives. Every field stays locked until then. Right after verifying, open **Basic details**: set "Do you deliver goods and services to your customers at their location?" to **Yes**, add the service areas from `seo/off-site-kit.md`, hide the street address, and add the email, description (medium, from the kit) and hours. Bing may show the street briefly before that edit goes through.
- **Yelp: live at https://www.yelp.com/biz/elimenti-oak-brook.** Category Web Design with services web design, website development and website maintenance; specialties, history, owner bio ("Hashim H."), logo, five Business Highlights (the ad shows Free consultations and Locally owned & operated), the call to action "Free call and written proposal" (Learn more, to `/contact/`), three captioned work photos pinned as the slideshow (1 of 1 Car Club first) and two Portfolio projects (1 of 1 Car Club and Aamineez Art, no prices). The page shows "Oak Brook, IL 60523" with no street.
  - Still yours: **hours**, and the amenities questions if you want any of them.
  - **Duplicate photos:** each work photo is in the gallery twice. The captioned set is the one pinned; delete the three uncaptioned copies under Photos unless you uploaded them on purpose.
  - **Quote requests:** the page has Yelp's Request a Quote button. Requests and messages arrive in the Yelp for Business Inbox and by email, and Yelp shows customers how fast you reply, so answer the same day.
- **Yelp Ads free trial: live until 12/25/26 (second trial).** Yelp's re-verification on November 25 reset the claim and wiped the first trial, so the trial was started again that evening. Billing shows both promotions active (Yelp Ads and the Upgrade Package, 30 days each) and a $0 balance. Yelp bills on 12/01/26 or when charges reach $150, so check that the 12/01 bill shows $0.
  - **Cancel both products (Yelp Ads and the Upgrade Package) on the desktop site under Billing, on 12/23 or 12/24.** Not earlier: the published trial terms say you must keep it for the whole period to get its full value. Not later: billing starts after 12/25.
  - Don't raise the budget ($13/day average): anything above the trial's amount is billed.
  - Set on the second trial: goal Get more website clicks (to elimenti.com); boosted keywords web design, website design, web designer, website redesign, web development, WordPress developer, small business website and website maintenance; 13 searches blocked (advertising, advertising agency, business consulting, digitizing services, e-commerce website development, ecommerce, mobile app development, printing services, product design, public relations, software development, video film production, web hosting); ad location Cook, DuPage, Will and Kane counties instead of the 20-mile default (Yelp's audience gauge went from Limited to Ideal); ad photo on smart selection, which now has the gallery photos to test.
  - Links (checked November 26): the page's website link and the ad's goal both go to plain `https://elimenti.com`, and the Learn more button goes to `/contact/`. Yelp sends every outside link through its own yelp.com/biz_redir hop first, which is how it counts clicks. Nothing to change after the trial.
- **Clutch: profile created, under Clutch's review (clutch.co/profile/elimenti).** Service lines Web Design 70%, Web Development 20%, Branding 10%. Minimum project size and hourly rate are set to N/A, so no prices show. Location Oak Brook, IL; Clutch takes 7–10 business days to validate a location, and its help pages don't say whether the street line appears on the public profile, so check once it's published. Logo and description were added on November 25. Portfolio items now come from Clutch's Projects, and adding one sends that client a review request, so add them when you send the review emails (2a). Clutch's edit page can show the Description box empty (0/2000) after a reload even though it's saved; reload until the text shows before pressing Save Changes on that page, because saving with an empty box may clear it.
- **Apple Business Connect: not started.** Needs your Apple ID. Stop if Apple insists on showing the street address.

Add each profile URL to `SAME_AS` in `seo/tools/build.py` once it's live and loads to a page that's clearly Elimenti's. Yelp was added on November 25. Listing images (square logo, work photos, desktop and phone screenshots) are in `seo/off-site-assets/` for Bing, Apple and Google.

## 2a. Reviews: Clutch first, Google once the profile exists

Clutch review link: https://review.clutch.co/review?provider_id=2779047 (clients write the review themselves and confirm their email). Three drafts are in Gmail with no recipient. Add the address and paste the link where it says `[PASTE CLUTCH LINK]`: the Gmail connector rewrites links into google.com redirects, so the link isn't in the drafts. Send them once Clutch publishes the profile.

- **ABN (Aldo):** send after invoice ELM-003 is paid, not in the same week as the invoice.
- **Burdi:** mentions the Father's Day and Toys for Tots event pages.
- **Aamineez Art:** add her name to the greeting.
- **Not drafted:** 1 of 1 Car Club (the project is paused with a balance open) and Bruce Hodes (not a client, so not eligible on Clutch; ask him for a Google review once the Business Profile is verified). Yelp forbids asking for reviews, so don't send anyone to Yelp.

## 2b. Press and chamber pitches about the western suburbs study

Five drafts in Gmail (hashim@elimenti.com), each under 100 words, no links, ending with one question: The Hinsdalean (Pamela Lannom, editor), Hinsdale Patch (David Giuliani), Hinsdale Magazine (its published story address), the Hinsdale Chamber (Amanda Wagner, President & CEO) and the Greater Oak Brook Chamber (David Carlin, President & CEO). Every address is published by the outlet or chamber. They're signed "Hashim H."; a reporter will likely ask for your full name. The Daily Herald wasn't drafted because no published business-news address was confirmed.

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
