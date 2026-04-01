---
layout: post
title: "VaultMem Part 3 — Hiding PII from Your LLM Provider"
permalink: /post/vaultmem-part-3-pii-sanitizer/
date: 2026-04-01
read_time: 8
---

[Part 1](/post/vaultmem-encrypted-memory-for-ai-agents/) covered the core encryption model. [Part 2](/post/vaultmem-part-2-multimodal-temporal-backends/) covered multi-modal ingestion and pluggable backends. This post covers v0.3.x — a new layer of privacy that addresses a problem encryption at rest cannot solve.

> **Install:** `pip install 'vaultmem[spacy]'` · **Code:** [github.com/aag1091-alt/vaultmem-sdk](https://github.com/aag1091-alt/vaultmem-sdk) · **Live demo:** [vaultmem-demo.streamlit.app](https://vaultmem-demo.streamlit.app)

---

## The gap encryption at rest doesn't close

VaultMem stores every memory atom encrypted with AES-256-GCM. Your passphrase never leaves your device. The platform operator cryptographically cannot read your vault. The threat model comes from the Memory-as-Asset framework (Pan, Huang & Yang, [arXiv:2603.14212](https://arxiv.org/abs/2603.14212)): memory is a personal asset, not a platform resource.

But there is a second exposure point I hadn't fully addressed: the moment you decrypt a memory and inject it into an LLM prompt.

Say your vault contains:

```
I met Sarah Chen at the NeurIPS conference. She works on ML infra at Google.
My accountant James Park can be reached at james@parkaccounting.com.
```

When you ask your assistant "what do I know about Sarah?", VaultMem retrieves those memories, decrypts them, and sends them as context to the LLM provider — Groq, OpenAI, Anthropic, whoever you're using. At that point, Sarah's name, her employer, and James's email address are all sitting in plaintext in an HTTP request to a third-party cloud.

Encryption at rest doesn't help here. The data is decrypted before it goes out the door.

---

## The solution: strip PII before injection, restore it after

VaultMem v0.3.0 ships a `Sanitizer` class that sits between your vault and your LLM call.

```python
from vaultmem import VaultSession, Sanitizer

san = Sanitizer(backend="spacy")   # one instance per session

with VaultSession.open("./my_vault", passphrase="...") as s:
    memories = s.search("sarah chen", top_k=5)
    context = "\n".join(f"- {m.atom.content}" for m in memories)

    # Sanitize context AND query with the same instance
    sanitized_context, rmap = san.sanitize(context)
    sanitized_query, rmap   = san.sanitize(user_query)

    raw_reply = llm.chat(sanitized_query, context=sanitized_context)

    # Restore real values in the LLM's response
    final_reply = san.restore(raw_reply, rmap)
```

The LLM provider receives:

```
I met Jordan at the NeurIPS conference. She works on ML infra at Globex.
My accountant Casey can be reached at [EMAIL_1].
```

It reasons about this correctly, responds naturally, and VaultMem restores the real values client-side before the answer is shown to the user.

The provider never sees the real names, companies, or contact details.

---

## Pseudonyms, not tokens

Person names are replaced with natural-sounding pseudonyms — Jordan, Casey, Morgan, Riley, Avery — rather than opaque tokens like `[PERSON_1]`.

The reason is fluency. If the LLM sees `[PERSON_1]` in context and addresses the user with it, the response reads awkwardly. With a pseudonym, it can write "Based on what Jordan told you at NeurIPS..." and after restoration the user reads "Based on what Sarah Chen told you at NeurIPS..." — completely natural.

Organisations get fictional company names (Acme, Globex, Initech, Pied Piper). Structured PII — emails, phone numbers, SSNs, credit cards, IPs — gets typed tokens (`[EMAIL_1]`, `[PHONE_2]`) because there's no natural-sounding substitute for those.

The mapping is **session-scoped and stable**: if "Sarah Chen" appears in five different memories, she is always Jordan in that session. The LLM can reason about her as a single consistent person across all memories.

---

## Two backends

Presidio supports different NLP backends. VaultMem exposes both:

```python
# Lightweight — ~12 MB spaCy model, no PyTorch dependency
# Works on Streamlit Cloud, CI, anywhere torch is unavailable
san = Sanitizer(backend="spacy")

# High-accuracy — ~400 MB transformers model, requires PyTorch
# Best for local deployments or privacy-critical production use
san = Sanitizer(backend="transformers")
```

The spaCy backend (`en_core_web_sm`) is the default. It handles the common cases — person names, organisations, locations, emails, phone numbers — and is small enough to deploy anywhere without a GPU or a multi-gigabyte dependency install.

```bash
# spaCy (default)
pip install 'vaultmem[spacy]'
python -m spacy download en_core_web_sm

# transformers (high accuracy)
pip install 'vaultmem[presidio]'
```

---

## What gets skipped

Not everything Presidio detects is PII. Temporal expressions (`DATE_TIME`), cardinal numbers, percentages, monetary values, and quantities are identifying in context but not on their own — and redacting them breaks the coherence of the context significantly.

VaultMem v0.3.2 introduced a skip list:

```python
_SKIP_ENTITY_TYPES = frozenset({
    "DATE_TIME", "CARDINAL", "ORDINAL",
    "PERCENT", "MONEY", "QUANTITY", "LANGUAGE",
})
```

Before this, a memory like "Every Friday at 4pm I do a weekly review — takes 20 minutes" was returned to the LLM as "Every [DATE_TIME_3] at [DATE_TIME_4] I do a weekly review — takes [DATE_TIME_5]". Correct in theory, unreadable in practice. The skip list fixes this.

The same release fixed two spaCy-specific label mismatches: spaCy reports organisations as `ORGANIZATION` (not `ORG`) and geopolitical entities as `GPE` (not `LOCATION`). Before the fix these fell through to typed tokens instead of receiving pseudonyms from the pools.

---

## A subtle bug: case-insensitive deduplication

During testing I hit a bug that's easy to miss until you actually run the system with real queries.

The memory stored `"Sarah Chen"` (title case). The user asked `"who is sarah chen?"` (lowercase). Presidio detected `"sarah chen"` as a PERSON — but the forward map looked it up with an exact string match. `"sarah chen" != "Sarah Chen"`, so it was treated as a new entity and assigned a fresh pseudonym: Casey.

The LLM then received context about Jordan but a query about Casey. Its response: *"There is no information about Casey."* Technically accurate. Completely useless.

The fix in v0.3.3: all forward-map keys are normalised to lowercase. A separate canonical map preserves the first-seen capitalisation so restoration returns `"Sarah Chen"`, not `"sarah chen"`. The variant seen first wins on casing; all subsequent variants map to the same pseudonym.

```python
def _assign(self, real: str, entity_type: str) -> str:
    key = real.lower()
    if key in self._forward:
        return self._forward[key]          # "sarah chen" hits "Sarah Chen"'s entry
    self._canonical[key] = real            # first-seen casing for restoration
    ...
```

---

## What this doesn't solve

The Sanitizer addresses what leaves your device. It doesn't address what the LLM infers or reconstructs. If your memory says "I grew up two blocks from the Eiffel Tower", stripping names doesn't prevent the LLM from inferring something about where you're from.

The complete solution is TEE-based inference — running the model inside a trusted execution environment so the provider's infrastructure never sees plaintext at all. That's the direction the research is heading (see the arXiv paper above), but it's not production-ready for general-purpose models yet.

PII stripping is the practical near-term answer. It's not perfect, but it meaningfully shrinks the surface area of personal data your LLM provider sees on every query.

---

## Changelog

- **v0.3.0** — `Sanitizer` class, transformers backend, pseudonym pools, restoration map
- **v0.3.1** — spaCy backend (`en_core_web_sm`), new `[spacy]` optional extra, `backend=` parameter
- **v0.3.2** — `DATE_TIME` skip list, `ORGANIZATION`/`GPE` label fixes for spaCy
- **v0.3.3** — case-insensitive entity deduplication

`pip install 'vaultmem[spacy]'` gets you the latest.

If you're building an AI agent that touches personal data, I'd love to hear what you're working on.
