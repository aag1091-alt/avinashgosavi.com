---
layout: default
description: "Writing by Avinash Gosavi on distributed systems, API design, privacy-first AI tools, agent memory and the craft of software engineering."
title: All Posts
---

<div class="blog-page">
  <h1>All Posts</h1>
  {% assign writing_posts = site.posts | where_exp: "p", "p.series != 'paper-tldr'" %}
  <p class="page-lede">Paper summaries live in their own section: <a href="{{ '/paper-tldr/' | relative_url }}">Paper TL;DR →</a> · Prefer reading in order? <a href="{{ '/series/' | relative_url }}">Browse the series →</a> · <a id="blog-feed-link" href="{{ '/feed.xml' | relative_url }}" data-default="{{ '/feed.xml' | relative_url }}">Subscribe via RSS</a><span id="blog-random-wrap" hidden> · <a id="blog-random" href="{{ writing_posts.first.url | relative_url }}" title="Opens one of the posts listed below, at random">Read a random post</a></span></p>

  <div id="search" class="search-box" role="search">
    <label for="post-search" class="visually-hidden">Search posts</label>
    <input type="search" id="post-search" placeholder="Search posts…" aria-label="Search posts">
  </div>

  {% assign feed_min = site.topic_feed_min | default: 2 %}{% comment %} same setting _plugins/topic_feeds.rb reads {% endcomment %}
  {% assign all_tags = writing_posts | map: "tags" | join: "," | split: "," | uniq | sort %}
  <div class="tag-filter" role="group" aria-label="Filter by topic">
    <button type="button" class="tag-chip is-active" data-tag="" aria-pressed="true">All</button>
    {% for t in all_tags %}{% if t == "" %}{% continue %}{% endif %}{% assign tagged = writing_posts | where_exp: "p", "p.tags contains t" %}{% assign feed_tagged = site.posts | where_exp: "p", "p.tags contains t" %}<button type="button" class="tag-chip" data-tag="{{ t | slugify }}"{% if feed_tagged.size >= feed_min %} data-feed="{{ t | slugify | prepend: '/feed/topic/' | append: '.xml' | relative_url }}"{% endif %} aria-pressed="false">{{ t }} <span class="tag-count">{{ tagged.size }}</span></button>{% endfor %}
  </div>
  <p id="post-count" class="search-status blog-count" role="status" aria-live="polite"></p>

  <ul id="post-list" class="post-list blog-list">
    {% assign sorted_posts = writing_posts | sort: 'date' | reverse %}
    {% for post in sorted_posts %}
    <li class="post-list-item blog-list-item" data-title="{{ post.title | downcase }}" data-excerpt="{{ post.excerpt | strip_html | downcase }}" data-tags="{% for t in post.tags %}{{ t | slugify }} {% endfor %}">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <div class="post-list-meta">
        <span>{{ site.author.username }}</span>
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %d, %Y" }}</time>
        <span>{% include read-time.html content=post.content %}</span>
      </div>
      <p class="post-list-excerpt">{{ post.excerpt | strip_html | truncate: 200 }}</p>
    </li>
    {% endfor %}
  </ul>

  <p id="blog-suggest" class="search-suggest" hidden></p>
  <p id="no-results" class="no-results" hidden>No posts match your search. <a href="{{ '/search/' | relative_url }}">Search projects, papers, talks and pages too →</a></p>
</div>

