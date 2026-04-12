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

## How your words travel

The diagram below traces a single diary entry — "went for a run today" — from your mouth to disk, and back to your eyes.

<svg viewBox="0 0 700 290" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:700px;display:block;margin:2rem 0;font-family:system-ui,sans-serif;font-size:12px">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#94a3b8"/>
    </marker>
  </defs>

  <!-- ── SAVING label ── -->
  <text x="10" y="14" font-size="10" fill="#64748b" font-weight="700" letter-spacing="0.12em">SAVING AN ENTRY</text>

  <!-- Write box 1: Speak -->
  <rect x="10" y="22" width="120" height="72" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="70" y="46" text-anchor="middle" font-size="16">🎤</text>
  <text x="70" y="63" text-anchor="middle" font-size="10" fill="#15803d" font-weight="600">You speak</text>
  <text x="70" y="78" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>

  <line x1="130" y1="58" x2="148" y2="58" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Write box 2: Browser -->
  <rect x="150" y="22" width="120" height="72" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="210" y="43" text-anchor="middle" font-size="10" fill="#15803d" font-weight="600">Browser</text>
  <text x="210" y="57" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <text x="210" y="70" text-anchor="middle" font-size="8" fill="#22c55e">transcribed on-device</text>
  <text x="210" y="83" text-anchor="middle" font-size="8" fill="#22c55e">nothing sent yet ✓</text>

  <line x1="270" y1="58" x2="288" y2="58" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Write box 3: HTTPS -->
  <rect x="290" y="22" width="120" height="72" rx="7" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="350" y="46" text-anchor="middle" font-size="10" fill="#1d4ed8" font-weight="600">HTTPS</text>
  <text x="350" y="60" text-anchor="middle" font-size="9" fill="#1d4ed8">"went for a run today"</text>
  <text x="350" y="74" text-anchor="middle" font-size="8" fill="#3b82f6">content encrypted</text>
  <text x="350" y="86" text-anchor="middle" font-size="8" fill="#3b82f6">in transit by TLS</text>

  <line x1="410" y1="58" x2="428" y2="58" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Write box 4: Vault encrypts -->
  <rect x="430" y="22" width="120" height="72" rx="7" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="490" y="43" text-anchor="middle" font-size="10" fill="#854d0e" font-weight="600">Vault encrypts</text>
  <text x="490" y="57" text-anchor="middle" font-size="8" fill="#92400e">AES-256-GCM</text>
  <text x="490" y="70" text-anchor="middle" font-size="8" fill="#92400e">🔑 using your key</text>
  <text x="490" y="83" text-anchor="middle" font-size="8" fill="#92400e">derived from password</text>

  <line x1="550" y1="58" x2="568" y2="58" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Write box 5: Disk -->
  <rect x="570" y="22" width="120" height="72" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="630" y="43" text-anchor="middle" font-size="14">💾</text>
  <text x="630" y="59" text-anchor="middle" font-size="10" fill="#991b1b" font-weight="600">Stored on disk</text>
  <text x="630" y="73" text-anchor="middle" font-size="9" fill="#b91c1c">7f3a·a4c8·e12d·...</text>
  <text x="630" y="86" text-anchor="middle" font-size="8" fill="#dc2626">ciphertext — unreadable</text>

  <!-- ── Divider ── -->
  <line x1="10" y1="112" x2="690" y2="112" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="5,4"/>

  <!-- ── READING label ── -->
  <text x="10" y="130" font-size="10" fill="#64748b" font-weight="700" letter-spacing="0.12em">READING YOUR ENTRIES</text>

  <!-- Read box 1: Disk -->
  <rect x="10" y="138" width="120" height="72" rx="7" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="70" y="157" text-anchor="middle" font-size="14">💾</text>
  <text x="70" y="174" text-anchor="middle" font-size="10" fill="#991b1b" font-weight="600">Stored on disk</text>
  <text x="70" y="188" text-anchor="middle" font-size="9" fill="#b91c1c">7f3a·a4c8·e12d·...</text>
  <text x="70" y="201" text-anchor="middle" font-size="8" fill="#dc2626">ciphertext</text>

  <line x1="130" y1="174" x2="148" y2="174" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Read box 2: Vault decrypts -->
  <rect x="150" y="138" width="120" height="72" rx="7" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="210" y="159" text-anchor="middle" font-size="10" fill="#854d0e" font-weight="600">Vault decrypts</text>
  <text x="210" y="173" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <text x="210" y="186" text-anchor="middle" font-size="8" fill="#92400e">🔑 your key only</text>
  <text x="210" y="199" text-anchor="middle" font-size="8" fill="#92400e">in memory, not logged</text>

  <line x1="270" y1="174" x2="288" y2="174" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Read box 3: HTTPS -->
  <rect x="290" y="138" width="120" height="72" rx="7" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="350" y="162" text-anchor="middle" font-size="10" fill="#1d4ed8" font-weight="600">HTTPS</text>
  <text x="350" y="176" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <text x="350" y="190" text-anchor="middle" font-size="8" fill="#3b82f6">content encrypted</text>
  <text x="350" y="202" text-anchor="middle" font-size="8" fill="#3b82f6">in transit by TLS</text>

  <line x1="410" y1="174" x2="428" y2="174" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Read box 4: Browser -->
  <rect x="430" y="138" width="120" height="72" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="490" y="159" text-anchor="middle" font-size="10" fill="#15803d" font-weight="600">Browser</text>
  <text x="490" y="173" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>
  <text x="490" y="186" text-anchor="middle" font-size="8" fill="#22c55e">plain text ✓</text>

  <line x1="550" y1="174" x2="568" y2="174" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Read box 5: You see it -->
  <rect x="570" y="138" width="120" height="72" rx="7" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="630" y="159" text-anchor="middle" font-size="14">📱</text>
  <text x="630" y="175" text-anchor="middle" font-size="10" fill="#15803d" font-weight="600">You see it</text>
  <text x="630" y="189" text-anchor="middle" font-size="9" fill="#166534">"went for a run today"</text>

  <!-- ── Legend ── -->
  <rect x="10" y="230" width="11" height="11" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5" rx="2"/>
  <text x="25" y="240" font-size="9" fill="#64748b">Readable text</text>

  <rect x="120" y="230" width="11" height="11" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5" rx="2"/>
  <text x="135" y="240" font-size="9" fill="#64748b">Encrypted — unreadable</text>

  <rect x="278" y="230" width="11" height="11" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5" rx="2"/>
  <text x="293" y="240" font-size="9" fill="#64748b">Secured in transit (TLS)</text>

  <rect x="445" y="230" width="11" height="11" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5" rx="2"/>
  <text x="460" y="240" font-size="9" fill="#64748b">Encryption / decryption point</text>
