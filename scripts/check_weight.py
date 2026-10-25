#!/usr/bin/env python3
"""Page-weight budget for the built site (warnings only; CI never blocks a deploy on it).

For every HTML page, estimate what a first visit downloads before the reader
scrolls: the page itself, its same-origin stylesheets and scripts, preloaded
fonts, and every image that is NOT loading="lazy". Text files are counted
gzipped (GitHub Pages compresses them); images and fonts as-is. For an image
with a srcset (or a <picture> with <source>s) the largest candidate is
counted, so the number is a worst case (wide, high-DPI screen).

Warnings (::warning):
  - a page's first-load weight is over PAGE_BUDGET
  - an eager (not lazy) image is over EAGER_IMAGE_BUDGET
  - any local image a page uses (lazy or not) is over IMAGE_BUDGET
  - a page's own HTML is over HTML_BUDGET gzipped
  - a referenced local file is missing (the link checker covers <a>; this covers src/srcset/href of assets)
Then one ::notice with the five heaviest pages. Third-party requests (analytics)
are listed in the notice but not counted. Usage: check_weight.py _site"""
import glob, gzip, html.parser, os, re, sys
from urllib.parse import urlsplit, unquote

root = sys.argv[1] if len(sys.argv) > 1 else "_site"
KB = 1024
PAGE_BUDGET = 500 * KB
EAGER_IMAGE_BUDGET = 150 * KB
IMAGE_BUDGET = 250 * KB
HTML_BUDGET = 60 * KB
SITE_HOSTS = {"www.avinashgosavi.com", "avinashgosavi.com"}
TEXT_EXT = {".html", ".css", ".js", ".svg", ".json", ".xml", ".txt"}

warn = lambda f, m: print(f"::warning file={f}::{m}")
note = lambda m: print(f"::notice title=page weight::{m}")
fmt = lambda n: f"{n / KB:.0f} KB"

_size_cache = {}
def wire_size(path):
    """Bytes on the wire: gzip -6 for text types, raw for the rest."""
    if path not in _size_cache:
        data = open(path, "rb").read()
        if os.path.splitext(path)[1].lower() in TEXT_EXT:
            _size_cache[path] = len(gzip.compress(data, 6))
        else:
            _size_cache[path] = len(data)
    return _size_cache[path]

def local_path(url, page_dir):
    """Map a URL in the page to a file under root, or None if it is off-site / not a file."""
    url = url.strip()
    if not url or url.startswith(("data:", "#", "mailto:", "javascript:")):
        return None
    u = urlsplit(url)
    if u.scheme and u.scheme not in ("http", "https"):
        return None
    if u.netloc and u.netloc.lower() not in SITE_HOSTS:
        return "EXTERNAL:" + u.netloc
    p = unquote(u.path)
    if not p:
        return None
    full = os.path.join(root, p.lstrip("/")) if p.startswith("/") else os.path.join(page_dir, p)
    full = os.path.normpath(full)
    if os.path.isdir(full):
        full = os.path.join(full, "index.html")
    return full

def srcset_urls(value):
    return [c.strip().split()[0] for c in (value or "").split(",") if c.strip()]

class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.css, self.js, self.fonts = [], [], []
        self.images = []  # (candidate urls, eager?)
        self.sources = []  # <source> srcsets inside the current <picture>
        self.in_picture = False
        self.in_pre = 0  # skip code samples that quote HTML

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag in ("pre", "code"):
            self.in_pre += 1
        if self.in_pre:
            return
        if tag == "link":
            rel = a.get("rel", "").lower().split()
            if "stylesheet" in rel:
                self.css.append(a.get("href", ""))
            elif "preload" in rel and a.get("as") == "font":
                self.fonts.append(a.get("href", ""))
            elif "preload" in rel and a.get("as") in ("style", "script", "image"):
                (self.css if a["as"] == "style" else self.js if a["as"] == "script" else self.fonts).append(a.get("href", ""))
        elif tag == "script" and a.get("src"):
            self.js.append(a["src"])
        elif tag == "picture":
            self.in_picture, self.sources = True, []
        elif tag == "source" and self.in_picture:
            self.sources += srcset_urls(a.get("srcset"))
        elif tag == "img":
            cands = list(self.sources) if self.in_picture else []
            cands += srcset_urls(a.get("srcset"))
            if a.get("src"):
                cands.append(a["src"])
            if cands:
                self.images.append((cands, a.get("loading", "").lower() != "lazy", bool(self.in_picture and self.sources)))

    def handle_endtag(self, tag):
        if tag in ("pre", "code") and self.in_pre:
            self.in_pre -= 1
        elif tag == "picture":
            self.in_picture, self.sources = False, []

