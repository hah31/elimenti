#!/usr/bin/env python3
"""Submit URLs to IndexNow (Bing, Yandex, Seznam, Naver and other participants).

Run after a deploy, once the key file is live at https://elimenti.com/<key>.txt:
    python3 seo/tools/indexnow.py                      # all sitemap URLs
    python3 seo/tools/indexnow.py /pricing/            # just these paths
    python3 seo/tools/indexnow.py --changed BEFORE AFTER [--wait-for-pages]
        # the pages whose HTML files changed between two commits; used by
        # .github/workflows/indexnow.yml on every push to main
Endpoint and payload per https://www.indexnow.org/documentation
"""
import glob
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HOST = 'elimenti.com'
ENDPOINT = 'https://api.indexnow.org/indexnow'
# Never published (Jekyll excludes them) or never meant for search.
SKIP_PREFIXES = ('seo/', 'concepts/', '.github/')

key_files = [os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.txt'))
             if re.fullmatch(r'[0-9a-f]{32}\.txt', os.path.basename(f))]
if len(key_files) != 1:
    sys.exit('Expected exactly one IndexNow key file (32 hex chars + .txt) at the repo root')
KEY = key_files[0][:-4]


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True)


def url_for(rel):
    if rel == 'index.html':
        return f'https://{HOST}/'
    if rel.endswith('/index.html'):
        return f'https://{HOST}/{rel[:-len("index.html")]}'
    return f'https://{HOST}/{rel}'


def changed_urls(before, after):
    """URLs of the .html files added, changed or deleted between two commits."""
    if not before or set(before) == {'0'} or git('cat-file', '-e', f'{before}^{{commit}}').returncode:
        print(f'Base commit {before or "(none)"} not available; comparing with the parent of {after}')
        before = f'{after}~1'
    diff = git('diff', '--name-status', '--no-renames', before, after, '--', '*.html')
    if diff.returncode:
        sys.exit(f'git diff failed: {diff.stderr.strip()}')
    urls = []
    for line in diff.stdout.splitlines():
        status, rel = line.split('\t', 1)
        if rel.startswith(SKIP_PREFIXES):
            continue
        path = os.path.join(ROOT, rel)
        if status != 'D' and os.path.exists(path):
            head = open(path, encoding='utf-8', errors='replace').read(4000)
            if re.search(r'<meta name="robots" content="[^"]*noindex', head):
                continue  # 404, thanks and concept pages: nothing to index
        urls.append(url_for(rel))
    return sorted(set(urls))


def wait_for_pages(sha, timeout=900):
    """Wait until GitHub Pages reports a finished build of this commit, so search engines
    that crawl right away get the new pages. Gives up after `timeout` seconds and submits anyway."""
    repo, token = os.environ.get('GITHUB_REPOSITORY'), os.environ.get('GITHUB_TOKEN')
    if not (repo and token):
        print('No GITHUB_REPOSITORY/GITHUB_TOKEN; waiting 120 s for the deploy instead')
        time.sleep(120)
        return
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/pages/builds/latest',
                                 headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json'})
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                build = json.load(r)
            print(f'Pages build: status={build.get("status")} commit={str(build.get("commit"))[:7]}')
            if build.get('commit') == sha and build.get('status') == 'built':
                time.sleep(30)  # let the CDN pick up the new files
                return
            if build.get('commit') == sha and build.get('status') == 'errored':
                sys.exit('GitHub Pages build failed for this commit; not submitting')
        except urllib.error.HTTPError as e:
            print(f'Pages API HTTP {e.code}; waiting 120 s for the deploy instead')
            time.sleep(120)
            return
        except Exception as e:  # noqa: BLE001 - network hiccup, try again
            print(f'Pages API error: {e}')
        time.sleep(20)
    print('Timed out waiting for the Pages build; submitting anyway')


def submit(urls):
    payload = {'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}
    print('Submitting:\n  ' + '\n  '.join(urls))
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f'IndexNow response: HTTP {r.status} ({len(urls)} URLs)')
    except urllib.error.HTTPError as e:
        print(f'IndexNow response: HTTP {e.code}: {e.read().decode()[:300]}')
        sys.exit(1)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[:1] == ['--changed']:
        before, after = args[1], args[2]
        urls = changed_urls(before, after)
        if not urls:
            print('No published HTML pages changed in this push; nothing to submit')
            sys.exit(0)
        if '--wait-for-pages' in args:
            wait_for_pages(after)
    elif args:
        urls = [f'https://{HOST}{p}' for p in args]
    else:
        urls = re.findall(r'<loc>([^<]+)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read())
    submit(urls)
