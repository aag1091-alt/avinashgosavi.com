---
layout: post
title: "Attractor: Building a Memory Engine Inspired by How the Brain Works"
permalink: /post/attractor-memory-engine/
read_time: 7
---

I've been thinking about memory — not human memory, but how machines store and retrieve it. Most systems today are either key-value stores (fast, exact, dumb) or vector databases (semantic, but still just nearest-neighbour). Neither of them works the way a brain does.

So I started building something different. I called it **Attractor**.

## The Problem with How Machines Remember

When you search a database, you give it a key and it returns a value. When you search a vector database, you give it a query and it returns the closest vectors by distance. Both are useful. But neither captures something important about how biological memory works — **context**.

Think about how you remember things. You don't retrieve memories by key. You retrieve them by *partial cues* — a smell, a phrase, a situation. And the retrieval is shaped by context: what you were doing, who you were with, what problem you were trying to solve. Two memories with identical content mean different things depending on when and why they were formed.

Machines don't do this. And for AI agents that need to reason across long conversations or accumulated knowledge, this is a real limitation.

## Hopfield Networks — The Intriguing Part

In 1982, John Hopfield described a type of recurrent neural network that stores memories as **energy minima** [[1]](#references). The idea is elegant: each memory is a stable state — a basin of attraction — in an energy landscape. When you give the network a partial or noisy input, it doesn't search for the closest match. It *converges* — like a ball rolling downhill — to the nearest stable state.

This is called **content-addressable memory**. You don't need the exact key. You need something close enough to fall into the right basin.

<img src="{{ '/assets/images/attractor-energy-landscape.svg' | relative_url }}" alt="Energy landscape showing memories as basins of attraction" style="width:100%; max-width:820px; border-radius:10px; margin: 1.5rem 0;"/>

The name Attractor comes directly from this. In dynamical systems, an attractor is a state that a system converges to over time. Hopfield memories are attractors. Retrieval is the process of finding which attractor your input belongs to.

What makes this intriguing is that it mirrors something real about biological memory. Your brain isn't doing a database lookup when you remember something. It's doing something closer to energy minimisation — pattern completion from partial cues.

What's also interesting: in 2020, researchers showed that modern Hopfield networks with continuous states have exponentially higher storage capacity than the original binary version [[2]](#references) — and that the attention mechanism in transformers is mathematically equivalent to a single Hopfield update step. The architecture powering every LLM today is, at its core, a Hopfield retrieval operation.

## What I Built — Phase 1

Attractor is a standalone memory service. Right now it's Phase 1: a working foundation that stores memories with context and retrieves them by meaning.

<img src="{{ '/assets/images/attractor-architecture.svg' | relative_url }}" alt="Attractor Phase 1 architecture diagram" style="width:100%; max-width:820px; border-radius:10px; margin: 1.5rem 0;"/>

**The data model** is built around something I call a `ContextFrame` — the situational state at the time a memory was formed:

```python
class ContextFrame(BaseModel):
    topic: str | None      # what was being discussed
    entities: list[str]    # who or what was involved
    task: str | None       # what was being done
    session_id: str | None # which session it came from
```

This isn't metadata. It's a retrieval key. When you search, you can filter by context — "find memories from this topic" or "find memories from this session" — and combine that with semantic search over the content itself.

**The storage layer** uses PostgreSQL with pgvector [[3]](#references). Each memory stores its content, context frame, tags, timestamps, access count, and a 384-dimensional embedding from a sentence-transformers model [[4]](#references). The embedding enables semantic search — retrieving by meaning rather than exact words.

**The API** is simple:

```
POST /memories          — store a memory with context
GET  /memories/:id      — retrieve by ID
POST /memories/search   — search by content + context filters
DELETE /memories/:id    — remove a memory
```

**The CLI** wraps the service:

```bash
attractor start    # starts the service on port 7747
attractor connect  # verifies it's running
```

Port 7747 is "loci" on a phone keypad — a nod to the method of loci, the memory palace technique [[5]](#references), which was the project's original name before I found a better one.

## A Concrete Example

Here's what makes it different from a plain vector search. Say you store these two memories:

```
"auth tokens should never be stored in localStorage"
  context: { topic: "security review", task: "reviewing PR #42" }

"switched from JWT to session tokens — stateless was causing issues"
  context: { topic: "auth refactor", task: "architecture decision" }
```

Now you search: `"why did we change the auth approach"` with `context_filter: { topic: "auth refactor" }`.

<img src="{{ '/assets/images/attractor-context-filtering.svg' | relative_url }}" alt="Context filtering showing same query returning different results with and without context" style="width:100%; max-width:820px; border-radius:10px; margin: 1.5rem 0;"/>

The second memory surfaces — not because the words match, but because:
1. The embedding is semantically close to the query
2. The context filter narrows to the right topic

Without the context filter, both memories are relevant. With it, you get the one that was formed in the right situation. That's the difference.

## The Roadmap

Phase 1 is the foundation. The more interesting work is ahead:

**Phase 2 — Association graph**: Memories aren't just points in a vector space. They're nodes in a graph with typed edges — `supports`, `contradicts`, `caused_by`, `followed_by`. Retrieval triggers spreading activation: surface the memory you asked for, and the ones connected to it.

**Phase 3 — Decay and consolidation**: Not all memories are equally important. The `access_count` field is already tracking how often each memory is retrieved. Phase 3 uses this to implement decay — memories that are never accessed fade, memories that are frequently retrieved strengthen. This mirrors how biological memory consolidation works [[6]](#references).

**Phase 4 — Hopfield retrieval**: Replace vector similarity with a proper Hopfield weight matrix. Retrieval becomes pattern completion — give the network a partial cue and it converges to the full memory. This is the step that moves from "semantic search with context" to something genuinely brain-inspired.

## Why This Matters for AI Agents

Most AI agents today are stateless between sessions or rely on crude context windows. The ones that do have memory bolt it on as an afterthought — store the last N messages, embed them, retrieve by cosine similarity.

Attractor is an attempt to do it properly. Not because the engineering is especially hard, but because the *model* of memory matters. If you treat memory as a lookup table, you get lookup-table behaviour. If you treat it as an energy landscape with context and decay, you get something closer to how intelligence actually works.

Phase 1 is live. `pip install attractor-engine` — start storing memories with context, retrieve by meaning.

The interesting phases are coming.

---

## References

<a name="references"></a>

1. Hopfield, J.J. (1982). [Neural networks and physical systems with emergent collective computational abilities](https://www.pnas.org/doi/10.1073/pnas.79.8.2554). *Proceedings of the National Academy of Sciences*, 79(8), 2554–2558.

2. Ramsauer, H., Schäfl, B., Lehner, J., et al. (2020). [Hopfield Networks is All You Need](https://arxiv.org/abs/2008.02217). *arXiv:2008.02217*. *(Shows modern Hopfield networks have exponential capacity and that transformer attention is a Hopfield update.)*

3. pgvector. (2021). [Open-source vector similarity search for Postgres](https://github.com/pgvector/pgvector). GitHub.

4. Reimers, N. & Gurevych, I. (2019). [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084). *arXiv:1908.10084*.

5. Yates, F.A. (1966). *The Art of Memory*. University of Chicago Press. *(The definitive account of the method of loci — the memory palace technique.)*

6. McClelland, J.L., McNaughton, B.L., & O'Reilly, R.C. (1995). [Why there are complementary learning systems in the hippocampus and neocortex](https://doi.org/10.1037/0033-295X.102.3.419). *Psychological Review*, 102(3), 419–457. *(The foundational paper on memory consolidation and why some memories strengthen while others decay.)*

---

*Source: [github.com/aag1091-alt/attractor](https://github.com/aag1091-alt/attractor)*
