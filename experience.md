---
layout: default
title: Experience
permalink: /experience/
---

<div class="experience-page">
  <h1>Experience</h1>
  <p class="experience-lede">13+ years building and operating production systems at enterprise scale — currently a Staff Software Engineer at Cisco Meraki.</p>

  <div class="timeline">
    {% for job in site.data.experience %}
    <section class="timeline-item">
      <header class="timeline-header">
        <h2 class="timeline-company">{{ job.company }}</h2>
        <span class="timeline-span">{{ job.span }}</span>
      </header>
      <p class="timeline-location">{{ job.location }}</p>
      {% for role in job.roles %}
      <div class="timeline-role">
        <h3 class="timeline-role-title">{{ role.title }}</h3>
        {% if role.highlights %}
        <ul class="timeline-highlights">
          {% for h in role.highlights %}
          <li>{{ h }}</li>
          {% endfor %}
        </ul>
        {% endif %}
      </div>
      {% endfor %}
      {% if job.tags %}
      <ul class="project-tags timeline-tags">
        {% for tag in job.tags %}
        <li>{{ tag }}</li>
        {% endfor %}
      </ul>
      {% endif %}
    </section>
    {% endfor %}
  </div>
</div>
