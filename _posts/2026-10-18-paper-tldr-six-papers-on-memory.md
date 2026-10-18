---
layout: post
date: 2026-10-18 09:00:00 -0700
title: "Paper TL;DR: Six Papers That Shaped How I Think About AI Memory"
permalink: /post/paper-tldr-six-papers-on-memory/
description: "Short, plain-language summaries of six papers behind my AI memory side projects — from Hopfield's 1982 associative memory to user-owned memory for agents."
series: paper-tldr
series_order: 1
read_time: 6
tags: ["Research", "Agent memory"]
image: /assets/og/paper-tldr-six-papers-on-memory.png
---

Most of my side projects over the past year have circled one question: **how should an AI system remember things?** Not just "where do we put the vectors," but how memory gets formed, found again, strengthened or forgotten — and who gets to read it.

I didn't start with papers. I started building, got stuck, and went looking for how other people had thought about the problem. These six are the ones that actually changed what I built. Here's each one in a few sentences, in plain language, plus what I took from it. If you only read one, read the first.

## 1. Hopfield (1982) — memory as a place you roll into

[*Neural networks and physical systems with emergent collective computational abilities*](https://www.pnas.org/doi/10.1073/pnas.79.8.2554) · PNAS

**TL;DR:** Wire up simple on/off neurons with symmetric connections and the network gets an "energy" that can only go down as it updates. Stored memories sit at the bottoms of valleys in that landscape. Give it a partial or noisy pattern and it slides downhill into the full memory. You don't look memories up by key — you fall into them.

**What I took from it:** this was the "oh" moment behind [Attractor](/post/attractor-memory-engine/). Recall from partial cues feels much closer to how I actually remember things than a database lookup does.

## 2. Ramsauer et al. (2020) — attention is a Hopfield update

[*Hopfield Networks is All You Need*](https://arxiv.org/abs/2008.02217) · arXiv

**TL;DR:** A "modern" Hopfield network with continuous states can store exponentially many patterns and usually retrieves one in a single step. And that single update step is mathematically the same operation as transformer attention.

**What I took from it:** the 1982 idea isn't a museum piece — it's sitting inside every LLM. That made me take attractor-style retrieval seriously as a design for agent memory, not just a curiosity.

## 3. McClelland, McNaughton & O'Reilly (1995) — two learners, not one

[*Why there are complementary learning systems in the hippocampus and neocortex*](https://doi.org/10.1037/0033-295X.102.3.419) · Psychological Review

**TL;DR:** The brain uses a fast learner that grabs specific episodes (hippocampus) and a slow learner that gradually pulls out general structure (neocortex). Replaying episodes into the slow system lets it learn without overwriting what it already knows.

**What I took from it:** a vocabulary for something agents get wrong — treating every memory the same forever. It's why Attractor tracks access and why I think memories should strengthen with use and fade without it.

## 4. Reimers & Gurevych (2019) — embeddings you can actually search

[*Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*](https://arxiv.org/abs/1908.10084) · arXiv

**TL;DR:** Plain BERT has to compare sentences two at a time, which is painfully slow for search. Training it in a "siamese" setup gives every sentence its own embedding you can compare with cosine similarity, so finding the closest match among thousands takes seconds instead of hours.

**What I took from it:** the unglamorous workhorse. The sentence-transformers models behind semantic search in Attractor, VaultMem and daylog all come from this line of work.

## 5. Maharana et al. (2024) — testing memory honestly

[*Evaluating Very Long-Term Conversational Memory of LLM Agents* (LoCoMo)](https://arxiv.org/abs/2402.17753) · arXiv

**TL;DR:** A benchmark of very long, multi-session conversations with questions that need single facts, multi-step reasoning, time awareness, or the sense to say "that never happened." Even strong long-context models and RAG setups struggle with it.

**What I took from it:** my own little synthetic test was flattering me. Running [VaultMem against LoCoMo](/post/vaultmem-part-2-multimodal-temporal-backends/) gave me numbers I could actually trust — and showed me where retrieval was weak.

## 6. Pan, Huang & Yang (2026) — whose memory is it?

[*Memory as Asset: From Agent-centric to Human-centric Memory Management*](https://arxiv.org/abs/2603.14212) · arXiv

**TL;DR:** Argues that agent memory today is built for the agent rather than the person, and proposes treating the memory an AI keeps about you as an asset you own, share under your own permissions, and grow over time.

**What I took from it:** this one reshaped [VaultMem](/series/#vaultmem) entirely. It gave words to the feeling that an agent's memory of your life shouldn't be readable by whoever runs the agent. VaultMem ended up implementing its first layer.

## What ties them together

Reading these in a row, I keep landing on the same picture: good memory is **found by meaning and context**, **changes over time**, and **belongs to the person it's about**. Most systems today nail the first, ignore the second, and get the third backwards.

All six live on my [papershelf](/research/#papershelf) with the rest of what I'm reading. If there's a paper on memory or agents you think I should read next, I'd genuinely love to hear about it.