</svg>

The key thing to notice: your words are readable on your device, and readable in your browser when you read them back. **Everything in between — transit, storage — is ciphertext.** The only thing that can decrypt your entries is the key that lives in the vault service's RAM, derived from your passphrase, which never leaves your browser.

---

## The one exception: AI summarise

When you tap **Summarise this day**, the browser sends that day's already-decrypted entries to the Rails API, which forwards them to [Groq](https://groq.com) (Llama 3.3 70B). What Groq receives:

```
09:10 AM: Went for a run today.
08:30 PM: Good session, finally fixed that bug.
```

Just time + text for the one day you asked to summarise. No name, no metadata, nothing from other days. The summary is never saved back to the vault.

This is the deliberate trade-off: everything else is vault-only, but summarise sends content to an external API. It's a button you tap explicitly, not something that runs automatically. If that's not acceptable, remove `GROK_API_KEY` from the config and the rest of the app works unchanged.

---

## Encryption: the details

**Your passphrase never leaves your device.** When you log in, your password is run through PBKDF2-SHA256 (100,000 rounds, salted with your email) entirely in the browser using WebCrypto. The result is stored in `sessionStorage` — cleared when the tab closes — and passed once to the vault service to open a session. The vault service derives a master encryption key (MEK) from it in RAM and never writes the passphrase or MEK to disk.

**Entries are encrypted before touching disk.** Each diary entry is encrypted with AES-256-GCM and stored in a `.vmem` file on the vault service's Fly.io volume. What's on disk is ciphertext. To read it back, the vault service needs the MEK — which only exists in RAM during an active session.

**Search never leaves the vault service.** Semantic search uses `sentence-transformers/all-MiniLM-L6-v2` running locally inside the vault container. Your query is embedded on the same machine as your entries. Nothing goes to any external API.

---

## What the Rails API sees

The Rails API handles auth (JWT tokens, bcrypt passwords). It proxies vault requests to the vault service over Fly's private internal network.

It can see: your email, that you opened a session, request timing.

It cannot see: your diary content (always ciphertext at the vault layer), your passphrase (passed through immediately without logging), your search queries.

The vault service is not reachable from the public internet — only from the Rails API over `*.internal`.

---

## Data at rest

| Where | What | Encrypted? |
|---|---|---|
| Fly.io volume | `.vmem` ciphertext | AES-256-GCM |
| Postgres (Neon) | email, bcrypt hash, session tokens | Passwords hashed; DB encrypted at rest |
| Browser sessionStorage | session_id, passphrase | Cleared on tab close |
| Browser localStorage | auth JWT | Cleared on sign out |

---

## The short version

- **Speaking**: transcribed on-device by Apple's neural engine. Nothing leaves your phone.
- **Saving**: encrypted with your key before hitting disk. Vault service holds the key in RAM only.
- **Searching**: runs inside the vault service. No external API.
- **Summarising**: sends that day's entries to Groq. Your choice, one day at a time.

---

*daylog is open source: [github.com/aag1091-alt/daylog](https://github.com/aag1091-alt/daylog)*
