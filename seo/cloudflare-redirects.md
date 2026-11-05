# Cloudflare redirect rules for elimenti.com

**Goal:** every `www` and `http` variant reaches `https://elimenti.com/<same path>` in **one 301**. The two retired URLs (`/portfolio.html` and `/glen-ellyn-web-design/`) become true server-side 301s instead of meta refreshes.

## Why there are two hops today (checked 2026-11-05)

```
http://www.elimenti.com/pricing/   -> 301 https://www.elimenti.com/pricing/   (Cloudflare, "Always Use HTTPS")
https://www.elimenti.com/pricing/  -> 301 https://elimenti.com/pricing/       (GitHub Pages, www -> apex)
```

`http://elimenti.com/...` and `https://www.elimenti.com/...` already take one hop. Only `http://www` takes two.

## Why three rules instead of one

One Single Redirect rule has one target URL. Sending `/portfolio.html` to `/work/` and everything else to the same path needs a different target for each case. Cloudflare's tools for doing that inside one rule don't fit:

- `regex_replace()` can be used only once per expression ([functions reference](https://developers.cloudflare.com/ruleset-engine/rules-language/functions/)).
- Regex isn't available on the Free or Pro plans ([availability table](https://developers.cloudflare.com/rules/url-forwarding/)).

Free allows 10 Single Redirect rules, so three is fine. Cloudflare applies **the first rule that matches** and stops there ([same page](https://developers.cloudflare.com/rules/url-forwarding/)), so the order below matters.

## Steps

Cloudflare dashboard → elimenti.com → **Rules** → **Overview** → **Create rule** → **Redirect Rule**. For each rule, choose **Custom filter expression**, click **Edit expression**, and paste the expression.

### Rule 1: Old portfolio URL

- **Rule name:** `Old portfolio URL to /work/`
- **Expression:**
  ```
  (http.host in {"elimenti.com" "www.elimenti.com"} and http.request.uri.path in {"/portfolio.html" "/portfolio"})
  ```
- **Then:** Type `Static`, URL `https://elimenti.com/work/`, Status code `301`, **Preserve query string** off.

### Rule 2: Glen Ellyn page merged into the suburbs hub

- **Rule name:** `Glen Ellyn page to suburbs hub`
- **Expression:**
  ```
  (http.host in {"elimenti.com" "www.elimenti.com"} and http.request.uri.path in {"/glen-ellyn-web-design/" "/glen-ellyn-web-design" "/glen-ellyn-web-design/index.html"})
  ```
- **Then:** Type `Static`, URL `https://elimenti.com/chicago-suburbs-web-design/#glen-ellyn`, Status code `301`, **Preserve query string** off.
- If Cloudflare rejects the `#glen-ellyn` part, use `https://elimenti.com/chicago-suburbs-web-design/` instead. I haven't confirmed whether it accepts the fragment. Google ignores the fragment either way; it only scrolls visitors to the Glen Ellyn section.

### Rule 3: www and http to https://elimenti.com

- **Rule name:** `www and http to https apex`
- **Expression:**
  ```
  (http.host eq "www.elimenti.com") or (http.host eq "elimenti.com" and not ssl)
  ```
- **Then:** Type `Dynamic`, Expression `concat("https://elimenti.com", http.request.uri.path)`, Status code `301`, **Preserve query string** on.

Deploy all three. In the rules list, the order must be 1, 2, 3; drag them into that order if they aren't.

Leave the `portfolio.html` and `glen-ellyn-web-design/index.html` files in the repo. They're the backup if a rule is ever removed, and they still redirect on `elimenti.pages.dev`.

## Test

Run in **PowerShell** (Windows), one line at a time. Each prints: number of hops, final status code, final URL.

```
curl.exe -s -o NUL -L -w "%{num_redirects} %{http_code} %{url_effective}\n" http://www.elimenti.com/pricing/
curl.exe -s -o NUL -L -w "%{num_redirects} %{http_code} %{url_effective}\n" https://www.elimenti.com/pricing/
curl.exe -s -o NUL -L -w "%{num_redirects} %{http_code} %{url_effective}\n" http://elimenti.com/pricing/
curl.exe -s -o NUL -L -w "%{num_redirects} %{http_code} %{url_effective}\n" "http://www.elimenti.com/guides/?utm_source=test"
curl.exe -s -o NUL -L -w "%{num_redirects} %{http_code} %{url_effective}\n" http://www.elimenti.com/portfolio.html
curl.exe -s -o NUL -L -w "%{num_redirects} %{http_code} %{url_effective}\n" https://elimenti.com/glen-ellyn-web-design/
curl.exe -s -o NUL -L -w "%{num_redirects} %{http_code} %{url_effective}\n" https://elimenti.com/pricing/
```

On Mac, Linux or the Raspberry Pi, use `curl` instead of `curl.exe` and `/dev/null` instead of `NUL`.

**Expected:**

| URL | Hops | Final |
|---|---|---|
| `http://www.elimenti.com/pricing/` | **1** | `200 https://elimenti.com/pricing/` |
| `https://www.elimenti.com/pricing/` | 1 | `200 https://elimenti.com/pricing/` |
| `http://elimenti.com/pricing/` | 1 | `200 https://elimenti.com/pricing/` |
| `http://www.elimenti.com/guides/?utm_source=test` | 1 | `200 https://elimenti.com/guides/?utm_source=test` |
| `http://www.elimenti.com/portfolio.html` | 1 | `200 https://elimenti.com/work/` |
| `https://elimenti.com/glen-ellyn-web-design/` | 1 | `200 https://elimenti.com/chicago-suburbs-web-design/` (curl drops the `#glen-ellyn` part) |
| `https://elimenti.com/pricing/` | **0** | `200 https://elimenti.com/pricing/` |

The last line checks that the rules don't touch the real site. Anything other than 0 hops there means a rule expression is wrong: turn rule 3 off and recheck it.

## Fallback: if `http://www` still shows 2 hops

That means Cloudflare's **Always Use HTTPS** setting runs before Redirect Rules. Cloudflare's docs don't say which runs first, so I couldn't confirm the order in advance.

1. Go to **SSL/TLS** → **Edge Certificates** and turn **Always Use HTTPS** off. Rule 3 already redirects every `http` request on both hostnames, so nothing is left unprotected.
2. Re-run the tests. `http://www` should now show 1 hop.
3. Also run `curl.exe -s -o NUL -L -w "%{num_redirects} %{http_code} %{url_effective}\n" http://elimenti.com/contact/`, which should show 1 hop to https.

If it's **still** 2 hops after that, turn Always Use HTTPS back on and keep the three rules. You'll still end on the right URL, and every hop will be a permanent 301, so the cost is one extra redirect on one rarely-typed variant.

## Undo

Delete or disable the three rules (and turn Always Use HTTPS back on if you turned it off). The site returns to exactly how it behaves today.
