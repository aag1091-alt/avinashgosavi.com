---
layout: default
title: Paper TL;DR
permalink: /paper-tldr/
description: "Plain-language summaries of research papers on AI memory, retrieval and vector search — what each paper says, why it matters for builders, and its caveats."
---

{% assign tldrs = site.posts | where: "series", "paper-tldr" | sort: "series_order" %}
<div class="tldr-page">
  <h1>Paper TL;DR</h1>
  <p class="page-lede">Research papers on AI memory, retrieval and search, each boiled down to what it says, why it matters, and where it falls short. {{ tldrs.size }} so far · <a href="{{ '/feed/paper-tldr.xml' | relative_url }}">RSS for this section</a></p>

  <ol class="tldr-list">
    {% for p in tldrs %}
    <li class="tldr-item">
      <a class="tldr-title" href="{{ p.url | relative_url }}">{{ p.title | remove_first: "Paper TL;DR: " }}</a>
      {% if p.description %}<p class="tldr-desc">{{ p.description }}</p>{% endif %}
      <div class="post-list-meta">
        <time datetime="{{ p.date | date_to_xmlschema }}">{{ p.date | date: "%b %d, %Y" }}</time>
        <span>{% include read-time.html content=p.content %}</span>
      </div>
    </li>
    {% endfor %}
  </ol>

  <p class="page-lede">The papers themselves, with one-line notes, are on the <a href="{{ '/research/#papershelf' | relative_url }}">papershelf</a>.</p>
</div>
