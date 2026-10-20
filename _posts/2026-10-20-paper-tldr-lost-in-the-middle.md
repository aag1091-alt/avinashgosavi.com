---
layout: post
date: 2026-10-20 03:45:00 -0700
title: "Paper TL;DR: Lost in the Middle — Where You Put Context Matters"
permalink: /post/paper-tldr-lost-in-the-middle/
description: "A plain-language TL;DR of Lost in the Middle (Liu et al., 2023): language models use information at the start and end of a long prompt far better than information buried in the middle, and what that means for RAG and agent memory."
series: paper-tldr
series_order: 10
tags: ["Research", "Agent memory"]
image: /assets/og/paper-tldr-lost-in-the-middle.png
---

**Paper:** Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni & Percy Liang (Stanford, UC Berkeley, Samaya AI), [*Lost in the Middle: How Language Models Use Long Contexts*](https://arxiv.org/abs/2307.03172v3) (arXiv, 2023)

**One-line TL;DR:** Give a model a long prompt with one useful passage in it, and how well it answers depends on *where* that passage sits: best at the very start or very end, noticeably worse in the middle — even for models built for long contexts.

## The question

Retrieval-augmented generation and agent memory both work the same way at the last step: fetch some passages, paste them into the prompt, and hope the model reads them. Bigger context windows make it tempting to paste in more. This paper asks a simple question first: does the model actually use everything in a long prompt equally well?

## How they tested it

Two tasks, each designed so the authors could move the one relevant piece of information around while keeping everything else the same.

- **Multi-document question answering.** Questions from NaturalQuestions-Open, each paired with one Wikipedia passage that contains the answer plus distractor passages that look relevant but don't. Prompts held 10, 20 or 30 passages, and the answer passage was moved from first to last.
- **Key-value retrieval.** A synthetic stress test: a JSON object of random UUID keys and values (75, 140 or 300 pairs), and the model has to return the value for one key. No language cues, just "find this and copy it."

They ran open models (MPT-30B-Instruct, LongChat-13B) and API models (GPT-3.5-Turbo, Claude-1.3, and their longer-context versions, plus GPT-4 on a subset).

## What they found

- **A U-shaped curve.** Accuracy was highest when the answer passage came at the very start or the very end, and dropped when it sat in the middle — by more than 20% in some settings. The authors describe this as a primacy bias plus a recency bias.
- **The middle can be worse than nothing.** In one 20-document setting, GPT-3.5-Turbo with the answer buried mid-prompt scored lower than the same model answering with no documents at all.
- **A longer window didn't fix it.** When a prompt fit in both a model and its extended-context version, the two scored almost the same. A bigger window lets you paste more; it doesn't make the model read it better.
- **More retrieved documents stop helping early.** In an open-domain QA case study, the retriever kept finding the answer more often as it returned more passages, but the model's accuracy flattened out well before that. Going from 20 to 50 passages bought only a point or two, at much higher cost and latency.
- **Asking the question twice helps for lookups.** Putting the query both before and after the data made key-value retrieval near-perfect, but it barely changed the multi-document QA results.

{% include diagrams/lost-in-the-middle-u-curve.html %}

## Why it matters for builders

1. **Order is part of retrieval.** Ranking isn't just about *which* passages make the cut but *where* they land. Putting the best matches first (and not burying them under weaker ones) is cheap and directly addresses this. A [re-ranking](/post/agent-memory-glossary/#re-ranking) pass earns its keep here.
2. **Fewer, better passages beat more passages.** The case study suggests a tighter [top-k](/post/agent-memory-glossary/#top-k-retrieval) can be nearly as accurate and a lot cheaper. It also connects to the idea of [sufficient evidence](/post/agent-memory-glossary/#sufficient-evidence): the goal is enough context, not all of it.
3. **Test position, not just recall.** A memory system can retrieve the right fact and still fail if the fact lands mid-prompt. Benchmarks like [LoCoMo](/post/paper-tldr-locomo-long-term-memory-benchmark/) measure the end answer; this paper's trick of moving the gold passage around is an easy extra check to run on your own pipeline.
4. **Keep the important stuff at the edges.** Designs like [MemGPT](/post/paper-tldr-memgpt/) keep a small, always-visible working context near the top of the prompt. This paper is one reason that kind of layout makes sense.

## Honest caveats

- **These are 2023 models.** The results cover GPT-3.5, Claude-1.3, MPT and LongChat, with only partial GPT-4 runs because of cost. Newer models may show a weaker (or different) position effect, so it's worth measuring on whatever you actually use.
- **The "why" is still open.** The authors test a few explanations — architecture, instruction tuning, model size — and call those analyses preliminary. Encoder-decoder models were fairly robust within their training length but showed the U-shape on longer inputs; base models without instruction tuning showed it too.
- **One answer per prompt.** Each test has a single relevant passage. Real questions often need several facts combined, which this setup doesn't measure.
- **Greedy decoding only,** and the key-value task is deliberately artificial, so it shows a capability gap rather than typical real-world behavior.

Earlier in the series: [MemGPT](/post/paper-tldr-memgpt/) (paging what goes into the context window), [Generative Agents](/post/paper-tldr-generative-agents/) (ranking memories by recency, importance and relevance) and [Sentence-BERT](/post/paper-tldr-sentence-bert/) (the embeddings behind most of the retrieval step).

Terms like [*context window*](/post/agent-memory-glossary/#context-window), [*position bias*](/post/agent-memory-glossary/#position-bias), [*re-ranking*](/post/agent-memory-glossary/#re-ranking) and [*top-k retrieval*](/post/agent-memory-glossary/#top-k-retrieval) are defined in the [agent memory glossary](/post/agent-memory-glossary/).
