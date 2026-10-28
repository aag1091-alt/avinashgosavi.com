---
layout: default
title: Conferences & Community
permalink: /events/
description: Conferences, hackathons and community events Avinash Gosavi has attended, hacked at, judged or mentored at, going back to RubyConf India 2013.
---

{%- comment -%}
An "upcoming" event counts as past at build time once its last day (end_date or
date) is more than a day behind the build clock (UTC), and the script below moves
it in the browser from the day after (visitor's local date) — so a finished event
leaves Upcoming on time even before an editor flips its status in events.yml.
{%- endcomment -%}
{%- assign ev_cutoff = site.time | date: "%s" | minus: 86400 | date: "%Y-%m-%d" -%}
{%- assign upcoming_all = site.data.events | where: "status", "upcoming" | sort: "date" -%}
{%- assign upcoming = "" | split: "" -%}{%- assign ended = "" | split: "" -%}
{%- for e in upcoming_all -%}{%- assign e_end = e.end_date | default: e.date | date: "%Y-%m-%d" -%}
{%- if e_end < ev_cutoff -%}{%- assign ended = ended | push: e -%}{%- else -%}{%- assign upcoming = upcoming | push: e -%}{%- endif -%}
{%- endfor -%}
{%- assign past = site.data.events | where: "status", "past" | concat: ended | sort: "date" | reverse -%}
{%- assign confs = past | where: "role", "attended" -%}
{%- assign hacks = past | where: "role", "hacker" -%}
<div class="events-page">
  <h1>Conferences &amp; Community</h1>
  <p class="page-lede">I've been showing up to Ruby conferences since RubyConf India 2013 — {{ confs.size }} conferences and {{ hacks.size }} hackathons so far, plus regular SF Ruby and East Bay Ruby meetups (including the ones hosted at Cisco Meraki). Where I wrote up what I learned, it's linked — and my favorite recordings are on <a href="{{ '/talks/' | relative_url }}">talks worth watching</a>.</p>

  {% if upcoming.size > 0 %}
  <h2 id="upcoming">Upcoming</h2>
  <ul class="event-list" id="upcoming-list">
    {% for e in upcoming %}{% include event-row.html e=e %}{% endfor %}
  </ul>
  <p class="events-ics" id="events-ics"><a href="{{ '/events.ics' | relative_url }}" type="text/calendar">Add upcoming events to your calendar</a> <span>(.ics — subscribe to the link and new ones appear on their own)</span></p>
  {% endif %}

  <h2 id="past">Past</h2>
  <ul class="event-list" id="past-list">
    {% for e in past %}{% include event-row.html e=e %}{% endfor %}
  </ul>
</div>

<script>
/* Upcoming events whose dates include today (visitor's local date) get a "Happening now" tag,
   ones still ahead get a countdown, and ones that have ended move to the top of Past (and Upcoming disappears if it empties). */
(function () {
  var d = new Date(), p = function (n) { return (n < 10 ? "0" : "") + n; };
  var today = d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
  var up = document.getElementById("upcoming-list"), past = document.getElementById("past-list");
  if (!up) return;
  up.querySelectorAll(".event-row[data-start]").forEach(function (row) {
    if (row.dataset.end < today && past) {
      var tag = row.querySelector(".event-live");
      if (tag) tag.remove();
      past.insertBefore(row, past.firstElementChild);
    } else if (row.dataset.start <= today && today <= row.dataset.end) {
      var live = row.querySelector(".event-live");
      if (live) live.hidden = false;
    } else if (today < row.dataset.start) {
      /* Not started yet: say how far off it is ("tomorrow", "in 5 days"), by calendar days. */
      var s = row.dataset.start.split("-");
      var days = Math.round((new Date(+s[0], s[1] - 1, +s[2]) - new Date(d.getFullYear(), d.getMonth(), d.getDate())) / 864e5);
      var name = row.querySelector(".event-name");
      if (name && days > 0) {
        var c = document.createElement("span");
        c.className = "event-countdown";
        c.textContent = days === 1 ? "tomorrow" : "in " + days + " days";
        name.parentNode.insertBefore(c, name.nextSibling);
      }
    }
  });
  if (!up.children.length) {
    up.hidden = true;
    var h = document.getElementById("upcoming");
    if (h) h.hidden = true;
    var ics = document.getElementById("events-ics");
    if (ics) ics.hidden = true;
  }
})();
</script>
