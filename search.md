---
layout: default
title: Search
permalink: /search/
description: Search every post, page, project and paper on avinashgosavi.com.
sitemap: false
---

<div class="search-page">
  <h1>Search</h1>
  <p class="page-lede">Posts, projects, papers, events and pages — all in one place.</p>

  <form class="site-search-form" role="search" action="{{ '/search/' | relative_url }}" method="get">
    <label for="site-search" class="visually-hidden">Search the site</label>
    <input type="search" id="site-search" name="q" placeholder="Try “embeddings” or “VaultMem”…" autocomplete="off" spellcheck="false">
  </form>

  <p id="search-status" class="search-status" role="status" aria-live="polite"></p>
  <ol id="search-results" class="search-results"></ol>
  <noscript><p>Search needs JavaScript. You can <a href="{{ '/blog/' | relative_url }}">browse all posts</a> instead.</p></noscript>
</div>

<script>
(function() {
  var input = document.getElementById('site-search');
  var list = document.getElementById('search-results');
  var status = document.getElementById('search-status');
  var form = input.form;
  var index = null, timer = null;
  var W = { title: 10, tags: 5, desc: 3, text: 1 };

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

  function render() {
    var q = input.value.trim();
    var url = q ? '?q=' + encodeURIComponent(q) : location.pathname;
    history.replaceState(null, '', url);
    list.innerHTML = '';
    if (!q) { status.textContent = ''; return; }
    if (!index) { status.textContent = 'Loading…'; return; }
    var ts = terms(q);
    if (!ts.length) { status.textContent = 'Type at least two letters.'; return; }
    var hits = index.map(function(it) { return { it: it, s: score(it, ts) }; })
      .filter(function(h) { return h.s > 0; })
      .sort(function(a, b) { return b.s - a.s; })
      .slice(0, 30);
    status.textContent = hits.length ? hits.length + (hits.length === 1 ? ' result' : ' results') + ' for “' + q + '”' : 'Nothing matches “' + q + '”. Try a shorter or different word.';
    hits.forEach(function(h) {
      var it = h.it;
      var li = document.createElement('li');
      li.className = 'search-result';
      var meta = document.createElement('div');
      meta.className = 'search-result-meta';
      meta.textContent = it.type + (it.date ? ' · ' + it.date : '');
      var a = document.createElement('a');
      a.href = it.url;
      a.className = 'search-result-title';
      highlight(a, it.title, ts);
      var p = document.createElement('p');
      p.className = 'search-result-snippet';
      highlight(p, snippet(it, ts), ts);
      li.appendChild(meta); li.appendChild(a); li.appendChild(p);
      list.appendChild(li);
    });
  }

  form.addEventListener('submit', function(e) { e.preventDefault(); render(); });
  input.addEventListener('input', function() { clearTimeout(timer); timer = setTimeout(render, 120); });

  var initial = new URLSearchParams(location.search).get('q');
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
    .catch(function() { status.textContent = 'Search index failed to load. Try the post list on the Writing page.'; });
})();
</script>
