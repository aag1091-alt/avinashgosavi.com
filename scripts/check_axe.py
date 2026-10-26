#!/usr/bin/env python3
"""axe-core accessibility audit of every built page (warnings only; CI never blocks a deploy on it).

check_a11y.py lints the static HTML and check_browser.py covers names, contrast and
layout after scripts run. This adds Deque's axe-core rule set (the engine behind
Lighthouse's accessibility score) on top: ARIA roles/attributes used correctly,
landmarks, list and definition-list structure, duplicate ids that ARIA points at,
nested interactive controls, and so on.

Each page is served from a local http.server and opened in headless Chromium twice: at
1280px, and as a 375px touch phone (is_mobile + has_touch, so hover:none states such as
always-visible copy buttons and heading anchors are audited too), plus /search/?q=memory
and /blog/?q=memory so script-built results are audited;
requests to other hosts are blocked, so the run is offline and never counts as a visit.
Rules: WCAG 2.0/2.1/2.2 A and AA plus axe "best-practice". color-contrast is switched
off here because check_browser.py measures contrast in both themes with composited
backgrounds.

Output: one ::warning per failing rule (impact, how many elements on how many pages,
a few examples, the axe help link), then a full list in the job summary.
Usage: check_axe.py _site --axe=path/to/axe.min.js [--strict] [--only=/post/x/,/about/] [--widths=1280,375]"""
import functools, http.server, os, sys, threading
from collections import defaultdict

args = [a for a in sys.argv[1:] if not a.startswith("--")]
root = os.path.abspath(args[0] if args else "_site")
opt = lambda name: next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--%s=" % name)), None)
axe_path = opt("axe") or os.environ.get("AXE_JS", "node_modules/axe-core/axe.min.js")
only = opt("only").split(",") if opt("only") else None
strict = "--strict" in sys.argv
widths = [int(w) for w in (opt("widths") or "1280,375").split(",") if w.strip()]
SKIP = {"/404.html", "/offline/", "/offline.html"}  # 404 is served at any path; offline page reloads itself
EXTRA = ("/search/?q=memory", "/blog/?q=memory")
RUN_OPTS = {
    "runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]},
    "rules": {"color-contrast": {"enabled": False}},
    "resultTypes": ["violations"],
}
AUDIT = """async (opts) => {
  const r = await axe.run(document, opts);
  return r.violations.map(v => ({id: v.id, impact: v.impact || 'minor', help: v.help, url: v.helpUrl,
    nodes: v.nodes.map(n => {
      const sel = n.target.map(t => Array.isArray(t) ? t.join(' >> ') : t).join(' ');
      if (v.id !== 'scrollable-region-focusable') return sel;
      const el = document.querySelector(sel);  // say how far it overflows and whether it is focusable
      return el ? sel + ' [scroll ' + el.scrollWidth + 'x' + el.scrollHeight + ' in ' + el.clientWidth + 'x' +
        el.clientHeight + ', tabindex=' + el.getAttribute('tabindex') + ']' : sel;
    })}));
}"""


class Handler(http.server.SimpleHTTPRequestHandler):
    """Static server that, like GitHub Pages, maps /about to about.html."""

    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and os.path.isfile(p + ".html"):
            return p + ".html"
        return p

    def log_message(self, *a):
        pass


def pages():
    out = []
    for d, _, files in os.walk(root):
        for f in files:
            if not f.endswith(".html"):
                continue
            rel = "/" + os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/")
            url = rel[: -len("index.html")] if rel.endswith("/index.html") else rel
            if rel.startswith("/assets/") or url in SKIP or rel in SKIP:
                continue
            head = open(os.path.join(d, f), encoding="utf-8", errors="ignore").read(600).lower()
            if 'http-equiv="refresh"' in head:  # redirect stubs
                continue
            out.append(url)
    return sorted(out)


def main():
    if not os.path.isfile(axe_path):
        print("::warning title=axe::axe-core not found at %s; skipped" % axe_path)
        return 0
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("::warning title=axe::playwright not installed; skipped")
        return 0
    urls = only or (pages() + [u for u in EXTRA if os.path.isfile(os.path.join(root, u.split("?")[0].strip("/"), "index.html"))])
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=root))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]
    found = defaultdict(lambda: {"pages": defaultdict(list)})  # rule id -> info
    failed = []
    with sync_playwright() as pw:
        browser = None
        for launch in ({"channel": "chrome"}, {}, {"executable_path": "/opt/pw-browsers/chromium"}):
            try:
                browser = pw.chromium.launch(**launch)
                break
            except Exception:
                continue
        if not browser:
            print("::warning title=axe::no Chromium/Chrome available; skipped")
            return 0
        for w in widths:
            phone = w < 640
            ctx = browser.new_context(viewport={"width": w, "height": 812 if phone else 800}, is_mobile=phone,
                                      has_touch=phone, service_workers="block")
            ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
            tag = "" if w == widths[0] else " @%dpx" % w  # first width unmarked; others tagged per page
            for url in urls:
                page = ctx.new_page()
                try:
                    page.goto(base + url, wait_until="load", timeout=20000)
                    page.wait_for_timeout(300)  # let deferred scripts build TOC, results, copy buttons
                    page.add_script_tag(path=axe_path)
                    for v in page.evaluate(AUDIT, RUN_OPTS):
                        info = found[v["id"]]
                        info.update(impact=v["impact"], help=v["help"], url=v["url"])
                        info["pages"][url + tag].extend(v["nodes"])
                except Exception as e:
                    failed.append((url + tag, str(e).splitlines()[0][:160]))
                page.close()
            ctx.close()
        browser.close()
    srv.shutdown()

    rank = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}
    rules = sorted(found.items(), key=lambda kv: (rank.get(kv[1]["impact"], 4), kv[0]))
    total = sum(len(n) for _, i in rules for n in i["pages"].values())
    for rid, i in rules:
        n = sum(len(x) for x in i["pages"].values())
        ex = "; ".join("%s (%s)" % (u, ", ".join(nodes[:2])[:120]) for u, nodes in list(i["pages"].items())[:3])
        print("::warning title=axe %s (%s)::%s — %d element(s) on %d page(s), e.g. %s — %s" % (
            rid, i["impact"], i["help"], n, len(i["pages"]), ex, i["url"]))
    for u, m in failed:
        print("::warning title=axe load::%s: %s" % (u, m))
    at = " and ".join("%dpx" % w for w in widths)
    print("::notice title=axe::%d pages audited at %s, %d rule(s) failing, %d element(s)" % (len(urls), at, len(rules), total))
    lines = ["### axe-core audit", "", "%d pages at %s: %d rule(s) failing on %d element(s)" % (len(urls), at, len(rules), total), ""]
    for rid, i in rules:
        lines.append("- **%s** (%s) — %s ([help](%s))" % (rid, i["impact"], i["help"], i["url"]))
        lines += ["  - %s: `%s`" % (u, "`, `".join(nodes[:5])) for u, nodes in i["pages"].items()]
    lines += ["- **load** %s — %s" % f for f in failed]
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if (strict and (total or failed)) else 0


if __name__ == "__main__":
    sys.exit(main())
