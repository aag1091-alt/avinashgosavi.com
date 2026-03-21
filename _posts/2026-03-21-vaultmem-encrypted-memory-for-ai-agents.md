---
layout: post
title: "VaultMem — Building Encrypted Memory for AI Agents"
permalink: /post/vaultmem-encrypted-memory-for-ai-agents/
read_time: 8
---

I spent the last few months building something I couldn't find anywhere else: a memory library for AI agents where the platform developer cryptographically **cannot read what the user stores**.

> **Install:** `pip install vaultmem` · **Code:** [github.com/aag1091-alt/vaultmem-sdk](https://github.com/aag1091-alt/vaultmem-sdk) · **Preprint:** [doi.org/10.5281/zenodo.19154079](https://doi.org/10.5281/zenodo.19154079)

---

## The problem

Every AI memory library I looked at — mem0, Zep, LangMem, Letta — stores user memories in plaintext on the platform's servers. The platform operator can read everything their users have ever told the agent. This isn't a privacy policy failure; it's a structural one. When the key lives with the operator, the guarantee lives with the operator.

This matters more than it sounds. The deepest use case for persistent AI memory isn't task management — it's candor. An agent that remembers across sessions only becomes genuinely useful when you can be completely honest with it. A person working through a difficult decision. Someone with early-stage dementia building a longitudinal record of their life. A user who just wants their preferences remembered without those preferences living in a corporate database.

For that to work, the privacy guarantee has to be mathematical, not a privacy policy.

---

## What VaultMem is

VaultMem is an embeddable Python library. A platform developer adds it as a dependency, and their users get encrypted, portable, private memory — without the developer being able to read it.

The analogy I keep coming back to: VaultMem is to AI memory what 1Password is to credentials. The library doesn't know what it's storing. The platform receives opaque ciphertext it can store, back up, and serve back — but cannot decrypt.

```python
from vaultmem import VaultSession, OllamaEmbedder

embedder = OllamaEmbedder("http://localhost:11434")

# Create an encrypted vault
with VaultSession.create("./vault", passphrase="s3cr3t", owner="alice",
                          embedder=embedder) as s:
    s.add("I met Bob at the AI conference yesterday")
    s.add("I prefer concise bullet-point answers")
    s.add("My go-to language for data work is Python")

# Search across sessions
with VaultSession.open("./vault", passphrase="s3cr3t",
                        embedder=embedder) as s:
    results = s.search("Bob conference")
    for r in results:
        print(f"[{r.tier}] {r.score:.3f}  {r.atom.content}")
```

Output:
```
[ATOM] 0.847  I met Bob at the AI conference yesterday
```

---

## How the encryption works

The key architecture has two layers:

```
User passphrase
  → Argon2id(passphrase, salt)      ← 64 MiB, 3 iterations
  → KEK (Key Encryption Key)         ← in RAM only; zeroed after open
  → AES-GCM-Dec(KEK, wrapped_MEK)
  → MEK (Master Encryption Key)      ← in RAM during session only
  → AES-256-GCM(memory atom)        ← to disk
```

The Master Encryption Key (MEK) is generated once at vault creation and stored only as a ciphertext wrapped with the user's passphrase-derived key. It never touches disk in plaintext. When the session closes, it's zeroed from RAM.

A platform developer who integrates VaultMem receives encrypted blobs from their users. They can store them, back them up, sync them — but they cannot read them. The math makes this true regardless of what their privacy policy says.

Two things I'm particularly happy with:

**Passphrase changes are O(1).** Because the MEK is wrapped separately from the data, changing a passphrase means re-wrapping one key — not re-encrypting every memory atom. A vault with 10,000 atoms changes passphrase in milliseconds.

**Per-atom tamper detection.** Each atom is encrypted with AES-256-GCM, which includes a 128-bit authentication tag. Each atom also has its UUID bound as Additional Authenticated Data, so you can't transplant a valid ciphertext from one slot to another. Any tampering is detected before the data surfaces.

---

## The memory model

Memories are stored as `MemoryObject` instances implementing the [Memory-as-Asset 5-tuple](https://arxiv.org/abs/2603.14212): content, context, owner, permissions, versioning state.

Four memory types: **EPISODIC** (things that happened), **SEMANTIC** (facts), **PERSONA** (preferences and habits), **PROCEDURAL** (how-to knowledge). Type is assigned by a deterministic classifier — no LLM call, no network request.

The more interesting part is the granularity hierarchy:

- **ATOM** — a single memory statement. Immutable once written.
- **COMPOSITE** — a type-homogeneous grouping of related atoms.
- **AFFINITY** — a derived atom representing a recurring pattern. "User drinks coffee every morning" synthesized from twenty individual coffee mentions.

AFFINITY atoms carry a significance score:

```
σ = (1 − e^(−κ × freq)) × e^(−λ × days_since_last)
```

Frequency drives the first factor (with diminishing returns), recency drives the second. The parameters vary by data class — medical memories decay slower than general ones.

---

## Three-tier retrieval — and why it matters

The retrieval model searches AFFINITY → COMPOSITE → ATOM and re-ranks results globally. On factual queries this behaves identically to flat cosine search — no regression. On pattern queries it's a different story.

I ran a benchmark to verify this. Three topic clusters (coffee habits, Python usage, exercise routine), each with one AFFINITY atom and five ATOM-granularity memories including a deliberately tricky **decoy**: an episodic memory containing the exact query keywords, designed to fool flat cosine.

For the query *"my morning coffee habits"*, flat cosine ranks the decoy atom first (it contains the words "coffee habits" and "morning") and the AFFINITY second. Three-tier flips this — the AFFINITY's significance score (~0.92 for a well-established habit) outweighs the cosine advantage of the decoy.

| Metric | Flat cosine | Three-tier | Δ |
|--------|:-----------:|:----------:|:---:|
| MRR (pattern queries) | 0.50 | **1.00** | **+0.50** |
| MRR (specific queries) | 1.00 | 1.00 | 0.00 |

Pattern queries: AFFINITY surfaced first every time. Specific queries: no regression. The significance weight isn't a heuristic — it's a correction for a systematic bias in pure cosine retrieval.

---

## The `.vmem` format

Vaults are stored as two files:

```
my_vault/
├── current.vmem      # encrypted index (48-byte self-describing header)
└── current.atoms     # append-only encrypted atom blocks
```

The 48-byte header is the only plaintext in the file. It carries the magic bytes (`VMEM`), format version, encryption algorithm, KDF, and file type — enough for any conforming implementation to decrypt the vault given the passphrase. No prior coordination with the writing implementation needed.

Atoms are append-only and immutable. Checkpoints update only the index file, atomically via `fsync` + `os.rename()`. Crash-safe.

The format is designed to be the interoperability layer for a future where encrypted memory vaults move between applications and agents — the same way a PDF can be opened by any conforming reader regardless of which app produced it.

---

## What's in the library

About 2,100 lines of Python, 39 unit tests, three core dependencies (`cryptography`, `argon2-cffi`, `numpy`). Sentence-transformers or a local Ollama instance for embeddings — or bring your own.

```python
# LocalEmbedder — no network, runs on CPU
from vaultmem import LocalEmbedder
embedder = LocalEmbedder()

# OllamaEmbedder — GPU-accelerated, localhost or Tailscale
from vaultmem import OllamaEmbedder
embedder = OllamaEmbedder("http://localhost:11434", model="all-minilm")

# Custom — implement .embed(text) -> list[float]
class MyEmbedder:
    def embed(self, text: str) -> list[float]: ...
    @property
    def dimension(self) -> int: return 384
```

---

## The research angle

VaultMem is also a research paper — the first implementation of Layer 1 of the [Memory-as-Asset framework](https://arxiv.org/abs/2603.14212) (Pan, Huang & Yang, 2026). The paper formalizes the threat model, scores ten existing AI memory systems against a four-dimension privacy taxonomy (no prior system achieves all four properties simultaneously), and specifies the `.vmem` format as a portable standard.

I submitted the preprint to Zenodo and I'm targeting ACM CCS 2026 for the full paper.

---

## Try it

```bash
pip install vaultmem                   # core
pip install "vaultmem[local]"          # + local embeddings (sentence-transformers)
```

The library is intentionally small — the code is the specification. If you're building an AI agent and want to give your users memory that's actually theirs, this is the starting point.

[github.com/aag1091-alt/vaultmem-sdk](https://github.com/aag1091-alt/vaultmem-sdk)
