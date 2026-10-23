#!/usr/bin/env python3
"""SEO lint for the built site (warnings only; CI never blocks a deploy on it).

For every HTML page that search engines may index, check:
  - exactly one non-empty <title>, and no other page shares it
  - a meta description, not shared with another page
  - a <link rel="canonical">
  - exactly one <h1>
Long titles (> 70 chars) and descriptions (> 160 chars, where search results
usually cut off) are reported as ::notice lines, not warnings.

Pages with <meta name="robots" content="noindex..."> or a meta refresh
(redirect stubs) are skipped. Usage: check_seo.py _site"""
import collections, glob, html, os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else "_site"
TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
CANON = re.compile(r'<link\s+rel="canonical"', re.I)
H1 = re.compile(r"<h1\b", re.I)
NOINDEX = re.compile(r'<meta\s+name="robots"\s+content="[^"]*noindex', re.I)
REFRESH = re.compile(r'<meta\s+http-equiv="refresh"', re.I)
# Only look at the document head for head tags (posts may quote HTML in code).
HEAD = re.compile(r"<head\b.*?</head>", re.S | re.I)

warn = lambda f, m: print(f"::warning file={f}::{m}")
note = lambda f, m: print(f"::notice file={f}::{m}")

titles, descs = collections.defaultdict(list), collections.defaultdict(list)
problems = pages = 0
for path in sorted(glob.glob(os.path.join(root, "**", "*.html"), recursive=True)):
    rel = os.path.relpath(path, root)
    doc = open(path, encoding="utf-8").read()
    head = HEAD.search(doc)
    head = head.group(0) if head else ""
    if not head or NOINDEX.search(head) or REFRESH.search(head):
        continue
    pages += 1
    t = [html.unescape(x).strip() for x in TITLE.findall(head)]
    if len(t) != 1 or not t[0]:
        problems += 1
        warn(rel, f"expected one non-empty <title>, found {t!r}")
    else:
        titles[t[0]].append(rel)
        if len(t[0]) > 70:
            note(rel, f"title is {len(t[0])} chars (> 70): {t[0]}")
    d = DESC.search(head)
    if not d or not d.group(1).strip():
        problems += 1
        warn(rel, "missing meta description")
    else:
        dv = html.unescape(d.group(1)).strip()
        descs[dv].append(rel)
        if len(dv) > 160:
            note(rel, f"meta description is {len(dv)} chars (> 160, may be cut off in search results)")
    if not CANON.search(head):
        problems += 1
        warn(rel, "missing <link rel=\"canonical\">")
    # Strip <pre>/<code> so headings quoted in code samples don't count.
    body = re.sub(r"<(pre|code)\b.*?</\1>", "", doc, flags=re.S | re.I)
    n = len(H1.findall(body))
    if n != 1:
        problems += 1
        warn(rel, f"expected exactly one <h1>, found {n}")

for kind, seen in (("title", titles), ("meta description", descs)):
    for value, where in seen.items():
        if len(where) > 1:
            problems += 1
            warn(where[0], f"duplicate {kind} on {len(where)} pages ({', '.join(where)}): {value[:80]}")

print(f"Checked {pages} indexable pages: {problems} SEO problem(s).")
sys.exit(1 if problems else 0)
