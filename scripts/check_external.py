#!/usr/bin/env python3
"""Check outbound (external) links in the built site (_site/).

Collects every <a href="https://..."> that leaves this site, fetches each
unique URL once (HEAD, falling back to a small GET), and reports links that
are clearly dead: 404/410, or a host that no longer resolves.

Anything ambiguous — 403/429 bot walls, 5xx, timeouts — is only listed in a
notice, because those flake. Share-intent links and sites that block bots
outright (LinkedIn, X, ...) are skipped. A hard time budget keeps the step
short. Never blocks a deploy: exit code is always 0 unless --strict.

Usage: python3 scripts/check_external.py [_site] [--strict] [--budget SECONDS]
"""
import os
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import TimeoutError as FutureTimeout
from html.parser import HTMLParser
from urllib.parse import urlsplit, urldefrag

SITE_HOSTS = {"www.avinashgosavi.com", "avinashgosavi.com"}
# Hosts that answer bots with 999/403/login walls whatever the link is.
SKIP_HOSTS = {
    "linkedin.com", "x.com", "twitter.com", "facebook.com", "instagram.com",
    "bsky.app", "news.ycombinator.com", "medium.com", "localhost", "example.com",
}
# Per-post "Suggest an edit" / history links (_includes/suggest-edit.html) are
# built from page.path, so they always point at a real file; /edit/ also needs
# a login. Skipping them keeps ~60 URLs out of the time budget.
SKIP_PREFIXES = (
    "https://github.com/aag1091-alt/avinashgosavi.com/edit/",
    "https://github.com/aag1091-alt/avinashgosavi.com/commits/",
)
UA = ("Mozilla/5.0 (compatible; avinashgosavi.com-linkcheck/1.0; "
      "+https://www.avinashgosavi.com/)")
TIMEOUT = 12
WORKERS = 16


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href") or ""
            if href.startswith(("http://", "https://")):
                self.hrefs.append(href)


def skipped(host):
    host = host.lower()
    return any(host == h or host.endswith("." + h) for h in SKIP_HOSTS | SITE_HOSTS)


def collect(site):
    urls = {}  # url -> set(page paths)
    for root, _, files in os.walk(site):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            page = "/" + os.path.relpath(path, site).replace("index.html", "")
            p = Links()
            with open(path, encoding="utf-8", errors="replace") as f:
                p.feed(f.read())
            for href in p.hrefs:
                url = urldefrag(href)[0]
                host = urlsplit(url).hostname or ""
                if not host or skipped(host) or url.startswith(SKIP_PREFIXES):
                    continue
                urls.setdefault(url, set()).add(page)
    return urls


def fetch(url):
    """Return (status, detail). status: int HTTP code, or 'dns'/'error'."""
    last = None
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={
            "User-Agent": UA, "Accept": "text/html,*/*;q=0.8", "Range": "bytes=0-1023"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status, ""
        except urllib.error.HTTPError as e:
            last = (e.code, "")
            if method == "HEAD" and e.code not in (404, 410):
                continue  # many servers mishandle HEAD; confirm with GET
            return last
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.gaierror):
                return "dns", str(e.reason)
            last = ("error", str(e.reason))
        except Exception as e:  # timeouts, resets, TLS
            last = ("error", type(e).__name__)
    return last


def main():
    args = sys.argv[1:]
    strict = "--strict" in args
    budget = 150
    if "--budget" in args:
        budget = int(args[args.index("--budget") + 1])
    site = next((a for a in args if not a.startswith("--") and not a.isdigit()), "_site")

    urls = collect(site)
    dead, unsure, ok, done = [], [], 0, 0
    pool = ThreadPoolExecutor(WORKERS)
    futs = {pool.submit(fetch, u): u for u in sorted(urls)}
    try:
        for fut in as_completed(futs, timeout=budget):
            u = futs[fut]
            done += 1
            status, detail = fut.result()
            if status in (404, 410) or status == "dns":
                dead.append((u, status, detail))
            elif isinstance(status, int) and status < 400:
                ok += 1
            else:
                unsure.append((u, status, detail))
    except FutureTimeout:
        pass
    unchecked = len(futs) - done
    pool.shutdown(wait=False, cancel_futures=True)

    for u, status, detail in sorted(dead):
        pages = ", ".join(sorted(urls[u])[:3])
        why = "host not found" if status == "dns" else "HTTP %s" % status
        print("::warning title=Dead external link::%s (%s) on %s" % (u, why, pages))
    if unsure:
        print("::group::Couldn't verify (bot walls, server errors, timeouts — usually fine)")
        for u, status, detail in sorted(unsure, key=lambda x: x[0]):
            print("  %s  %s %s" % (status, u, detail))
        print("::endgroup::")
    print("::notice title=External links::%d unique URLs on %d pages — %d ok, %d dead, "
          "%d unverified, %d over the %ds budget"
          % (len(urls), len({p for s in urls.values() for p in s}), ok, len(dead),
             len(unsure), unchecked, budget))
    sys.stdout.flush()
    os._exit(1 if strict and dead else 0)  # don't wait on threads still fetching past the budget


if __name__ == "__main__":
    main()
