---
layout: post
date: 2026-10-18 11:00:00 -0700
title: "Paper TL;DR: Complementary Learning Systems — Why Agents Need Two Kinds of Memory"
permalink: /post/paper-tldr-complementary-learning-systems/
description: "A TL;DR of McClelland, McNaughton & O'Reilly (1995): the brain's fast and slow learners, catastrophic interference, and what it suggests for AI agent memory."
series: paper-tldr
series_order: 3
tags: ["Research", "Agent memory"]
read_time: 5
image: /assets/og/paper-tldr-complementary-learning-systems.png
---

**Paper:** McClelland, McNaughton & O'Reilly, [*Why there are complementary learning systems in the hippocampus and neocortex*](https://doi.org/10.1037/0033-295X.102.3.419), Psychological Review (1995)

**One-line TL;DR:** the brain learns with two systems on purpose — a fast one that grabs specific experiences and a slow one that gradually extracts general knowledge — because a single system can't do both without wrecking what it already knows.

It's a 1995 psychology paper, and it's one of the most useful things I've read about designing memory for AI agents.

## The problem: learning fast breaks things

The paper starts from a puzzle that anyone who has fine-tuned a neural network will recognize. If you teach a network something new by adjusting the same shared weights that hold everything else, the new learning can overwrite the old. This is **catastrophic interference**: learn B, forget A.

The fix that works in artificial networks is to learn slowly and *interleave* — mix new examples with old ones so the weights find a setting that serves both. But that's slow. You can't wait for hundreds of repetitions to remember where you parked this morning.

## The brain's answer: two learners

The authors argue the brain splits the job:

- **Hippocampus — the fast learner.** Stores specific episodes quickly, often after a single exposure, using sparse, separate codes so similar memories don't collide. Great for "what happened at Tuesday's meeting."
- **Neocortex — the slow learner.** Learns gradually, with overlapping representations that capture structure shared across many experiences. Great for "how meetings at my company usually go."

The bridge between them is **replay**. Over time — notably during sleep — the hippocampus reactivates recent episodes, and the neocortex learns from those replays *interleaved* with older knowledge. That's consolidation: specific memories slowly become general knowledge without overwriting what came before.

{% include diagrams/cls-two-learners.html %}

The paper backs this with evidence from people with hippocampal damage, who struggle to form new episodic memories yet keep older knowledge, and with network simulations showing why interleaved learning avoids interference.

## Why it matters for AI agents

Read with agents in mind, the paper is basically a design doc:

1. **Keep an episodic store separate from the model.** Fine-tuning a model on every conversation is the "learn fast in shared weights" mistake. A separate, fast-writing memory — a log or vector store of specific events — is the hippocampus.
2. **Consolidate on a schedule, not on every write.** Periodically summarize or distill many episodes into durable facts and preferences, mixing in what's already known instead of overwriting it.
3. **Let memories change over time.** Things that keep getting recalled should get stronger; one-off details can fade. A store that treats every memory as equally permanent forever is missing half the design.

This is the model I borrowed for [Attractor](/post/attractor-memory-engine/): memories carry the context they were formed in, track how often they're used, and are meant to strengthen or decay rather than sit frozen.

## Caveats worth knowing

- The theory has been extended since 1995 — the neocortex can learn new things quickly when they fit an existing schema — so "neocortex is always slow" is a simplification.
- Brains aren't databases; the analogy is a guide for design choices, not a blueprint.

Next in the series: the benchmark that told me how good my own memory system actually was. Earlier parts: [six papers on AI memory](/post/paper-tldr-six-papers-on-memory/) and [Hopfield Networks Is All You Need](/post/paper-tldr-hopfield-networks-is-all-you-need/).

Quick definitions of [*consolidation*](/post/agent-memory-glossary/#consolidation) and [*decay*](/post/agent-memory-glossary/#decay) are in the [agent memory glossary](/post/agent-memory-glossary/).
