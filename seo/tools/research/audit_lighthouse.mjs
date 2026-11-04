// Step 3a of the western suburbs website study: Lighthouse, mobile, three runs per site.
//
// Usage:
//   LH_MODULES=/path/with/node_modules node seo/tools/research/audit_lighthouse.mjs SAMPLE.json OUT.jsonl
// SAMPLE.json is a list of {id, url}. OUT.jsonl gets one line per site; sites already in
// OUT.jsonl are skipped, so the script can be stopped and restarted.
//
// Needs: npm install lighthouse@13.6.0 chrome-launcher (in LH_MODULES), Chromium in CHROME_PATH.
// Settings: Lighthouse defaults for mobile (emulated Moto G Power, simulated throttling:
// 150 ms RTT, 1.6 Mbps down, 4x CPU slowdown). One Chrome per run, runs strictly one at a time.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const LH_MODULES = process.env.LH_MODULES || process.cwd();
const req = createRequire(path.join(LH_MODULES, 'noop.js'));
const lighthouse = (await import(pathToFileURL(req.resolve('lighthouse')).href)).default;
const chromeLauncher = await import(pathToFileURL(req.resolve('chrome-launcher')).href);

const [samplePath, outPath] = process.argv.slice(2);
const RUNS = Number(process.env.RUNS || 3);
const sample = JSON.parse(fs.readFileSync(samplePath, 'utf8'));
const done = new Set(fs.existsSync(outPath)
  ? fs.readFileSync(outPath, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l).id) : []);

const flags = ['--headless=new', '--no-sandbox', '--disable-gpu'];
// All traffic through the session's HTTPS proxy, which only tunnels https.
if (process.env.HTTPS_PROXY) flags.push(`--proxy-server=${process.env.HTTPS_PROXY}`);

const AUDITS = ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time',
  'cumulative-layout-shift', 'speed-index', 'total-byte-weight', 'server-response-time'];
const PASSFAIL = ['is-on-https', 'target-size', 'color-contrast', 'image-alt', 'meta-description',
  'document-title', 'link-text', 'http-status-code', 'is-crawlable', 'errors-in-console', 'deprecations',
  'button-name', 'link-name', 'html-has-lang', 'label'];

async function runOnce(url) {
  const chrome = await chromeLauncher.launch({chromePath: process.env.CHROME_PATH, chromeFlags: flags});
  try {
    const result = await lighthouse(url, {
      port: chrome.port, output: 'json', logLevel: 'error', maxWaitForLoad: 45000,
      onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
    });
    const lhr = result.lhr;
    const out = {
      runtimeError: lhr.runtimeError ? lhr.runtimeError.code : null,
      finalUrl: lhr.finalDisplayedUrl, mainDocumentUrl: lhr.mainDocumentUrl,
      warnings: lhr.runWarnings, benchmarkIndex: lhr.environment.benchmarkIndex,
      lighthouseVersion: lhr.lighthouseVersion, fetchTime: lhr.fetchTime,
      scores: Object.fromEntries(Object.entries(lhr.categories).map(([k, v]) => [k, v.score])),
      metrics: Object.fromEntries(AUDITS.map(a => [a, lhr.audits[a] ? lhr.audits[a].numericValue : null])),
      checks: Object.fromEntries(PASSFAIL.map(a => [a, lhr.audits[a] ? lhr.audits[a].score : null])),
    };
    return out;
  } finally {
    await chrome.kill();
  }
}

const median = (xs) => {
  const v = xs.filter(x => typeof x === 'number').sort((a, b) => a - b);
  return v.length ? v[Math.floor((v.length - 1) / 2)] : null;
};

for (const site of sample) {
  if (done.has(site.id)) continue;
  const runs = [];
  for (let i = 0; i < RUNS; i++) {
    try {
      runs.push(await runOnce(site.url));
    } catch (e) {
      runs.push({runtimeError: 'SCRIPT_ERROR', message: String(e).slice(0, 300)});
    }
  }
  const ok = runs.filter(r => !r.runtimeError && r.scores && typeof r.scores.performance === 'number');
  const pick = (fn) => median(ok.map(fn));
  const summary = {
    id: site.id, url: site.url, runs: runs.length, okRuns: ok.length,
    runtimeErrors: runs.filter(r => r.runtimeError).map(r => r.runtimeError),
    finalUrl: ok.length ? ok[0].finalUrl : null,
    benchmarkIndex: pick(r => r.benchmarkIndex),
    median: ok.length ? {
      performance: pick(r => r.scores.performance), accessibility: pick(r => r.scores.accessibility),
      bestPractices: pick(r => r.scores['best-practices']), seo: pick(r => r.scores.seo),
      ...Object.fromEntries(AUDITS.map(a => [a, pick(r => r.metrics[a])])),
    } : null,
    // pass/fail checks are page properties, not timings: take them from the first good run
    checks: ok.length ? ok[0].checks : null,
    warnings: ok.length ? ok[0].warnings : [],
    lighthouseVersion: ok.length ? ok[0].lighthouseVersion : null,
    fetchTime: ok.length ? ok[0].fetchTime : null,
  };
  fs.appendFileSync(outPath, JSON.stringify(summary) + '\n');
  console.log(`${site.id} perf=${summary.median ? summary.median.performance : 'ERR'} ok=${ok.length}/${runs.length}`);
}
console.log('done');
