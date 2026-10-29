---
layout: default
title: Changelog
permalink: /changelog/
description: What's new on avinashgosavi.com — new writing, design changes and site improvements, newest first.
---

<div class="changelog-page">
  <h1>Changelog</h1>
  <p class="page-lede">This site is a work in progress, and I like it that way. Here's what changed recently — new writing, design tweaks and under-the-hood fixes. New posts also go out via <a href="{{ '/feed.xml' | relative_url }}">RSS</a>. The site runs on Jekyll and GitHub Pages — <a href="{{ '/post/building-your-website-with-jekyll-and-github-pages/' | relative_url }}">here's how that setup works</a>.</p>
  <p class="series-feed-link"><a href="{{ '/feed/changelog.xml' | relative_url }}" type="application/atom+xml">{% include feed-icon.html %}Follow the changelog via RSS</a></p>
  {% assign desks = "Writing,Design,Engineering" | split: "," %}
  <div class="tag-filter changelog-filter" role="group" aria-label="Filter by desk" hidden>
    <button type="button" class="tag-chip is-active" data-desk="" aria-pressed="true">All <span class="tag-count">{{ site.data.changelog.size }}</span></button>
    {% for d in desks %}{% assign dn = site.data.changelog | where: "desk", d %}{% if dn.size > 0 %}<button type="button" class="tag-chip" data-desk="{{ d | slugify }}" aria-pressed="false">{{ d }} <span class="tag-count">{{ dn.size }}</span></button>{% endif %}{% endfor %}
  </div>
  <p id="changelog-count" class="search-status blog-count" role="status" aria-live="polite"></p>
  {% assign by_date = site.data.changelog | group_by: "date" %}
  {% assign recent_days = 7 %}{% assign fold_at = recent_days | plus: 1 %}
  {% assign recent_n = 0 %}{% for day in by_date limit: recent_days %}{% assign recent_n = recent_n | plus: day.items.size %}{% endfor %}
  {% assign older_n = site.data.changelog.size | minus: recent_n %}
  {% for day in by_date %}
  {% if forloop.index == fold_at %}
  <details class="changelog-older" id="older">
    <summary>{{ older_n }} earlier changes, {{ by_date.last.name | date: "%B %-d" }} – {{ day.name | date: "%B %-d, %Y" }}</summary>
  {% endif %}
  <section class="changelog-day">
    <h2 class="changelog-date" id="{{ day.name | date: '%B %-d, %Y' | slugify }}"><time datetime="{{ day.name | date: '%Y-%m-%d' }}">{{ day.name | date: "%B %-d, %Y" }}</time></h2>
    <ul class="changelog-list">
      {% for c in day.items %}
      <li data-desk="{{ c.desk | slugify }}"><span class="changelog-desk changelog-desk-{{ c.desk | slugify }}">{{ c.desk }}</span> {{ c.text }}{% if c.link %} <a href="{{ c.link | relative_url }}" aria-label="See: {{ c.text | truncatewords: 6 | escape }}">→</a>{% endif %}</li>
      {% endfor %}
    </ul>
  </section>
  {% endfor %}
  {% if by_date.size > recent_days %}</details>{% endif %}
</div>

<script>
/* Desk filter: show only Writing, Design or Engineering changes. /changelog/#design opens a filter. */
(function () {
  var bar = document.querySelector('.changelog-filter');
  if (!bar) return;
  var chips = bar.querySelectorAll('.tag-chip');
  var items = document.querySelectorAll('.changelog-list li[data-desk]');
  var days = document.querySelectorAll('.changelog-day');
  var count = document.getElementById('changelog-count');
  var older = document.querySelector('.changelog-older');
  bar.hidden = false;
  function apply(desk, fromHash) {
    var shown = 0, label = '';
    chips.forEach(function (c) {
      var on = (c.getAttribute('data-desk') || '') === desk;
      c.classList.toggle('is-active', on);
      c.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on && desk) label = c.firstChild.textContent.trim();
    });
    items.forEach(function (li) {
      var show = !desk || li.getAttribute('data-desk') === desk;
      li.hidden = !show;
      if (show) shown++;
    });
    days.forEach(function (day) { day.hidden = !day.querySelector('li:not([hidden])'); });
    if (older) {
      older.hidden = !older.querySelector('.changelog-day:not([hidden])');
      if (desk) older.open = true;
    }
    if (count) count.textContent = desk ? 'Showing ' + shown + ' of ' + items.length + ' changes from the ' + label + ' desk.' : '';
    if (!fromHash && history.replaceState) history.replaceState(null, '', location.pathname + location.search + (desk ? '#' + desk : ''));
  }
  chips.forEach(function (c) { c.addEventListener('click', function () { apply(c.getAttribute('data-desk') || ''); }); });
  function fromHash() {
    var h = decodeURIComponent(location.hash.slice(1));
    /* A date link like #october-19-2026 inside the folded older days opens them first */
    var t = h && document.getElementById(h);
    if (t && older && older.contains(t) && !older.open) { older.open = true; t.scrollIntoView(); }
    for (var i = 0; i < chips.length; i++) if (h && chips[i].getAttribute('data-desk') === h) return apply(h, true);
  }
  fromHash();
  addEventListener('hashchange', fromHash);
  if (older) addEventListener('beforeprint', function () { older.open = true; });
})();
</script>
