---
layout: default
title: Series
permalink: /series/
description: Multi-part blog series by Avinash Gosavi, read in order.
---

<div class="series-page">
  <h1>Series</h1>
  <p class="page-lede">Multi-part write-ups, meant to be read in order. Each series has its own RSS feed if you only want new parts of one; <a href="{{ '/feed.xml' | relative_url }}">the main feed</a> has every post.</p>
  {% for s in site.data.series %}
  {% assign parts = site.posts | where: "series", s.slug | sort: "series_order" %}
  {% if parts.size > 0 %}
  <section class="series-section" id="{{ s.slug }}">
    <h2>{{ s.title }}</h2>
    <p class="series-description">{{ s.description }}</p>
    <p class="series-feed-link"><a href="{{ '/feed/' | append: s.slug | append: '.xml' | relative_url }}" type="application/atom+xml">{% include feed-icon.html %}Follow {{ s.title }} via RSS</a></p>
    <ol class="series-parts" role="list">
      {% for p in parts %}
      <li><a href="{{ p.url | relative_url }}">{{ p.title }}</a> <span class="series-meta"><time datetime="{{ p.date | date_to_xmlschema }}">{{ p.date | date: "%b %d, %Y" }}</time> · {% include read-time.html content=p.content %}</span></li>
      {% endfor %}
    </ol>
  </section>
  {% endif %}
  {% endfor %}
</div>

{% include read-marks.html items=".series-parts li" meta=".series-meta" %}
