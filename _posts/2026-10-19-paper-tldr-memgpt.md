---
layout: post
date: 2026-10-19 03:40:00 -0700
title: "Paper TL;DR: MemGPT — Treating the Context Window Like RAM"
permalink: /post/paper-tldr-memgpt/
description: "A plain-language TL;DR of MemGPT (Packer et al., 2023): how an LLM can page information in and out of a small context window with function calls, the way an operating system manages memory."
series: paper-tldr
series_order: 8
tags: ["Research", "Agent memory"]
image: /assets/og/paper-tldr-memgpt.png
---

**Paper:** Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica & Joseph E. Gonzalez (UC Berkeley), [*MemGPT: Towards LLMs as Operating Systems*](https://arxiv.org/abs/2310.08560) (arXiv, 2023)

**One-line TL;DR:** Instead of waiting for bigger context windows, MemGPT treats the prompt like a computer's RAM and lets the model itself move information between that small fast space and larger external storage, using function calls.

## The problem

An LLM can only "see" what fits in its context window. Long chats and big document collections don't fit, so something has to decide what stays in view. Operating systems solved a version of this decades ago: programs act as if they have lots of memory, while the OS quietly pages data between fast RAM and slower disk. The paper calls its version **virtual context management**.

## How it works

MemGPT splits memory into two places.

**Main context** — what's actually in the prompt — has three parts:

- **System instructions:** read-only rules, including how to use the memory functions.
- **Working context:** a small, fixed-size scratchpad of key facts (for example, things learned about the user). The model can only change it through function calls.
- **A FIFO message queue:** the recent conversation. Its first entry is a running summary of older messages that were pushed out.

**External context** lives outside the prompt:

- **Recall storage:** the full message history, searchable on demand.
- **Archival storage:** a store for arbitrary text the model chooses to save or look up later.

{% include diagrams/memgpt-virtual-context.html %}

The clever part is who moves things around: **the model does**. Its output is parsed as function calls (search recall, write to archival, edit working context), and the results are fed back in. A few mechanics make this work:

- **Memory pressure warnings.** When the prompt gets close to full (the paper's example uses 70%), the system adds a warning so the model can save what matters before it's lost.
- **Eviction with summaries.** When the prompt is full, a chunk of the oldest messages is evicted and folded into the running summary. Evicted messages aren't deleted — they stay in recall storage.
- **Heartbeats.** A function call can ask to keep going (`request_heartbeat`), so the model can chain several lookups before replying.
- **Events.** User messages, system alerts and scheduled timers all wake the agent up, so it doesn't only act when a person types.

## What they tested

Two settings, each with a "can it really remember?" task:

- **Multi-session chat.** In a deep memory retrieval task, the agent is asked about something from an earlier session. MemGPT answered far more of these correctly than the same models with a fixed context. In a "conversation opener" task, its openers drew on what it knew about the person, and the authors found that saving facts to working context was key.
- **Document analysis.** For question answering over many documents, MemGPT could page through more search results than fit in one prompt. In a nested key-value lookup task, where one value points to another key, fixed-context models broke down as nesting got deeper, while MemGPT with GPT-4 kept answering by looking things up repeatedly.

## Why it matters for builders

1. **Memory can be a set of tools, not just a bigger prompt.** Giving the model explicit read/write/search functions makes memory something you can inspect and log.
2. **Separate "always in view" from "look it up."** A small working context of key facts plus searchable history is a pattern that shows up again and again in agent memory designs.
3. **Plan for overflow.** Warning before the window fills, and summarizing instead of silently truncating, is a simple idea worth copying.

## Honest caveats

- **It leans on the model's function-calling skill.** The authors report that results dropped noticeably with GPT-3.5, which was weaker at calling functions.
- **Retrieval is still the bottleneck.** With embedding search, the right document often wasn't near the top, and the agent tended to stop paging before exhausting the results.
- **More model isn't always better.** On the nested lookup task, the GPT-4 Turbo version did worse than GPT-4, and some versions gave up after too few lookups.
- **Self-managed memory is a judgment call by the model.** What gets saved, summarized or forgotten depends on the model's choices, which is harder to predict than a fixed rule.

Earlier in the series: [LoCoMo](/post/paper-tldr-locomo-long-term-memory-benchmark/) (a benchmark for exactly this kind of long-term memory), [Sentence-BERT](/post/paper-tldr-sentence-bert/) (the embeddings behind most semantic search), and [Complementary Learning Systems](/post/paper-tldr-complementary-learning-systems/) (a brain-inspired split between fast and slow memory).

Terms like *context window*, *episodic memory* and *top-k retrieval* are defined in the [agent memory glossary](/post/agent-memory-glossary/#kinds-of-memory).
