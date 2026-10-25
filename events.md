---
layout: default
title: Conferences & Community
permalink: /events/
description: Conferences, hackathons and community events Avinash Gosavi has attended, hacked at, judged or mentored at — from RubyConf India 2013 to SF Ruby 2025.
---

{% assign upcoming = site.data.events | where: "status", "upcoming" | sort: "date" %}
{% assign past = site.data.events | where: "status", "past" | sort: "date" | reverse %}
{% assign past_events = site.data.events | where: "status", "past" %}{% assign confs = past_events | where: "role", "attended" %}
{% assign hacks = past_events | where: "role", "hacker" %}
<div class="events-page">
  <h1>Conferences &amp; Community</h1>
  <p class="page-lede">I've been showing up to Ruby conferences since RubyConf India 2013 — {{ confs.size }} conferences and {{ hacks.size }} hackathons so far, plus regular SF Ruby and East Bay Ruby meetups (including the ones hosted at Cisco Meraki). Where I wrote up what I learned, it's linked — and my favorite recordings are on <a href="{{ '/talks/' | relative_url }}">talks worth watching</a>.</p>

  {% if upcoming.size > 0 %}
  <h2 id="upcoming">Upcoming</h2>
  <ul class="event-list">
    {% for e in upcoming %}{% include event-row.html e=e %}{% endfor %}
  </ul>
  {% endif %}

  <h2 id="past">Past</h2>
  <ul class="event-list">
    {% for e in past %}{% include event-row.html e=e %}{% endfor %}
  </ul>
</div>

<script>
/* Upcoming events whose dates include today (visitor's local date) get a "Happening now" tag. */
(function () {
  var d = new Date(), p = function (n) { return (n < 10 ? "0" : "") + n; };
  var today = d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
  document.querySelectorAll(".event-row[data-start]").forEach(function (row) {
    if (row.dataset.start <= today && today <= row.dataset.end) {
      var tag = row.querySelector(".event-live");
      if (tag) tag.hidden = false;
    }
  });
})();
</script>
