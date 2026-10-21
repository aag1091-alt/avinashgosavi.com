---
layout: default
description: "Open-source side projects by Avinash Gosavi — encrypted memory for AI agents, voice AI, local-first tools and developer utilities."
title: Hobby Projects
permalink: /projects/
---

<div class="projects-page">
  <h1>Hobby Projects</h1>
  <p class="projects-lede">Things I build off hours — mostly privacy-first AI tools, agents, and small utilities I wanted for myself. Most have a write-up on the blog; all of them are open source.</p>
  {% assign order = "Memory & privacy for AI|Agents & voice|Tools I wanted for myself|Just for fun" | split: "|" %}
  {% for cat in order %}
  {% assign group = site.data.projects | where: "category", cat %}
  {% if group.size > 0 %}
  <h2 class="project-category" id="{{ cat | replace: '&', ' and ' | slugify }}">{{ cat }}</h2>
  <div class="project-grid">
    {% for project in group %}
      {% include project-card.html project=project %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}
</div>
