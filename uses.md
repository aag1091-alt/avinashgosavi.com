---
layout: default
title: Uses
permalink: /uses/
description: The hardware, languages, AI tools and hosting stack Avinash Gosavi uses for work and side projects — including a home Ollama inference server.
---

<div class="uses-page prose-page">
  <h1>Uses</h1>
  <p class="page-lede">The tools behind my day job and side projects. People ask about the home inference server most, so it's first.</p>

  <h2>Home inference server</h2>
  <ul>
    <li><strong>Minisforum AI X1 Pro</strong> — AMD Ryzen AI 9 HX 370 with Radeon 890M graphics, 32&nbsp;GB RAM (planning a 96&nbsp;GB upgrade to fit 70B models).</li>
    <li><strong>Ollama</strong> with Vulkan GPU acceleration — <code>qwen2.5:14b</code> runs fully on the integrated GPU.</li>
    <li><strong>Tailscale</strong> so my laptop, phone and side-project servers can reach it from anywhere, without opening ports.</li>
    <li>It powers local transcription, embeddings and chat for <a href="{{ '/projects/' | relative_url }}">my projects</a>.</li>
  </ul>

  <h2>Languages &amp; frameworks</h2>
  <ul>
    <li><strong>Ruby &amp; Rails</strong> — my first love since 2011, and still most of my day job.</li>
    <li><strong>Python</strong> for AI work, <strong>TypeScript/React</strong> for front ends, <strong>Scala</strong> and <strong>Java</strong> on the JVM, plenty of <strong>SQL</strong>.</li>
    <li><strong>Kafka, gRPC, Elasticsearch, PostgreSQL, Kubernetes</strong> on the platform side.</li>
  </ul>

  <h2>AI tooling</h2>
  <ul>
    <li><strong>Claude</strong> and <strong>Codex</strong> for coding — with my workflow baked into <a href="{{ '/post/codex-skills-baking-your-workflow-into-the-tool/' | relative_url }}">skills</a>.</li>
    <li><strong>Gemini Live API &amp; Google ADK</strong> for voice agents (<a href="{{ '/post/building-rena-ai-health-companion-gemini-live/' | relative_url }}">Rena</a>), <strong>LangGraph</strong> for multi-agent pipelines, <strong>MCP</strong> for tool interfaces.</li>
    <li><strong>faster-whisper</strong> for transcription and <strong>sentence-transformers</strong> for embeddings, both self-hosted.</li>
  </ul>

  <h2>Hosting side projects for ~$0</h2>
  <p>The full reasoning is in <a href="{{ '/post/hobby-project-stack/' | relative_url }}">What should you actually use to build your next hobby project?</a></p>
  <ul>
    <li><strong>Cloudflare Pages</strong> for front ends, <strong>Fly.io</strong> for backends that need persistent state and private networking.</li>
    <li><strong>Neon</strong> serverless Postgres and <strong>Upstash</strong> Redis — both scale to zero.</li>
    <li><strong>GitHub Pages + Jekyll</strong> for this site and my static projects (<a href="{{ '/post/building-your-website-with-jekyll-and-github-pages/' | relative_url }}">how I set it up</a>).</li>
  </ul>
</div>
