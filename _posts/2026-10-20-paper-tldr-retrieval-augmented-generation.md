---
layout: post
date: 2026-10-20 08:45:00 -0700
title: "Paper TL;DR: RAG — The Paper That Named Retrieval-Augmented Generation"
permalink: /post/paper-tldr-retrieval-augmented-generation/
description: "A plain-language TL;DR of Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al., 2020): a language model paired with a searchable Wikipedia index, trained together, and why you can update what it knows by swapping the index."
series: paper-tldr
series_order: 11
tags: ["Research", "Agent memory"]
image: /assets/og/paper-tldr-retrieval-augmented-generation.png
---

**Paper:** Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel & Douwe Kiela (Facebook AI Research, University College London, New York University), [*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401v4) (arXiv, 2020; revised 2021)

**One-line TL;DR:** Instead of hoping a language model memorized the right fact, give it a search step: look up a few relevant Wikipedia passages, generate the answer from them, and train the search and the writer together.

## The question

By 2020, large language models clearly stored a lot of facts in their weights. But the paper points out the downsides: that knowledge is hard to expand or revise, the model can't show where an answer came from, and it can hallucinate. Earlier hybrid models that paired a language model with a retriever (REALM and ORQA) had only been tried on *extractive* question answering — pulling answer spans out of passages rather than writing new text. This paper asks whether one general recipe can combine the two: a model that retrieves documents *and* generates free-form answers, fine-tuned end to end for many different tasks.

## How it works

The paper splits knowledge into two kinds of memory:

- **Parametric memory** — what's baked into the model's weights. Here that's BART-large, a pre-trained sequence-to-sequence generator.
- **Non-parametric memory** — an external index you can search. Here that's a December 2018 Wikipedia dump cut into 100-word chunks (about 21 million of them), each turned into an [embedding](/post/agent-memory-glossary/#embedding) by a BERT document encoder from DPR (Dense Passage Retrieval). The vectors live in a FAISS index using an [HNSW](/post/agent-memory-glossary/#hnsw) approximation, so lookups stay fast.

At question time, a second BERT encoder turns the input into a query vector, the index returns the [top-k](/post/agent-memory-glossary/#top-k-retrieval) passages, and BART generates an answer conditioned on the input plus each passage. Nobody labels which passage is "right": the retriever learns only from whether the final answer comes out well.

Two variants decide how the passages get combined:

- **RAG-Sequence** uses the same passage for the whole answer, then weighs the answers it would give for each passage.
- **RAG-Token** can lean on a different passage for each word, so one answer can stitch together facts from several documents.

One practical shortcut: only the query encoder and the generator are trained. The document encoder — and so the whole 21-million-vector index — stays frozen, because re-embedding Wikipedia during training is expensive. The authors report they didn't need that step for strong results.

## What they found

- **Strong open-domain question answering.** On Natural Questions, WebQuestions and CuratedTrec, RAG beat the previous best systems in the paper's comparison, while writing answers instead of copying spans. On TriviaQA the picture is mixed: it led on one test split but not the standard one.
- **It can answer even when the passage doesn't spell it out.** On Natural Questions, RAG still got about 11.8% of answers right in cases where the exact answer wasn't in any retrieved passage — something a pure extractor can't do.
- **More factual, more specific text.** In a human evaluation of generated Jeopardy-style questions, raters judged RAG more factual than plain BART far more often than the other way round (42.7% vs. 7.1% of cases), and more specific too.
- **Small next to giant models.** RAG has 626M trainable parameters; the largest closed-book model it's compared to, T5-11B, has 11 billion — yet RAG scored higher on open-domain QA.
- **Swap the index, update the knowledge.** The authors built a second index from a 2016 Wikipedia dump and asked "Who is {position}?" about 82 world leaders who changed between 2016 and 2018. With the matching index RAG got roughly 70% right; with the mismatched one, 4–12%. Changing what the model knows meant replacing the index, not retraining.

## Why it matters for builders

1. **It's the template most "chat with your docs" systems still follow.** Embed chunks, search by meaning, paste the top results into the prompt, generate. Agent memory systems do the same thing with memories instead of Wikipedia pages — the [glossary's "Storing and finding memories" section](/post/agent-memory-glossary/#storing-and-finding-memories) walks through each piece.
2. **Updating knowledge is a data problem, not a training problem.** The hot-swap experiment is the cleanest argument for keeping facts outside the weights: if something changes, you change the index. The same idea is why memory systems store facts with timestamps and [versions](/post/agent-memory-glossary/#versioned-facts) rather than hoping the model "knows" the latest.
3. **Provenance comes for free.** Because the answer is conditioned on specific passages, you can show where it came from — useful for debugging and for trust.
4. **Retrieval quality still caps everything.** The retriever here is learned only through the final answer, and the paper reports it can fail badly (see caveats). Later work in this series picks up from there: [Lost in the Middle](/post/paper-tldr-lost-in-the-middle/) shows that even good passages help less when they land mid-prompt, and [MemGPT](/post/paper-tldr-memgpt/) treats the context window as something to manage rather than fill.

## Honest caveats

- **This is 2020-era plumbing.** "RAG" today usually means an instruction-tuned LLM plus an off-the-shelf retriever, with no joint training. The paper's specific recipe — BART, DPR, a frozen Wikipedia index — is mostly of historical interest now; the *idea* is what stuck.
- **Retrieval can collapse.** In early story-generation experiments, the retriever learned to return the same documents no matter the input, after which the generator ignored them and RAG behaved just like plain BART. The authors suggest tasks with long outputs or less need for facts may give the retriever too weak a signal.
- **Not state of the art everywhere.** On FEVER fact verification, RAG came within about 4.3% of the best pipeline (3-way) without being given gold evidence — close, but not ahead.
- **The index is only as good as its source.** The authors note that Wikipedia will likely never be fully factual or free of bias, and that the same misuse concerns as other text generators apply.
- **Big infrastructure for its time.** The paper notes the Wikipedia index initially needed about 100 GB of CPU memory, cut to 36 GB with FAISS compression.

Earlier in the series: [Sentence-BERT](/post/paper-tldr-sentence-bert/) (the kind of embeddings that make the search step work), [Lost in the Middle](/post/paper-tldr-lost-in-the-middle/) (where retrieved passages land in the prompt) and [MemGPT](/post/paper-tldr-memgpt/) (an agent that pages its own memory in and out).

Terms like [*retrieval-augmented generation*](/post/agent-memory-glossary/#rag), [*embedding*](/post/agent-memory-glossary/#embedding), [*semantic search*](/post/agent-memory-glossary/#semantic-search), [*top-k retrieval*](/post/agent-memory-glossary/#top-k-retrieval) and [*HNSW*](/post/agent-memory-glossary/#hnsw) are defined in the [agent memory glossary](/post/agent-memory-glossary/).
