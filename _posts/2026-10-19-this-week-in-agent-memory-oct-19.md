---
layout: post
date: 2026-10-19 04:50:00 -0700
title: "This Week in Agent Memory: Forgetting on Request, Sufficient Evidence, Facts That Change"
permalink: /post/this-week-in-agent-memory-2026-10-19/
description: "Seven agent-memory papers posted to arXiv between Oct 13 and Oct 16, 2026: two benchmarks on deleting memories when asked, new ideas for picking enough evidence, tracking facts that change over time, and two surveys."
tags: ["Agent memory", "Roundup", "Research"]
image: /assets/og/this-week-in-agent-memory-oct-19.png
---

A short, neutral roundup of agent-memory papers that appeared on arXiv this past week (submitted Oct 13–16, 2026). Each summary comes from the paper's own abstract; numbers are what the authors report, not independent results. New to the vocabulary? The [agent memory glossary](/post/agent-memory-glossary/) covers the terms.

## Theme 1: Can an agent forget when you ask it to?

Two benchmarks landed on the same question in the same week, and both answer "not really, yet."

- **[Can Agents Forget When Asked? A Benchmark for Memory Unlearning in LLM Agents](https://arxiv.org/abs/2610.18052)** (Xie et al., Oct 13). Introduces *Bemula*: 50 multi-session dialogues with 135 forget requests and 1,742 test questions, plus paired control dialogues so a system only gets credit for forgetting something it actually stored. Across six memory systems and three backbone models, the authors report success on at most 1.5% of forget requests — systems either leave the fact extractable or delete far more than asked.
- **[MemCut: Every Secret Leaves a Trail in the Long-Term Memory of LLM Agents](https://arxiv.org/abs/2610.21405)** (Zhang et al., Oct 15). 456 hand-written secrets are planted in long conversations, with annotated "evidence trails" showing whether a secret can still be pieced together after deletion, including from indirect hints. The finding: deleting the original disclosure makes the secret much harder to reach through the system's own retrieval, but much less so from leftover traces elsewhere in memory.

Why builders might care: "delete this" is a privacy feature users expect, and both papers suggest that removing the one record that mentions a fact isn't the same as forgetting it. (The [privacy section of the glossary](/post/agent-memory-glossary/#privacy) has more on why stored memory is sensitive.)

## Theme 2: Relevant isn't the same as enough

- **[From Relevant Memories to Sufficient Evidence: Rethinking Memory Utilization in LLM Agents](https://arxiv.org/abs/2610.22668)** (Li et al., Oct 15). Argues that retrieving relevant memories doesn't guarantee the agent has what it needs: key facts may be scattered, over-summarized, or missing the links between them. Their method, *QEMem*, builds a per-question evidence set by retrieving at several granularities, organizing results into structured "cards" with source references, and recovering missing pieces. On [LoCoMo](/post/paper-tldr-locomo-long-term-memory-benchmark/), the authors report 91.43% LLM-judge accuracy, 7.6 points above their strongest baseline.
- **[Beyond Marginal Influence: Interaction-Aware Memory Selection for LLM Agents](https://arxiv.org/abs/2610.23266)** (Subrahmanyam et al., Oct 16). Points out that ranking memories one at a time fails when evidence is redundant or only useful in combination. It defines a per-decision notion of a *sufficient* set of memories, releases *JointCoreBench* with exact answers for what the smallest sufficient set is, and offers a baseline that tests groups of records before single ones. The authors are careful to call it a benchmark baseline, not a ready-to-ship compression method.

## Theme 3: Facts that change over time

- **[TEM: Temporal State Tracking Memory for Large Language Model Agents](https://arxiv.org/abs/2610.21900)** (Song et al., Oct 15). A training-free approach that keeps each fact as a list of versions linked to their sources, orders retrieved versions, and labels older ones as historical before the answering model sees them. Event memory and raw dialogue turns fill in details the structured facts miss. The authors report better hit rates than session-aware RAG on two evaluations while using noticeably fewer evidence tokens.

This connects to the older idea of [consolidation and memory updating](/post/agent-memory-glossary/#how-memories-change-over-time): rather than overwriting "I live in Austin" with "I moved to Denver", keep both and say which is current.

## Two surveys worth bookmarking

- **[Seeing, Maintaining, and Learning: The Evolution of Multimodal Agent Memory](https://arxiv.org/abs/2610.19366)** (Guo et al., Oct 14). A two-axis framework for multimodal agent memory: how information gets captured and encoded, and how memory management matures — from fixed memory, to memory updated by a fixed policy, to memory that learns its own update policy.
- **[From Long Context to Selective Memory: A Survey of Memory-Centric Compression for Large Language Models](https://arxiv.org/abs/2610.21165)** (Gou, Oct 15). Treats long-context handling as memory management: writing, offloading, eviction and consolidation are modeled as state changes with costs. The central question it poses is which information should enter expensive inference, when, and in what form — a framing close to [MemGPT's "context window as RAM"](/post/paper-tldr-memgpt/) idea.

## Caveats

These are fresh preprints, not peer-reviewed results, and this list is not exhaustive — it's a sample of what turned up in arXiv searches for agent memory this week. Benchmarks with new names tend to show low scores for existing systems; that's partly the point of a benchmark, so the more durable takeaway is the question each one asks.

For deeper single-paper write-ups, see the [Paper TL;DR series](/series/).
