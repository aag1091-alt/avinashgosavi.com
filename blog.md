---
layout: default
description: "Writing by Avinash Gosavi on distributed systems, API design, privacy-first AI tools, agent memory and the craft of software engineering."
title: All Posts
---

<div class="blog-page">
  <h1>All Posts</h1>
  <p class="page-lede">Prefer reading in order? <a href="{{ '/series/' | relative_url }}">Browse the series →</a> · <a href="{{ '/feed.xml' | relative_url }}">Subscribe via RSS</a></p>

  <div id="search" class="search-box" role="search">
    <label for="post-search" class="visually-hidden">Search posts</label>
    <input type="search" id="post-search" placeholder="Search posts…" aria-label="Search posts">
  </div>

  {% assign all_tags = site.tags | sort %}
  <div class="tag-filter" role="group" aria-label="Filter by topic">
    <button type="button" class="tag-chip is-active" data-tag="">All</button>
    {% for t in all_tags %}<button type="button" class="tag-chip" data-tag="{{ t[0] | slugify }}">{{ t[0] }} <span class="tag-count">{{ t[1].size }}</span></button>{% endfor %}
  </div>

  <ul id="post-list" class="post-list blog-list">
    {% assign sorted_posts = site.posts | sort: 'date' | reverse %}
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

  <p id="no-results" class="no-results" hidden>No posts match your search. <a href="{{ '/search/' | relative_url }}">Search projects, papers and pages too →</a></p>
</div>

<script>
(function() {
  var input = document.getElementById('post-search');
  var list = document.getElementById('post-list');
  var items = list ? list.querySelectorAll('.blog-list-item') : [];
  var noResults = document.getElementById('no-results');
  if (!input || !list) return;

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
    if (noResults) noResults.hidden = visible > 0;
  }
  input.addEventListener('input', apply);
  chips.forEach(function(chip) {
    chip.addEventListener('click', function() {
      activeTag = chip.getAttribute('data-tag') || '';
      chips.forEach(function(c) { c.classList.toggle('is-active', c === chip); });
      apply();
    });
  });
  var hash = (location.hash || '').replace('#', '');
  if (hash) { chips.forEach(function(c) { if (c.getAttribute('data-tag') === hash) c.click(); }); }
})();
</script>
