---
layout: post
title: "Doing the Right Thing, Fast"
permalink: /post/doing-the-right-thing-fast/
read_time: 3
---

We recently deprecated the initial version of Cisco Catalyst Cloud Monitoring. That means the code that drove it — onboarding flows, device-specific paths, integrations that only existed for those devices — needed to go.

In the old world, this kind of cleanup almost never happens on schedule. It's not that people don't want to do it. It's that the cost is high: you're touching interconnected parts, there's real risk of breaking something unrelated, and the work has to fit around ongoing feature development. So it gets triaged below the line. Unused code paths don't disappear — they just quietly accumulate. Every engineer knows the feeling of working around code that should have been deleted six months ago.

This time was different.

## What We Actually Did

I split the cleanup into 20-25 focused work streams. A few people helped with specific areas, but most of it was mine. Over two weeks, every stream went through the same cycle: identify what to remove, make the change, review it carefully, test, and move on.

The Meraki developer tools team's **jira-to-PR skill** made the pipeline from ticket to code review almost frictionless. I wasn't fighting process — I was just doing the work.

That work is now fully deployed to production. No errors. The legacy load is gone.

## Where Codex Fit In

Codex handled the mechanical side of each stream — finding the right call sites, generating the deletions, updating the ripple effects across the codebase. I've been here since inception, so I know this code well. That matters. A new person would have needed more time to build the mental model before they could trust what was being removed. My 4.5 years gave me the confidence to move fast without second-guessing.

The way I verify is consistent: I do all my visual inspection in VS Code, diff by diff. When I wasn't sure what Codex had generated, I asked it to explain the change in plain terms. That became a reliable part of my review loop — not a crutch, just a check.

*Takeaway: experience and AI compound. The codebase knowledge lets you set the right scope. Codex handles the execution. The combination is what made 2 weeks possible instead of 2 quarters.*

## The Shift I Keep Coming Back To

What I used to put off, I now just do.

Not because the work got trivial — the cleanup was real work, done the right way, with proper reviews and manual testing. But the overhead that used to make it not worth starting has collapsed. The cost of doing the right thing is now low enough that "we'll do it properly later" is no longer the default answer.

That's the shift. You can do the right thing *and* do it fast. Not by cutting corners, but because the slow parts — finding call sites, writing boilerplate, generating consistent changes across files — aren't slow anymore.

I'm writing less code than I used to. But I'm seeing more of my intentions land exactly as I wanted them to. That's a trade I'll take every time.

I'm genuinely excited to see where this goes next.

---

*Read about how I approach repeatable workflows in Codex: [Codex Skills: Baking Your Workflow Into the Tool]({% post_url 2026-02-17-codex-skills %})*
