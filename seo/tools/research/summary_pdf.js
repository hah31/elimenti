// Step 6 of the western suburbs website study: the downloadable two-page PDF summary.
//
// Usage (from the repo root, after analyze.py):
//   node seo/tools/research/summary_pdf.js
// Reads seo/data/western-suburbs-2026-summary.json and seo/data/sample-frame.json and writes
// research/western-suburbs-website-report-2026/western-suburbs-website-report-2026.pdf
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const S = JSON.parse(fs.readFileSync(path.join(ROOT, 'seo/data/western-suburbs-2026-summary.json'), 'utf8'));
const F = JSON.parse(fs.readFileSync(path.join(ROOT, 'seo/data/sample-frame.json'), 'utf8'));
const OUT = path.join(ROOT, 'research/western-suburbs-website-report-2026/western-suburbs-website-report-2026.pdf');
const font = (f) => 'data:font/woff2;base64,' + fs.readFileSync(path.join(ROOT, 'assets/fonts', f)).toString('base64');
const p0 = (x) => `${Math.round(x)}`;

const perf = S.lh_performance, phone = S.phone, https = S.https, sd = S.structured_data;
const basics = [
  ['Phone number shown but not tappable (of sites showing one)', phone.not_tappable_of_shown],
  ['Some phone numbers tappable, others not (of sites showing one)', phone.partly_tappable_of_shown],
  ['Tap targets too small or too close', S.tap_targets_fail.pct],
  ['No local business structured data', 100 - sd.local_business],
  ['No meta description', S.meta_description_missing.pct],
  ['HTTPS broken or sends visitors back to plain HTTP', https.broken + https.downgrades],
  ['A tap-to-call link with a malformed number', phone.malformed_tel_link],
].sort((a, b) => b[1] - a[1]);
const plat = Object.entries(S.platforms).filter(([, v]) => v.n >= 3);
const bar = (label, v, text) => `<div class="row"><span class="lab">${label}</span><span class="track"><span class="b" style="width:${Math.max(0.5, v)}%"></span></span><span class="val">${text}</span></div>`;

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: 'Cormorant Garamond'; font-weight: 300 700; src: url(${font('cormorant-garamond-latin.woff2')}) format('woff2'); }
@font-face { font-family: 'Outfit'; font-weight: 100 900; src: url(${font('outfit-latin.woff2')}) format('woff2'); }
@page { size: Letter; margin: 0.6in 0.65in; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Outfit', sans-serif; color: #171315; font-size: 10.5pt; line-height: 1.5; }
.word { font-family: 'Cormorant Garamond', serif; letter-spacing: 0.2em; text-transform: uppercase; font-size: 11pt; }
.kicker { margin-top: 18pt; color: #6D1A36; font-size: 8.5pt; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 500; }
h1 { font-family: 'Cormorant Garamond', serif; font-weight: 300; font-size: 30pt; line-height: 1.05; margin-top: 4pt; }
h2 { font-family: 'Cormorant Garamond', serif; font-weight: 400; font-size: 16pt; margin: 16pt 0 6pt; }
p { color: #3d3539; }
.lede { font-family: 'Cormorant Garamond', serif; font-size: 13.5pt; line-height: 1.35; color: #171315; margin-top: 8pt; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8pt; margin-top: 14pt; }
.stat { border: 0.75pt solid #E8E2E4; border-radius: 4pt; padding: 8pt; background: #F3EFEA; }
.fig { display: block; font-size: 24pt; font-weight: 300; line-height: 1; }
.cap { display: block; margin-top: 5pt; font-size: 8.5pt; line-height: 1.35; color: #6A6266; }
.row { display: grid; grid-template-columns: 52% 1fr 34pt; align-items: center; gap: 6pt; margin: 4pt 0; font-size: 9pt; }
.track { height: 9pt; border-left: 0.75pt solid #CFC6CA; }
.b { display: block; height: 100%; background: #6D1A36; border-radius: 0 2pt 2pt 0; }
.val { text-align: right; font-variant-numeric: tabular-nums; }
ol { margin: 4pt 0 0 14pt; } li { margin: 3pt 0; color: #3d3539; }
.small { font-size: 8.5pt; color: #6A6266; }
.foot { margin-top: 14pt; padding-top: 8pt; border-top: 2pt solid #6D1A36; font-size: 8.5pt; color: #6A6266; }
.page2 { break-before: page; }
</style></head><body>
<div class="word">Elimenti</div>
<div class="kicker">Western suburbs website report · 2026</div>
<h1>How local business websites hold up on a phone</h1>
<p class="lede">We tested the websites of ${S.sample_size} independent businesses from the Hinsdale and Oak Brook chambers of commerce, the way customers see them: on a phone.</p>
<div class="stats">
  <div class="stat"><span class="fig">${perf.median}</span><span class="cap">Median mobile performance score out of 100 (${perf.n} sites)</span></div>
  <div class="stat"><span class="fig">${p0(perf.poor_under_50)}%</span><span class="cap">Scored under 50, the range Lighthouse labels poor</span></div>
  <div class="stat"><span class="fig">${S.lcp.median_s} s</span><span class="cap">Median time for the largest content to appear, simulated phone</span></div>
  <div class="stat"><span class="fig">${p0(phone.not_tappable_of_shown)}%</span><span class="cap">Of sites showing a phone number didn't make it tappable</span></div>
</div>
<h2>The basics, and how often they were missed</h2>
${basics.map(([l, v]) => bar(l, v, p0(v) + '%')).join('')}
<h2>What they're built on</h2>
${plat.map(([k, v]) => bar(k === 'No builder detected' ? 'No builder detected (custom or less common)' : k, v.pct, p0(v.pct) + '%')).join('')}
<p class="small">Share of the ${S.loaded} sites that loaded in our phone test.</p>
<div class="page2">
<h2>What owners should fix first</h2>
<ol>
<li><strong>Make the phone number tappable.</strong> A tel: link turns it into a call with one tap.</li>
<li><strong>Check the tap-to-call link dials.</strong> ${p0(phone.malformed_tel_link)}% of sites had one with a malformed number.</li>
<li><strong>Put hours, address and phone in text,</strong> matching your Google Business Profile, and add local business structured data.</li>
<li><strong>Fix HTTPS.</strong> Usually a certificate renewal or a hosting setting.</li>
<li><strong>Write a meta description,</strong> the sentence a search result shows under your name.</li>
<li><strong>Cut page weight.</strong> The median homepage downloaded ${(S.page_weight.median_kb / 1024).toFixed(1)} MB. Resize and compress photos, and remove unused plugins and widgets.</li>
</ol>
<h2>How we did this</h2>
<p>Businesses listed in the public online member directories of the Hinsdale Chamber of Commerce and the Greater Oak Brook Chamber of Commerce, read on November 4, 2026 (${F.steps.directory_listings} listings). We kept independent businesses with their own website and a listed address in Hinsdale, Oak Brook or a neighboring suburb, leaving out chains, franchises, banks, public bodies, nonprofits and web agencies (${F.steps.unique_websites} websites), and drew a random sample of ${F.steps.sample}. Each homepage was tested with Lighthouse 13.6.0 on mobile settings, three runs per site, median reported, and checked as a phone for phone links, contact links, copyright year, structured data, HTTPS and platform. These are lab tests on one day, not measurements of real visits. No business is named; we publish totals and shares only.</p>
<h2>Use these findings</h2>
<p>Free to cite and republish with credit under Creative Commons Attribution 4.0: "Elimenti, Western Suburbs Website Report 2026." The full report, charts and method: elimenti.com/research/western-suburbs-website-report-2026/</p>
<div class="foot">Elimenti · WordPress and custom-coded websites · Hinsdale, IL · (630) 509-8822 · hello@elimenti.com · elimenti.com</div>
</div>
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: OUT, format: 'Letter', printBackground: true,
    displayHeaderFooter: false, preferCSSPageSize: true });
  await browser.close();
  console.log('PDF written:', path.relative(ROOT, OUT), fs.statSync(OUT).size, 'bytes');
})();
