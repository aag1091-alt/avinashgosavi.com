#!/usr/bin/env python3
"""Check every <script type="application/ld+json"> block in the built site parses
as JSON, and print a summary of @types found. Usage: check_jsonld.py _site"""
import collections, glob, json, os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else "_site"
pat = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
types, bad = collections.Counter(), 0
for path in sorted(glob.glob(os.path.join(root, "**", "*.html"), recursive=True)):
    html = open(path, encoding="utf-8").read()
    for block in pat.findall(html):
        try:
            data = json.loads(block)
        except ValueError as e:
            bad += 1
            print(f"::warning file={os.path.relpath(path, root)}::invalid JSON-LD: {e}")
            continue
        for d in data if isinstance(data, list) else [data]:
            t = d.get("@type", "?")
            types[t if isinstance(t, str) else ",".join(t)] += 1
            if t == "BreadcrumbList":
                pos = [i.get("position") for i in d.get("itemListElement", [])]
                if pos != list(range(1, len(pos) + 1)):
                    bad += 1
                    print(f"::warning file={os.path.relpath(path, root)}::breadcrumb positions {pos}")
            if t == "ProfilePage":
                me = d.get("mainEntity") or {}
                if me.get("@type") != "Person" or not me.get("name"):
                    bad += 1
                    print(f"::warning file={os.path.relpath(path, root)}::ProfilePage needs a Person mainEntity with a name")
# Speculation rules (link prefetch on hover) must also be valid JSON with a prefetch list.
spec = re.compile(r'<script type="speculationrules">(.*?)</script>', re.S)
nspec = 0
for path in sorted(glob.glob(os.path.join(root, "**", "*.html"), recursive=True)):
    for block in spec.findall(open(path, encoding="utf-8").read()):
        nspec += 1
        try:
            assert json.loads(block).get("prefetch")
        except (ValueError, AssertionError) as e:
            bad += 1
            print(f"::warning file={os.path.relpath(path, root)}::invalid speculation rules: {e!r}")
print("Pages with speculation rules:", nspec)
print("JSON-LD types:", dict(types))
print(f"{bad} problem(s)")
sys.exit(1 if bad else 0)
