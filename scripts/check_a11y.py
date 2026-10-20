#!/usr/bin/env python3
"""Basic accessibility lint for the built site (_site/).

Offline, stdlib only, runs in a second or two. For every HTML page it checks:
  - <html lang> is set and <title> is not empty
  - exactly one <h1>, and headings never skip a level going down (h2 -> h4)
  - every <img> has an alt attribute (alt="" is fine for decoration)
  - links and buttons have an accessible name (text, aria-label,
    aria-labelledby, title, img alt or svg <title>; aria-hidden parts ignored)
  - form fields have a label (aria-label, aria-labelledby, title or <label for>)
  - no duplicate id values on a page

Usage: python3 scripts/check_a11y.py [_site] [--strict]
Exit code is 1 with --strict when anything is found, else always 0.
Prints one GitHub Actions ::warning annotation per rule (annotations are capped,
so each one carries the count and the first few examples) and the full list to
the job summary.
"""
import os
import sys
from collections import defaultdict
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
FIELDS = {"input", "select", "textarea"}
UNLABELLED_INPUT_TYPES = {"hidden", "submit", "button", "reset", "image"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = None
        self.in_title = False
        self.headings = []  # (level, line)
        self.ids = defaultdict(list)
        self.issues = []  # (rule, line, detail)
        self.label_for = set()
        self.fields = []  # (line, id, desc)
        self.stack = []  # open elements: dict(tag, hidden, name_parts, needs_name, line, desc)
        self.text_by_id = defaultdict(str)
        self.labelledby = []  # (rule, line, ids, desc)

    # -- helpers ---------------------------------------------------------
    def hidden(self):
        return any(e["hidden"] for e in self.stack)

    def add_name(self, text):
        """Give text to every open element that is collecting an accessible name."""
        if not text.strip() or self.hidden():
            return
        for e in self.stack:
            if e["collect"]:
                e["name"].append(text)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        line = self.getpos()[0]
        if tag == "html":
            self.lang = a.get("lang", "").strip()
        if tag == "title" and not self.stack_has("svg"):
            self.in_title = True
            self.title = ""
        if a.get("id"):
            self.ids[a["id"]].append(line)
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6") and not self.hidden():
            self.headings.append((int(tag[1]), line))
        if tag == "label" and a.get("for"):
            self.label_for.add(a["for"])

        hidden = a.get("aria-hidden") == "true" or "hidden" in a
        labelled = a.get("aria-label", "").strip() or a.get("title", "").strip()
        if tag == "img":
            if "alt" not in a and not hidden:
                self.issues.append(("img-alt", line, a.get("src", "")[:80]))
            if a.get("alt", "").strip() and not hidden:
                self.add_name(a["alt"])
        elif labelled and not hidden:
            self.add_name(labelled)

        # kramdown task-list checkboxes get an aria-label from their item text in
        # _includes/post-tools.html (they are disabled, display-only)
        task_box = "task-list-item-checkbox" in a.get("class", "")
        if tag in FIELDS and not hidden and not task_box and not self.hidden() \
                and a.get("type", "text") not in UNLABELLED_INPUT_TYPES:
            if not (labelled or a.get("aria-labelledby") or self.stack_has("label")):
                self.fields.append((line, a.get("id", ""), f"<{tag} {a.get('type', '')}>".replace(" >", ">")))

        if tag in VOID:
            return
        # skip elements that are hidden themselves or inside a hidden ancestor
        needs = tag in ("a", "button") and not hidden and not self.hidden() and (tag == "button" or "href" in a)
        desc = f"<{tag}>" + (f" {a.get('href', '')[:80]}" if tag == "a" else "") + (f" .{a['class'].split()[0]}" if a.get("class") else "")
        if needs and a.get("aria-labelledby"):
            self.labelledby.append(("name", line, a["aria-labelledby"].split(), desc))
            needs = False
        self.stack.append({
            "tag": tag, "hidden": hidden, "line": line, "desc": desc,
            "needs": needs and not labelled,
            "collect": (needs and not labelled) or bool(a.get("id")) or tag == "title",
            "id": a.get("id", ""), "name": [],
        })

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def stack_has(self, tag):
        return any(e["tag"] == tag for e in self.stack)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in VOID:
            return
        # pop to the matching open tag (tolerates sloppy HTML)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                closed = self.stack[i:]
                del self.stack[i:]
                for e in reversed(closed):
                    name = " ".join(e["name"]).strip()
                    if e["id"]:
                        self.text_by_id[e["id"]] = name
                    if e["tag"] == "title" and self.stack and name:
                        # svg <title> names its parent link/button
                        self.add_name(name)
                    if e["needs"] and not name:
                        self.issues.append(("name", e["line"], e["desc"]))
                return

    def handle_data(self, data):
        if self.in_title and self.title is not None:
            self.title += data
        if self.stack and self.stack[-1]["tag"] in ("script", "style"):
            return
        self.add_name(data)

    def finish(self):
        if not self.lang:
            self.issues.append(("html-lang", 1, "<html> has no lang"))
        if self.title is None or not self.title.strip():
            self.issues.append(("title", 1, "empty or missing <title>"))
        h1 = [l for lvl, l in self.headings if lvl == 1]
        if len(h1) != 1:
            self.issues.append(("one-h1", h1[1] if len(h1) > 1 else 1, f"{len(h1)} <h1> elements"))
        prev = 0
        for lvl, line in self.headings:
            if prev and lvl > prev + 1:
                self.issues.append(("heading-order", line, f"h{prev} -> h{lvl}"))
            prev = lvl
        for _id, lines in self.ids.items():
            if len(lines) > 1:
                self.issues.append(("duplicate-id", lines[1], f'id="{_id}" x{len(lines)}'))
        for rule, line, ids, desc in self.labelledby:
            if not any(self.text_by_id.get(i, "").strip() for i in ids):
                self.issues.append((rule, line, desc + " (aria-labelledby target empty)"))
        for line, fid, desc in self.fields:
            if not (fid and fid in self.label_for):
                self.issues.append(("field-label", line, desc))


RULES = {
    "html-lang": "page language",
    "title": "page title",
    "one-h1": "exactly one h1",
    "heading-order": "heading levels skip",
    "img-alt": "image without alt",
    "name": "link/button without an accessible name",
    "field-label": "form field without a label",
    "duplicate-id": "duplicate id",
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    site = args[0] if args else "_site"
    found = defaultdict(list)  # rule -> [(rel, line, detail)]
    pages = 0
    for root, _, files in os.walk(site):
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, f), site)
            with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                html = fh.read()
            if "<html" not in html[:500].lower():
                continue  # fragments / redirects
            p = Page()
            p.feed(html)
            p.close()
            p.finish()
            pages += 1
            for rule, line, detail in p.issues:
                found[rule].append((rel, line, detail))

    total = sum(len(v) for v in found.values())
    for rule, items in sorted(found.items()):
        ex = "; ".join(f"{r}:{l} {d}" for r, l, d in items[:4])
        rel, line, _ = items[0]
        print(f"::warning file={rel},line={line}::a11y {rule} ({RULES[rule]}): {len(items)} found, e.g. {ex}")
    summary = f"Checked {pages} pages: {total} accessibility issues in {len(found)} rules."
    print(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
            fh.write(f"### Accessibility lint\n\n{summary}\n\n")
            for rule, items in sorted(found.items()):
                fh.write(f"**{rule}** — {RULES[rule]} ({len(items)})\n\n")
                for rel, line, detail in items:
                    fh.write(f"- `{rel}` line {line}: {detail}\n")
                fh.write("\n")
    if total and strict:
        sys.exit(1)


if __name__ == "__main__":
    main()
