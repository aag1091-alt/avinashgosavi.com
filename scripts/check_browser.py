#!/usr/bin/env python3
"""Open every built page in headless Chromium and report what static lints can't see
(warnings only; CI never blocks a deploy on it).

For each HTML page in the built site, at a 375px phone viewport and a 1280px desktop one:
  - js-error:    uncaught JavaScript exceptions and console.error messages
  - h-scroll:    the page scrolls sideways (document wider than the viewport)
  - scroll-focus: a wide code block or table that scrolls sideways but can't be reached
                 by keyboard (post-tools.html should give it tabindex=0 + an aria-label)
  - a11y-dom:    after scripts ran: a visible link, button, form field or focusable widget
                 with no accessible name, or an id used twice — covers what JS builds
                 (TOC, search results, copy buttons) that the static a11y lint never sees.
                 /search/ and /blog/ are also opened with ?q=memory so results render.
  - layout-shift: Cumulative Layout Shift during load above 0.05 (Google's "good" is
                 <=0.1; a local server is faster than the real one, so the bar is tighter),
                 naming the elements that moved — e.g. an image without width/height, a
                 font swap, or a script inserting a box above content.
Then once more per theme (sepia and dark, 1280px):
  - contrast:    visible text below WCAG AA (4.5:1, or 3:1 for large text) against the
                 background it actually sits on (semi-transparent fills composited; text
                 over images/gradients is skipped; .diagram SVG text is measured against the
                 filled shape it sits on)

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
EXTRA = ("/search/?q=memory", "/blog/?q=memory")  # pages whose content only exists after JS runs
THEMES = ("sepia", "dark")
CLS_MAX = 0.05
SHIFTS = r"""window.__shifts = [];
try {
  new PerformanceObserver(list => {
    for (const e of list.getEntries()) {
      if (e.hadRecentInput) continue;
      const who = (e.sources || []).map(s => {
        const n = s.node, el = n && (n.nodeType === 1 ? n : n.parentElement);
        if (!el) return '?';
        const c = typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/)[0] : '';
        return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + c;
      });
      window.__shifts.push([e.value, who]);
    }
  }).observe({type: 'layout-shift', buffered: true});
} catch (e) {}"""  # contrast pass, via the theme switch's localStorage key


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


NAMES = r"""() => {
  const out = [];
  const hiddenAnc = el => el.closest('[aria-hidden="true"], [hidden], [inert], template');
  const visible = el => { if (hiddenAnc(el) || !el.getClientRects().length) return false;
    const cs = getComputedStyle(el); return cs.visibility === 'visible' && cs.display !== 'none'; };
  const textOf = root => {  // text a screen reader would read: skips aria-hidden parts, counts img alt / svg title
    let t = '';
    const walk = n => {
      if (n.nodeType === 3) { t += n.textContent; return; }
      if (n.nodeType !== 1 || n.getAttribute('aria-hidden') === 'true' || n.hidden) return;
      const tag = n.tagName.toLowerCase();
      if (tag === 'img') { t += n.getAttribute('alt') || ''; return; }
      if (tag === 'svg') { const ti = n.querySelector('title'); t += (n.getAttribute('aria-label') || (ti && ti.textContent) || ''); return; }
      if (n.getAttribute('aria-label')) { t += ' ' + n.getAttribute('aria-label'); return; }
      for (const c of n.childNodes) walk(c);
    };
    walk(root);
    return t.trim();
  };
  const named = el => {
    if ((el.getAttribute('aria-label') || '').trim()) return true;
    const lb = el.getAttribute('aria-labelledby');
    if (lb && lb.split(/\s+/).some(id => { const r = document.getElementById(id); return r && textOf(r); })) return true;
    if (el.labels && [...el.labels].some(l => textOf(l))) return true;
    if ((el.getAttribute('title') || '').trim()) return true;
    const tag = el.tagName.toLowerCase();
    if (tag === 'input') {
      const ty = (el.type || '').toLowerCase();
      if (/^(submit|reset|button)$/.test(ty)) return !!(el.value || ty !== 'button');
      if (ty === 'image') return !!el.alt;
      return !!(el.placeholder || '').trim();
    }
    if (tag === 'select' || tag === 'textarea') return false;
    return !!textOf(el);
  };
  const desc = el => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : '') +
    (el.getAttribute('href') ? ' href=' + el.getAttribute('href').slice(0, 50) : '');
  const sel = 'a[href], button, input:not([type="hidden"]), select, textarea, summary, [role="button"], [role="link"], [role="tab"], [role="switch"], [role="checkbox"], [role="menuitem"], [tabindex]:not([tabindex="-1"])';
  for (const el of document.body.querySelectorAll(sel)) {
    if (out.length >= 10) break;
    if (!visible(el) || named(el)) continue;
    // A plain [tabindex] container (e.g. a scrolling region) with readable text inside is fine.
    if (!el.matches('a, button, input, select, textarea, summary, [role]') && textOf(el)) continue;
    out.push('no accessible name: ' + desc(el));
  }
  const ids = new Map();
  for (const el of document.querySelectorAll('[id]')) if (el.id) ids.set(el.id, (ids.get(el.id) || 0) + 1);
  for (const [id, n] of ids) if (n > 1 && out.length < 14) out.push('id "' + id + '" used ' + n + ' times');
  return out;
}"""


CONTRAST = r"""() => {
  const parse = c => {
    let m = c.match(/^rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)$/);
    if (m) return [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]];
    m = c.match(/^color\(srgb ([\d.]+) ([\d.]+) ([\d.]+)(?: \/ ([\d.]+))?\)$/);
    if (m) return [m[1] * 255, m[2] * 255, m[3] * 255, m[4] === undefined ? 1 : +m[4]];
    return null;  // other color spaces: skip
  };
  const over = (top, base) => { const a = top[3];
    return [top[0] * a + base[0] * (1 - a), top[1] * a + base[1] * (1 - a), top[2] * a + base[2] * (1 - a), 1]; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const hex = c => '#' + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  // Background the element's text is drawn on: composite ancestor fills from the canvas up.
  const bgOf = el => {
    const layers = [];
    for (let a = el; a; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.backgroundImage !== 'none') return null;  // image/gradient: can't know
      const c = parse(cs.backgroundColor);
      if (c === null) return null;
      if (c[3] > 0) layers.push(c);
      if (c[3] >= 1) break;
    }
    let bg = [255, 255, 255, 1];
    for (let i = layers.length - 1; i >= 0; i--) bg = over(layers[i], bg);
    return bg;
  };
  const out = [], seen = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n && out.length < 8; n = w.nextNode()) {
    const el = n.parentElement;
    if (!n.textContent.trim() || !el || el.closest('svg, script, style, noscript, [aria-hidden="true"], [hidden]')) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;  // visually-hidden helpers
    const cs = getComputedStyle(el);
    if (cs.visibility !== 'visible' || cs.display === 'none') continue;
    let op = 1; for (let a = el; a; a = a.parentElement) op *= +getComputedStyle(a).opacity;
    if (op < 0.1) continue;  // faded-out widgets (e.g. back-to-top before scrolling)
    let fg = parse(cs.color), bg = bgOf(el);
    if (!fg || !bg) continue;
    fg = over([fg[0], fg[1], fg[2], fg[3] * op], bg);
    const px = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700;
    const need = (px >= 24 || (bold && px >= 18.66)) ? 3 : 4.5;
    const cr = ratio(fg, bg);
    if (cr + 0.005 >= need) continue;
    const name = el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : '');
    const key = name + hex(fg) + hex(bg);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(name + ' "' + n.textContent.trim().replace(/\s+/g, ' ').slice(0, 30) + '" ' + hex(fg) + ' on ' + hex(bg) + ' = ' + cr.toFixed(2) + ':1 (needs ' + need + ')');
  }
  // SVG diagram text: fill vs. the topmost filled shape under the text's centre (or the
  // HTML background behind the figure). Rendered px size decides the large-text threshold.
  const fillOf = (s, cs) => { const c = parse(cs.fill || ''); if (!c) return null;
    let op = (+cs.fillOpacity) * (+cs.opacity); for (let a = s.parentElement; a && a.tagName.toLowerCase() !== 'svg'; a = a.parentElement) op *= +getComputedStyle(a).opacity;
    return [c[0], c[1], c[2], c[3] * op]; };
  for (const t of document.querySelectorAll('.diagram svg text')) {
    if (out.length >= 16 || !t.textContent.trim() || t.closest('defs, [aria-hidden="true"]')) continue;
    t.scrollIntoView({block: 'center', behavior: 'instant'});
    const r = t.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    const tcs = getComputedStyle(t);
    if (tcs.visibility !== 'visible' || tcs.display === 'none') continue;
    let fg = fillOf(t, tcs);
    if (!fg) continue;
    const layers = []; let base = null;
    for (const e of document.elementsFromPoint(r.left + r.width / 2, r.top + r.height / 2)) {
      if (e === t || t.contains(e)) continue;
      if (!(e instanceof SVGElement) || e.tagName.toLowerCase() === 'svg') { base = bgOf(e); break; }
      const tag = e.tagName.toLowerCase();
      if (!/^(rect|circle|ellipse|path|polygon)$/.test(tag)) continue;
      const c = fillOf(e, getComputedStyle(e));
      if (!c || c[3] <= 0) continue;
      layers.push(c);
      if (c[3] >= 1) { base = [255, 255, 255, 1]; break; }
    }
    if (!base) continue;
    let bg = base;
    for (let i = layers.length - 1; i >= 0; i--) bg = over(layers[i], bg);
    fg = over(fg, bg);
    const scale = r.height / (t.getBBox().height || r.height);
    const px = parseFloat(tcs.fontSize) * scale, bold = parseInt(tcs.fontWeight, 10) >= 700;
    const need = (px >= 24 || (bold && px >= 18.66)) ? 3 : 4.5;
    const cr = ratio(fg, bg);
    if (cr + 0.005 >= need) continue;
    const name = 'svg text.' + (t.getAttribute('class') || '').trim().split(/\s+/).join('.');
    const key = name + hex(fg) + hex(bg);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(name + ' "' + t.textContent.trim().replace(/\s+/g, ' ').slice(0, 30) + '" ' + hex(fg) + ' on ' + hex(bg) + ' = ' + cr.toFixed(2) + ':1 (needs ' + need + ')');
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
    urls = only or (pages() + list(EXTRA))
    problems = defaultdict(list)  # rule -> [(url, msg)]
    seen_dom = set()

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
            ctx.add_init_script(SHIFTS)
            for url in urls:
                page = ctx.new_page()
                errs = []
                page.on("pageerror", lambda e: errs.append(str(e).splitlines()[0][:160]))
                page.on("console", lambda m: m.type == "error" and errs.append(m.text[:160]))
                try:
                    page.goto(base + url, wait_until="load", timeout=20000)
                    page.wait_for_timeout(300)  # let ResizeObserver / deferred scripts run
                    r = page.evaluate(PROBE)
                    named = page.evaluate(NAMES)
                    shifts = page.evaluate("window.__shifts || []")
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
                for m in named:
                    if (url, m) not in seen_dom:  # same issue at both widths: report once
                        seen_dom.add((url, m))
                        problems["a11y-dom"].append((url, "%dpx: %s" % (width, m)))
                cls = sum(v for v, _ in shifts)
                if cls > CLS_MAX:
                    movers = ", ".join(dict.fromkeys(w for _, ws in sorted(shifts, key=lambda x: -x[0]) for w in ws))
                    problems["layout-shift"].append((url, "%dpx: CLS %.3f (%s)" % (width, cls, movers[:120] or "no source reported")))
                for s in r["stuck"]:
                    problems["scroll-focus"].append((url, "%dpx: %s scrolls but isn't focusable" % (width, s)))
                page.close()
            ctx.close()
        for theme in THEMES:
            ctx = browser.new_context(viewport={"width": 1280, "height": 800}, service_workers="block",
                                      reduced_motion="reduce")
            ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
            ctx.add_init_script("try { localStorage.setItem('blog_color_theme', '%s'); } catch (e) {}" % theme)
            for url in urls:
                page = ctx.new_page()
                try:
                    page.goto(base + url, wait_until="load", timeout=20000)
                    page.wait_for_timeout(300)
                    for m in page.evaluate(CONTRAST):
                        problems["contrast"].append((url, "%s: %s" % (theme, m)))
                except Exception as e:
                    problems["load"].append((url, "%s: %s" % (theme, str(e).splitlines()[0][:160])))
                page.close()
            ctx.close()
        browser.close()
    srv.shutdown()

    total = sum(len(v) for v in problems.values())
    for rule, items in sorted(problems.items()):
        ex = "; ".join("%s (%s)" % (u, m) for u, m in items[:4])
        print("::warning title=browser %s::%d issue(s), e.g. %s" % (rule, len(items), ex))
    lines = ["### Browser check", "", "%d pages × %s px, contrast in %s: %d issue(s)" % (len(urls), "/".join(map(str, WIDTHS)), "/".join(THEMES), total), ""]
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
