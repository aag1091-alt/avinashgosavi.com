---
layout: default
title: Changelog
permalink: /changelog/
description: What's new on avinashgosavi.com — new writing, design changes and site improvements, newest first.
---

<div class="changelog-page">
  <h1>Changelog</h1>
  <p class="page-lede">This site is a work in progress, and I like it that way. Here's what changed recently — new writing, design tweaks and under-the-hood fixes. New posts also go out via <a href="{{ '/feed.xml' | relative_url }}">RSS</a>.</p>
  {% assign by_date = site.data.changelog | group_by: "date" %}
  {% for day in by_date %}
  <section class="changelog-day">
    <h2 class="changelog-date">{{ day.name | date: "%B %-d, %Y" }}</h2>
    <ul class="changelog-list">
      {% for c in day.items %}
      <li><span class="changelog-desk changelog-desk-{{ c.desk | slugify }}">{{ c.desk }}</span> {{ c.text }}{% if c.link %} <a href="{{ c.link | relative_url }}" aria-label="See: {{ c.text | truncatewords: 6 }}">→</a>{% endif %}</li>
      {% endfor %}
    </ul>
  </section>
  {% endfor %}
</div>
