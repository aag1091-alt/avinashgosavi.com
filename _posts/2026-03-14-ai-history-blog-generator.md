---
layout: post
title: "AI History Blog Generator"
permalink: /post/ai-history-blog-generator/
read_time: 5
---

I was curious how AI had evolved over the years — not just the big headline moments but the smaller steps in between that actually moved things forward. I wanted something I could browse casually, not a research paper or a Wikipedia rabbit hole. Just a clean walkthrough: milestone by milestone, a bit of context, who was involved, when it happened.

I couldn't find exactly that, so I started building it. Around the same time I was also exploring what local models could actually do — running Ollama, trying different models, seeing how far you could get without sending everything to an API. That combination clicked: use a local model to do the writing, keep costs low, and let it run as long as needed. And somewhere while putting that together I thought — wait, this doesn't have to be about AI. It could be about anything with a history. That's how [AI History Blog Generator](https://github.com/aag1091-alt/AI-History-Blog-Generator) came about — an autonomous agent that turns any historical topic into a fully-functioning Jekyll blog, one milestone at a time.

**Live examples:**
- Default (AI history): [aag1091-alt.github.io/AI-History-Blog](https://aag1091-alt.github.io/AI-History-Blog/)
- Custom topic (Golden Gate Bridge history): [aag1091-alt.github.io/Golden-Gate-History](https://aag1091-alt.github.io/Golden-Gate-History/)

---

## What It Does

Give it a topic — "the history of jazz music", "the history of the Golden Gate Bridge", anything — and it will:

1. Ask Claude to define **eras** and **categories** for the topic (only once, on first run)
2. Pick the next interesting milestone not yet covered
3. Research it via Wikipedia and arXiv
4. Write a full blog post and self-critique it
5. Fetch a relevant Wikimedia image (with NSFW filtering)
6. Generate a **person profile page** for everyone mentioned in the post
7. Commit and push everything to GitHub Pages
8. Repeat — indefinitely if you want

It tracks everything in a `state.json` file so you can stop it mid-run, restart later, and it picks up exactly where it left off.

---

## How the Pipeline Works

Each post goes through a four-stage LangGraph pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude / OpenAI                           │
│           "What's the next milestone to cover?"              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Research Node                                               │
│  ├─ Wikipedia lookup                                         │
│  ├─ arXiv lookup (for science/tech topics)                   │
│  └─ Wikimedia image fetch (relevance + NSFW filtered)        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Write Node (Ollama — local LLM)                             │
│  ├─ WriterAgent with tool calling                            │
│  │   Tools: search_wikipedia, search_arxiv, write_post       │
│  └─ Runs multi-turn until write_post tool is called          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Critique Node (Ollama — structured output via Pydantic)     │
│  Checks: year mentioned · people named · section format      │
│          word count · no hallucinated URLs                   │
│  Returns: approved (bool) + issues list                      │
└───────────┬───────────────────────────┬─────────────────────┘
            │ approved                  │ issues found (max 2x)
            ▼                           ▼
          Publish                  Rewrite Node
          & Push                  (fixes issues, loops back)
```

**Milestone selection** uses Claude (or OpenAI as fallback) via API — this is the "thinking" layer that picks what to write about. **Post writing** is entirely local via Ollama, so you're not paying per token for every paragraph.

Before any of this starts, the agent checks two things to avoid covering the same ground twice: an exact slug match against `state.json`, and a semantic check — if the proposed milestone shares >40% keyword overlap with something already written in the same year, it's rejected and a different one is picked.

---

## Models Used

| Task | Model |
|---|---|
| Milestone selection | Claude (Anthropic API) → OpenAI → Claude CLI |
| Post writing | Ollama — `qwen2.5:14b` (configurable) |
| Critique & structured validation | Ollama with Pydantic output |

The writing model is fully swappable via `.env`. The critique node uses Pydantic models to enforce structured JSON output so there's no fragile text parsing — if the model doesn't return valid JSON, it retries.

Here's how the models I tested compare on RAM footprint and post quality:

| Model | RAM | RAM usage | Post quality |
|---|---|---|---|
| `llama3.2:3b` | ~2 GB | ▓▓░░░░░░░░ | ▓▓▓░░░░░░░ |
| `mistral:7b` | ~4 GB | ▓▓▓░░░░░░░ | ▓▓▓▓▓░░░░░ |
| `qwen2.5:7b` | ~5 GB | ▓▓▓▓░░░░░░ | ▓▓▓▓▓▓░░░░ |
| `qwen2.5:14b` ✦ | ~9 GB | ▓▓▓▓▓░░░░░ | ▓▓▓▓▓▓▓▓░░ |
| `llama3.3:70b` | ~43 GB | ▓▓▓▓▓▓▓▓▓░ | ▓▓▓▓▓▓▓▓▓░ |

✦ default

`qwen2.5:14b` is the sweet spot for most machines — the quality jump from 7b is noticeable in post structure and factual coherence, and 9 GB fits comfortably on a laptop with 16 GB RAM. `llama3.2:3b` works if you're just testing the pipeline; `llama3.3:70b` produces the best output but needs a well-specced machine or a dedicated GPU box.

---

## Try It Yourself

You'll need [Ollama](https://ollama.com) running locally and an Anthropic API key. The model is local so the only API cost is milestone selection (one call per post).

```bash
# 1. Clone and install
git clone https://github.com/aag1091-alt/AI-History-Blog-Generator.git
cd AI-History-Blog-Generator
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Set ANTHROPIC_API_KEY and OLLAMA_MODEL in .env

# 3. Create a blog for any topic
python -m generate --new \
  --topic "the history of jazz music" \
  --dir ~/projects/jazz-blog \
  --github-url https://github.com/you/jazz-blog

# 4. Push to GitHub and enable GitHub Pages in repo settings
cd ~/projects/jazz-blog && git push -u origin main

# 5. Generate posts
python -m generate          # one post
python -m generate --daemon # run forever (Ctrl+C to stop)
python -m generate --status # check progress
```

The `--new` command clones a Jekyll template (layouts, CSS, dark/light theme, era pages, person profiles, live search) from the [template branch](https://github.com/aag1091-alt/AI-History-Blog/tree/template) and wires it up for your topic. From there, every `python -m generate` run adds a new post and pushes it live.

---

## What Surprised Me

The self-critique loop was the most interesting part to build. Early versions would occasionally write posts with no dates, or refer to people without naming them, or include made-up Wikipedia URLs. The critique node catches all of that with Pydantic-enforced checks and sends the post back for a rewrite with a specific list of issues. Most posts pass on the first try; the rewrite loop rarely triggers more than once.

The other thing that exceeded my expectations was the image pipeline. Wikimedia Commons has an enormous archive, and the relevance filtering (matching image title keywords against the milestone title) produces surprisingly good results. The NSFW filter — checking filenames, metadata restrictions, and category labels — has never let anything through in my testing.

What started as wanting a casual way to browse AI history turned into something I keep finding new uses for. If you have a topic you've always wanted a proper reference for, this is a pretty fast way to build one.
