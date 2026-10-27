---
layout: default
description: "Writing by Avinash Gosavi on distributed systems, API design, privacy-first AI tools, agent memory and the craft of software engineering."
title: All Posts
---

<div class="blog-page">
  <h1>All Posts</h1>
  {% assign writing_posts = site.posts | where_exp: "p", "p.series != 'paper-tldr'" %}
  <p class="page-lede">Paper summaries live in their own section: <a href="{{ '/paper-tldr/' | relative_url }}">Paper TL;DR →</a> · Prefer reading in order? <a href="{{ '/series/' | relative_url }}">Browse the series →</a> · <a href="{{ '/feed.xml' | relative_url }}">Subscribe via RSS</a></p>

  <div id="search" class="search-box" role="search">
    <label for="post-search" class="visually-hidden">Search posts</label>
    <input type="search" id="post-search" placeholder="Search posts…" aria-label="Search posts">
  </div>

  {% assign all_tags = writing_posts | map: "tags" | join: "," | split: "," | uniq | sort %}
  <div class="tag-filter" role="group" aria-label="Filter by topic">
    <button type="button" class="tag-chip is-active" data-tag="" aria-pressed="true">All</button>
    {% for t in all_tags %}{% if t == "" %}{% continue %}{% endif %}{% assign tagged = writing_posts | where_exp: "p", "p.tags contains t" %}<button type="button" class="tag-chip" data-tag="{{ t | slugify }}" aria-pressed="false">{{ t }} <span class="tag-count">{{ tagged.size }}</span></button>{% endfor %}
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
  function apply() {
    var q = (input.value || '').trim().toLowerCase();
    var visible = 0;
    items.forEach(function(item) {
      var title = (item.getAttribute('data-title') || '');
      var excerpt = (item.getAttribute('data-excerpt') || '');
      var tags = ' ' + (item.getAttribute('data-tags') || '') + ' ';
      var matchQ = !q || title.indexOf(q) !== -1 || excerpt.indexOf(q) !== -1;
      var matchT = !activeTag || tags.indexOf(' ' + activeTag + ' ') !== -1;
      var show = matchQ && matchT;
      item.style.display = show ? '' : 'none';
      if (show) visible++;
    });
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
      count.textContent = visible === 0 ? 'No posts match.' :
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
})();
</script>
