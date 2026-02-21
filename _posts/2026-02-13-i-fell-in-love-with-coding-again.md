---
layout: post
title: "I Fell in Love with Coding Again"
permalink: /post/i-fell-in-love-with-coding-again/
read_time: 3
---

I didn't expect to say this, but I fell in love with coding again.

For a while I heard "the fun is gone" from a lot of people. I hear that argument — with LLMs doing the heavy lifting, the process can feel less tactile and more like directing than building. But lately it feels completely opposite for me. The speed at which I can talk through an idea, validate it quickly by asking Codex CLI, and move from concept to working code has been a reset. Building a full UI in days instead of weeks, and turning designs from Figma into a React codebase, has honestly brought back a lot of joy.

Two examples made this really clear for me.

**1) Triaging a Wrong Alert**

We had an alert that kept firing after a system re‑sync. The root cause turned out to be stale state left behind from an earlier lifecycle step. The first pass through logs and code didn't reveal that. I asked the LLM where the alert is triggered, then narrowed it with follow‑ups: "What data drives this alert?" and "Where else could that state be cached or persisted?"

That pointed me to an initial fix (cleanup at the source). But the deeper issue was that the same state was also stored elsewhere. With more focused questions, the LLM helped me track those paths and add the cleanup there too.

*Takeaway: the coding was easy; the hard part was asking the right questions. LLMs don't fully understand large, customized systems. They can loop or miss hidden state. Your system knowledge and how you frame the next question is still the key.*

**2) Rebuilding a Legacy UI From Figma**

I plugged Figma MCP into Codex CLI and asked it to build a modernized UI. With broad instructions, it "worked," but it missed a lot of visual and interaction details. I tried to patch it piecemeal and it wasn't great. I reset and changed my approach.

I built a mental model of each component and broke the work into steps. I asked it to implement one component at a time, then added hooks and actions for each piece. That was the turning point. The final output was so good I surprised myself. It still took a couple of days, but I never felt stuck. I mostly worked via the CLI and used the IDE to review diffs.

*Takeaway: LLMs work best when you give them a map and clear milestones. Big instructions lead to a rough sketch. Smaller steps with structure lead to quality.*

## What's Changed for Me

I used other tools (and even vibe‑coded a few personal apps) but it didn't feel the same. What brought back the energy was using LLMs for the stuff I used to procrastinate: creating Jira tickets with proper details, writing commit messages, updating branches, automating the repetitive chores. That work now happens faster and more consistently, and I can focus on the actual problem. That makes me happy.

It also doesn't really matter which tool you use — Codex, Claude, or anything else — go with what fits your workflow and what your company can support. I use Codex at work and Cursor for personal projects.

## A Simple Workflow That Helped Me

1. Know the system and ask precise questions.
2. Break tasks into steps and validate each step.
3. Use automation for the boring, high‑friction parts.

It's not that the fun is gone. For me, it's back — and I'm excited to see where this goes.

*You can read the follow-up on turning that workflow into repeatable [Codex Skills]({% post_url 2026-02-17-codex-skills %}).*
