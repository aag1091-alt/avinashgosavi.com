---
layout: default
title: All Posts
---

<div class="blog-page">
  <h1>All Posts</h1>

  <div id="search" class="search-box" role="search">
    <label for="post-search" class="visually-hidden">Search posts</label>
    <input type="search" id="post-search" placeholder="Search posts…" aria-label="Search posts">
  </div>

  <ul id="post-list" class="post-list blog-list">
    {% assign sorted_posts = site.posts | sort: 'date' | reverse %}
    {% for post in sorted_posts %}
    <li class="post-list-item blog-list-item" data-title="{{ post.title | downcase }}" data-excerpt="{{ post.excerpt | strip_html | downcase }}">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <div class="post-list-meta">
        <span>{{ site.author.username }}</span>
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %d, %Y" }}</time>
        {% if post.read_time %}<span>{{ post.read_time }} min read</span>{% endif %}
      </div>
      <p class="post-list-excerpt">{{ post.excerpt | strip_html | truncate: 200 }}</p>
    </li>
    {% endfor %}
  </ul>

  <p id="no-results" class="no-results" hidden>No posts match your search.</p>
</div>

<script>
(function() {
  var input = document.getElementById('post-search');
  var list = document.getElementById('post-list');
  var items = list ? list.querySelectorAll('.blog-list-item') : [];
  var noResults = document.getElementById('no-results');
  if (!input || !list) return;

  input.addEventListener('input', function() {
    var q = (this.value || '').trim().toLowerCase();
    var visible = 0;
    items.forEach(function(item) {
      var title = (item.getAttribute('data-title') || '');
      var excerpt = (item.getAttribute('data-excerpt') || '');
      var show = !q || title.indexOf(q) !== -1 || excerpt.indexOf(q) !== -1;
      item.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    if (noResults) noResults.hidden = visible > 0;
  });
})();
</script>
