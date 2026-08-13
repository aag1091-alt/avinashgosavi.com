---
layout: default
title: Projects
permalink: /projects/
---

<div class="projects-page">
  <h1>Projects</h1>
  <p class="projects-lede">Things I've built — mostly privacy-first AI tools, voice interfaces, and agents. Each has a write-up on the blog.</p>
  <div class="project-grid">
    {% for project in site.data.projects %}
      {% include project-card.html project=project %}
    {% endfor %}
  </div>
</div>
