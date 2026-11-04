// Step 3b of the western suburbs website study: checks Lighthouse doesn't make.
//
// Usage:
//   node seo/tools/research/audit_pages.js SAMPLE.json OUT.jsonl
// For each {id, url}: loads the homepage as a phone (390 x 844, touch, mobile Chrome user agent)
// and records the viewport tag, sideways scrolling, small text, phone and email links, the
// contact page link and whether it resolves, the newest year in a copyright notice, structured
// data types and platform fingerprints. Then checks plain-HTTP and HTTPS behaviour with curl.
// Resumable: sites already in OUT.jsonl are skipped.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');

const [samplePath, outPath] = process.argv.slice(2);
const sample = JSON.parse(fs.readFileSync(samplePath, 'utf8'));
const done = new Set(fs.existsSync(outPath)
  ? fs.readFileSync(outPath, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l).id) : []);

const UA = 'Mozilla/5.0 (Linux; Android 11; moto g power (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36';

// Platform fingerprints, checked against the page HTML and response headers.
const PLATFORMS = [
  ['WordPress', [/\/wp-content\//i, /\/wp-includes\//i, /<meta[^>]+generator[^>]+WordPress/i, /wp-json/i]],
  ['Wix', [/static\.wixstatic\.com/i, /wix-bolt|wixstatic|_wixCssImports|wix\.com\/website/i, /x-wix-request-id/i]],
  ['Squarespace', [/static1\.squarespace\.com/i, /squarespace-cdn\.com/i, /<!-- This is Squarespace\. -->/i, /Static\.SQUARESPACE_CONTEXT/]],
  ['Shopify', [/cdn\.shopify\.com/i, /Shopify\.theme/, /x-shopify-stage|x-shopid/i]],
  ['GoDaddy Website Builder', [/img1\.wsimg\.com/i, /<meta[^>]+generator[^>]+Starfield/i, /websites\.godaddy\.com/i]],
  ['Duda', [/irp\.cdn-website\.com|lirp\.cdn-website\.com|cdn-website\.com/i, /multiscreensite\.com/i, /dmAlbum|dmBody|dudamobile/i]],
  ['Webflow', [/data-wf-site=/i, /webflow\.(js|com)/i, /website-files\.com/i]],
  ['Weebly', [/editmysite\.com|weebly\.com/i]],
  ['Showit', [/showit\.(co|site)|static\.showit\.co/i]],
  ['HubSpot CMS', [/hs-sites\.com|hubspot\.net\/hub\/|hs-scripts\.com.*\n?.*hsappstatic|<meta[^>]+generator[^>]+HubSpot/i]],
  ['Drupal', [/<meta[^>]+generator[^>]+Drupal/i, /drupal-settings-json|Drupal\.settings|\/sites\/default\/files\//i]],
  ['Joomla', [/<meta[^>]+generator[^>]+Joomla/i, /\/media\/jui\//i]],
  ['Framer', [/framerusercontent\.com|framer\.com\/m\//i]],
  ['Hibu or other hosted builder', [/hibu|yext-pages|thryv|vagaro\.com\/.*widget|ueni\.com|site123|jimdo|strikingly|yola|carrd\.co/i]],
];

async function checkPage(context, url) {
  const page = await context.newPage();
  const res = { loaded: false };
  let headers = {};
  try {
    const resp = await page.goto(url, { waitUntil: 'load', timeout: 45000 });
    res.status = resp ? resp.status() : null;
    headers = resp ? await resp.allHeaders() : {};
    await page.waitForTimeout(2500);
    res.loaded = true;
    res.finalUrl = page.url();
    const data = await page.evaluate(() => {
      const out = {};
      const vp = document.querySelector('meta[name="viewport" i]');
      out.viewportMeta = vp ? vp.getAttribute('content') : null;
      out.title = document.title;
      const md = document.querySelector('meta[name="description" i]');
      out.hasMetaDescription = !!(md && md.getAttribute('content') && md.getAttribute('content').trim());
      out.scrollWidth = document.documentElement.scrollWidth;
      out.innerWidth = window.innerWidth;
      // Share of visible text characters set below 12px
      let small = 0, total = 0;
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const t = walker.currentNode.textContent.trim();
        if (!t) continue;
        const el = walker.currentNode.parentElement;
        if (!el) continue;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden' || el.closest('script,style,noscript')) continue;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;
        total += t.length;
        if (parseFloat(cs.fontSize) < 12) small += t.length;
      }
      out.smallTextShare = total ? small / total : null;
      out.textChars = total;
      // Phone and email links
      const telLinks = [...document.querySelectorAll('a[href^="tel:" i]')].map(a => a.getAttribute('href'));
      out.telLinks = [...new Set(telLinks)].slice(0, 20);
      out.mailtoLinks = [...new Set([...document.querySelectorAll('a[href^="mailto:" i]')].map(a => a.getAttribute('href')))].slice(0, 20);
      // Phone numbers shown in text, and whether each sits inside a tel: link
      const text = document.body.innerText || '';
      const re = /(?:\+?1[\s.-]?)?\(?\b([2-9]\d{2})\)?[\s.-]?(\d{3})[\s.-](\d{4})\b/g;
      const shown = new Set();
      let m;
      while ((m = re.exec(text))) shown.add(m[1] + m[2] + m[3]);
      out.phonesShown = [...shown].slice(0, 20);
      // Contact link (by URL or link text)
      const links = [...document.querySelectorAll('a[href]')];
      const contact = links.find(a => /contact/i.test(a.getAttribute('href') || '') && !/^(mailto|tel):/i.test(a.getAttribute('href')))
        || links.find(a => /contact/i.test(a.textContent || '') && !/^(mailto|tel|javascript):/i.test(a.getAttribute('href') || '') && (a.getAttribute('href') || '#') !== '#');
      out.contactHref = contact ? contact.href : null;
      out.hasForm = !!document.querySelector('form input[type="email" i], form textarea');
      // Copyright notice: newest year mentioned next to a copyright mark or word
      const footer = [...document.querySelectorAll('footer, [class*="footer" i], [id*="footer" i]')].map(f => f.innerText).join('\n');
      const findYears = (s) => {
        const years = [];
        const rc = /(?:©|\(c\)|&copy;|copyright)([^\n]{0,60})/gi;
        let mm;
        while ((mm = rc.exec(s))) {
          const ys = (mm[0].match(/\b(19[89]\d|20[0-4]\d)\b/g) || []).map(Number);
          years.push(...ys);
        }
        return years;
      };
      let years = findYears(footer);
      if (!years.length) years = findYears(text);
      out.copyrightYear = years.length ? Math.max(...years) : null;
      out.hasCopyright = /©|copyright|\(c\)\s*\d{4}/i.test(footer || text);
      // Structured data
      const types = [];
      const collect = (n) => {
        if (Array.isArray(n)) return n.forEach(collect);
        if (n && typeof n === 'object') {
          if (n['@type']) [].concat(n['@type']).forEach(t => types.push(String(t)));
          if (n['@graph']) collect(n['@graph']);
        }
      };
      document.querySelectorAll('script[type="application/ld+json" i]').forEach(s => {
        try { collect(JSON.parse(s.textContent)); } catch (e) { types.push('INVALID_JSON'); }
      });
      out.jsonLdTypes = [...new Set(types)];
      out.html = document.documentElement.outerHTML.slice(0, 600000);
      return out;
    });
    const headerText = Object.entries(headers).map(([k, v]) => `${k}: ${v}`).join('\n');
    const hay = data.html + '\n' + headerText;
    res.platforms = PLATFORMS.filter(([, pats]) => pats.some(p => p.test(hay))).map(([n]) => n);
    res.proxyError = res.status === 405 && (data.textChars || 0) < 400;
    res.challenge = /just a moment|attention required|access denied|captcha|are you a human/i.test(data.title)
      || /cf-challenge|challenge-platform|px-captcha|_Incapsula_Resource/i.test(data.html.slice(0, 20000));
    delete data.html;
    Object.assign(res, data);
    res.serverHeader = headers['server'] || null;
    res.poweredBy = headers['x-powered-by'] || null;
    // Does the contact link resolve?
    if (res.contactHref && /^https:/i.test(res.contactHref)) {
      const r = curl(res.contactHref, true);
      res.contactStatus = r.code ? r.code : 'ERROR';
      if (!r.code) res.contactError = r.error;
    }
  } catch (e) {
    res.error = String(e).split('\n')[0].slice(0, 300);
  } finally {
    await page.close();
  }
  return res;
}

function curl(url, follow = false) {
  // Returns {code, redirect, exit} for one request (following redirects only when asked).
  try {
    const out = execFileSync('curl', ['-sS', '-o', '/dev/null', '--max-time', '25', '-A', UA, '--proto', '=https', '--proto-redir', '=https']
      .concat(follow ? ['-L', '--max-redirs', '10'] : [])
      .concat(['-w', '%{http_code} %{redirect_url}', url]), { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    const [code, redirect] = out.trim().split(' ');
    return { code: Number(code), redirect: redirect || null, exit: 0 };
  } catch (e) {
    return { code: null, redirect: null, exit: e.status, error: String(e.stderr || e).split('\n')[0].slice(0, 200) };
  }
}

function httpChecks(url) {
  // HTTPS only: every request goes through the session's HTTPS proxy.
  const host = new URL(url).host;
  const https = curl(`https://${host}/`);
  return { httpsCode: https.code, httpsExit: https.exit, httpsError: https.error || null };
}

(async () => {
  // All traffic goes through the session's HTTPS proxy, which only tunnels https. So every site
  // is tested at its https:// address; a site without working HTTPS is recorded as not measured.
  const browser = await chromium.launch({
    proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined,
    args: ['--no-sandbox'],
  });
  for (const site of sample) {
    if (done.has(site.id)) continue;
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true,
      userAgent: UA, locale: 'en-US', timezoneId: 'America/Chicago',
    });
    const result = { id: site.id, url: site.url, checkedAt: new Date().toISOString() };
    Object.assign(result, httpChecks(site.url));
    const host = new URL(site.url).host;
    result.testedUrl = `https://${host}/`;
    if (result.httpsCode >= 200 && result.httpsCode < 400) {
      Object.assign(result, await checkPage(context, result.testedUrl));
    } else {
      result.loaded = false;
      result.error = 'HTTPS unavailable; not measured';
    }
    await context.close();
    fs.appendFileSync(outPath, JSON.stringify(result) + '\n');
    console.log(`${site.id} loaded=${result.loaded} platforms=${(result.platforms || []).join('/')} year=${result.copyrightYear} tel=${(result.telLinks || []).length} https=${result.httpsCode}`);
  }
  await browser.close();
  console.log('done');
})();
