---
layout: post
date: 2026-11-22 12:00:00 -0800
title: "Building a purpose-built small model: the prework"
permalink: /post/building-a-purpose-built-small-model-the-prework/
description: "The prework for building a small, open-source model that turns plain-English intent into network configs: where the data comes from, how small the model can be, what training actually costs, and what publishing a model really involves."
tags: ["AI", "Networking", "Open source"]
image: /assets/og/building-a-purpose-built-small-model-the-prework.png
---

## Why build a small model at all

I'm building a small, open-source model that does one thing: turn a plain-English request ("add VLAN 20 on these three switches and trunk it to the core") into a correct network configuration. It starts with Cisco, and grows to other vendors later.

A big chat model can already do a rough version of this. So why bother?

- **It runs locally.** A small model can live on a box in the closet. No config ever leaves the building.
- **It can be checked.** A model trained for one narrow job can be tested properly, config by config, in a way a general chat model can't.
- **It teaches me how training works.** Most engineers I know (me included, until recently) treat training a model as a dark art. It isn't, and I want to show that by doing it in the open.

This post is the homework I did before writing any training code. Four questions: where does the data come from, how small can the model be, what does training cost, and what does publishing a model actually involve?

## The plan, in one picture

{% include diagrams/netconfig-slm-training.html %}

The short version: draft a config for a request, run it in a simulator, and log what happens. Keep the ones that work, drop the rest — that log becomes the dataset. Then fine-tune a small open model on it, test it in the same simulator on requests it has never seen, and publish it. Then do the same with even smaller models, to find out where quality falls off.

## Where the data comes from

First, the hard truth: there is no big public collection of real network configs to train on. Network engineers don't share configs, because configs leak passwords, SNMP strings, and the shape of the network. So the dataset can't be found. It has to be made.

There are two ways to make it:

1. **Take examples from Cisco's own config guides.** These are public, correct, and complete. One paper closest to this project, [Network Self-Configuration based on Fine-Tuned Small Language Models](https://arxiv.org/abs/2512.02861), built about 10,000 request → config pairs exactly this way.
2. **Generate extra examples with a bigger model** — but only keep the ones that pass the checks below.

The checks go from cheap to expensive:

1. **Parse it.** A tool called [ciscoconfparse2](http://www.pennington.net/py/ciscoconfparse2/) reads the config. If it can't, the syntax is wrong.
2. **Test what it means.** [Batfish](https://github.com/batfish/batfish) checks the config would actually work — for example, that two routers would really form a BGP session.
3. **Boot it.** Run the config in an emulator such as [containerlab](https://containerlab.dev/manual/kinds/) and see if the device comes up.

Anything that fails is thrown out. The model only ever learns from configs that work.

How many examples do I need? Fewer than I expected. The [LIMA](https://oumi.ai/blog/small-data-is-all-you-need) result showed 1,000 carefully chosen examples beating 52,000 sloppy ones. My target is about **5,000 checked pairs**, covering everyday jobs: VLANs, trunks, SVIs, static routes, and basic OSPF and BGP. On the request side I'll use OpenConfig YANG, a vendor-neutral format, so the same dataset can grow to other vendors later.

## How small can the model be?

One thing to clear up first: nobody trains a model from scratch at this scale. That takes a data center — one small from-scratch model (TinyLlama, 1.1B) needed 16 high-end GPUs running for 90 days. "Training" here means **fine-tuning**: start with an open model that already knows English and code, and teach it this one job.

My shortlist is the Qwen3 family, because its license (Apache 2.0) lets me share the result freely. All of them are small enough to run on a laptop:

| Model | Download size (Q4) |
| --- | --- |
| Qwen3-0.6B | 523 MB |
| Qwen3-1.7B | 1.4 GB |
| Qwen3-4B | 2.6 GB |

Why I think small can work: a network config is mostly grammar — fixed commands, in a fixed order, with a few values filled in. That's the easiest kind of thing for a small model to learn, and [one study](https://arxiv.org/html/2501.19085v1) found fine-tuning helped most at exactly this size, around 1B.

The honest answer to "how small is too small" is that nobody has published that number for network configs. So I'll start at 4B, then try 1.7B and 0.6B, and watch where it breaks.

## What training costs

This surprised me most: **about $3.**

The trick is a method called QLoRA. Instead of retraining the whole model, you freeze it and train a small add-on next to it. That fits on one gaming GPU, so the whole run is a few hours on a rented card:

| Run | Hardware | Time | Cost |
| --- | --- | --- | --- |
| Fine-tune Qwen3-4B | Rented RTX 4090 | 2–4 hours | ~$2–3 |
| Same run, on my Mac | M-series, owned | 8–10 hours | Electricity |

The GPU bill is a rounding error. The real cost is time: building the dataset, and running the checks and tests around each training run.

## What "publishing" means

It's simpler than it sounds. A published model is a page on [Hugging Face](https://huggingface.co/docs/hub/model-cards) with the model files, the license, and a short README — the "model card" — that shows my test scores. Two extra steps make it easy for anyone to run: merge the fine-tuned add-on back into the model, and shrink it into a format called GGUF, so it runs with one [Ollama](https://huggingface.co/docs/hub/ollama) command.

Before I publish anything, I want three numbers on that card:

- How often the model's config **parses**
- How often it **actually works** (the Batfish and emulator checks)
- A general sanity check that fine-tuning didn't damage the model's basic abilities

The dataset and the training scripts get published too, so anyone can repeat the run for the same $3.

## So, the plan

Writing this down changed how I see the project. The hard part is not the model. It's the dataset, and the checker that can say, cheaply and automatically, "this config is correct." Build that, and the model almost follows on its own.

First milestone: a few thousand checked request → config pairs for everyday Cisco tasks. Then the Qwen3-4B fine-tune. Then the step down to 1.7B and 0.6B. I'll write up each step here as I go, including the parts that don't work.
