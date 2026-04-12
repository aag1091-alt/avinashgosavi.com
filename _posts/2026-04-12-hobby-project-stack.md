---
layout: post
title: "What Should You Actually Use to Build Your Next Hobby Project?"
permalink: /post/hobby-project-stack/
read_time: 9
---

I recently built **daylog** — a personal diary app where you speak or type your thoughts and they get encrypted and stored privately, with AI transcription happening server-side using Whisper. The interesting technical core is [vaultmem](https://pypi.org/project/vaultmem/), a Python SDK for building encrypted memory vaults for AI apps. Daylog is essentially a live demo of it.

But the more interesting story — the one I keep getting asked about — is the stack. Because I built this with a hard constraint: **it should cost me nothing to run**, and I should be able to deploy it from my laptop to a URL I can test on my phone in under 10 minutes.

Here's everything I learned about what's actually available in 2025, what's free, and what I'd pick if I were starting fresh today.

---

## The constraints that shaped every decision

Before comparing services, the constraints matter:

1. **Zero fixed cost** — I'm not charging for this. It needs to run on free tiers or scale-to-zero infrastructure.
2. **Phone-first** — I needed a real URL on day one, testable on mobile, installable as a PWA.
3. **Privacy-first** — Audio diary. Nothing goes to third-party AI APIs. Transcription happens on my own server.
4. **Deploy from laptop** — No CI/CD setup in the first week. Just push and it works.

---

## The architecture at a glance

Before diving into each choice, here's how all the pieces connect:

<div class="mermaid">
graph TD
    Phone["📱 Phone / Browser\nCloudflare Pages PWA"]
    Rails["Rails API\ndaylog-rails-api.fly.dev\n─────────────\nAuth · routing · proxy"]
    Postgres[("Neon Postgres\nusers · sessions · tokens")]
    Vault["Vault Service\nFastAPI + vaultmem\n─────────────\ntranscription · search · storage"]
    Redis[("Upstash Redis\nvault locks")]
    Volume[/"Fly Volume\nAES-256 .vmem files"/]
    Whisper["faster-whisper\ntiny · int8 · CPU"]
    Embed["sentence-transformers\nsemantic search"]

    Phone -->|"HTTPS"| Rails
    Rails -->|"SQL"| Postgres
    Rails -->|"Fly internal network\n:8000 — never public"| Vault
    Vault -->|"distributed lock"| Redis
    Vault -->|"read / write"| Volume
    Vault --- Whisper
    Vault --- Embed
</div>

The key insight: the vault service is **never exposed to the internet**. Rails acts as the public face — it handles auth, verifies the JWT, and only then forwards requests to the vault service over Fly's private network. The vault service doesn't need its own auth layer, rate limiting, or TLS. That's what makes this setup so lean.

---

## The stack, and why

### Frontend: Cloudflare Pages

**Chose:** Cloudflare Pages
**Also considered:** Vercel, Netlify, GitHub Pages

Cloudflare Pages is the easy winner for hobby frontends. Free tier includes:
- Unlimited requests
- 500 builds/month
- Global CDN
- Custom domains with auto-SSL

But the real reason I chose it over Vercel: **Cloudflare's ecosystem**. If you ever need edge functions, object storage (R2), or KV, they're right there in the same platform. Vercel's free tier is also generous, but it optimises for Next.js specifically — if you're not using Next.js (I'm using Vite + React), Cloudflare has less lock-in.

**Netlify** is fine but feels like it's slowly losing the race. Their free tier has a 100GB bandwidth cap and slower build times.

> **My pick for your next hobby frontend:** Cloudflare Pages, unless you're building a Next.js app — then Vercel.

---

### Backend: Fly.io

**Chose:** Fly.io
**Also considered:** Railway, Render, Heroku (lol)

For a backend that needs to actually run a persistent server process — not a serverless function — Fly.io is currently the best deal available:

- **3 shared-cpu-1x VMs with 256MB RAM** completely free
- **Persistent volumes** (I use this for encrypted vault files)
- **Private networking** between apps via `.internal` DNS — no API keys needed between your services
- **Deploy from Docker** — no magic, no platform-specific config

The private networking was the killer feature for daylog. My Rails API talks to the vault service at `http://daylog-vault-service.internal:8000`. Zero latency, zero egress cost, zero authentication surface area exposed to the internet.

**Railway** is the other serious contender. Their developer plan gives you $5 of free credit per month, which is enough to run a small app. The UX is genuinely nicer than Fly's. But Railway doesn't give you persistent volumes on the free tier, and their private networking story is less mature.

**Render** has a free tier but web services sleep after 15 minutes of inactivity. If your app gets a request after sleeping, the first one takes 30+ seconds to respond. For a production app this is a dealbreaker. Their paid plans are reasonable.

**Heroku** effectively killed their free tier in 2022. Don't bother.

> **My pick:** Fly.io if you need persistent state, private networking between services, or Docker deploys. Railway if you want a nicer UI and don't need volumes.

---

### Database: Neon Postgres

**Chose:** Neon
**Also considered:** Supabase, Railway Postgres, PlanetScale

Neon is **serverless Postgres**. It scales to zero when idle, so you're not paying for compute when nothing's happening. Free tier:
- 512MB storage
- 1 project, 10 branches
- Branches are perfect for testing schema changes

The branch feature is genuinely underrated. You can spin up a copy of your database for a feature branch, test a migration, and delete it — all from the CLI.

**Supabase** is the obvious alternative and it's excellent — you get Postgres, auth, real-time, and file storage in one package. Their free tier is a 500MB Postgres database. The catch: free tier projects pause after 7 days of inactivity. Fine if you're actively building, annoying if you step away for two weeks.

**PlanetScale** had the best free tier in the business for a while — then they removed it entirely in 2024. Avoid for hobby projects unless you're paying.

**Railway Postgres** is convenient if you're already on Railway, but pricier than Neon for the same storage.

> **My pick:** Neon for pure SQL, Supabase if you also need auth/file storage out of the box.

---

### Cache / Ephemeral State: Upstash Redis

**Chose:** Upstash Redis
**Also considered:** Railway Redis, Render Redis

Upstash is serverless Redis. I use it for one thing: a distributed lock that prevents two vault service instances from opening the same encrypted vault simultaneously. Free tier:
- 10,000 commands/day
- 256MB storage
- Pay-per-request above that

For a hobby app this is effectively infinite. I've never come close to the limit.

The key property: **it doesn't cost you anything when you're not using it**. Railway and Render both charge you for Redis even when idle. Upstash charges zero for zero activity.

> **My pick:** Upstash Redis for anything ephemeral, rate-limiting, locking, or session state in a hobby project.

---

### AI / ML: Whisper on CPU, on your own server

This is where daylog gets opinionated.

The obvious path for audio transcription is the OpenAI Whisper API — $0.006 per minute, accurate, fast. For a diary app that's maybe 5 minutes of audio a day, that's $0.03/day — practically free.

But I'm building a *private* diary. Audio of your thoughts shouldn't route through third-party APIs, even cheap ones. So I run Whisper locally on the vault service VM.

The practical setup:
- **faster-whisper** (Python, CTranslate2 backend) — 2-4x faster than the original openai-whisper package
- **tiny model with int8 quantization** — fits in memory, transcribes a 5-second chunk in ~2-3 seconds on a shared CPU
- **Model baked into the Docker image** — no cold download on VM restart

The tradeoff: it's slower than the API (3-5s per chunk vs instant), and `tiny` makes occasional errors. For a private diary that's fine. For a customer-facing product, you'd probably use the API.

**What this teaches you:** The "serverless AI API" path is usually the right default for hobby projects — OpenAI, Replicate, Together AI all have generous free tiers or pay-per-use pricing that rounds to zero at hobby scale. Only run models yourself if you have a specific reason (cost at scale, privacy, customisation).

---

### Encrypted Storage: vaultmem

This is the part I want to highlight because it's why daylog exists at all.

[vaultmem](https://pypi.org/project/vaultmem/) is a Python SDK that gives you an **encrypted, embeddable memory vault** for AI applications. You give it a passphrase and it gives you a session where you can store text atoms, media blobs, and run semantic search — all encrypted at rest.

For daylog, this means:
- Your diary entries are encrypted on the server with a key derived from your passphrase
- I (the server operator) can't read your diary
- The vault is a single `.vmem` file on a Fly volume — no database schema, no migrations
- Semantic search ("what did I write about three weeks ago?") works out of the box

The SDK handles all the hard parts: PBKDF2 key derivation, AES-256 encryption, sentence embeddings for search, flush/commit semantics. You write:

```python
session = vault.open(user_id, passphrase)
session.add("Had a great meeting with the team today")
session.flush()
```

And you get encrypted storage with semantic search for free.

This is what makes the whole stack work at hobby scale — instead of a Postgres schema for diary entries + a vector database for search + an encryption layer + blob storage for audio, you have one SDK and one file.

---

## What everything costs

Here's the actual bill:

| Service | What I use it for | Monthly cost |
|---|---|---|
| Cloudflare Pages | Web app hosting | **$0** |
| Fly.io | Rails API + vault service | **$0** (2 VMs, free tier) |
| Neon | Postgres (users, sessions) | **$0** (free tier) |
| Upstash | Redis (vault locks) | **$0** (free tier) |
| **Total** | | **$0** |

The only way this crosses zero is if I add a persistent volume larger than 3GB (Fly charges $0.15/GB/month) or if my Neon database exceeds 512MB.

For context: the same app on managed infrastructure — RDS, ElastiCache, EC2, CloudFront — would run $50-100/month minimum.

---

## My opinionated guide for your next hobby project

**Static site / frontend only:**
Cloudflare Pages. Nothing else comes close on the free tier.

**Full-stack app, no persistent state:**
Cloudflare Pages (frontend) + Cloudflare Workers (API). Everything runs at the edge, free tier is very generous.

**Full-stack app with a database:**
Cloudflare Pages + Fly.io + Neon. This is the setup I'd start with today. All three have genuine free tiers with no sleeping, no credit card traps.

**Need auth out of the box:**
Add Supabase for the database and use their auth — or keep Neon and use Clerk (generous free tier for up to 10k MAU).

**Need background jobs or scheduled tasks:**
Fly.io handles this natively — just run a separate machine. Or use Upstash QStash ($0 for low volume).

**AI features:**
Start with the API (OpenAI, Anthropic, Together, Replicate). Only run models yourself when you have a specific reason. CPU inference on Fly is possible (I'm doing it) but it's slow — GPU machines are still expensive even at hobby scale.

**Encrypted, private AI memory:**
vaultmem. That's the pitch.

---

## The one thing I'd do differently

I'd set up a simple CI/CD pipeline earlier. Deploying from the terminal (`fly deploy --local-only`, `wrangler pages deploy`) is fine for the first week, but it gets old fast. GitHub Actions + Fly + Cloudflare deploy actions take maybe 30 minutes to set up and remove a lot of friction.

---

The broader point: the free tier ecosystem for hobby projects has genuinely never been better. In 2025 you can run a full-stack app with a real database, Redis, background jobs, and AI inference for exactly zero dollars a month — and none of these services are traps that will surprise you with a bill when a tweet goes viral.

The days of "I can't afford to run this side project" are over. The only cost now is your time.

---

## What's next for daylog

I'm putting the finishing touches on a proper demo — the full flow of opening the app, speaking a thought, watching it transcribe in real time, and searching back through weeks of entries with a natural language query. All encrypted, all on-device passphrase, running on the stack described above.

If you want to see what a privacy-first, AI-powered personal knowledge tool looks like when it costs nothing to run — keep an eye out. Demo coming soon.

*vaultmem is on PyPI. daylog is coming.*

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true, theme: 'neutral' });
</script>
