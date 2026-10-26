#!/usr/bin/env python3
"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver, ...) which pages
changed in this deploy, so they recrawl them in minutes instead of days.

  diff   python3 scripts/indexnow.py diff _site [LIVE_SITEMAP_URL]
         Compares _site/sitemap.xml with the sitemap that is live right now
         (before deploy) and prints the URLs that are new or whose <lastmod>
         changed, one per line. Prints nothing if the live sitemap can't be
         fetched — never guesses.
  submit python3 scripts/indexnow.py submit FILE
         POSTs those URLs (max 10,000) to api.indexnow.org.

Stdlib only. Never fails the build: problems become ::warning annotations.
The key file lives at the site root (/<KEY>.txt), as the protocol requires.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET

HOST = "www.avinashgosavi.com"
KEY = "cd4471ebd9b322f9b4bc4d7adab382c5"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
UA = "avinashgosavi.com-indexnow/1.0 (+https://www.avinashgosavi.com/)"


def entries(xml_bytes):
    root = ET.fromstring(xml_bytes)
    out = {}
    for u in root.findall(NS + "url"):
        loc = (u.findtext(NS + "loc") or "").strip()
        if loc:
            out[loc] = (u.findtext(NS + "lastmod") or "").strip()
    return out


def warn(msg):
    print("::warning title=IndexNow::" + msg, file=sys.stderr)


def diff(site, live_url):
    new = entries(open(site + "/sitemap.xml", "rb").read())
    try:
        req = urllib.request.Request(live_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            old = entries(r.read())
    except Exception as e:  # network, HTTP or XML error: submit nothing
        warn("could not read live sitemap (%s); nothing will be submitted" % e)
        return
    changed = [loc for loc, mod in new.items() if old.get(loc) != mod]
    changed = [u for u in changed if u.startswith("https://" + HOST + "/")]
    for u in changed:
        print(u)
    print("::notice title=IndexNow::%d of %d sitemap URLs changed since the live deploy"
          % (len(changed), len(new)), file=sys.stderr)


def submit(path):
    urls = [l.strip() for l in open(path) if l.strip()][:10000]
    if not urls:
        print("::notice title=IndexNow::no changed URLs to submit")
        return
    body = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": "https://%s/%s.txt" % (HOST, KEY),
        "urlList": urls,
    }).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=body, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("::notice title=IndexNow::submitted %d URLs (HTTP %d)" % (len(urls), r.status))
    except urllib.error.HTTPError as e:
        warn("HTTP %d submitting %d URLs: %s" % (e.code, len(urls), e.read()[:200]))
    except Exception as e:
        warn("submit failed: %s" % e)
    for u in urls:
        print("  " + u)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "diff":
        diff(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "https://%s/sitemap.xml" % HOST)
    elif len(sys.argv) == 3 and sys.argv[1] == "submit":
        submit(sys.argv[2])
    else:
        sys.exit(__doc__)
