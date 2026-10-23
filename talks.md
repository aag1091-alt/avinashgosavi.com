---
layout: default
title: Talks Worth Watching
permalink: /talks/
description: "Conference talks Avinash Gosavi recommends — engineering in the AI era, Rails architecture, performance at scale and open source — each with a reason to watch."
---

<div class="talks-page">
  <h1>Talks Worth Watching</h1>
  <p class="page-lede">Conference talks I keep recommending, each with one line on why it's worth your time. Most are from <a href="{{ '/post/my-sf-ruby-2025-experience-talks-side-quests-community-inspiration/' | relative_url }}">SF Ruby 2025</a>; recordings are on RubyEvents.</p>
  {% assign groups = site.data.talks | group_by: "topic" %}
  {% for g in groups %}
  <h2 class="paper-topic" id="{{ g.name | replace: '&', ' and ' | slugify }}">{{ g.name }}</h2>
  <ul class="paper-list">
    {% for t in g.items %}
    <li class="paper">
      <a class="paper-title" href="{{ t.url }}" rel="noopener">{{ t.title }}</a>
      <div class="paper-meta">{{ t.speaker }} · {{ t.event }}</div>
      <p class="paper-why">{{ t.take }}</p>
    </li>
    {% endfor %}
  </ul>
  {% endfor %}
</div>