problems, totals, external = 0, [], set()
pages = sorted(glob.glob(os.path.join(root, "**", "*.html"), recursive=True))
for path in pages:
    rel = os.path.relpath(path, root)
    page_dir = os.path.dirname(path)
    doc = open(path, encoding="utf-8").read()
    if re.search(r'<meta\s+http-equiv="refresh"', doc, re.I):
        continue  # redirect stub
    p = Page()
    try:
        p.feed(doc)
    except Exception as e:  # never let one odd page stop the run
        warn(rel, f"could not parse for page weight: {e}")
        continue
    seen, total = set(), wire_size(path)
    if total > HTML_BUDGET:
        problems += 1
        warn(rel, f"HTML is {fmt(total)} gzipped (budget {fmt(HTML_BUDGET)})")

    def add(url, kind):
        global problems
        f = local_path(url, page_dir)
        if f is None:
            return 0
        if f.startswith("EXTERNAL:"):
            external.add(f[9:])
            return 0
        if f in seen:
            return 0
        seen.add(f)
        if not os.path.isfile(f):
            problems += 1
            warn(rel, f"{kind} {url} is missing from the built site")
            return 0
        return wire_size(f)

    for u in p.css:
        total += add(u, "stylesheet")
    for u in p.js:
        total += add(u, "script")
    for u in p.fonts:
        total += add(u, "preloaded file")
    for cands, eager, picture_sources in p.images:
        # Browsers take a <picture> <source> when one exists, so the <img src> fallback isn't fetched.
        fetched = cands[:-1] if picture_sources and len(cands) > 1 else cands
        sizes = []
        for u in fetched:
            f = local_path(u, page_dir)
            if f is None or f.startswith("EXTERNAL:"):
                if f:
                    external.add(f[9:])
                continue
            if not os.path.isfile(f):
                problems += 1
                warn(rel, f"image {u} is missing from the built site")
                continue
            sizes.append((wire_size(f), u, f))
        if not sizes:
            continue
        biggest = max(sizes)
        if biggest[0] > IMAGE_BUDGET:
            problems += 1
            warn(rel, f"image {biggest[1]} is {fmt(biggest[0])} (budget {fmt(IMAGE_BUDGET)}) — resize or convert to WebP")
        if eager:
            if biggest[0] > EAGER_IMAGE_BUDGET:
                problems += 1
                warn(rel, f"image {biggest[1]} loads eagerly at {fmt(biggest[0])} (budget {fmt(EAGER_IMAGE_BUDGET)}) — add loading=\"lazy\" if it is below the fold, or shrink it")
            if biggest[2] not in seen:
                seen.add(biggest[2])
                total += biggest[0]
    if total > PAGE_BUDGET:
        problems += 1
        warn(rel, f"first-load weight is {fmt(total)} (budget {fmt(PAGE_BUDGET)})")
    totals.append((total, rel))

totals.sort(reverse=True)
top = ", ".join(f"{r} {fmt(t)}" for t, r in totals[:5])
note(f"{len(totals)} pages; heaviest first loads: {top}; third-party hosts not counted: {', '.join(sorted(external)) or 'none'}; {problems} over budget")
sys.exit(1 if problems else 0)
