---
layout: post
date: 2026-10-20 13:45:00 -0700
title: "Paper TL;DR: HNSW — How Vector Search Skips Most of the Haystack"
permalink: /post/paper-tldr-hnsw/
description: "A plain-language TL;DR of Hierarchical Navigable Small World graphs (Malkov & Yashunin): a layered neighbor graph that finds approximate nearest vectors in roughly logarithmic time, and the index behind a lot of today's vector search."
series: paper-tldr
series_order: 12
tags: ["Research", "Agent memory"]
image: /assets/og/paper-tldr-hnsw.png
---

**Paper:** Yu. A. Malkov & D. A. Yashunin, [*Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs*](https://arxiv.org/abs/1603.09320) (arXiv, first posted March 2016; later published in IEEE Transactions on Pattern Analysis and Machine Intelligence, [DOI 10.1109/TPAMI.2018.2889473](https://doi.org/10.1109/TPAMI.2018.2889473))

**One-line TL;DR:** Stack a few neighbor graphs on top of each other — sparse ones with long jumps at the top, a dense one with every item at the bottom — and you can find the closest vectors to a query by hopping down the stack instead of checking everything.

## The question

Every memory or [RAG](/post/agent-memory-glossary/#rag) system eventually asks the same thing: *which stored [embeddings](/post/agent-memory-glossary/#embedding) are closest to this query vector?* Checking every vector works, but the cost grows linearly with the collection. Exact shortcuts like k-d trees stop helping once vectors have hundreds of dimensions. So practical systems use *approximate* nearest neighbor (ANN) search: accept that you'll occasionally miss a true neighbor, and measure how often you don't with [recall](/post/agent-memory-glossary/#recall-at-k).

One family of ANN methods builds a *proximity graph* — each item linked to its near neighbors — and searches by greedily walking toward the query. The authors' own earlier method, Navigable Small World (NSW), did this but had two problems: search cost grew faster than logarithmically as the data grew, and on low-dimensional or tightly clustered data the greedy walk could get stuck in a "false" local minimum. HNSW is their fix.

## How it works

The paper describes the idea as a [skip list](https://en.wikipedia.org/wiki/Skip_list) where the linked lists are replaced by proximity graphs.

- **Layers.** Every item lives in the bottom layer. When it's inserted, it also draws a random top layer from an exponentially decaying distribution, so only a few items reach the upper layers. Upper layers are sparse and their links span long distances; the bottom layer is dense with short links.
- **Search.** Start at a fixed entry point on the top layer. On each layer, greedily move to whichever neighbor is closer to the query until none is, then drop down a layer and continue from there. On the bottom layer, keep a wider list of candidates (size `ef`) and return the best k. A bigger `ef` means higher recall and more work.
- **Insertion.** A new item is placed by running the same descent, then — on each layer from its own top layer down — linking to up to `M` neighbors found by a wider search (`efConstruction`). If a neighbor ends up with too many links, its list is pruned back to a cap.
- **A smarter way to pick neighbors.** Rather than always linking to the closest candidates, the heuristic keeps a candidate only if it's closer to the new item than to any neighbor already chosen. That spreads links out in different directions, which keeps separate clusters connected — exactly where plain NSW got stuck.

The knobs the paper discusses are few: `M` (links per item; it suggests roughly 5–48, higher for high-recall or high-dimensional data), `efConstruction` (build quality) and `ef` (search effort). The graph links cost roughly 60–450 bytes per item on top of the vectors themselves.

## What they found

- **Roughly logarithmic search.** The authors argue search cost scales as O(log N) under idealized assumptions, and see logarithmic scaling empirically on low-dimensional data. Construction is roughly O(N log N) there.
- **Fastest in their vector benchmarks.** Single-threaded on the ann-benchmarks suite, HNSW clearly beat NSW, FLANN, Annoy, VP-tree and FALCONN (an LSH library) on SIFT, GloVe, DEEP and CoPhIR, and stayed ahead on random 4-dimensional data.
- **Not just for vectors.** Because it only needs a distance function, it also led on non-vector data — sparse text, topic histograms, image signatures, even DNA strings compared by edit distance. The biggest gain over NSW was roughly three orders of magnitude on one low-dimensional, clustered dataset.
- **Speed versus memory against compression.** On 200 million SIFT vectors, HNSW used more RAM than Faiss's product-quantization index (about 64 GB versus 23.5–30 GB) but was more accurate, faster to search and much faster to build.

## Why it matters for builders

1. **It's probably already in your stack.** The paper notes that Faiss added its own HNSW implementation, and RAG's Wikipedia index used a FAISS HNSW index (see the [RAG TL;DR](/post/paper-tldr-retrieval-augmented-generation/)). [VaultMem](/post/vaultmem-part-2-multimodal-temporal-backends/) has an optional `HNSWVectorIndex` that wraps the [hnswlib](https://github.com/nmslib/hnswlib) library.
2. **Small collections don't need it.** The graph has real overhead, so brute force is often fine early on — VaultMem Part 2 falls back to exact cosine search below 1,000 memories and shows where the crossover happens.
3. **Recall is a dial, not a constant.** `ef` trades speed for recall at query time, without rebuilding. When a memory system "forgets" something it stored, the index settings are one more place to look — alongside the embeddings and the [re-ranking](/post/agent-memory-glossary/#re-ranking) step.
4. **The index decides which candidates you even see.** Better embeddings ([Sentence-BERT](/post/paper-tldr-sentence-bert/)) and better prompt placement ([Lost in the Middle](/post/paper-tldr-lost-in-the-middle/)) only help with the neighbors the index returns.

## Honest caveats

- **The O(log N) story has gaps.** The guarantee leans on idealized graphs the heuristic doesn't actually build, and the authors say high-dimensional behavior isn't proven. On the 200M-vector test, query time drifted somewhat from pure logarithmic growth.
- **Memory hungry.** All those links live alongside the vectors, so it needs more RAM than compressed indexes like product quantization.
- **No deletes or updates — at the time.** The paper lists element updates and removal as future work. That matters for memory systems that edit or [unlearn](/post/agent-memory-glossary/#memory-unlearning) facts; check what your library supports today.
- **Hard to distribute.** Every search starts at the top layer, which can become a hotspot, and the authors found that simply splitting data across machines scales poorly in total throughput.
- **Benchmarks are a snapshot.** Results depend on the hardware and the library versions of the time, and some baselines were older builds.

Earlier in the series: [RAG](/post/paper-tldr-retrieval-augmented-generation/) (the retrieve-then-generate loop this index sits inside) and [Sentence-BERT](/post/paper-tldr-sentence-bert/) (the embeddings it searches over).

Terms like [*HNSW*](/post/agent-memory-glossary/#hnsw), [*embedding*](/post/agent-memory-glossary/#embedding), [*semantic search*](/post/agent-memory-glossary/#semantic-search), [*top-k retrieval*](/post/agent-memory-glossary/#top-k-retrieval) and [*Recall@k*](/post/agent-memory-glossary/#recall-at-k) are defined in the [agent memory glossary](/post/agent-memory-glossary/).
