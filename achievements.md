---
layout: default
title: Achievements
permalink: /achievements/
description: Engineering impact, open-source work, community roles and education of Avinash Gosavi, Staff Software Engineer at Cisco Meraki.
---

<div class="achievements-page">
  <h1>Achievements</h1>
  <p class="page-lede">A few things I've worked on that I'm glad I got to be part of — with links wherever there's something public to look at.</p>
  {% for group in site.data.achievements %}
  <section class="achievement-group">
    <h2 id="{{ group.section | replace: '&', ' and ' | slugify }}">{{ group.section }}</h2>
    <ul class="achievement-list">
      {% for a in group.items %}
      <li class="achievement">
        <div class="achievement-head">
          <span class="achievement-title">{{ a.title }}</span>
          {% if a.year %}<span class="achievement-year">{{ a.year }}</span>{% endif %}
        </div>
        {% if a.detail %}<p class="achievement-detail">{{ a.detail }}</p>{% endif %}
        {% if a.links %}<p class="achievement-links">{% for l in a.links %}<a href="{{ l.url | relative_url }}">{{ l.label }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}</p>{% endif %}
      </li>
      {% endfor %}
    </ul>
  </section>
  {% endfor %}
</div>
