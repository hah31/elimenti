// Generate a 1200x630 Open Graph card for every page in the registry.
// Each card shows the page's H1 in the site's type, colors and logo mark.
//
// Usage (from the repo root, after `python3 seo/tools/build.py`):
//   node seo/tools/og.js
// Needs Playwright with Chromium. Output: assets/img/og/<slug>.png
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..', '..');
const OUT = path.join(ROOT, 'assets/img/og');
fs.mkdirSync(OUT, { recursive: true });

// Page list and H1s come from the registry and the built pages.
const pages = JSON.parse(execFileSync('python3', [path.join(__dirname, 'pages_json.py')], { encoding: 'utf8' }));

const font = (f) => 'data:font/woff2;base64,' + fs.readFileSync(path.join(ROOT, 'assets/fonts', f)).toString('base64');
const logo = 'data:image/webp;base64,' + fs.readFileSync(path.join(ROOT, 'assets/img/logo-720.webp')).toString('base64');

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
// Keep hyphenated words ("high-end") on one line.
const nobreak = (s) => esc(s).replace(/(\S+-\S+)/g, '<span style="white-space:nowrap">$1</span>');

const card = (title, kicker) => `<!doctype html><html><head><style>
@font-face { font-family: 'Cormorant Garamond'; font-weight: 300 700; src: url(${font('cormorant-garamond-latin.woff2')}) format('woff2'); }
@font-face { font-family: 'Outfit'; font-weight: 100 900; src: url(${font('outfit-latin.woff2')}) format('woff2'); }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1200px; height: 630px; background: #FAF8F5; color: #171315; font-family: 'Outfit', sans-serif; position: relative; overflow: hidden; }
.frame { position: absolute; inset: 0; border-bottom: 10px solid #6D1A36; }
.word { position: absolute; top: 64px; left: 80px; font-family: 'Cormorant Garamond', serif; font-size: 26px; letter-spacing: 0.22em; text-transform: uppercase; }
.kicker { position: absolute; top: 160px; left: 80px; font-size: 18px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: #6D1A36; }
h1 { position: absolute; top: 200px; left: 80px; width: 760px; font-family: 'Cormorant Garamond', serif; font-weight: 300; font-size: ${title.length > 48 ? 60 : 72}px; line-height: 1.04; letter-spacing: -0.02em; }
.foot { position: absolute; bottom: 58px; left: 80px; font-size: 21px; color: #6A6266; letter-spacing: 0.02em; }
.mark { position: absolute; right: 70px; top: 50%; transform: translateY(-50%); width: 300px; opacity: 0.95; }
</style></head><body><div class="frame"></div>
<div class="word">Elimenti</div>
<div class="kicker">${esc(kicker)}</div>
<h1>${nobreak(title)}</h1>
<div class="foot">Custom-coded websites · Hinsdale and Oak Brook, IL · elimenti.com</div>
<img class="mark" src="${logo}" alt="">
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  for (const p of pages) {
    await page.setContent(card(p.h1, p.kicker), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(OUT, p.slug + '.png') });
  }
  await browser.close();
  // Palette-compress the PNGs (flat colors, so 256 colors is visually lossless).
  execFileSync('python3', ['-c', `
import glob
from PIL import Image
for f in glob.glob(${JSON.stringify(OUT)} + '/*.png'):
    Image.open(f).convert('RGB').quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(f, optimize=True)
`]);
  console.log(`${pages.length} cards written to assets/img/og/`);
})();
