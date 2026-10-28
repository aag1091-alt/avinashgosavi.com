#!/usr/bin/env python3
"""Microformats2 check for the built site (warnings only; CI never blocks a deploy on it).

IndieWeb readers and reply tools read h-entry / h-card markup instead of JSON-LD.
  - every post page (_site/post/*/index.html) must parse to one h-entry with
    name, published, url (absolute), content and an author h-card with a name;
    a dt-updated, when shown, must not be earlier than dt-published
  - the homepage must expose an h-card with name, url and photo
  - /about/ must expose an h-card with name, photo and u-uid = the homepage URL
  - every /events/ row must be an h-event with name, start (YYYY-MM-DD) and an
    absolute url; a dt-end, when present, must not be earlier than dt-start
Needs mf2py (pip install mf2py). Usage: check_mf2.py _site"""
import glob, os, sys

import mf2py

root = sys.argv[1] if len(sys.argv) > 1 else "_site"
warn = lambda f, m: print(f"::warning file={f}::{m}")
problems = 0
updated = 0  # posts showing an "Updated <date>" line


def items(path, kind):
    doc = open(path, encoding="utf-8").read()
    return [i for i in mf2py.parse(doc=doc)["items"] if kind in i["type"]]


for path in sorted(glob.glob(os.path.join(root, "post", "*", "index.html"))):
    rel = os.path.relpath(path, root)
    entries = items(path, "h-entry")
    if len(entries) != 1:
        problems += 1
        warn(rel, f"expected one h-entry, found {len(entries)}")
        continue
    p = entries[0]["properties"]
    missing = [k for k in ("name", "published", "url", "content", "author") if not p.get(k)]
    if p.get("url") and not str(p["url"][0]).startswith("http"):
        missing.append("absolute url")
    author = (p.get("author") or [{}])[0]
    if isinstance(author, dict) and not author.get("properties", {}).get("name"):
        missing.append("author name")
    if missing:
        problems += 1
        warn(rel, "h-entry missing " + ", ".join(missing))
    if p.get("updated"):
        updated += 1
        if str(p["updated"][0]) < str(p["published"][0]):
            problems += 1
            warn(rel, "h-entry dt-updated is earlier than dt-published")

home = os.path.join(root, "index.html")
cards = items(home, "h-card")
if not cards:
    problems += 1
    warn("index.html", "homepage has no h-card")
else:
    p = cards[0]["properties"]
    missing = [k for k in ("name", "url", "photo") if not p.get(k)]
    if missing:
        problems += 1
        warn("index.html", "homepage h-card missing " + ", ".join(missing))

about = os.path.join(root, "about", "index.html")
if os.path.exists(about):
    cards = items(about, "h-card")
    homeurl = (items(home, "h-card") or [{"properties": {}}])[0]["properties"].get("uid") or []
    if not cards:
        problems += 1
        warn("about/index.html", "about page has no h-card")
    else:
        p = cards[0]["properties"]
        missing = [k for k in ("name", "uid", "photo") if not p.get(k)]
        if p.get("uid") and homeurl and p["uid"][0] != homeurl[0]:
            missing.append("uid matching the homepage")
        if missing:
            problems += 1
            warn("about/index.html", "about h-card missing " + ", ".join(missing))

events_page = os.path.join(root, "events", "index.html")
events = 0
if os.path.exists(events_page):
    rows = open(events_page, encoding="utf-8").read().count('class="event-row')
    evs = items(events_page, "h-event")
    events = len(evs)
    if events != rows:
        problems += 1
        warn("events/index.html", f"{rows} event rows but {events} h-event(s)")
    for e in evs:
        p = e["properties"]
        name = (p.get("name") or ["?"])[0]
        missing = [k for k in ("name", "start", "url") if not p.get(k)]
        if p.get("url") and not str(p["url"][0]).startswith("http"):
            missing.append("absolute url")
        if p.get("end") and p.get("start") and str(p["end"][0]) < str(p["start"][0]):
            missing.append("dt-end not before dt-start")
        if missing:
            problems += 1
            warn("events/index.html", f"h-event '{name}' missing " + ", ".join(missing))

posts = len(glob.glob(os.path.join(root, "post", "*", "index.html")))
print(f"microformats: {posts} posts ({updated} with an Updated date) + homepage + about + {events} event(s) checked, {problems} problem(s)")
