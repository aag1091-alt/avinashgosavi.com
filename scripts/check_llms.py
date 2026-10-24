#!/usr/bin/env python3
"""Keep /llms.txt in step with the real site (warnings only; CI never blocks a deploy on it).

Checks the built site for:
  - every URL in sitemap.xml that /llms.txt doesn't list (a new page nobody added
    to the "Pages" section, so AI agents reading llms.txt never learn about it)
  - every on-site URL in /llms.txt or /llms-full.txt that doesn't resolve to a
    built file (a page that was renamed or removed)

Problems are ::warning annotations plus a list in the job summary.
Usage: check_llms.py _site [--strict]"""
import os, re, sys, xml.etree.ElementTree as ET
from urllib.parse import urlsplit, unquote

args = [a for a in sys.argv[1:] if not a.startswith("--")]
root = args[0] if args else "_site"
strict = "--strict" in sys.argv
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
HOSTS = {"www.avinashgosavi.com", "avinashgosavi.com"}
URL = re.compile(r"https?://[^\s)<>\"'\]]+")


def norm(path):
    """/post/x/index.html, /post/x and /post/x/ all mean the same page."""
    path = unquote(path or "/")
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    elif path.endswith(".html"):  # /about.html and /about/ are the same page
        path = path[: -len(".html")] + "/"
    if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path += "/"
    return path


def exists(path):
    rel = unquote(path).lstrip("/")
    full = os.path.join(root, rel)
    if path.endswith("/"):
        return os.path.isfile(os.path.join(full, "index.html")) or os.path.isfile(full.rstrip("/") + ".html")
    return os.path.isfile(full) or os.path.isfile(full + ".html") or os.path.isfile(os.path.join(full, "index.html"))


def site_paths(text):
    out = []
    for u in URL.findall(text):
        u = u.rstrip(".,;:")
        p = urlsplit(u)
        if p.hostname in HOSTS:
            out.append(p.path or "/")
    return out


problems = []
llms_file = os.path.join(root, "llms.txt")
if not os.path.isfile(llms_file):
    problems.append(("llms.txt", "/llms.txt was not built"))
    listed = set()
else:
    listed = {norm(p) for p in site_paths(open(llms_file, encoding="utf-8").read())}

# 1. Sitemap pages missing from llms.txt.
sitemap = os.path.join(root, "sitemap.xml")
urls = []
if os.path.isfile(sitemap):
    urls = [e.text.strip() for e in ET.parse(sitemap).getroot().iter(NS + "loc") if e.text]
for u in urls:
    p = norm(urlsplit(u).path)
    if p == "/" or p in listed:
        continue
    problems.append(("llms.txt", f"{p} is in sitemap.xml but not listed in /llms.txt — add it to the Pages section"))

# 2. Dead on-site links in llms.txt / llms-full.txt.
for name in ("llms.txt", "llms-full.txt"):
    f = os.path.join(root, name)
    if not os.path.isfile(f):
        continue
    seen = set()
    for p in site_paths(open(f, encoding="utf-8").read()):
        if p in seen:
            continue
        seen.add(p)
        if not exists(p):
            problems.append((name, f"links {p}, which isn't a page on the built site"))

for f, m in problems:
    print(f"::warning file={f},title=llms.txt::{m}")

summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a", encoding="utf-8") as s:
        s.write(f"### llms.txt check\n\n{len(urls)} sitemap URLs, {len(listed)} site URLs in llms.txt, {len(problems)} problem(s).\n\n")
        for f, m in problems:
            s.write(f"- `{f}`: {m}\n")

print(f"Checked {len(urls)} sitemap URLs against {len(listed)} llms.txt links: {len(problems)} problem(s).")
sys.exit(1 if problems and strict else 0)
