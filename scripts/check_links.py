#!/usr/bin/env python3
"""Check internal links in the built site (_site/).

Looks at every href/src in every HTML file and makes sure links that stay on
this site point at a real file, and that #fragments point at a real id on the
target page. External links are never fetched (they flake), so this runs
offline in a second or two.

Usage: python3 scripts/check_links.py [_site] [--strict]
Exit code is 1 with --strict when anything is broken, else always 0.
Prints GitHub Actions ::warning annotations so problems show on the run page.
"""
import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

SITE_HOSTS = {"www.avinashgosavi.com", "avinashgosavi.com"}
SKIP_SCHEMES = {"mailto", "tel", "javascript", "data", "sms"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []  # (attr, value, line)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("id", "name"):
            if a.get(key) and (key == "id" or tag == "a"):
                self.ids.add(a[key])
        if a.get("data-tag"):  # /blog/#tag opens the blog filtered by that tag (JS)
            self.ids.add(a["data-tag"])
        line = self.getpos()[0]
        if tag in ("a", "link", "area") and a.get("href"):
            # rel=preconnect/dns-prefetch etc. point at hosts, not pages
            if tag == "link" and a.get("rel", "") in ("preconnect", "dns-prefetch"):
                return
            self.links.append(("href", a["href"], line))
        if tag in ("img", "script", "source", "iframe", "audio", "video") and a.get("src"):
            self.links.append(("src", a["src"], line))
        if tag in ("img", "source") and a.get("srcset"):
            # "a.webp 280w, b.webp 560w" -> each candidate URL must exist
            for cand in a["srcset"].split(","):
                if cand.strip():
                    self.links.append(("srcset", cand.split()[0], line))

    handle_startendtag = handle_starttag


def resolve(site, page_rel, path):
    """Map a URL path to a file under site, or None."""
    if not path.startswith("/"):
        base = os.path.dirname("/" + page_rel)
        path = os.path.normpath(os.path.join(base, path)) + ("/" if path.endswith("/") else "")
    path = unquote(path)
    full = os.path.join(site, path.lstrip("/"))
    candidates = [os.path.join(full, "index.html")] if path.endswith("/") else [
        full, full + ".html", os.path.join(full, "index.html")]
    for c in candidates:
        if os.path.isfile(c):
            return os.path.relpath(c, site)
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    site = args[0] if args else "_site"
    pages = {}
    for root, _, files in os.walk(site):
        for f in files:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(root, f), site)
                p = Page()
                with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                    p.feed(fh.read())
                pages[rel] = p

    problems = []
    checked = 0
    for rel, page in sorted(pages.items()):
        for attr, url, line in page.links:
            url = url.strip()
            if not url or url.startswith("{{") or "{%" in url:
                continue
            parts = urlsplit(url)
            if parts.scheme in SKIP_SCHEMES:
                continue
            if parts.scheme or parts.netloc:
                if parts.netloc.lower() not in SITE_HOSTS:
                    continue  # external: not checked
            checked += 1
            if not parts.path:  # same-page "#frag"
                target = rel
            else:
                target = resolve(site, rel, parts.path)
                if target is None:
                    problems.append((rel, line, url, "no such page or file"))
                    continue
            frag = unquote(parts.fragment)
            if frag and frag != "top" and target in pages and frag not in pages[target].ids:
                problems.append((rel, line, url, f"no id=\"{frag}\" on {target}"))

    for rel, line, url, why in problems:
        print(f"::warning file={rel},line={line}::Broken internal link {url} ({why})")
    summary = f"Checked {checked} internal links on {len(pages)} pages: {len(problems)} broken."
    print(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):  # full list (annotations are capped at 10)
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
            fh.write(f"### Internal links\n\n{summary}\n\n")
            for rel, line, url, why in problems:
                fh.write(f"- `{rel}` line {line}: `{url}` ({why})\n")
    if problems and strict:
        sys.exit(1)


if __name__ == "__main__":
    main()
