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

I'm building a small, open-source model that does one thing: turn a plain-English intent ("add VLAN 20 on these three switches and trunk it to the core") into a correct device configuration, starting with Cisco and expanding to other vendors through a vendor-neutral schema (OpenConfig YANG). A frontier model can already do a passable version of this, so why bother?

Three reasons. A small model runs on the box in the closet, with no config leaving the building. It can be made deterministic and auditable in a way a general chat model can't. And, frankly, I want to demystify what training a model actually involves, because most engineers I know (me included, until recently) treat it as a dark art.

Before writing a line of training code I wanted answers to four questions, and this post is my working notes on them: where does the data come from, how small can the model be and still be worth publishing, what does training actually cost in hardware and dollars, and what does "publishing a model" even mean mechanically. Nothing here is from a position of authority. It's a software engineer reading the manuals before touching the equipment.

## Where the data comes from

The uncomfortable truth first: there is no good public corpus of real network configs. Real configs are the one thing network engineers never share, because they leak topology, credentials and SNMP strings ([MITRE lists config dumps as a collection technique](https://attack.mitre.org/techniques/T1602/002/)). When someone asked NANOG for a big scrubbed dump in 2022, the [only concrete answer](https://lists.nanog.org/archives/list/test@lists.nanog.org/thread/JT5MQ4CVDSL777DL6CSQW7LPEEO6BUOR) was Vincent Bernat's generated Jerikan configs. Hugging Face has one 750-row Cisco command dataset. GitHub has configs, but most sit in unlicensed repos, which [GitHub's terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) say you can view and fork, not redistribute as a dataset.

So the dataset has to be made, not found. The recipe that keeps showing up in the literature is to mine the vendor documentation. The paper closest to what I want, [Network Self-Configuration based on Fine-Tuned Small Language Models](https://arxiv.org/abs/2512.02861), built about 10,000 intent→config pairs by extracting examples from Cisco IOS XE configuration-guide PDFs and using an LLM to write the matching requirement for each one. Command references and config guides are the one place where correct, complete, licensed-for-reading configs exist in bulk, and every vendor publishes them.

The second source is synthetic data from a stronger model, which is only safe with a validator in the loop. The validation ladder I'm planning is cheap to expensive: parse with [ciscoconfparse2](http://www.pennington.net/py/ciscoconfparse2/) for syntax, run [Batfish](https://github.com/batfish/batfish) (Apache 2.0, supports Cisco, Juniper, Arista and more) for semantic checks like "does this actually form a BGP session", then boot the config in an emulator such as [containerlab](https://containerlab.dev/manual/kinds/) or Cisco Modeling Labs. [NetConfArena](https://arxiv.org/html/2608.23179) does exactly this at scale: 96 task templates expanded to 480 tasks, validated in GNS3 emulation. Anything that fails validation gets thrown out, so the model only ever sees configs that work.

How much do you need? Less than I assumed. [LIMA](https://oumi.ai/blog/small-data-is-all-you-need) showed 1,000 well-curated examples beating 52,000 sloppy ones, and the [LIMIT](https://arxiv.org/abs/2311.13133) follow-up puts the useful range at 1,000 to 6,000. For a domain this syntax-heavy, a practitioner [estimate](https://www.jaredwatkins.com/research/local-llm-finetuning/training-data/network-engineering-data/) of 10,000 to 19,000 examples across config generation, command translation and troubleshooting feels right. My plan: start with the config-generation slice only, around 5,000 validated pairs, with OpenConfig YANG as the intent format on the input side so the same dataset can grow to other vendors later.

## How small can it be

First, a vocabulary correction I needed: nobody at hobby scale trains a model from scratch. Qwen3 was pretrained on 36 trillion tokens; [TinyLlama](https://github.com/jzhang38/TinyLlama), a 1.1B model, took 16 A100s for 90 days. "Training a small model" in practice means taking an open-weight base model that already knows English and code, and fine-tuning it on your domain. The question is which base, and how small.

The candidates with a clean license and a base (not instruct-tuned) checkpoint are few. These are the ones I'm choosing between:

| Model | Params | Context | License |
| --- | --- | --- | --- |
| [Gemma 3 270M](https://huggingface.co/google/gemma-3-270m) | 0.27B | 32K | Gemma Terms |
| [Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | 0.6B | 32K | Apache 2.0 |
| [Qwen3-1.7B-Base](https://huggingface.co/Qwen/Qwen3-1.7B-Base) | 1.7B | 32K | Apache 2.0 |
| [SmolLM3-3B-Base](https://huggingface.co/HuggingFaceTB/SmolLM3-3B-Base) | 3B | 64K | Apache 2.0 |
| [Qwen3-4B-Base](https://huggingface.co/Qwen/Qwen3-4B-Base) | 4B | 32K | Apache 2.0 |
| [Gemma 4 E4B](https://huggingface.co/google/gemma-4-E4B) | 4.5B effective (8B on disk) | 128K | Apache 2.0 |

The evidence on "smallest useful size" for structured generation is encouraging but thin. The networking paper above fine-tuned a 7B model and got 57% fully syntactically correct configs plus 38% partially correct, against 42% and 12% for a general LLM, which is a real win but not yet a product. For code-adjacent DSLs, [one study](https://arxiv.org/html/2501.19085v1) found fine-tuning helped most at 1B (Racket pass rate 7% to 18%) and actually hurt at 33B, because small models can't follow complex prompts but can absorb a grammar. Another [fine-tuned a 7B coder on 1,500 examples](https://arxiv.org/pdf/2507.10182) and matched GPT-4o on spec generation. Google explicitly pitches the [270M Gemma](https://developers.googleblog.com/en/introducing-gemma-3-270m/) for "unstructured to structured text" fine-tunes.

My read: a config is a grammar, not a reasoning problem, which is the best case for a small model. The honest answer to "smallest model before publishing" is "the smallest one that passes my validation suite", and nobody has published that number for IOS configs. So the plan is to replicate the 7B paper's recipe at 4B, then step down to 1.7B and 0.6B and watch where accuracy falls off a cliff. Memory-wise all of these are trivial to run: at Q4 quantization Qwen3-4B is a [2.6 GB download](https://ollama.com/library/qwen3/tags) and the 0.6B is 523 MB, so the whole range fits on a laptop or an access point-class box.

## What training actually costs

This was the biggest surprise of the prework. I had a mental model of training as "rent a rack of H100s". For fine-tuning a model under 8B, the cost is closer to a lunch.

The trick is LoRA. Instead of updating all the weights, you freeze the base model and train a pair of small low-rank matrices beside each layer ([Hugging Face PEFT](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora)), which cuts trainable parameters by orders of magnitude. QLoRA goes further and keeps the frozen base in 4-bit. [Unsloth's requirements page](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md) puts QLoRA on a 3B model at 3.5 GB of VRAM and an 8B at 6 GB; a full fine-tune of an 8B wants [60 to 100 GB](https://jarvislabs.ai/ai-faqs/best-gpu-for-fine-tuning-llms). A 4B QLoRA run fits on a gaming GPU with room to spare.

On rented hardware, as of early October 2026 [RunPod](https://www.runpod.io/pricing) lists an RTX 4090 at $0.74/hr, an A100 80GB at $1.59/hr and an H100 at $2.89 to $3.49/hr; [Lambda](https://lambda.ai/pricing) is $2.79 for the A100 and $3.99 for the H100. One [write-up](https://dev.to/sebuzdugan/how-to-fine-tune-a-7b-model-for-three-dollars-on-one-gpu-2lf2) QLoRA-tuned a 7B model for about $3 in 2 to 4 hours on an A100. Scaling that to my case:

| Run | VRAM | Hardware | Time | Cost |
| --- | --- | --- | --- | --- |
| QLoRA, 4B, \~10k examples, 3 epochs | 4–8 GB | RTX 4090, $0.74/hr | 2–4 h | \~$2–3 |
| QLoRA, 8B, same data | 6–16 GB | A100 80GB, $1.59/hr | 2–4 h | \~$3–6 |
| Full fine-tune, 8B, 1 epoch | 60–100 GB | 1–2× A100/H100 | 3–6 h | \~$10–20 |
| LoRA, 8B, on my Mac via MLX | 32 GB unified | M-series, owned | 8–10 h | electricity |
| Pretrain 1.1B from scratch (TinyLlama) | 16× A100 | 90 days | 35k GPU-h | \~$55k |

The hours column is derived from the throughput numbers in those sources, so treat it as order-of-magnitude. The point survives any fudge factor: the GPU bill is a rounding error. What actually costs money and time is building and validating the dataset, and the many small eval runs you do before the one you publish.

Local hardware works too. Apple's [mlx-lm](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md) does LoRA and QLoRA natively on Apple Silicon, reportedly around 250 tokens/sec for a 7B LoRA on an M1 Max. On the AMD side, ROCm training on a Ryzen AI mini PC is [possible but rough](https://dev.to/ankk98/observations-from-finetuning-gemma-model-on-strix-halo-fedora-43-2cdo), and the Vulkan path that makes inference easy there doesn't cover training. The tooling I'll be using: [Unsloth](https://github.com/unslothai/unsloth) for fast low-VRAM LoRA, [TRL](https://huggingface.co/docs/trl/index)'s SFTTrainer as the plain reference implementation, and mlx-lm for experiments on the Mac.

## What "publishing a model" means

Mechanically, publishing is a git push. A model on the [Hugging Face Hub](https://huggingface.co/docs/huggingface_hub/guides/upload) is a repo containing the weights as `.safetensors` files (pickle checkpoints get [flagged](https://huggingface.co/docs/hub/security-pickle)), the tokenizer, a chat template, and a `README.md` whose YAML header is the [model card](https://huggingface.co/docs/hub/model-cards): `license`, `base_model`, `datasets`, `pipeline_tag`, and a `model-index` block that renders your eval numbers as a widget. Free public storage is best-effort but a few GB is fine, and a 4B model in bf16 is about 8 GB.

The license is mostly decided for you by the base model. Qwen3 is Apache 2.0, so the fine-tune can be Apache 2.0 too with the notice kept. Gemma 3 derivatives must ship the [Gemma Terms](https://open.windriver.com/info/uni-license-list/licenses/gemma-tou-2025-03-24.html), a NOTICE file and its use restrictions, which also applies to models trained on Gemma-generated synthetic data. Llama derivatives must carry "Llama" in the name and "Built with Meta Llama" in the card. That constraint is one reason the Qwen3 base checkpoints are at the top of my list.

Getting the model to where people actually run it takes two more steps. First, merge the LoRA adapter back into a bf16 copy of the base ([merge\_and\_unload](https://huggingface.co/docs/peft/main/en/developer_guides/lora); you can't merge into the 4-bit base you trained against). Second, convert to GGUF with llama.cpp's `convert_hf_to_gguf.py` and [quantize](https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md) to Q4\_K\_M (the balanced default) and Q8\_0 (near-lossless). Upload those to a `-GGUF` repo and anyone can run `ollama run hf.co/you/model-GGUF` with [no further packaging](https://huggingface.co/docs/hub/ollama); a `Modelfile` plus `ollama push` gets it into the Ollama registry as well.

The part that separates a real release from a weights dump is evaluation. Before I publish anything I want three things in the card: a held-out test split the model never saw, a task benchmark that reports validity rate (parses, passes Batfish, boots in emulation) per config category, and a general-ability sanity check via [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) to show the fine-tune didn't lobotomise the base. The dataset gets its own repo with a [dataset card](https://huggingface.co/docs/hub/datasets-cards) in Parquet, and the training config and scripts go in GitHub, linked from the model card, so anyone can reproduce the run for the $3 it costs.

## So, the plan

Writing this down changed the plan. I came in thinking the hard part was compute; it's the dataset and the validator. The model is almost a by-product of having a pipeline that can say, cheaply and automatically, whether a config is correct.

Concretely, the first milestone is a few thousand validated intent→config pairs for everyday Cisco IOS tasks (VLANs, trunks, SVIs, static routes, basic OSPF and BGP), mined from the public config guides and checked by ciscoconfparse2 and Batfish. Then a QLoRA fine-tune of Qwen3-4B-Base on a rented 4090, which should cost less than a coffee, followed by the same run on 1.7B and 0.6B to find the floor. Whatever clears the validation bar ships as safetensors plus GGUF on Hugging Face, with the dataset and scripts beside it. I'll write up each step here as I go, including the parts that don't work.
