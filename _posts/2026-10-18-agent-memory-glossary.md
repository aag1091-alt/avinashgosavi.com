---
layout: post
date: 2026-10-18 19:45:00 -0700
title: "An Agent Memory Glossary: Terms in Plain Language"
permalink: /post/agent-memory-glossary/
description: "Plain-language definitions of the terms that come up when building memory for AI agents — episodic vs. semantic memory, embeddings, HNSW, re-ranking, consolidation, Recall@k, zero-knowledge storage and more."
tags: ["Agent memory", "Explainers"]
image: /assets/og/agent-memory-glossary.png
---

The vocabulary around AI agent memory borrows from neuroscience, databases, search and cryptography all at once, which makes it easy to talk past each other. This is a working glossary — short, plain definitions, with links to where each idea shows up in my own projects. I'll keep adding to it.

## Kinds of memory

**Context window (working memory).** What the model can see right now: the prompt, the recent conversation and anything retrieved for this turn. Fast and precise, but limited in size and gone when the session ends. Everything else on this list exists because of that limit.
{: #context-window .glossary-term}

**Episodic memory.** Specific events: *what happened, when, with whom.* "On Tuesday you said the demo slipped to Friday." In [VaultMem](/post/vaultmem-encrypted-memory-for-ai-agents/) these are one of the memory types the agent can store and retrieve.
{: #episodic-memory .glossary-term}

**Semantic memory.** General facts and knowledge, detached from when they were learned. "Flash Attention reduces memory traffic by tiling." Often distilled from many episodes.
{: #semantic-memory .glossary-term}

**Procedural memory.** How to do things: workflows, preferences about process, steps that worked before. "When debugging, check the logs before the config."
{: #procedural-memory .glossary-term}

**Persona (profile) memory.** Stable facts about the person the agent works with — name, role, standing preferences. Small, high-value and read on almost every turn.
{: #persona-memory .glossary-term}

**Virtual context (paging).** Treating the context window like a computer's RAM: the agent moves information in and out of the prompt — saving facts to external storage, searching old messages, summarizing what gets pushed out — usually through function calls. Popularized by [MemGPT](/post/paper-tldr-memgpt/).
{: #virtual-context .glossary-term}

## Storing and finding memories

**Embedding.** A list of numbers that represents the meaning of a piece of text, so that similar meanings land close together. Most memory systems store an embedding next to each memory. See the [Sentence-BERT TL;DR](/post/paper-tldr-sentence-bert/) for where modern sentence embeddings come from.
{: #embedding .glossary-term}

**Semantic search.** Finding memories by meaning instead of exact words: embed the query, then return the stored memories whose embeddings are closest.
{: #semantic-search .glossary-term}

**Top-k retrieval.** Returning the *k* closest matches (say, the top 10) and putting them into the context window. Simple and effective; also where most retrieval mistakes start.
{: #top-k-retrieval .glossary-term}

**Retrieval-augmented generation (RAG).** Search first, then write: fetch the passages most relevant to the input and have the model generate its answer from them, instead of relying only on what's stored in its weights. The term comes from a 2020 paper that also showed you can update what the system knows by swapping the search index — see the [RAG TL;DR](/post/paper-tldr-retrieval-augmented-generation/).
{: #rag .glossary-term}

**Vector index (HNSW).** A data structure that makes "find the closest vectors" fast at scale. HNSW (Hierarchical Navigable Small World) builds layered graphs of neighbors so a search can hop quickly toward the right region instead of comparing against every vector.
{: #hnsw .glossary-term}

**Re-ranking.** A second, slower and more careful pass over the top results — often a cross-encoder that reads the query and each candidate together — to put the truly relevant ones first.
{: #re-ranking .glossary-term}

**Position bias (lost in the middle).** Models tend to use information at the start and end of a long prompt better than information buried in the middle, so *where* retrieved memories land in the prompt affects whether they get used. Putting the strongest matches first, and keeping top-k small, helps. See the [Lost in the Middle TL;DR](/post/paper-tldr-lost-in-the-middle/).
{: #position-bias .glossary-term}

**Hybrid search.** Combining meaning-based search with keyword search (or filters like dates and tags), because embeddings are bad at exact names, numbers and IDs.
{: #hybrid-search .glossary-term}

**Context frame.** The situation a memory was formed in — topic, people involved, task, session — stored alongside it so retrieval can filter by context, not just content. This is the core idea in [Attractor](/post/attractor-memory-engine/).
{: #context-frame .glossary-term}

**Sufficient evidence.** The idea that a memory system's job isn't just to return *relevant* memories but a set that is *enough* to answer. Ranking memories one at a time can miss this: several records may say the same thing (so the set gets bloated), or two weak-looking records may only make sense together (so both get dropped). One recent paper defines a sufficient set as a small subset that leads the agent to the same decision it would make with its full memory ([Beyond Marginal Influence](https://neurips.cc/virtual/2026/169578)). See [this week's roundup](/post/this-week-in-agent-memory-2026-10-19/#theme-2-relevant-isnt-the-same-as-enough).
{: #sufficient-evidence .glossary-term}

## How memories change over time

**Consolidation.** Turning many specific episodes into durable, general knowledge — summarizing a month of conversations into "prefers short answers," for example. The brain's version is covered in the [Complementary Learning Systems TL;DR](/post/paper-tldr-complementary-learning-systems/).
{: #consolidation .glossary-term}

**Reflection.** Having the agent periodically read its recent memories and write down higher-level conclusions ("she cares a lot about her research"), stored back as memories that point to the evidence they came from. Introduced for LLM agents in [Generative Agents](/post/paper-tldr-generative-agents/), which also ranks memories by recency, importance and relevance together.
{: #reflection .glossary-term}

**Decay (forgetting).** Letting memories that are never used fade in importance, so old noise doesn't crowd out what matters. Forgetting is a feature.
{: #decay .glossary-term}

**Event time vs. write time.** Two different timestamps for one memory: when the thing happened, and when it was saved. A photo from 2019 imported today should come back for "what did I do in 2019?", not for "what did I add today?". [VaultMem Part 2](/post/vaultmem-part-2-multimodal-temporal-backends/#temporal-search) keeps them as separate fields (`captured_at` and `created_at`) for exactly this reason.
{: #event-time .glossary-term}

**Versioned facts (temporal state).** Keeping every value a fact has had — "lives in Boston", then "lives in Seattle" — as a list of versions linked to where each came from, instead of overwriting the old one. The newest version answers "where does she live?", while the older ones still answer "where did she live before?". The [TEM paper](https://www.emergentmind.com/papers/2610.21900) adds one more step: older versions are marked as historical before the model sees them, and the authors report that this label alone gave large gains on questions about repeatedly updated facts. See [this week's roundup](/post/this-week-in-agent-memory-2026-10-19/#theme-3-facts-that-change-over-time).
{: #versioned-facts .glossary-term}

**Associative (content-addressable) memory.** Retrieving a whole memory from a partial or noisy piece of it, rather than by key or address. Hopfield networks are the classic example — see [Hopfield (1982)](/post/paper-tldr-hopfield-1982/) and [the modern version](/post/paper-tldr-hopfield-networks-is-all-you-need/).
{: #associative-memory .glossary-term}

## Privacy

**Zero-knowledge storage.** The service storing your data cannot read it, because it's encrypted with a key only you hold. The operator sees ciphertext. This is VaultMem's core design.
{: #zero-knowledge-storage .glossary-term}

**Client-side encryption.** Encrypting data before it leaves your device (or your session), so the server only ever handles encrypted bytes. The usual way to get zero-knowledge storage.
{: #client-side-encryption .glossary-term}

**PII sanitization.** Detecting and masking personal details — names, emails, phone numbers — before text is sent to a model provider, then restoring them in the response. It closes a gap encryption at rest can't: the model still has to read the text. See [VaultMem Part 3](/post/vaultmem-part-3-pii-sanitizer/).
{: #pii-sanitization .glossary-term}

**Memory unlearning (forget requests).** Deleting a specific fact when the user asks — and only that fact. Done well, the fact can no longer be recalled or pieced together from other memories, while everything unrelated survives. The [Bemula benchmark](https://www.emergentmind.com/papers/2610.18052) tests exactly this and reports two common failures: the fact stays extractable with simple prompts, or the system deletes far more than it was asked to. See [this week's roundup](/post/this-week-in-agent-memory-2026-10-19/#theme-1-can-an-agent-forget-when-you-ask-it-to).
{: #memory-unlearning .glossary-term}

## Measuring it

**Recall@k.** Of the questions asked, how often the right memory appears somewhere in the top *k* results. Measures "did we find it at all."
{: #recall-at-k .glossary-term}

**MRR (mean reciprocal rank).** Rewards putting the right memory near the top: 1 if it's first, ½ if second, ⅓ if third, averaged over all questions.
{: #mrr .glossary-term}

**LoCoMo.** A benchmark of very long, multi-session conversations with questions across single-hop, multi-hop, temporal, open-domain and adversarial categories. See the [LoCoMo TL;DR](/post/paper-tldr-locomo-long-term-memory-benchmark/).
{: #locomo .glossary-term}

---

Missing a term, or think one of these is off? I'd like to hear it — I'll keep this page up to date.
