---
layout: post
title: "How daylog Keeps Your Diary Private (Even from Itself)"
permalink: /post/daylog-security-architecture/
read_time: 8
---

daylog is a voice diary. You open it, tap the mic, say what's on your mind, and it saves. You can search your entries semantically — type "frustrated" and it surfaces the day you wrote *"couldn't make progress, everything felt blocked"* even though that exact word never appears.

That search working at all, while keeping your diary private, requires a few things to be true simultaneously: the content must be encrypted at rest, the search index must also be encrypted, and nothing should leave the device to answer a query. This post explains how each of those holds.

---

## How your words travel

The diagram traces a single entry from your mouth to disk, and back to your eyes.

<svg viewBox="0 0 700 290" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:700px;display:block;margin:2rem 0;font-family:system-ui,sans-serif;font-size:12px">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#94a3b8"/>
    </marker>
  </defs>

  <!-- SAVING label -->
  <text x="10" y="14" font-size="10" fill="#64748b" font-weight="700" letter-spacing="0.12em">SAVING AN ENTRY</text>

  <rect x="10" y="22" width="120" height="72" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="70" y="46" text-anchor="middle" font-size="16">🎤</text>
  <text x="70" y="63" text-anchor="middle" font-size="10" fill="#15803d" font-weight="600">You speak</text>
  <text x="70" y="78" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <line x1="130" y1="58" x2="148" y2="58" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <rect x="150" y="22" width="120" height="72" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="210" y="43" text-anchor="middle" font-size="10" fill="#15803d" font-weight="600">Browser</text>
  <text x="210" y="57" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <text x="210" y="70" text-anchor="middle" font-size="8" fill="#22c55e">transcribed on-device</text>
  <text x="210" y="83" text-anchor="middle" font-size="8" fill="#22c55e">nothing sent yet ✓</text>
  <line x1="270" y1="58" x2="288" y2="58" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <rect x="290" y="22" width="120" height="72" rx="7" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="350" y="46" text-anchor="middle" font-size="10" fill="#1d4ed8" font-weight="600">HTTPS</text>
  <text x="350" y="60" text-anchor="middle" font-size="9" fill="#1d4ed8">"went for a run today"</text>
  <text x="350" y="74" text-anchor="middle" font-size="8" fill="#3b82f6">content encrypted</text>
  <text x="350" y="86" text-anchor="middle" font-size="8" fill="#3b82f6">in transit by TLS</text>
  <line x1="410" y1="58" x2="428" y2="58" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <rect x="430" y="22" width="120" height="72" rx="7" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="490" y="43" text-anchor="middle" font-size="10" fill="#854d0e" font-weight="600">Vault encrypts</text>
  <text x="490" y="57" text-anchor="middle" font-size="8" fill="#92400e">embed → AES-256-GCM</text>
  <text x="490" y="70" text-anchor="middle" font-size="8" fill="#92400e">🔑 using your key</text>
  <text x="490" y="83" text-anchor="middle" font-size="8" fill="#92400e">text + vector encrypted</text>
  <line x1="550" y1="58" x2="568" y2="58" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <rect x="570" y="22" width="120" height="72" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="630" y="43" text-anchor="middle" font-size="14">💾</text>
  <text x="630" y="59" text-anchor="middle" font-size="10" fill="#991b1b" font-weight="600">Stored on disk</text>
  <text x="630" y="73" text-anchor="middle" font-size="9" fill="#b91c1c">7f3a·a4c8·e12d·...</text>
  <text x="630" y="86" text-anchor="middle" font-size="8" fill="#dc2626">ciphertext — unreadable</text>

  <!-- Divider -->
  <line x1="10" y1="112" x2="690" y2="112" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="5,4"/>

  <!-- READING label -->
  <text x="10" y="130" font-size="10" fill="#64748b" font-weight="700" letter-spacing="0.12em">READING YOUR ENTRIES</text>

  <rect x="10" y="138" width="120" height="72" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="70" y="157" text-anchor="middle" font-size="14">💾</text>
  <text x="70" y="174" text-anchor="middle" font-size="10" fill="#991b1b" font-weight="600">Stored on disk</text>
  <text x="70" y="188" text-anchor="middle" font-size="9" fill="#b91c1c">7f3a·a4c8·e12d·...</text>
  <text x="70" y="201" text-anchor="middle" font-size="8" fill="#dc2626">ciphertext</text>
  <line x1="130" y1="174" x2="148" y2="174" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <rect x="150" y="138" width="120" height="72" rx="7" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="210" y="159" text-anchor="middle" font-size="10" fill="#854d0e" font-weight="600">Vault decrypts</text>
  <text x="210" y="173" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <text x="210" y="186" text-anchor="middle" font-size="8" fill="#92400e">🔑 your key only</text>
  <text x="210" y="199" text-anchor="middle" font-size="8" fill="#92400e">in memory, not logged</text>
  <line x1="270" y1="174" x2="288" y2="174" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <rect x="290" y="138" width="120" height="72" rx="7" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="350" y="162" text-anchor="middle" font-size="10" fill="#1d4ed8" font-weight="600">HTTPS</text>
  <text x="350" y="176" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <text x="350" y="190" text-anchor="middle" font-size="8" fill="#3b82f6">content encrypted</text>
  <text x="350" y="202" text-anchor="middle" font-size="8" fill="#3b82f6">in transit by TLS</text>
  <line x1="410" y1="174" x2="428" y2="174" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <rect x="430" y="138" width="120" height="72" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="490" y="159" text-anchor="middle" font-size="10" fill="#15803d" font-weight="600">Browser</text>
  <text x="490" y="173" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <text x="490" y="186" text-anchor="middle" font-size="8" fill="#22c55e">plain text ✓</text>
  <line x1="550" y1="174" x2="568" y2="174" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <rect x="570" y="138" width="120" height="72" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="630" y="159" text-anchor="middle" font-size="14">📱</text>
  <text x="630" y="175" text-anchor="middle" font-size="10" fill="#15803d" font-weight="600">You see it</text>
  <text x="630" y="189" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>

  <!-- Legend -->
  <rect x="10" y="230" width="11" height="11" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5" rx="2"/>
  <text x="25" y="240" font-size="9" fill="#64748b">Readable text</text>
  <rect x="120" y="230" width="11" height="11" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5" rx="2"/>
  <text x="135" y="240" font-size="9" fill="#64748b">Encrypted — unreadable</text>
  <rect x="278" y="230" width="11" height="11" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5" rx="2"/>
  <text x="293" y="240" font-size="9" fill="#64748b">Secured in transit (TLS)</text>
  <rect x="445" y="230" width="11" height="11" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5" rx="2"/>
  <text x="460" y="240" font-size="9" fill="#64748b">Encryption / decryption point</text>
