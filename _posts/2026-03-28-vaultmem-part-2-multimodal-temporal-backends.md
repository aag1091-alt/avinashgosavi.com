---
layout: post
title: "VaultMem Part 2 — Multi-Modal Memory, Temporal Search, and Pluggable Backends"
permalink: /post/vaultmem-part-2-multimodal-temporal-backends/
date: 2026-03-28
read_time: 10
---

[Part 1](/post/vaultmem-encrypted-memory-for-ai-agents/) covered why I built VaultMem, how the encryption works, and the core memory model. This post covers what came next in v0.2.0 and v0.2.1 — the parts that took the library from a solid foundation to something that can handle real-world agent use cases: multi-modal memory ingestion, time-aware retrieval, production-grade storage backends, O(log N) ANN search, and a pluggable query normalizer.

> **Install:** `pip install vaultmem` · **Code:** [github.com/aag1091-alt/vaultmem-sdk](https://github.com/aag1091-alt/vaultmem-sdk) · **Live demo:** [vaultmem-demo.streamlit.app](https://vaultmem-demo.streamlit.app)

---

## Multi-modal memory

Text-only memory is a significant limitation for a personal AI agent. The moments that matter most — a photo from a trip, a voice note recorded mid-commute, a scanned medical document — aren't text.

VaultMem v0.2.0 added `add_media()`, which ingests an image, audio file, PDF, or video and stores it as a fully encrypted memory atom. The raw bytes go into `vault/media/{uuid}.enc` (AES-256-GCM, same key architecture as text atoms). The extracted content becomes the searchable atom.

```python
with VaultSession.open("./vault", passphrase, embedder=embedder) as s:
    # Image — extracts EXIF date, GPS coordinates, optional OCR
    atom = s.add_media("holiday_photo.jpg", passphrase)
    print(atom.content)      # "Photo taken 2023-07-14 in Split, Croatia"
    print(atom.captured_at)  # EXIF timestamp as Unix int
    print(atom.location)     # {"lat": 43.5, "lon": 16.4, "place": "Split"}

    # Audio — Whisper transcription
    atom = s.add_media("voice_note.mp3", passphrase)

    # PDF — PyMuPDF text extraction
    atom = s.add_media("contract.pdf", passphrase)

    # Retrieve raw bytes later (decrypted on demand, not in search results)
    raw = s.get_media(atom.id, passphrase)
```

The media bytes are never loaded into RAM during search — only the extracted text atom participates in embedding and retrieval. This keeps the privacy model intact: even if you extract metadata, the raw file stays encrypted behind the passphrase.

Each extractor is a pluggable Protocol, so adding new file types is straightforward:

```python
from vaultmem import MediaExtractor, MediaExtractionResult, MediaIngester

class HeicExtractor:
    MIME_TYPES = {"image/heic", "image/heif"}

    def extract(self, path, mime_type):
        return MediaExtractionResult(
            content_type=mime_type,
            transcript="...",
            captured_at=...,
        )

ingester = MediaIngester(extra_extractors=[HeicExtractor()])
```

Install the extras to activate the built-in extractors:

```bash
pip install "vaultmem[media]"   # Pillow, piexif, openai-whisper, PyMuPDF, ffmpeg-python
```

---

## Temporal search

The second gap I wanted to close: time. A personal agent should be able to answer "what was I doing in 2019?" or "show me everything from last summer" — not just "what's most semantically similar to this query?"

This required two new timestamp fields on `MemoryObject`:

- `created_at` — when the atom was written to the vault (set automatically, immutable)
- `captured_at` — when the real-world event happened (set manually or from EXIF/metadata)

These are deliberately separate. A photo taken in 2019 but added to the vault today has `captured_at` in 2019 and `created_at` today. The distinction matters for any use case involving retroactive journaling or importing old media.

### Browse by time window

```python
from datetime import datetime, timezone

def ts(year, month=1, day=1):
    return int(datetime(year, month, day, tzinfo=timezone.utc).timestamp())

with VaultSession.open("./vault", passphrase, embedder=embedder) as s:
    memories_2019 = s.search_by_time(ts(2019), ts(2020))
    q3_2021 = s.search_by_time(ts(2021, 7), ts(2021, 10))

    # What was written to the vault in the last 24 hours
    import time
    recent = s.diff(int(time.time()) - 86400, int(time.time()))
```

### Natural-language time queries

I wanted to avoid the experience of asking "what happened summer 2019?" and getting results from all time. The `TimeQueryParser` extracts a timestamp range from the query string, strips the time phrase, and passes the remainder to the embedding — all in pure Python with no dependencies:

```python
from vaultmem import TimeQueryParser

from_ts, to_ts, remainder = TimeQueryParser.parse("what happened summer 2019")
# from_ts  → 2019-06-01 UTC
# to_ts    → 2019-09-01 UTC
# remainder → "what happened"
```

Supported phrases: season + year, month + year, bare year, "last year", "this month", "last N days", "yesterday".

Pass `parse_time=True` to `search()` and it handles everything automatically:

```python
# Strips "in 2019" → timestamp range; embeds "what did I do"
results = s.search("what did I do in 2019", top_k=10, parse_time=True)
```

---

## Pluggable storage backends

The default storage model — two files on the local filesystem — is the right starting point. But a production agent deployment might need S3 for durability, Postgres for searchability, or both. I didn't want to bake those in as optional flags on the session object; I wanted them to be proper extension points.

v0.2.0 introduced three ABCs:

| ABC | Default | Production |
|-----|---------|------------|
| `BlobStore` | `FileBlobStore` | `S3BlobStore` |
| `SearchIndex` | `SQLiteSearchIndex` | `PostgresSearchIndex` |
| `VectorIndex` | — (exact O(N) cosine) | `HNSWVectorIndex` |

All three are injected at session creation:

```python
from vaultmem import (
    VaultSession, LocalEmbedder,
    S3BlobStore, PostgresSearchIndex, HNSWVectorIndex,
)

with VaultSession.open(
    "./vault", passphrase,
    embedder=LocalEmbedder(),
    blob_store=S3BlobStore(bucket="my-vault-atoms"),
    search_index=PostgresSearchIndex("postgresql://user:pass@host/db"),
    vector_index=HNSWVectorIndex(),
) as s:
    results = s.search("coffee habits", top_k=10)
```

The important design decision: the vault format stays the same regardless of which backends you use. `FileBlobStore` and `S3BlobStore` store the same encrypted bytes. `SQLiteSearchIndex` and `PostgresSearchIndex` store the same metadata. Migrating between backends is O(N) byte-copies, no decryption required:

```python
from vaultmem import migrate_vault

migrate_vault(
    src_blob_store=FileBlobStore("./old"),
    dst_blob_store=S3BlobStore(bucket="new-vault"),
    passphrase=passphrase,
)
```

### HNSW and the O(N) problem

At small scale, exact cosine search over all atoms in RAM is fine. At 10,000 atoms it becomes the bottleneck — the benchmark showed ~148ms per query, all of it in the embedding comparison loop.

`HNSWVectorIndex` wraps [hnswlib](https://github.com/nmslib/hnswlib) and plugs into the same `VectorIndex` ABC. The HNSW graph is built incrementally as atoms are added and serialized encrypted to `vault/vector_index.hnsw.enc` on flush. At session open it's loaded once into RAM. Search then runs in O(log N):

| Atoms | Exact cosine | HNSW |
|-------|:------------:|:----:|
| 1,000 | ~15ms | ~0.3ms |
| 10,000 | ~148ms | ~0.8ms |
| 100,000 | ~1,500ms | ~1.2ms |

Below 1,000 atoms, the implementation falls back to exact cosine automatically — the HNSW graph has overhead that isn't worth paying at small N.

```bash
pip install "vaultmem[ann]"   # hnswlib
```

---

## Query normalizer

A subtler problem surfaced while building the [interactive demo](https://vaultmem-demo.streamlit.app): the question framing users naturally type — "What do I know about Sarah Chen?" — dilutes the embedding. A bag-of-words or hash-projection embedder assigns equal weight to "what", "do", "i", "know", "about" and "Sarah", "Chen". The meaningful terms are swamped by question scaffolding.

Sentence-transformers handle this natively through attention — they learn that "Sarah Chen" carries the semantic weight in the sentence. But not every deployment uses a 22M-parameter ML model.

v0.2.1 introduced a `QueryNormalizer` Protocol:

```python
from vaultmem import QueryNormalizer  # Protocol — implement normalize(text) -> str
```

The built-in `RegexQueryNormalizer` strips common English question preamble:

```python
from vaultmem import RegexQueryNormalizer

# "What do I know about Sarah Chen?" → "Sarah Chen"
# "How does Flash Attention work?"   → "Flash Attention work"
# "Am I vegetarian?"                 → "vegetarian"
```

More interesting is the custom path — since it's a Protocol, any object with a `normalize(self, text: str) -> str` method works. The interactive demo uses a Groq-backed normalizer with a server-side API key, so users get LLM-quality query extraction without needing their own key:

```python
class GroqQueryNormalizer:
    def __init__(self, api_key: str) -> None:
        from groq import Groq
        self._client = Groq(api_key=api_key)

    def normalize(self, text: str) -> str:
        resp = self._client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=20,
            messages=[
                {"role": "system",
                 "content": "Extract key search terms. Return only keywords."},
                {"role": "user", "content": text},
            ],
        )
        return resp.choices[0].message.content.strip() or text
```

The normalizer is injected once at session creation and runs on all searches where `normalize_query=True`:

```python
with VaultSession.open("./vault", passphrase,
                        query_normalizer=GroqQueryNormalizer(api_key),
                        embedder=embedder) as s:
    results = s.search("What do I know about Sarah?", normalize_query=True)
```

---

## Data classes

One design detail worth calling out: memory doesn't all decay at the same rate, and not all memory deserves the same cryptographic protection.

VaultMem has three data classes, set at vault creation:

| Class | Use case | Argon2id memory | Decay λ | Half-life |
|-------|----------|:---------------:|:-------:|:---------:|
| `GENERAL` | Standard | 64 MiB | 0.005 | ~5 months |
| `MEDICAL` | Health data | 128 MiB + mlock | 0.002 | ~12 months |
| `ARCHIVAL` | Long-term records | 64 MiB | 0.0007 | ~3 years |

`MEDICAL` doubles the Argon2id memory cost, making brute-force twice as expensive. `ARCHIVAL` slows the significance decay so memories stay surfaced for years rather than months — appropriate for journals, legal records, or anything you want to last.

```python
VaultSession.create("./health_vault", passphrase, owner="alice", data_class="MEDICAL")
```

---

## The LoCoMo benchmark

I wanted a more rigorous evaluation than the 18-atom synthetic benchmark I described in Part 1. The [LoCoMo dataset](https://arxiv.org/abs/2402.17753) is a collection of long-form conversational memory — 1,982 QA pairs across five categories (single-hop factual, multi-hop reasoning, temporal, adversarial, open-domain). It's the closest thing to a realistic test of a personal memory system.

VaultMem's Recall@10 and MRR scores on a random sample:

| Category | Recall@10 | MRR |
|----------|:---------:|:---:|
| Single-hop factual | 0.91 | 0.87 |
| Temporal | 0.84 | 0.79 |
| Multi-hop | 0.73 | 0.68 |
| Adversarial | 0.78 | 0.71 |

Multi-hop is the hardest — it requires reasoning across atoms that weren't individually asked about, which is a retrieval problem before it's even an LLM problem.

---

## The interactive demo

The fastest way to see all of this in action is the [live demo](https://vaultmem-demo.streamlit.app). It runs a pre-seeded vault with 36 memories across all four types — enough variety to demonstrate the retrieval model without you having to type anything first.

Every retrieved result shows its relevancy score, memory type, and retrieval tier. The right panel shows the raw encrypted bytes of `current.vmem` and `current.atoms` — what the platform operator actually sees. Each browser tab gets an isolated vault; your data can't be seen by or contaminated by other visitors.

Some things worth trying:

| Question | What it exercises |
|----------|------------------|
| What do I know about Sarah Chen? | Groq query normalizer → EPISODIC retrieval |
| How does Flash Attention work? | SEMANTIC retrieval |
| What's my coffee order? | PERSONA retrieval |
| How do I debug problems? | PROCEDURAL retrieval |
| Tell me about my cat | Natural language → EPISODIC |

---

## What's next

The library is at v0.2.1. The things I'm thinking about for v0.3.0:

- **Composite and Affinity generation** — right now the tiers exist in the retrieval model but atoms are only created at ATOM granularity. Automated COMPOSITE and AFFINITY synthesis from accumulated atoms is the next big addition.
- **Cross-agent memory sharing** — Layer 2 of the Memory-as-Asset framework. A shared encrypted memory space where multiple agents can read without the platform being able to.
- **LoCoMo full benchmark** — running the complete 1,982-pair dataset rather than a sample.

The paper targeting ACM CCS 2026 is in progress.

---

> `pip install vaultmem` · [GitHub](https://github.com/aag1091-alt/vaultmem-sdk) · [Preprint](https://doi.org/10.5281/zenodo.19154079) · [Live demo](https://vaultmem-demo.streamlit.app)
