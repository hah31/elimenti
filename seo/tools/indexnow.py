#!/usr/bin/env python3
"""Submit every sitemap URL to IndexNow (Bing, Yandex, Seznam, Naver and other participants).

Run after a deploy, once the key file is live at https://elimenti.com/<key>.txt:
    python3 seo/tools/indexnow.py            # all sitemap URLs
    python3 seo/tools/indexnow.py /pricing/  # just these paths
Endpoint and payload per https://www.indexnow.org/documentation
"""
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HOST = 'elimenti.com'
key_files = [os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '*.txt'))
             if re.fullmatch(r'[0-9a-f]{32}\.txt', os.path.basename(f))]
if len(key_files) != 1:
    sys.exit('Expected exactly one IndexNow key file (32 hex chars + .txt) at the repo root')
KEY = key_files[0][:-4]

if len(sys.argv) > 1:
    urls = [f'https://{HOST}{p}' for p in sys.argv[1:]]
else:
    urls = re.findall(r'<loc>([^<]+)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read())

payload = {'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=json.dumps(payload).encode(),
                             headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f'HTTP {r.status}: {len(urls)} URLs submitted')
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:300]}')
    sys.exit(1)
