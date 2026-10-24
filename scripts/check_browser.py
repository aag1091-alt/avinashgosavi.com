#!/usr/bin/env python3
"""Open every built page in headless Chromium and report what static lints can't see
(warnings only; CI never blocks a deploy on it).

For each HTML page in the built site, at a 375px phone viewport and a 1280px desktop one:
  - js-error:    uncaught JavaScript exceptions and console.error messages
  - h-scroll:    the page scrolls sideways (document wider than the viewport)
  - scroll-focus: a wide code block or table that scrolls sideways but can't be reached
                 by keyboard (post-tools.html should give it tabindex=0 + an aria-label)

The site is served from a local http.server; every request to another host (analytics,
external images) is blocked, so the run is offline and never counts as a visit.
Problems are ::warning annotations (one per rule, a few examples) plus a full list in the
job summary. Usage: check_browser.py _site [--strict] [--only=/post/x/,/about]"""
import functools, http.server, os, sys, threading
from collections import defaultdict

args = [a for a in sys.argv[1:] if not a.startswith("--")]
root = os.path.abspath(args[0] if args else "_site")
strict = "--strict" in sys.argv
only = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--only=")), None)
SKIP = {"/404.html", "/offline/"}  # 404 is served at any path; offline page reloads itself
WIDTHS = (375, 1280)


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


PROBE = r"""() => {
  const vw = document.documentElement.clientWidth;
  const out = {sw: document.documentElement.scrollWidth, vw, stuck: []};
  for (const el of document.querySelectorAll('.post-content pre, .table-scroll')) {
    if (el.scrollWidth > el.clientWidth + 1 && el.tabIndex < 0 &&
        !el.querySelector('a, button, input, [tabindex]')) {
      out.stuck.push((el.className || el.tagName).toString().slice(0, 40));
    }
  }
  if (out.sw > vw + 1) {  // name the elements that stick out (topmost ones, not inside a scroller)
    out.wide = [];
    const clipped = el => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement)
      if (/(auto|scroll|hidden|clip)/.test(getComputedStyle(a).overflowX)) return true; return false; };
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect(), pr = el.parentElement.getBoundingClientRect();
      if (r.right > vw + 1 && pr.right <= vw + 1 && getComputedStyle(el).position !== 'fixed' && !clipped(el)) {
        const name = el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '');
        out.wide.push(name + ' "' + (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40) + '"');
        if (out.wide.length >= 3) break;
      }
    }
    if (!out.wide.length) {  // nothing sticks out as a box: look for text spilling out of its box
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      const range = document.createRange();
      for (let n = w.nextNode(); n && out.wide.length < 3; n = w.nextNode()) {
        const el = n.parentElement;
        if (!n.textContent.trim() || /(auto|scroll|hidden|clip)/.test(getComputedStyle(el).overflowX) || clipped(el)) continue;
        range.selectNodeContents(n);
        if (range.getBoundingClientRect().right > vw + 1) {
          out.wide.push('text in ' + el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '') +
            ' "' + n.textContent.trim().replace(/\s+/g, ' ').slice(0, 40) + '"');
        }
      }
    }
  }
  return out;
}"""


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("::warning title=browser check::playwright not installed; skipped")
        return 0

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=root))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]
    urls = only or pages()
    problems = defaultdict(list)  # rule -> [(url, msg)]

    with sync_playwright() as pw:
        browser = None
        for opts in ({"channel": "chrome"}, {}, {"executable_path": "/opt/pw-browsers/chromium"}):
            try:
                browser = pw.chromium.launch(**opts)
                break
            except Exception:
                continue
        if browser is None:
            print("::warning title=browser check::no Chromium/Chrome available; skipped")
            return 0
        for width in WIDTHS:
            ctx = browser.new_context(viewport={"width": width, "height": 800}, service_workers="block")
            ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
            for url in urls:
                page = ctx.new_page()
                errs = []
                page.on("pageerror", lambda e: errs.append(str(e).splitlines()[0][:160]))
                page.on("console", lambda m: m.type == "error" and errs.append(m.text[:160]))
                try:
                    page.goto(base + url, wait_until="load", timeout=20000)
                    page.wait_for_timeout(300)  # let ResizeObserver / deferred scripts run
                    r = page.evaluate(PROBE)
                except Exception as e:
                    problems["load"].append((url, "%dpx: %s" % (width, str(e).splitlines()[0][:160])))
                    page.close()
                    continue
                # Blocked off-site requests log "Failed to load resource" — not a page bug.
                for e in dict.fromkeys(x for x in errs if "net::ERR_FAILED" not in x and "Failed to load resource" not in x):
                    problems["js-error"].append((url, "%dpx: %s" % (width, e)))
                if r["sw"] > r["vw"] + 1:
                    problems["h-scroll"].append((url, "%dpx: page is %dpx wide%s" % (
                        width, r["sw"], (" — " + ", ".join(r.get("wide", []))) if r.get("wide") else "")))
                for s in r["stuck"]:
                    problems["scroll-focus"].append((url, "%dpx: %s scrolls but isn't focusable" % (width, s)))
                page.close()
            ctx.close()
        browser.close()
    srv.shutdown()

    total = sum(len(v) for v in problems.values())
    for rule, items in sorted(problems.items()):
        ex = "; ".join("%s (%s)" % (u, m) for u, m in items[:4])
        print("::warning title=browser %s::%d issue(s), e.g. %s" % (rule, len(items), ex))
    lines = ["### Browser check", "", "%d pages × %s px: %d issue(s)" % (len(urls), "/".join(map(str, WIDTHS)), total), ""]
    for rule, items in sorted(problems.items()):
        lines += ["- **%s** %s — %s" % (rule, u, m) for u, m in items]
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if (strict and total) else 0


if __name__ == "__main__":
    sys.exit(main())
