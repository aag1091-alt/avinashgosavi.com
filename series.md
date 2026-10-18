---
layout: default
title: Series
permalink: /series/
description: Multi-part blog series by Avinash Gosavi, read in order.
---

<div class="series-page">
  <h1>Series</h1>
  <p class="page-lede">Multi-part write-ups, meant to be read in order.</p>
  {% for s in site.data.series %}
  {% assign parts = site.posts | where: "series", s.slug | sort: "series_order" %}
  {% if parts.size > 0 %}
  <section class="series-section" id="{{ s.slug }}">
    <h2>{{ s.title }}</h2>
    <p class="series-description">{{ s.description }}</p>
    <ol class="series-parts">
      {% for p in parts %}
      <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <span class="series-meta">{{ p.date | date: "%b %d, %Y" }}{% if p.read_time %} · {{ p.read_time }} min{% endif %}</span></li>
      {% endfor %}
    </ol>
  </section>
  {% endif %}
  {% endfor %}
</div>
