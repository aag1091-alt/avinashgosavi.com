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
            if t == "ScholarlyArticle":
                if not d.get("name") or not str(d.get("url", "")).startswith("http") \
                        or not re.fullmatch(r"\d{4}", str(d.get("datePublished", ""))):
                    bad += 1
                    print(f"::warning file={os.path.relpath(path, root)}::ScholarlyArticle needs name, http url and a 4-digit datePublished")
            posts = list(d.get("blogPost", [])) if t == "Blog" else []
            if t == "ItemList":
                posts += [(li.get("item") or {}) for li in d.get("itemListElement", [])
                          if (li.get("item") or {}).get("@type") == "BlogPosting"]
            for bp in posts:
                types["listed BlogPosting"] += 1
                if not bp.get("headline") or not str(bp.get("url", "")).startswith("http") \
                        or not re.match(r"\d{4}-\d\d-\d\d", str(bp.get("datePublished", ""))):
                    bad += 1
                    print(f"::warning file={os.path.relpath(path, root)}::listed BlogPosting needs a headline, http url and datePublished")
            if t == "ItemList":
                for li in d.get("itemListElement", []):
                    it = li.get("item") or {}
                    if it.get("@type") == "SoftwareSourceCode":
                        types["SoftwareSourceCode"] += 1
                        if not it.get("name") or not str(it.get("url", "")).startswith("http"):
                            bad += 1
                            print(f"::warning file={os.path.relpath(path, root)}::SoftwareSourceCode needs a name and an http url")
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
print(f"::notice title=JSON-LD::{types['ScholarlyArticle']} Paper TL;DR posts name their paper (ScholarlyArticle); BlogPosting {types['BlogPosting']}, BreadcrumbList {types['BreadcrumbList']}, SoftwareSourceCode {types['SoftwareSourceCode']}, Blog {types['Blog']} ({types['listed BlogPosting']} posts listed on /blog/ and /paper-tldr/)")
print(f"{bad} problem(s)")
sys.exit(1 if bad else 0)
