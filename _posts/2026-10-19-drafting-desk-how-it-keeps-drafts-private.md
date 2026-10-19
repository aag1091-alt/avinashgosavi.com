---
layout: post
date: 2026-10-19 08:50:00 -0700
title: "How Drafting Desk Keeps Your Drafts in Your Browser"
permalink: /post/drafting-desk-how-it-keeps-drafts-private/
description: "A walkthrough of Drafting Desk's privacy design: no server or account, posts in localStorage, keys you can keep for one tab only, a strict Content-Security-Policy, and an assistant that only sees the text you ask about."
tags: ["Privacy", "Local-first", "AI tools"]
image: /assets/og/drafting-desk-how-it-keeps-drafts-private.png
---

[Drafting Desk](https://github.com/aag1091-alt/drafting-desk) is one of my side projects: a page for writing blog posts yourself, with notes and research beside the draft and an optional AI "partner" that fixes grammar, points at unclear sentences and asks questions when you're stuck. It never writes the post for you.

A writing tool sees your unfinished thinking, so where that text goes matters. This post walks through how the app handles it, using only what's in the [README](https://github.com/aag1091-alt/drafting-desk#readme) and the source.

## There is no server

Drafting Desk is a static web app: an `index.html`, one stylesheet and a handful of JavaScript modules, with a workflow that publishes it to GitHub Pages. There's no backend, no account and no database. You can run it yourself with any static file server:

```sh
python3 -m http.server 8000
```

That one decision does most of the privacy work. With no server of its own, the app has nowhere to send your drafts even if it wanted to.

## Posts live in localStorage

Everything you write (the draft, notes, saved versions) is stored in your browser's `localStorage`. The top of `js/store.js` says it plainly:

```js
// Everything lives in this browser's localStorage. Nothing is sent anywhere
// except the prompts you choose to send to the model provider you configure.
```

Each post gets a random 12-character id made with `crypto.getRandomValues`, so ids say nothing about the post's title or content. Because browser storage stays on one device, the app gives you **Back up all** (exports every post as JSON) and **Import** to move your writing to another browser.

## API keys: this tab only, unless you say otherwise

To use the assistant you connect a model provider. Where the key goes depends on one checkbox, **Remember keys on this device**:

- **Ticked:** the key is saved in `localStorage` and survives restarts.
- **Unticked:** it goes into `sessionStorage`, which the browser clears when the tab closes.

**Forget all keys** wipes both. For OpenRouter you can skip keys entirely and use **Sign in with OpenRouter**, an OAuth flow with PKCE (the app sends a SHA-256 code challenge, so no client secret is needed in the page). You can revoke that sign-in from your OpenRouter account at any time.

The README is upfront about the limit here: a key in browser storage is readable by anything that runs on the same origin. Its advice is to use a key with a spending limit and to prefer the OpenRouter sign-in.

## A Content-Security-Policy that keeps other code out

Since the key's safety depends on nothing else running on the page, the app loads no third-party scripts, fonts or analytics. A `Content-Security-Policy` meta tag in `index.html` enforces that: scripts and styles may only come from the site itself (`script-src 'self'; style-src 'self'`), forms can't submit anywhere (`form-action 'none'`), and plugins are blocked (`object-src 'none'`).

Network requests (`connect-src`) are allowed to the providers it supports, plus localhost for Ollama. It also allows any `https:` address, because you can point the app at your own OpenAI-compatible server (LM Studio, vLLM, llama.cpp). That's a deliberate trade-off: the policy stops injected scripts, but it doesn't restrict which https server the app's own code may call.

## The assistant only sees what you ask about

When you use the assistant, only the text you ask about is sent, straight from your browser to the provider you chose: OpenRouter, Anthropic, OpenAI, Google Gemini, a local Ollama, or any OpenAI-compatible server. There's no middle server that sees the request. With Ollama on your own machine, the text never leaves it.

The partner reads along and only chimes in when you pause, about paragraphs you've just written or changed. Turn off **Chime in** and it sends nothing until you ask.

## "Never writes it for you" is in the prompts

Privacy is half the design; the other half is keeping the words yours. That rule lives in `js/prompts.js`, which every request starts from. The shared instruction tells the model the writer types the post and it never writes it for them, and to never invent facts, examples, numbers or opinions. The "Ask" prompt adds that if you ask it to write a section, it should explain what the passage needs and ask you a question instead.

Nothing changes in your draft until you click **Use**, and accepted changes go through the browser's normal Undo. The app also keeps a rough count of characters that came from accepted suggestions, so it can show how much of a post is yours.

## Honest caveats

- **Browser storage isn't encryption.** Posts sit in `localStorage` as plain JSON. Anyone with access to your browser profile can read them, and clearing site data deletes them, so back up.
- **Your provider still sees what you send.** Choosing who that is (or running Ollama locally) is up to you.
- **A prompt is a request, not a guarantee.** The instructions steer the model away from writing for you; a model can still ignore them, which is why nothing lands in the draft without your click.

## Related

- [How daylog keeps your diary private](/post/daylog-security-architecture/): another local-first app, with encryption at rest and an on-device search index.
- [VaultMem: encrypted memory for AI agents](/post/vaultmem-encrypted-memory-for-ai-agents/): the same "the platform shouldn't read your text" idea, for agent memory.
- [Building this website with Jekyll and GitHub Pages](/post/building-your-website-with-jekyll-and-github-pages/): the kind of blog Drafting Desk exports to, with Jekyll front matter.