</svg>

Your words are readable on your device and readable back in your browser. Everything in between — transit, storage — is ciphertext. Notice the saving path says *"text + vector encrypted"*: the search index is encrypted too, not just the content. More on that below.

---

## What vaultmem actually does

The vault service uses vaultmem — a library I built for giving AI agents a private, searchable long-term memory. In daylog it does three things every time you save an entry:

**1. Classifies the entry automatically.**

Every entry is run through a fast, rule-based classifier (no LLM involved) that assigns a memory type:

- **EPISODIC** — a time-anchored personal experience. *"Yesterday I went for a run."* Has a temporal marker + first-person reference.
- **PERSONA** — a habitual trait or preference. *"I usually start work before 8am."* Has a frequency word + first-person framing.
- **PROCEDURAL** — a how-to or sequence. *"First compile, then run tests."* Has sequential markers.
- **SEMANTIC** — a timeless fact. Everything else.

Most diary entries classify as EPISODIC. The type determines how the memory is weighted and how it ages — episodic memories have a natural recency decay, semantic ones don't.

**2. Embeds the entry as a 384-dimensional vector.**

Before the entry is encrypted, it is run through `sentence-transformers/all-MiniLM-L6-v2` — a 22M parameter model running locally inside the vault container. The model converts your text into a 384-float vector that captures the semantic meaning of what you wrote.

*"went for a run today"* → `[0.312, -0.087, 0.441, ..., 0.198]` (384 values)

This vector is how search finds relevant entries later. It is stored alongside the text.

**3. Encrypts text + vector together and writes to disk.**

The entry object — text, classification, timestamp, and embedding vector — is serialised to JSON, compressed with zlib, and encrypted with AES-256-GCM using the master encryption key (MEK). The result is appended to a `.vmem` file on disk as `IV + length + ciphertext + GCM tag`.

**The embedding is encrypted.** The search index — the thing that makes semantic search work — is not sitting in a plaintext index somewhere. It is inside the same ciphertext block as your diary entry. Nobody can search your vault without your key.

