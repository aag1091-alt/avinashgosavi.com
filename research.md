---
layout: default
title: Research & Interests
permalink: /research/
description: Topics Avinash Gosavi researches and builds around — private memory for AI agents, brain-inspired retrieval, local-first AI and API design at scale — plus a papershelf with TL;DRs.
---

<div class="research-page">
  <h1>Research &amp; Interests</h1>
  <p class="page-lede">What I keep coming back to, at work and off hours — and the papers that shaped how I think about it. Each paper gets a TL;DR, and the ones that shaped something I built get a note on how.</p>

  <h2 id="topics-i-follow">Topics I follow</h2>
  <ul class="interest-list">
    <li><strong>Private, user-owned memory for AI agents.</strong> If an agent remembers your life, the platform running it shouldn't be able to read that memory. <a href="{{ '/series/' | relative_url }}#vaultmem">VaultMem</a>, <a href="{{ '/post/daylog-security-architecture/' | relative_url }}">daylog</a>.</li>
    <li><strong>Brain-inspired retrieval.</strong> Associative memory, attractor dynamics and consolidation as alternatives to plain vector search. <a href="{{ '/post/attractor-memory-engine/' | relative_url }}">Attractor</a>.</li>
    <li><strong>Local-first AI.</strong> Running useful models on hardware you own — transcription, embeddings and chat without sending data to third parties. <a href="{{ '/post/live-audio-transcription-whisper/' | relative_url }}">Whisper on a $0 server</a>, <a href="{{ '/uses/' | relative_url }}">my setup</a>.</li>
    <li><strong>Distributed systems &amp; API design at scale.</strong> My day job: aggregating data across shards and products into APIs that stay fast for the biggest customers. <a href="{{ '/experience/' | relative_url }}">Experience</a>.</li>
    <li><strong>AI-assisted software engineering.</strong> Where AI genuinely speeds up engineering work — and how to keep its output honest. <a href="{{ '/post/doing-the-right-thing-fast/' | relative_url }}">Doing the right thing, fast</a>, <a href="{{ '/post/reviewing-ai-generated-tests-istqb-framework/' | relative_url }}">reviewing AI-generated tests</a>.</li>
    <li><strong>Ruby &amp; Rails architecture.</strong> Thirteen years in the community, from RubyConf India 2013 to SF Ruby 2025. <a href="{{ '/events/' | relative_url }}">Events</a>.</li>
  </ul>

  <h2 id="my-own-work">My own work</h2>
  <ul class="interest-list">
    <li><strong>VaultMem: zero-knowledge encrypted memory for AI agents</strong> — research preprint, 2026. <a href="https://doi.org/10.5281/zenodo.19154079" rel="noopener">Zenodo (DOI)</a> · <a href="https://pypi.org/project/vaultmem/" rel="noopener">PyPI</a> · <a href="https://github.com/aag1091-alt/vaultmem-sdk" rel="noopener">Code</a></li>
  </ul>

  <h2 id="papershelf">Papershelf</h2>
  <p>Prefer video? See <a href="{{ '/talks/' | relative_url }}">talks worth watching</a>.</p>
  {% assign groups = site.data.papers | group_by: "topic" %}
  {% for g in groups %}
  <h3 class="paper-topic">{{ g.name }}</h3>
  <ul class="paper-list">
    {% for p in g.items %}
    <li class="paper" id="paper-{{ p.title | slugify }}">
      <a class="paper-title" href="{{ p.url }}" rel="noopener">{{ p.title }}</a>
      <div class="paper-meta">{{ p.authors }} · {{ p.year }} · {{ p.venue }}</div>
      <p class="paper-tldr"><span class="paper-label">TL;DR</span> {{ p.tldr }}{% if p.tldr_post %} <a href="{{ p.tldr_post | relative_url }}">Full write-up →</a>{% endif %}</p>
      {% if p.why %}<p class="paper-why"><span class="paper-label">Why it matters to me</span> {{ p.why }}{% if p.post %} <a href="{{ p.post | relative_url }}" aria-label="Read more about {{ p.title | escape }}">Read more →</a>{% endif %}</p>{% endif %}
    </li>
    {% endfor %}
  </ul>
  {% endfor %}

  <h2 id="reading">Newsletters I read</h2>
  <ul class="interest-list">
    <li><a href="https://every.to" rel="noopener">Every</a> — essays on AI and how people actually work with it.</li>
    <li><a href="https://sfruby.substack.com" rel="noopener">SF Ruby</a> and the <a href="https://rubycentral.org" rel="noopener">Ruby Central</a> README — what's happening in the Ruby community.</li>
    <li><a href="https://softwareengineeringdaily.com" rel="noopener">Software Engineering Daily</a> — infrastructure and engineering deep dives.</li>
    <li>We Love Open Source — a weekly roundup of open-source projects and people.</li>
    <li><a href="https://www.indiehackers.com" rel="noopener">Indie Hackers</a> — people shipping small products on their own.</li>
    <li><a href="https://technews.acm.org" rel="noopener">ACM TechNews</a> — a quick scan of computing research news.</li>
  </ul>
</div>