<script>
(function() {
  var input = document.getElementById('post-search');
  var list = document.getElementById('post-list');
  var items = list ? list.querySelectorAll('.blog-list-item') : [];
  var noResults = document.getElementById('no-results');
  var count = document.getElementById('post-count');
  if (!input || !list) return;
  var countTimer;

  var activeTag = '';
  var chips = document.querySelectorAll('.tag-chip');
  var suggest = document.getElementById('blog-suggest');
  /* Every word has to appear somewhere in the title, excerpt or tags, in any
     order: "memory hopfield" finds the Hopfield posts. */
  var hay = [];
  items.forEach(function(item, i) {
    hay[i] = (item.getAttribute('data-title') || '') + ' ' + (item.getAttribute('data-excerpt') || '') + ' ' + (item.getAttribute('data-tags') || '').replace(/-/g, ' ');
  });
  function terms(q) { return q.split(/\s+/).filter(Boolean); }
  function tagOk(item) {
    return !activeTag || (' ' + (item.getAttribute('data-tags') || '') + ' ').indexOf(' ' + activeTag + ' ') !== -1;
  }
  function hit(i, ts) { return ts.every(function(t) { return hay[i].indexOf(t) !== -1; }); }
  /* "Did you mean …?" when nothing matches: swap each word that appears in no
     post for the closest word the posts use (1 typo, 2 for 6+ letters; words
     in titles and tags win ties), offered only if that finds a post. Same idea
     as /search/, with a vocabulary from this list. */
{% include typo-suggest.js %}
  var vocab = null;
  function buildVocab() {
    vocab = {};
    items.forEach(function(item) {
      ['data-title', 'data-tags', 'data-excerpt'].forEach(function(f, n) {
        typoAdd(vocab, item.getAttribute(f), n < 2 ? 20 : 1);
      });
    });
  }
  function didYouMean(ts) {
    if (!vocab) buildVocab();
    var fixed = false;
    var out = ts.map(function(t) {
      if (t.length < 3 || hay.some(function(h) { return h.indexOf(t) !== -1; })) return t;
      var c = typoClosest(vocab, t);
      if (c) fixed = true;
      return c || t;
    });
    if (!fixed) return '';
    for (var i = 0; i < items.length; i++) if (tagOk(items[i]) && hit(i, out)) return out.join(' ');
    return '';
  }
  function showSuggest(alt) {
    if (!suggest) return;
    suggest.innerHTML = '';
    suggest.hidden = !alt;
    if (!alt) return;
    var a = document.createElement('a');
    a.href = '?q=' + encodeURIComponent(alt) + (activeTag ? '#' + activeTag : '');
    a.textContent = alt;
    a.addEventListener('click', function(e) {
      e.preventDefault();
      input.value = alt;
      apply();
      syncUrl();
      input.focus();
    });
    suggest.appendChild(document.createTextNode('Did you mean '));
    suggest.appendChild(a);
    suggest.appendChild(document.createTextNode('?'));
  }
  var alt = '';
  function apply() {
    var q = (input.value || '').trim().toLowerCase();
    var ts = terms(q);
    var visible = 0;
    items.forEach(function(item, i) {
      var show = (!ts.length || hit(i, ts)) && tagOk(item);
      item.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    alt = visible === 0 && ts.length ? didYouMean(ts) : '';
    showSuggest(alt);
    if (noResults) {
      noResults.hidden = visible > 0;
      /* Carry the words over to the site-wide search. */
      var more = noResults.querySelector('a');
      if (more) more.href = more.href.split('?')[0] + (q ? '?q=' + encodeURIComponent(input.value.trim()) : '');
    }
    /* Say how many posts are showing (screen readers hear it via role=status);
       debounced so typing doesn't announce every keystroke. */
    clearTimeout(countTimer);
    countTimer = setTimeout(function() {
      if (!count) return;
      count.classList.toggle('visually-hidden', visible === 0);
      if (!q && !activeTag) { count.textContent = ''; return; }
      var chip = document.querySelector('.tag-chip.is-active');
      var label = activeTag && chip ? chip.firstChild.textContent.trim() : '';
      count.textContent = visible === 0 ? 'No posts match.' + (alt ? ' Did you mean \u201c' + alt + '\u201d?' : '') :
        'Showing ' + visible + ' of ' + items.length + ' posts' + (label ? ' tagged \u201c' + label + '\u201d' : '') + (q ? ' matching \u201c' + input.value.trim() + '\u201d' : '') + '.';
    }, q ? 400 : 0);
  }
  /* Keep the search in the address too (/blog/?q=hopfield#paper-tldr) so a
     filtered list can be shared or bookmarked. */
  var urlTimer;
  function syncUrl() {
    if (!history.replaceState) return;
    var params = new URLSearchParams(location.search);
    var q = input.value.trim();
    if (q) params.set('q', q); else params.delete('q');
    var qs = params.toString();
    history.replaceState(null, '', location.pathname + (qs ? '?' + qs : '') + (activeTag ? '#' + activeTag : ''));
  }
  input.addEventListener('input', function() {
    apply();
    clearTimeout(urlTimer);
    urlTimer = setTimeout(syncUrl, 400);
  });
  chips.forEach(function(chip) {
    chip.addEventListener('click', function() {
      activeTag = chip.getAttribute('data-tag') || '';
      chips.forEach(function(c) { c.classList.toggle('is-active', c === chip); c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      apply();
      /* The RSS link follows the topic: /feed/topic/<slug>.xml when it has one. */
      var feedLink = document.getElementById('blog-feed-link');
      if (feedLink) {
        var f = chip.getAttribute('data-feed');
        feedLink.href = f || feedLink.getAttribute('data-default');
        feedLink.textContent = f ? 'Subscribe to \u201c' + chip.firstChild.textContent.trim() + '\u201d via RSS' : 'Subscribe via RSS';
      }
      /* Keep the address shareable: /blog/#agent-memory reopens this filter. */
      if (!fromHash && history.replaceState) {
        syncUrl();
      }
    });
  });
  var fromHash = false;
  function applyHash() {
    var hash = decodeURIComponent((location.hash || '').replace('#', ''));
    fromHash = true;
    chips.forEach(function(c) { if (c.getAttribute('data-tag') === hash) c.click(); });
    fromHash = false;
  }
  var startQ = new URLSearchParams(location.search).get('q');
  if (startQ) { input.value = startQ; apply(); }
  if (location.hash) applyHash();
  window.addEventListener('hashchange', applyHash);
  /* "Read a random post": picks from the posts showing right now, so it
     respects the topic chip and search box; never the same post twice in a
     row. Hidden without JS (the link alone would always open one post). */
  var rnd = document.getElementById('blog-random');
  if (rnd) {
    document.getElementById('blog-random-wrap').hidden = false;
    rnd.addEventListener('click', function(e) {
      var urls = [];
      items.forEach(function(item) {
        var a = item.querySelector('a');
        if (a && item.style.display !== 'none') urls.push(a.getAttribute('href'));
      });
      if (!urls.length) return;
      var last = null;
      try { last = sessionStorage.getItem('blog-random-last'); } catch (err) {}
      if (urls.length > 1) urls = urls.filter(function(u) { return u !== last; });
      var pick = urls[Math.floor(Math.random() * urls.length)];
      try { sessionStorage.setItem('blog-random-last', pick); } catch (err) {}
      e.preventDefault();
      location.href = pick;
    });
  }
})();
</script>