---

## How search works end to end

When you type "frustrated" into the search bar:

**1. The vault service embeds your query.**

"frustrated" → `[0.289, -0.041, 0.509, ...]` (the same 384-dim model, same vector space as your stored entries).

**2. It decrypts all stored embeddings from disk.**

Every `.vmem` entry is decrypted in RAM. The vault service now holds a matrix of shape `(N entries) × 384`.

**3. It runs a batched dot product.**

Since both vectors are unit-normalised, dot product = cosine similarity. One matrix multiply gives a relevance score for every entry simultaneously.

**4. It filters, ranks, and returns.**

Entries with score below 0.3 are dropped. The rest are sorted and the top 8 returned — with their decrypted text.

The decrypted entries exist only in RAM during this step. They are never written back to disk.

**Why this finds meaning, not just keywords.**

Two sentences with similar meaning will have similar vectors even if they share no words. "couldn't make any progress today, everything felt blocked" scores ~0.62 against "frustrated" because the model has learned that these concepts occupy the same region of the vector space.

This is the same reason "angry" might surface an entry about a deploy failing at midnight, or "energised" might surface one about a flow state — the words you actually wrote don't have to match the words you search for.

---

## The memory hierarchy

vaultmem stores entries at three granularity levels:

- **ATOM** — a single diary entry. This is what you write.
- **COMPOSITE** — an auto-generated aggregation of related atoms. A weekly summary, or a cluster of entries about the same topic. Not yet used in daylog but the foundation is there.
- **AFFINITY** — a detected standing pattern. If the vault notices you mention sleep problems every week, it could surface that as a persistent affinity. This is where it starts to feel less like a diary and more like a memory that knows you.

Search queries all three tiers in priority order — AFFINITY first, then COMPOSITE, then ATOM — so a standing pattern surfaces above any individual entry that mentions the same thing.

---

## The one trade-off: AI summarise

When you tap **Summarise this day**, the browser's already-decrypted entries for that day are sent to [Groq](https://groq.com) (Llama 3.3 70B) via the Rails API. What Groq receives:

```
09:10 AM: Went for a run today.
08:30 PM: Good session, finally fixed that bug.
```

Time + text for one day. No name, no metadata, nothing from other days. The summary is returned and displayed — it's never saved back into the vault.

Everything else — adding entries, browsing, searching — is vault-only. No external API. Summarise is the one feature that trades privacy for convenience, and it's a button you tap deliberately.

If that trade-off isn't right for you, remove `GROK_API_KEY` from the Rails API config and everything else works unchanged.

---

## Data at rest

| Where | What | Status |
|---|---|---|
| Fly.io volume (`/data/vaults/`) | `.vmem` — text + embedding vectors, all encrypted | AES-256-GCM |
| Postgres (Neon) | email, bcrypt password hash | Passwords hashed; DB encrypted at rest |
| Browser sessionStorage | session_id, derived passphrase | Cleared on tab close |
| Browser localStorage | auth JWT | Cleared on sign out |
| Vault service RAM | MEK, decrypted atoms during active session | Never written to disk |

---

## The short version

- **Voice input**: transcribed on-device by Apple's neural engine. Nothing leaves your phone at this step.
- **Saving**: entry is classified, embedded, then encrypted. Text and search vector hit disk together, both as ciphertext.
- **Searching**: vault decrypts embeddings in RAM, runs cosine similarity, returns matching plaintext. No external API.
- **Summarising**: sends that day's entries to Groq. Optional, explicit, one day at a time.

The encrypted search index is the part most people don't expect. Normally if you want full-text or semantic search, you need a plaintext index somewhere — Elasticsearch, pgvector, whatever. vaultmem stores the vectors encrypted alongside the content, so you get semantic search without giving the index to anyone.

---

## Try it yourself

The app is live. You can log in with the demo account and poke around — all entries are pre-seeded across the last two months.

**[daylog-ds3.pages.dev](https://daylog-ds3.pages.dev)**

```
email:    demo@daylog.app
password: demo1234
```

Things worth trying:

- **Search** (bottom nav → Search tab): type `frustrated`, `flow state`, `couldn't sleep`, or `good run` — these find entries by meaning, not exact words
- **Summarise**: navigate to any day that has entries, scroll past the list, tap **Summarize this day** — it reads everything you logged that day and reflects back themes and mood
- **Voice**: tap the mic, say something, watch the live transcription appear word by word
