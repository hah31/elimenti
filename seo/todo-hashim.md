# To do: things only Hashim can do

From the November 2026 SEO pass. Each item is something I couldn't do or verify from the repo or the web.

## 1. Send your profile URLs for `sameAs`

No Elimenti profile URL appears anywhere in the repo, so the LocalBusiness schema has no `sameAs` yet. Search engines use `sameAs` to connect the website to the same business elsewhere. Send whichever of these exist, as the public URL a stranger would open:

- [ ] Google Business Profile: in the profile, **Share profile** → copy the link (looks like `https://share.google/...` or `https://maps.app.goo.gl/...`)
- [ ] LinkedIn company page (`https://www.linkedin.com/company/...`)
- [ ] Instagram (`https://www.instagram.com/...`)
- [ ] Clutch (`https://clutch.co/profile/...`)
- [ ] Yelp (`https://www.yelp.com/biz/...`)
- [ ] Bing Places (the public Bing Maps link to the listing)

Each one goes in the `SAME_AS` list near the top of `seo/tools/build.py`; then run `python3 seo/tools/build.py`. Only add a profile that's live, public and clearly Elimenti's.

## 2. Turn the Glen Ellyn redirect into a real 301 (Cloudflare)

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

## 3. Industry pages that need a real project or first-hand detail

The brief allowed one sentence from the report on each of these if the report broke results out by business type with at least five businesses of that type. It doesn't: the downloadable CSV has no business-type breakdown, and the site-level data only has broad sectors ("Health, wellness and beauty", "Home and building", "Professional services"), none of which is one of these. So none of these pages changed. Each needs a real project, or something you've seen first-hand working with that kind of business:

- [ ] `/med-spa-websites/`: no med spa client or case study yet
- [ ] `/interior-designer-websites/`: no interior designer client (it links the Aamineez portfolio case study, which is the closest work)
- [ ] `/custom-home-builder-websites/`: no home builder client (links ABN Construction Group, a general contractor)
- [ ] `/landscape-design-websites/`: no landscape client (also links ABN)

The fastest real fix is one project, even small, in any of these, written up the way the 1 of 1 case study is.

## 4. Ask Google to index the new and changed pages

Paste each URL in `seo/request-indexing.md` into Search Console's URL Inspection, in order, and click **Request indexing**.

## 5. Optional

- [ ] If Bing Webmaster Tools isn't verified yet, verify it (it can import from Search Console). The IndexNow submissions this pass sets up show there under **IndexNow**.
