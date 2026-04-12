---
layout: post
title: "How daylog Keeps Your Diary Private (Even from Itself)"
permalink: /post/daylog-security-architecture/
read_time: 7
---

[daylog](https://github.com/aag1091-alt/daylog) is a voice diary. You open it, tap the mic, say what's on your mind, and it saves. You can search your entries semantically — "when was I frustrated?" — and ask an AI to summarise your day.

That last part sounds like a contradiction. Private diary. AI summary. How does that work without handing your thoughts to a cloud service?

This post walks through exactly what goes where, what's encrypted and when, and what the one deliberate trade-off is.

---

## The architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Your phone                           │
│                                                             │
│   Safari (daylog PWA)                                       │
│   ┌──────────────────────────────────────────────────────┐  │
│   │  passphrase (derived from password, never sent)      │  │
│   │  sessionStorage: session_id, passphrase              │  │
│   │  Web Speech API → text (on-device, Apple neural)     │  │
│   └──────────────────────────────────────────────────────┘  │
│                     │ HTTPS                                  │
└─────────────────────┼───────────────────────────────────────┘
                      │
          ┌───────────▼────────────┐
          │     Rails API          │
          │   (Fly.io, iad)        │
          │                        │
          │  • auth (JWT tokens)   │
          │  • proxies vault ops   │──────────────────────────┐
          │  • calls Groq for      │                          │
          │    summarise only      │                          │
          └────────────────────────┘                          │
                      │ internal (Fly private network)        │
          ┌───────────▼────────────┐                          │
          │   vault service        │                          │
          │   (Fly.io, iad)        │                          │
          │                        │                          │
          │  vaultmem SDK          │                          │
          │  AES-256-GCM at rest   │                          │
          │  sentence-transformers │                          │
          │  (on-device, no API)   │                          │
          │  /data volume          │                          │
          └────────────────────────┘                          │
                                                              │
          ┌───────────────────────────────────────────────────┘
          │
          ▼
   ┌──────────────────┐
   │   Groq API       │
   │ (api.groq.com)   │
   │                  │
   │  receives only:  │
   │  "time: content" │
   │  lines for the   │
   │  day you asked   │
   │  to summarise    │
   └──────────────────┘
```

---

## Encryption: what, where, how

### Your passphrase never leaves your device

When you first set up daylog, you choose a password. The app derives a cryptographic passphrase from it using PBKDF2-SHA256 — 100,000 iterations, salted with your email:

```js
// In the browser, using WebCrypto
const key = await crypto.subtle.importKey("raw", passwordBytes, "PBKDF2", false, ["deriveBits"]);
const bits = await crypto.subtle.deriveBits(
  { name: "PBKDF2", hash: "SHA-256", salt: encoder.encode(`daylog:${email}`), iterations: 100_000 },
  key, 256
);
const passphrase = Array.from(new Uint8Array(bits)).map(b => b.toString(16).padStart(2, "0")).join("");
```

This passphrase is stored in `sessionStorage` only (cleared when the browser tab closes). **It is never sent to any server.** The Rails API never sees it. The vault service receives it once per session to derive the vault's master encryption key (MEK), then keeps the MEK in RAM for that session only.

### Your entries are encrypted before touching disk

The vault service uses [vaultmem](https://github.com/aag1091-alt/vaultmem) — a zero-knowledge encrypted memory library. Each atom (diary entry) is encrypted with AES-256-GCM using the MEK before being written to the `/data` volume on Fly.io. The encrypted file is a `.vmem` file containing a header, an index, and individually encrypted atom blocks.

What's on disk: ciphertext. What the vault service needs to read it: the MEK, which it derives from your passphrase at session-open time and holds in RAM until the session expires or you sign out.

### Search is fully on-device

Semantic search uses `sentence-transformers/all-MiniLM-L6-v2` — a 384-dim embedding model running locally inside the vault service container. Your query is embedded on the same machine as your entries. The cosine similarity calculation happens in RAM. No text leaves the vault service for search.

---

## The one trade-off: AI summarise

This is the honest part.

When you tap **Summarise this day**, your entries for that day are sent to [Groq](https://groq.com) — specifically to `api.groq.com/openai/v1/chat/completions` — running Llama 3.3 70B. Groq is a fast inference API; Llama 3.3 is an open-weight model.

What's sent:

```
09:10 AM: Starting fresh. Cleared everything and decided to actually use this properly.
09:30 PM: Good day. Got a lot done. Need to sleep earlier.
```

Just the time and text of each entry from that day. No name, no account info, no metadata. The Rails API holds the Groq key and makes the call server-side — your phone never talks to Groq directly.

What this means in practice:

- **Groq sees your diary content for the day you summarise.** Their [privacy policy](https://groq.com/privacy-policy/) governs what they do with it.
- **Nothing else goes to Groq.** Navigation, search, adding entries, viewing past days — all of this is vault-only.
- **You choose when to summarise.** It's a button you tap, not something that runs automatically.

If this trade-off isn't acceptable for you, the summarise feature can be disabled by removing `GROK_API_KEY` from the Rails API config. Everything else continues to work.

---

## What the Rails API can and can't see

The Rails API owns authentication (JWT tokens, bcrypt passwords stored in Postgres). It proxies vault operations to the vault service over Fly's private network.

What it can see:
- Your email address and hashed password
- That you opened a session (but not the passphrase it received — that's passed through to the vault service immediately)
- Timing of requests

What it can't see:
- Your diary content (always encrypted at the vault service layer)
- Your passphrase (it's in the proxy body but the Rails API passes it through without logging or storing it)
- Your search queries (same — passed through to vault service)

The vault service's internal endpoint is only reachable via Fly's private network (`*.internal`), so it's not accessible from the public internet — only from the Rails API machine.

---

## Data at rest

| Location | What's there | Encrypted? |
|---|---|---|
| Fly.io volume (`/data/vaults/`) | `.vmem` files — atom ciphertext + index | Yes — AES-256-GCM |
| Postgres (Neon) | email, bcrypt password hash, session tokens | Passwords hashed; DB encrypted at rest |
| Browser sessionStorage | session_id, passphrase | Cleared on tab close |
| Browser localStorage | auth JWT | Cleared on sign out |

---

## Data in transit

All external traffic is HTTPS. The Rails API ↔ vault service communication uses Fly's private IPv6 network, which is encrypted at the Wireguard layer.

---

## The short version

- **Voice transcription**: on-device (Apple's neural engine via Web Speech API). Nothing leaves your phone.
- **Adding and reading entries**: passphrase stays in your browser; entries are encrypted before touching disk.
- **Search**: fully on-device inside the vault service. No external API.
- **AI summarise**: sends that day's entries to Groq. Optional, explicit, one day at a time.

The goal was to make something that feels like a private notebook — where the default is that your thoughts stay yours, and you explicitly opt in to the parts that touch the cloud.

---

*daylog is open source: [github.com/aag1091-alt/daylog](https://github.com/aag1091-alt/daylog)*
