---
layout: default
title: Conferences & Community
permalink: /events/
description: Conferences, hackathons and community events Avinash Gosavi has attended, hacked at or judged — from RubyConf India 2013 to SF Ruby 2025.
---

{% assign upcoming = site.data.events | where: "status", "upcoming" | sort: "date" %}
{% assign past = site.data.events | where: "status", "past" | sort: "date" | reverse %}
{% assign confs = site.data.events | where: "role", "attended" %}
{% assign hacks = site.data.events | where: "role", "hacker" %}
<div class="events-page">
  <h1>Conferences &amp; Community</h1>
  <p class="page-lede">I've been showing up to Ruby conferences since RubyConf India 2013 — {{ confs.size }} conferences and {{ hacks.size }} hackathons so far, plus regular SF Ruby and East Bay Ruby meetups (including the ones hosted at Cisco Meraki). Where I wrote up what I learned, it's linked — and my favorite recordings are on <a href="{{ '/talks/' | relative_url }}">talks worth watching</a>.</p>

  {% if upcoming.size > 0 %}
  <h2>Upcoming</h2>
  <ul class="event-list">
    {% for e in upcoming %}{% include event-row.html e=e %}{% endfor %}
  </ul>
  {% endif %}

  <h2>Past</h2>
  <ul class="event-list">
    {% for e in past %}{% include event-row.html e=e %}{% endfor %}
  </ul>
</div>
