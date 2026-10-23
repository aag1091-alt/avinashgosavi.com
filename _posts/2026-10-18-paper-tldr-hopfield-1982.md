---
layout: post
date: 2026-10-18 15:00:00 -0700
title: "Paper TL;DR: Hopfield (1982) — Memory as a Valley You Roll Into"
permalink: /post/paper-tldr-hopfield-1982/
description: "A TL;DR of John Hopfield's 1982 paper on associative memory: energy landscapes, Hebbian storage, recall from partial cues and its limits — with a NumPy demo."
series: paper-tldr
series_order: 7
tags: ["Research", "Agent memory"]
read_time: 5
image: /assets/og/paper-tldr-hopfield-1982.png
---

**Paper:** J. J. Hopfield, [*Neural networks and physical systems with emergent collective computational abilities*](https://www.pnas.org/doi/10.1073/pnas.79.8.2554), PNAS 79(8), 1982

**One-line TL;DR:** connect lots of simple on/off neurons with symmetric weights and the network gets an energy that only goes down as it runs — so stored memories become stable valleys, and a partial or noisy cue rolls downhill into the full memory.

Almost everything I've built around memory started here. It's also one of the most readable classic papers I know: five pages, very little math, a physicist explaining computation.

## The setup

- **Neurons** are either on or off (+1 or −1).
- **Every neuron connects to every other**, and the connection strengths are **symmetric**: the weight from A to B equals the weight from B to A.
- **Storing a memory** uses a Hebbian rule — "neurons that fire together wire together." For each pattern you want to remember, strengthen connections between neurons that agree and weaken those between neurons that disagree. Store several patterns by adding up their contributions.
- **Recalling** means picking neurons one at a time and flipping each to agree with the weighted vote of its neighbors, until nothing changes.

## The key insight: an energy that only goes down

Hopfield's move was to define an **energy** for the whole network's state and show that, with symmetric weights and one-at-a-time updates, every update either lowers the energy or leaves it unchanged. The network can't cycle forever; it has to settle.

Stored patterns sit at the bottoms of valleys in that energy landscape. Start anywhere nearby — a corrupted photo, half a phone number — and the network slides down into the nearest stored memory. That's **content-addressable memory**: you retrieve by *what* you remember, not by *where* it's stored. It's also robust: knock out some neurons or connections and recall still mostly works.

{% include diagrams/hopfield-store-recall.html %}

## Twenty-five lines of NumPy

Store five random patterns in 100 neurons, flip 30% of the bits of one, and let it settle:

```python
import numpy as np

rng = np.random.default_rng(1)
N, P = 100, 5
patterns = rng.choice([-1, 1], size=(P, N))
W = (patterns.T @ patterns) / N        # Hebbian storage
np.fill_diagonal(W, 0)                 # no self-connections

def energy(s):
    return -0.5 * s @ W @ s

def recall(s, sweeps=5):
    s = s.copy()
    for _ in range(sweeps):
        for i in rng.permutation(N):   # one neuron at a time
            s[i] = 1 if W[i] @ s >= 0 else -1
    return s

target = patterns[0]
noisy = target.copy()
noisy[rng.choice(N, 30, replace=False)] *= -1

out = recall(noisy)
print((noisy == target).mean(), (out == target).mean())   # 0.7 -> 1.0
print(round(energy(noisy), 1), round(energy(out), 1))     # -8.6 -> -50.5
```

70% correct goes to 100% correct, and the energy drops as it does.

## The limits

- **Capacity is small.** Hopfield found the network reliably holds only about **0.15 memories per neuron**. Push past that and recall falls apart.
- **Spurious memories.** The landscape also grows valleys nobody stored — blends of real memories — and a cue can get stuck in one.
- **Similar memories interfere.** Patterns that overlap a lot blur into each other.

Those limits are exactly what the 2020 follow-up fixes: [modern Hopfield networks](/post/paper-tldr-hopfield-networks-is-all-you-need/) sharpen the valleys so capacity grows exponentially — and their update turns out to be transformer attention.

## Why it still matters to me

Databases retrieve by key. Vector stores retrieve by nearest neighbor. Hopfield networks retrieve by **settling** — pattern completion from a partial cue, which is much closer to how remembering feels. That idea is the reason [Attractor](/post/attractor-memory-engine/) is called Attractor.

That completes the six papers from [Part 1](/post/paper-tldr-six-papers-on-memory/). The whole list, with short TL;DRs, lives on my [papershelf](/research/#papershelf). The series keeps going with [MemGPT](/post/paper-tldr-memgpt/), which treats an LLM's context window like an operating system's memory.

For a one-paragraph definition of [*associative (content-addressable) memory*](/post/agent-memory-glossary/#associative-memory), see the [agent memory glossary](/post/agent-memory-glossary/).
