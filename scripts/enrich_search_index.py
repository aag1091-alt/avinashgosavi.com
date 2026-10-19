#!/usr/bin/env python3
"""Fill in body text for Page entries in the built search index.

Jekyll renders search.json before (or alongside) the other pages, so Liquid
can only index a page's title and description. This runs after
`jekyll build`: for every "Page" entry in _site/search.json with empty text,
it reads the built HTML, takes the visible text inside <main>, and stores up
to 8,000 characters of it. Stdlib only, offline.

Usage: python3 scripts/enrich_search_index.py [_site]
The index is only rewritten if everything parsed, so a failure leaves the
original (title + description) index in place.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

MAX_CHARS = 8000
SKIP_TAGS = {"script", "style", "noscript", "svg", "template", "button"}


class MainText(HTMLParser):
    """Collect text inside <main>, skipping scripts, styles, svg and buttons."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = 0
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main += 1
        elif self.in_main and tag in SKIP_TAGS:
            self.skip += 1
        elif self.in_main and tag in ("p", "li", "h1", "h2", "h3", "h4", "td", "th", "br", "div", "dt", "dd"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag == "main" and self.in_main:
            self.in_main -= 1
        elif self.in_main and tag in SKIP_TAGS and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self.in_main and not self.skip:
            self.parts.append(data)

    def text(self):
        return re.sub(r"\s+", " ", "".join(self.parts)).strip()


def html_path(site, url):
    path = url.split("#", 1)[0].split("?", 1)[0].lstrip("/")
    candidates = [os.path.join(site, path, "index.html")] if path == "" or path.endswith("/") else [
        os.path.join(site, path),
        os.path.join(site, path + ".html"),
        os.path.join(site, path, "index.html"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def main():
    site = sys.argv[1] if len(sys.argv) > 1 else "_site"
    index_file = os.path.join(site, "search.json")
    with open(index_file, encoding="utf-8") as f:
        index = json.load(f)

    filled, missing = 0, []
    for item in index:
        if item.get("type") != "Page" or item.get("text"):
            continue
        src = html_path(site, item.get("url", ""))
        if not src:
            missing.append(item.get("url"))
            continue
        parser = MainText()
        with open(src, encoding="utf-8") as f:
            parser.feed(f.read())
        text = parser.text()
        # The page title is already weighted separately; drop it from the front.
        title = item.get("title", "")
        if title and text.startswith(title):
            text = text[len(title):].lstrip(" —:-")
        item["text"] = text[:MAX_CHARS]
        filled += 1

    tmp = index_file + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, index_file)

    print(f"search index: filled text for {filled} pages; {len(index)} entries total")
    for url in missing:
        print(f"::warning::search index: no built HTML found for {url}")


if __name__ == "__main__":
    main()
