#!/usr/bin/env python3
"""HTML conformance check of every built page with the Nu Html Checker (vnu) — warnings only.

The other checks look at what a page means (links, ARIA, SEO, JSON-LD) or how it renders;
this one asks whether the markup itself is valid HTML: stray or unclosed tags, elements
in places the content model forbids (a <div> inside a <p>, a <ul> inside an <a>), bad
attribute values, duplicate ids, obsolete attributes. Browsers silently repair those, but
each repair can move content around, and screen readers and feed readers see the repaired
tree, not the one we wrote.

vnu runs once over every HTML file in _site (Java, offline; no page is fetched). Errors
only — vnu's "info" notes (e.g. the trailing slash on void elements that Jekyll emits) are
skipped. Output: one ::warning per distinct message (how many times, on which pages, the
first source line and a short extract), a ::notice with totals, and the full list in the
job summary. GitHub keeps only 10 warning annotations per step, so the summary is the
complete record.

Usage: check_html.py _site --vnu=path/to/vnu.jar [--strict]"""
import json, os, re, subprocess, sys
from collections import defaultdict

args = [a for a in sys.argv[1:] if not a.startswith("--")]
root = os.path.abspath(args[0] if args else "_site")
opt = lambda name: next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--%s=" % name)), None)
vnu = opt("vnu") or os.environ.get("VNU_JAR", "node_modules/vnu-jar/build/dist/vnu.jar")
strict = "--strict" in sys.argv
SKIP = re.compile(r"^google[0-9a-f]+\.html$")  # search-console verification stubs, not pages
# Known vnu false positives (valid in today's HTML spec, not yet in the checker):
# <script type="speculationrules"> (the prefetch rules in _layouts/default.html).
IGNORE = re.compile(r"Bad value “speculationrules” for attribute “type” on element “script”")


def page_url(path):
    rel = "/" + os.path.relpath(path, root).replace(os.sep, "/")
    return rel[: -len("index.html")] if rel.endswith("/index.html") else rel


files = sorted(
    os.path.join(d, f)
    for d, _, fs in os.walk(root)
    for f in fs
    if f.endswith(".html") and not SKIP.match(f)
)
if not files:
    print("::warning title=html::no HTML files under %s" % root)
    sys.exit(0)

proc = subprocess.run(
    ["java", "-jar", vnu, "--errors-only", "--format", "json", "--exit-zero-always"] + files,
    capture_output=True, text=True,
)
raw = proc.stderr + proc.stdout
m = re.search(r'^\{"(version|messages)"', raw, re.M)  # the JVM may print notes (e.g. "Picked up JAVA_TOOL_OPTIONS") first
try:
    messages = json.JSONDecoder().raw_decode(raw[m.start():] if m else raw)[0]["messages"]
except (ValueError, KeyError):
    print("::warning title=html::could not run vnu (%s)" % (proc.stderr or proc.stdout).strip()[:300])
    sys.exit(0)

groups = defaultdict(list)  # message text -> [(page, line, extract)]
for m in messages:
    if m.get("type") != "error" or IGNORE.search(m.get("message", "")):
        continue
    path = (m.get("url") or "").replace("file:", "", 1)
    path = re.sub(r"^/+", "/", path)
    extract = re.sub(r"\s+", " ", m.get("extract") or "").strip()[:120]
    groups[m.get("message", "?")].append((page_url(path), m.get("lastLine"), extract))

total = sum(len(v) for v in groups.values())
pages_hit = {p for v in groups.values() for p, _, _ in v}
ordered = sorted(groups.items(), key=lambda kv: -len(kv[1]))
for msg, hits in ordered:
    pages = sorted({p for p, _, _ in hits})
    first = hits[0]
    shown = ", ".join(pages[:4]) + (" …" if len(pages) > 4 else "")
    text = "%s — %d× on %d page(s): %s (first: %s line %s: %s)" % (
        msg.replace("\n", " "), len(hits), len(pages), shown, first[0], first[1], first[2])
    print("::warning title=html::" + text.replace("%", "%25").replace("\r", "").replace("\n", " "))

print("::notice title=html::%d page(s) checked with the Nu Html Checker; %d error(s) of %d kind(s) on %d page(s)"
      % (len(files), total, len(groups), len(pages_hit)))

summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a") as out:
        out.write("### HTML validity (Nu Html Checker)\n\n%d pages, %d errors\n\n" % (len(files), total))
        for msg, hits in ordered:
            out.write("- **%s** (%d)\n" % (msg.replace("\n", " "), len(hits)))
            for p, line, ex in hits[:20]:
                out.write("  - `%s` line %s: `%s`\n" % (p, line, ex.replace("`", "'")))
        out.write("\n")

sys.exit(1 if strict and total else 0)
