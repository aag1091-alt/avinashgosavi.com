---
layout: default
title: Now
permalink: /now/
description: What Avinash Gosavi is working on, building, reading and attending right now.
---

<div class="now-page">
  <h1>Now</h1>
  <p class="page-lede">What I'm focused on at the moment. Updated <time datetime="{{ site.data.now.updated | date: '%Y-%m-%d' }}">{{ site.data.now.updated | date: "%B %-d, %Y" }}</time>. <span class="muted">(Inspired by <a href="https://nownownow.com/about" rel="noopener">nownownow.com</a>.)</span></p>
  <dl class="now-list">
    {% for item in site.data.now.items %}
    <div class="now-item">
      <dt>{{ item.label }}</dt>
      <dd>{{ item.text }}{% if item.link %} <a class="now-more" href="{{ item.link | relative_url }}" aria-label="More about {{ item.label | downcase }}">→</a>{% endif %}</dd>
    </div>
    {% endfor %}
  </dl>
</div>
