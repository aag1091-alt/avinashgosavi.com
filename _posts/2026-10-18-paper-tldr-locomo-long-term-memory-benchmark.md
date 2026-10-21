---
layout: post
date: 2026-10-18 12:00:00 -0700
title: "Paper TL;DR: LoCoMo — How Good Is Your Agent's Memory, Really?"
permalink: /post/paper-tldr-locomo-long-term-memory-benchmark/
description: "A plain-language TL;DR of the LoCoMo benchmark (Maharana et al., 2024) for very long-term conversational memory — what it tests, what it found, and how I used it to evaluate VaultMem."
series: paper-tldr
series_order: 4
tags: ["Research", "Agent memory"]
read_time: 4
image: /assets/og/paper-tldr-locomo-long-term-memory-benchmark.png
---

**Paper:** Maharana et al., [*Evaluating Very Long-Term Conversational Memory of LLM Agents*](https://arxiv.org/abs/2402.17753) (ACL 2024)

**One-line TL;DR:** LoCoMo is a benchmark of very long, multi-session conversations with questions that probe whether a system really remembers — and even strong long-context models and retrieval setups fall well short of people on it.

If you're building memory for an agent, this is the paper that keeps you honest.

## What's in the benchmark

Most chat benchmarks are a few turns long. LoCoMo conversations run for **dozens of sessions and hundreds of turns**, spread over simulated weeks and months. The authors generated them with LLM agents that each had a persona and a timeline of life events, then had people review and fix them so the conversations stay consistent. Some turns include shared images, too.

On top of the conversations they built three tasks: answering questions, summarizing events, and generating responses. The question-answering part is the one I care about, and its categories are what make it useful:

- **Single-hop** — one fact from one place in the history.
- **Multi-hop** — needs to connect facts from different sessions.
- **Temporal** — when did something happen, or what happened before or after.
- **Open-domain** — combine the conversation with general knowledge.
- **Adversarial** — questions about things that *never* happened, where the right answer is "that wasn't mentioned."

## What they found

Even with long context windows or [retrieval-augmented generation](/post/paper-tldr-retrieval-augmented-generation/), models trail human performance by a wide margin. Retrieval helps, but the hard categories stay hard — especially reasoning about time and resisting the urge to make up answers to adversarial questions. Bigger context alone doesn't fix it.

## How I used it

When I built [VaultMem](/series/#vaultmem), my first benchmark was 18 synthetic memories I wrote myself. It looked great — which was the problem. LoCoMo gave me a test I didn't design. [On a sample of its questions](/post/vaultmem-part-2-multimodal-temporal-backends/), retrieval was strong for single-hop facts and weakest for multi-hop, which needs pieces that weren't individually asked about. That's a retrieval problem before it's a model problem, and it changed what I worked on next.

## The takeaway for builders

1. **Test against data you didn't write.** A memory system always looks good on its author's examples.
2. **Score by category, not just overall.** "85% accurate" hides that temporal and multi-hop questions might be failing.
3. **Measure the "I don't know."** A memory that confidently invents a past is worse than one that admits a gap.

Earlier in the series: [six papers on AI memory](/post/paper-tldr-six-papers-on-memory/), [Hopfield Networks Is All You Need](/post/paper-tldr-hopfield-networks-is-all-you-need/), and [Complementary Learning Systems](/post/paper-tldr-complementary-learning-systems/). Next in the series: [Memory as Asset](/post/paper-tldr-memory-as-asset/), on who should own an agent's memory.

[*Recall@k*](/post/agent-memory-glossary/#recall-at-k) and [*MRR*](/post/agent-memory-glossary/#mrr), the usual ways to score retrieval, are explained in the [agent memory glossary](/post/agent-memory-glossary/#measuring-it).
