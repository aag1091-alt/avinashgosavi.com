---
layout: post
date: 2026-10-19 14:40:00 -0700
title: "Paper TL;DR: Generative Agents — Memory Streams, Reflection and Plans"
permalink: /post/paper-tldr-generative-agents/
description: "A plain-language TL;DR of Generative Agents (Park et al., 2023): how 25 LLM characters in a sandbox town remember, reflect and plan, and which parts of that memory design builders still copy."
series: paper-tldr
series_order: 9
tags: ["Research", "Agent memory"]
image: /assets/og/paper-tldr-generative-agents.png
---

**Paper:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang & Michael S. Bernstein (Stanford, Google Research, Google DeepMind), [*Generative Agents: Interactive Simulacra of Human Behavior*](https://arxiv.org/abs/2304.03442) (UIST 2023)

**One-line TL;DR:** Give an LLM a running log of everything it observes, a way to score which memories matter right now, and a habit of periodically writing down higher-level conclusions — and simulated characters start to behave believably over days, not just single replies.

## The setup

The authors built **Smallville**, a small sandbox town populated by 25 characters. Each one is driven by an LLM (gpt-3.5-turbo in the paper) and starts from a single paragraph describing who they are: job, relationships, habits. From there the characters wake up, go to work, chat, form opinions of each other and make plans — all generated, step by step, by the model.

The interesting part isn't the town. It's the memory design that keeps each character consistent over time, which the paper splits into three pieces: a **memory stream**, **reflection** and **planning**.

## 1. The memory stream

Every character keeps a **memory stream**: a plain list of memories, each written in natural language with a creation time and a "last accessed" time. The basic memories are **observations** — things the character perceived, such as (to give an illustrative example) "a neighbor is watering the garden."

The stream grows far too large to fit into a prompt, so each time a character needs to act, it retrieves only the most useful memories. Each memory gets three scores:

- **Recency:** recently used memories score higher, fading exponentially with each in-game hour (the paper uses a decay factor of 0.995).
- **Importance:** when a memory is created, the model rates it from 1 (mundane, like cleaning a room) to 10 (poignant, like asking someone out).
- **Relevance:** cosine similarity between the memory's embedding and the current situation's embedding.

Each score is scaled to 0–1 and the three are added up (the paper weights them equally). The top-scoring memories that fit into the context window go into the prompt.

## 2. Reflection

Raw observations are too low-level to generalize from. Fifty separate observations of a neighbor reading in the library don't, by themselves, tell a character "she cares a lot about her research."

So characters **reflect**. When the summed importance of recent memories passes a threshold (150 in the paper — roughly two or three times per simulated day), the model looks at the 100 most recent memories, asks itself three high-level questions about them, retrieves memories relevant to each question, and writes down insights that cite the memories they came from.

Those insights go back into the same memory stream, where they can be retrieved — and reflected on again. The result is a **reflection tree**: raw observations at the leaves, more abstract conclusions higher up.

## 3. Planning

To keep behavior coherent across a day, each character drafts a rough plan (about five to eight chunks), then breaks each chunk into hour-long actions, then into 5–15 minute steps. Plans are stored in the memory stream too. At every step, the model decides whether something it just noticed is worth reacting to; if so, it rewrites the plan from that point.

## What they tested

**Interviews.** The authors "interviewed" characters with questions about themselves, their memories, plans, reactions and reflections. 100 human evaluators ranked answers from the full architecture, versions with pieces removed, and human crowdworkers role-playing the same characters. The full architecture ranked most believable; removing reflection, then planning, then memory each made answers noticeably worse. The crowdworker answers landed below every version that still had memory.

**Emergent behavior over two game days.** One character was seeded with the idea of throwing a Valentine's Day party. Without further scripting, word spread from 1 character to 13 of 25, and 5 of the 12 who were invited showed up. A mayoral candidacy spread from 1 character to 8 the same way.

## Why it matters for builders

1. **Rank memories on more than similarity.** Recency + importance + relevance is a simple, readable scoring rule, and variations of it show up across agent memory systems. [VaultMem](/post/vaultmem-encrypted-memory-for-ai-agents/), for example, re-ranks on cosine similarity plus a significance score that decays over time.
2. **Store conclusions, not just events.** Reflections are cheap summaries the agent can retrieve later, and keeping links back to the source memories makes them auditable.
3. **Memory and planning are the same store.** Writing plans into the memory stream means "what am I doing next?" is answered by the same retrieval as "what happened?"

## Honest caveats

- **Retrieval still misses.** The authors show characters failing to recall something they had heard, or recalling a detail of an event but not the event itself.
- **Embellishment.** Characters sometimes added details nobody had said, or blended in the model's world knowledge — one described a neighbor as the author of a famous 18th-century economics book.
- **Too polite.** The authors attribute overly formal, overly agreeable dialogue to instruction tuning; one character rarely said no to suggestions, and her own interests drifted as a result.
- **Expensive.** Running 25 characters for two game days took multiple days and, in the authors' words, "thousands of dollars in token credits."
- **Believability isn't accuracy.** The evaluation measured whether behavior *seemed* human, not whether memories were retrieved correctly. Benchmarks like [LoCoMo](/post/paper-tldr-locomo-long-term-memory-benchmark/) test that more directly.

Earlier in the series: [MemGPT](/post/paper-tldr-memgpt/) (an OS-style alternative where the model pages its own memory), [Complementary Learning Systems](/post/paper-tldr-complementary-learning-systems/) (the brain's version of turning episodes into general knowledge — close in spirit to reflection), and [Sentence-BERT](/post/paper-tldr-sentence-bert/) (the kind of embeddings behind the relevance score).

Terms like *consolidation* and *decay* are defined in the [agent memory glossary](/post/agent-memory-glossary/#how-memories-change-over-time).
