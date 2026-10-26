#!/usr/bin/env python3
"""Freshness and shape lint for the hand-edited data files (warnings only; CI never blocks a deploy on it).

Checks the source tree (not _site) for:
  _data/events.yml   - required fields (location is optional), known role/status values, valid dates;
                       an "upcoming" event whose end_date (or date) is more than 3 days ago
                       (time to move it to past), a "past" event dated in the
                       future, and a recap path that isn't a real post
  _data/now.yml      - `updated` older than 30 days; an item whose `until` date has
                       passed or isn't YYYY-MM-DD; an undated item that links to an
                       /events/#anchor that no event produces, or to a past event
  _data/changelog.yml - required fields, known desk values, newest-first order,
                       dates in the future

"Today" is Pacific time (the site's dates are written in PT).
Problems are ::warning annotations plus a list in the job summary.
Usage: check_data.py [repo_root] [--strict] [--today=YYYY-MM-DD]"""
import datetime as dt, glob, json, os, re, subprocess, sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
root = args[0] if args else "."
strict = "--strict" in sys.argv
today_arg = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--today=")), None)

ROLES = {"attended", "judge", "mentor", "hacker", "speaker"}
STATUSES = {"upcoming", "past"}
DESKS = {"Writing", "Design", "Engineering"}
GRACE_DAYS = 3      # multi-day events: `date` is the first day
NOW_STALE_DAYS = 30


def today_pt():
    if today_arg:
        return dt.date.fromisoformat(today_arg)
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("America/Los_Angeles")).date()
    except Exception:
        return (dt.datetime.utcnow() - dt.timedelta(hours=8)).date()


def load(rel):
    """PyYAML if present, else Ruby's Psych (always there in the Jekyll job)."""
    path = os.path.join(root, rel)
    try:
        import yaml
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ImportError:
        out = subprocess.run(
            ["ruby", "-ryaml", "-rjson", "-rdate", "-e",
             "puts JSON.generate(YAML.load_file(ARGV[0], permitted_classes: [Date, Time]))", path],
            check=True, capture_output=True, text=True).stdout
        return json.loads(out)


def as_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def slugify(s):
    """Jekyll's default slugify: lowercase, non-alphanumerics become '-'."""
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


problems = []


def warn(file, msg):
    problems.append((file, msg))
    print("::warning file=%s,title=data::%s" % (file, msg.replace("\n", " ")))


today = today_pt()
post_urls = set()
for p in glob.glob(os.path.join(root, "_posts", "*.md")):
    m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)\.md$", os.path.basename(p))
    if m:
        post_urls.add("/post/%s/" % m.group(1))
        # a permalink in front matter wins over the filename
        with open(p, encoding="utf-8") as f:
            head = f.read(2000)
        pm = re.search(r"^permalink:\s*['\"]?(\S+?)['\"]?\s*$", head, re.M)
        if pm:
            post_urls.add(pm.group(1).rstrip("/") + "/")

# events
EV = "_data/events.yml"
events = load(EV) or []
anchors = {}
for i, ev in enumerate(events):
    name = ev.get("name") or "(entry %d)" % (i + 1)
    for key in ("name", "date", "when", "role", "status"):  # location is optional
        if not ev.get(key):
            warn(EV, "%s: missing `%s`" % (name, key))
    if ev.get("role") and ev["role"] not in ROLES:
        warn(EV, "%s: role `%s` is not one of %s" % (name, ev["role"], ", ".join(sorted(ROLES))))
    if ev.get("status") and ev["status"] not in STATUSES:
        warn(EV, "%s: status `%s` is not upcoming or past" % (name, ev["status"]))
    d = as_date(ev.get("date"))
    if ev.get("date") and d is None:
        warn(EV, "%s: date `%s` is not YYYY-MM-DD" % (name, ev["date"]))
    end = as_date(ev.get("end_date")) if ev.get("end_date") else d
    if ev.get("end_date") and end is None:
        warn(EV, "%s: end_date `%s` is not YYYY-MM-DD" % (name, ev["end_date"]))
        end = d
    if d and end and end < d:
        warn(EV, "%s: end_date %s is before date %s" % (name, end, d))
    if end and ev.get("status") == "upcoming" and (today - end).days > GRACE_DAYS:
        warn(EV, "%s: still `upcoming` but ended %s (%d days ago) - move it to past" % (name, end, (today - end).days))
    if d and ev.get("status") == "past" and d > today:
        warn(EV, "%s: marked `past` but dated %s, in the future" % (name, d))
    rc = ev.get("recap")
    if rc and rc.startswith("/") and rc.rstrip("/") + "/" not in post_urls:
        warn(EV, "%s: recap %s is not a post in _posts/" % (name, rc))
    anchors[slugify(name)] = ev

# now
NW = "_data/now.yml"
now = load(NW) or {}
upd = as_date(now.get("updated"))
if not upd:
    warn(NW, "missing or invalid `updated` date")
elif (today - upd).days > NOW_STALE_DAYS:
    warn(NW, "`updated` is %s (%d days ago) - review the items" % (upd, (today - upd).days))
elif upd > today:
    warn(NW, "`updated` %s is in the future" % upd)
for it in now.get("items") or []:
    link = str(it.get("link") or "")
    if not it.get("label") or not it.get("text"):
        warn(NW, "an item is missing `label` or `text` (%s)" % (it.get("label") or link or "?"))
    if it.get("until"):
        u = as_date(it["until"])
        if u is None:
            warn(NW, "%s item: until `%s` is not YYYY-MM-DD" % (it.get("label"), it["until"]))
        elif u < today:
            warn(NW, "%s item expired %s (hidden on the site now) - remove it from now.yml" % (it.get("label"), u))
        continue  # dated items hide themselves, so the events cross-check below is moot
    m = re.match(r"^/events/#(.+)$", link)
    if m:
        ev = anchors.get(m.group(1))
        if ev is None:
            warn(NW, "%s item links /events/#%s, but no event has that anchor" % (it.get("label"), m.group(1)))
        else:
            d = as_date(ev.get("end_date")) or as_date(ev.get("date"))
            if ev.get("status") == "past" or (d and (today - d).days > GRACE_DAYS):
                warn(NW, "%s item points at %s, which is over - drop or reword it" % (it.get("label"), ev.get("name")))

# changelog
CL = "_data/changelog.yml"
log = load(CL) or []
prev = None
for i, e in enumerate(log):
    where = "entry %d (%s)" % (i + 1, e.get("date"))
    for key in ("date", "desk", "text"):
        if not e.get(key):
            warn(CL, "%s: missing `%s`" % (where, key))
    if e.get("desk") and e["desk"] not in DESKS:
        warn(CL, "%s: desk `%s` is not Writing, Design or Engineering" % (where, e["desk"]))
    d = as_date(e.get("date"))
    if d and d > today + dt.timedelta(days=1):
        warn(CL, "%s: dated in the future" % where)
    if d and prev and d > prev:
        warn(CL, "%s: newer than the entry above it - the file is newest first" % where)
    prev = d or prev

print("checked %d events, %d now items, %d changelog entries (today %s PT): %d warning(s)"
      % (len(events), len(now.get("items") or []), len(log), today, len(problems)))
summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a", encoding="utf-8") as f:
        f.write("### Data files\n\n")
        if problems:
            f.writelines("- `%s`: %s\n" % p for p in problems)
        else:
            f.write("events.yml, now.yml and changelog.yml look current.\n")
        f.write("\n")
sys.exit(1 if strict and problems else 0)
