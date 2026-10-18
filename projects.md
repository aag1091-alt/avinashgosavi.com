---
layout: default
description: "Open-source side projects by Avinash Gosavi — encrypted memory for AI agents, voice AI, local-first tools and developer utilities."
title: Hobby Projects
permalink: /projects/
---

<div class="projects-page">
  <h1>Hobby Projects</h1>
  <p class="projects-lede">Things I build off hours — mostly privacy-first AI tools, agents, and small utilities I wanted for myself. Most have a write-up on the blog; all of them are open source.</p>
  <div class="project-grid">
    {% for project in site.data.projects %}
      {% include project-card.html project=project %}
    {% endfor %}
  </div>
</div>
