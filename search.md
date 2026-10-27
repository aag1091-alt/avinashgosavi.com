---
layout: default
title: Search
permalink: /search/
description: Search every post, page, project, paper, talk and event on avinashgosavi.com.
sitemap: false
---

<div class="search-page">
  <h1>Search</h1>
  <p class="page-lede">Posts, projects, papers, talks, events and pages — all in one place.</p>

  <form class="site-search-form" role="search" action="{{ '/search/' | relative_url }}" method="get">
    <label for="site-search" class="visually-hidden">Search the site</label>
    <input type="search" id="site-search" name="q" placeholder="Try “embeddings” or “VaultMem”…" autocomplete="off" spellcheck="false">
  </form>

  <p class="search-hint" aria-hidden="true">Tip: press <kbd>↓</kbd> to move through results, <kbd>Esc</kbd> to clear.</p>
  <p id="search-status" class="search-status" role="status" aria-live="polite"></p>
  <div id="search-filter" class="tag-filter search-filter" role="group" aria-label="Show only one kind of result" hidden></div>
  <ol id="search-results" class="search-results"></ol>
  <noscript><p>Search needs JavaScript. You can <a href="{{ '/blog/' | relative_url }}">browse all posts</a> instead.</p></noscript>
</div>

<script>
(function() {
  var input = document.getElementById('site-search');
  var list = document.getElementById('search-results');
  var status = document.getElementById('search-status');
  var form = input.form;
  var filter = document.getElementById('search-filter');
  var index = null, timer = null, sayTimer = null;

  /* The status line is a live region: while someone is typing, wait 400ms so
     screen readers hear the settled result count, not one per keystroke. */
  function say(msg, wait) {
    clearTimeout(sayTimer);
    if (!wait) { status.textContent = msg; return; }
    sayTimer = setTimeout(function() { status.textContent = msg; }, 400);
  }
  var W = { title: 10, tags: 5, desc: 3, text: 1 };
  var TYPES = ['Post', 'Project', 'Paper', 'Talk', 'Event', 'Page'];
  var PLURAL = { Post: 'Posts', Project: 'Projects', Paper: 'Papers', Talk: 'Talks', Event: 'Events', Page: 'Pages' };
  var params = new URLSearchParams(location.search);
  /* A ?q= link only shows results once search.json arrives — hold the space now so
     the footer doesn't jump up the screen and back (layout shift) when they land. */
  if ((params.get('q') || '').trim()) list.style.minHeight = '100vh';
  var activeType = TYPES.indexOf(params.get('type')) !== -1 ? params.get('type') : '';

  function terms(q) {
    return q.toLowerCase().split(/\s+/).filter(function(t) { return t.length > 1; });
  }

  function score(item, ts) {
    var total = 0;
    for (var i = 0; i < ts.length; i++) {
      var t = ts[i], s = 0;
      for (var f in W) {
        var v = item['_' + f];
        if (!v) continue;
        var at = v.indexOf(t);
        if (at === -1) continue;
        s += W[f];
        if (f === 'title' && (at === 0 || v.charAt(at - 1) === ' ')) s += 5;
      }
      if (!s) return 0; // every term must match somewhere
      total += s;
    }
    return total;
  }

  function snippet(item, ts) {
    var src = item.text || item.desc || '';
    var low = src.toLowerCase(), at = -1;
    for (var i = 0; i < ts.length && at === -1; i++) at = low.indexOf(ts[i]);
    if (at === -1) { src = item.desc || src; at = 0; }
    var start = Math.max(0, at - 70);
    var out = src.slice(start, start + 200);
    return (start > 0 ? '…' : '') + out + (start + 200 < src.length ? '…' : '');
  }

  // Text fragment (#:~:text=) so the post opens scrolled to the matched words, highlighted.
  // Browsers without support just open the page at the top; anchored URLs keep their own #id.
  var WORD = /[0-9A-Za-z_\u00C0-\u024F]/;
  function fragment(item, ts) {
    if (!item.text || item.url.indexOf('#') !== -1) return '';
    var src = item.text, low = src.toLowerCase();
    for (var i = 0; i < ts.length; i++) {
      var at = low.indexOf(ts[i]);
      if (at === -1) continue;
      var s = at, e = at + ts[i].length;
      while (s > 0 && WORD.test(src.charAt(s - 1))) s--;
      while (e < src.length && WORD.test(src.charAt(e))) e++;
      var more = src.slice(e, e + 50).match(/^(?: [0-9A-Za-z_\u00C0-\u024F]+){0,2}/);
      var word = src.slice(s, e), phrase = word + (more ? more[0] : '');
      var enc = function(t) { return encodeURIComponent(t).replace(/-/g, '%2D'); };
      // If the phrase spans a block boundary in the rendered post (heading → paragraph,
      // list items) it won't match; the second directive falls back to the word alone.
      return '#:~:text=' + enc(phrase) + (phrase !== word ? '&text=' + enc(word) : '');
    }
    return '';
  }

  function highlight(el, str, ts) {
    var re = new RegExp('(' + ts.map(function(t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')', 'gi');
    var last = 0, m;
    while ((m = re.exec(str))) {
      el.appendChild(document.createTextNode(str.slice(last, m.index)));
      var mk = document.createElement('mark');
      mk.textContent = m[0];
      el.appendChild(mk);
      last = m.index + m[0].length;
    }
    el.appendChild(document.createTextNode(str.slice(last)));
  }

  function chip(type, label, count) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'tag-chip' + (type === activeType ? ' is-active' : '');
    b.setAttribute('aria-pressed', type === activeType ? 'true' : 'false');
    b.setAttribute('data-type', type);
    b.appendChild(document.createTextNode(label + ' '));
    var c = document.createElement('span');
    c.className = 'tag-count';
    c.textContent = count;
    b.appendChild(c);
    return b;
  }

  function renderFilter(all, counts, refocus) {
    filter.innerHTML = '';
    var kinds = TYPES.filter(function(t) { return counts[t]; });
    if (kinds.length < 2) { filter.hidden = true; return; }
    filter.appendChild(chip('', 'All', all));
    kinds.forEach(function(t) { filter.appendChild(chip(t, PLURAL[t], counts[t])); });
    filter.hidden = false;
    if (refocus) {
      var on = filter.querySelector('.is-active');
      if (on) on.focus();
    }
  }

  function render(refocus, typing) {
    var q = input.value.trim();
    var qs = [];
    if (q) qs.push('q=' + encodeURIComponent(q));
    if (q && activeType) qs.push('type=' + activeType);
    history.replaceState(null, '', qs.length ? '?' + qs.join('&') : location.pathname);
    list.innerHTML = '';
    filter.hidden = true;
    if (!q) { list.style.minHeight = ''; say(''); return; }
    if (!index) { say('Loading…', typing); return; }
    var ts = terms(q);
    if (!ts.length) { say('Type at least two letters.', typing); return; }
    var all = index.map(function(it) { return { it: it, s: score(it, ts) }; })
      .filter(function(h) { return h.s > 0; })
      .sort(function(a, b) { return b.s - a.s; });
    var counts = {};
    all.forEach(function(h) { counts[h.it.type] = (counts[h.it.type] || 0) + 1; });
    if (activeType && !counts[activeType]) activeType = '';
    renderFilter(all.length, counts, refocus);
    var hits = all.filter(function(h) { return !activeType || h.it.type === activeType; }).slice(0, 30);
    say(hits.length
      ? hits.length + (hits.length === 1 ? ' result' : ' results') + (activeType ? ' (' + PLURAL[activeType].toLowerCase() + ')' : '') + ' for “' + q + '”'
      : 'Nothing matches “' + q + '”. Try a shorter or different word.', typing);
    hits.forEach(function(h) {
      var it = h.it;
      var li = document.createElement('li');
      li.className = 'search-result';
      var meta = document.createElement('div');
      meta.className = 'search-result-meta';
      meta.textContent = it.type + (it.date ? ' · ' + it.date : '');
      var a = document.createElement('a');
      a.href = it.url + fragment(it, ts);
      a.className = 'search-result-title';
      highlight(a, it.title, ts);
      var p = document.createElement('p');
      p.className = 'search-result-snippet';
      highlight(p, snippet(it, ts), ts);
      li.appendChild(meta); li.appendChild(a); li.appendChild(p);
      list.appendChild(li);
    });
  }

  filter.addEventListener('click', function(e) {
    var b = e.target.closest('button[data-type]');
    if (!b) return;
    activeType = b.getAttribute('data-type');
    render(true);
  });

  // Keyboard: ↓ from the box walks the result titles, ↑ walks back (and returns to the box); Esc clears.
  function links() { return Array.prototype.slice.call(list.querySelectorAll('.search-result-title')); }
  input.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowDown') {
      var ls = links();
      if (ls.length) { e.preventDefault(); ls[0].focus(); }
    } else if (e.key === 'Escape' && input.value) {
      e.preventDefault();
      input.value = '';
      render();
    }
  });
  list.addEventListener('keydown', function(e) {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' && e.key !== 'Escape') return;
    var ls = links(), i = ls.indexOf(document.activeElement);
    if (i === -1) return;
    e.preventDefault();
    if (e.key === 'Escape') { input.focus(); return; }
    var next = e.key === 'ArrowDown' ? i + 1 : i - 1;
    if (next < 0) input.focus();
    else if (next < ls.length) { ls[next].focus(); ls[next].scrollIntoView({ block: 'nearest' }); }
  });

  form.addEventListener('submit', function(e) { e.preventDefault(); render(); });
  input.addEventListener('input', function() { clearTimeout(timer); timer = setTimeout(function() { render(false, true); }, 120); });

  var initial = params.get('q');
  if (initial) input.value = initial;
  input.focus();

  fetch('{{ "/search.json" | relative_url }}')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      index = data.map(function(it) {
        for (var f in W) it['_' + f] = (it[f] || '').toLowerCase();
        return it;
      });
      render();
    })
    .catch(function() { say('Search index failed to load. Try the post list on the Writing page.'); });
})();
</script>
