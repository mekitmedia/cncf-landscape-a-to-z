---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.951004'
description: Go ahead and axolotl questions
homepage_url: https://github.com/axolotl-ai-cloud/axolotl
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Axolotl
repo_url: https://github.com/axolotl-ai-cloud/axolotl
status: completed
title: Axolotl
---



## Overview

Axolotl is a free and open-source tool designed to streamline post-training and fine-tuning for the latest large language models (LLMs).



## Key Features


- Multiple Model Support: Train various models like GPT-OSS, LLaMA, Mistral, Mixtral, Pythia, and many more models available on the Hugging Face Hub.

- Multimodal Training: Fine-tune vision-language models (VLMs) and audio models.

- Training Methods: Full fine-tuning, LoRA, QLoRA, GPTQ, QAT, FP8 mixed-precision training, NVFP4/MXFP4 MoE LoRA, Preference Tuning, RL, and Reward Modelling.

- Performance Optimizations: Multipacking, Flash Attention 2/3/4, Xformers, Flex Attention, Sequence Parallelism, Multi-GPU and Multi-node training, etc.

- Easy Configuration: Re-use a single YAML configuration file across the full fine-tuning pipeline.




## Use Cases

LLM Post-Training and Fine-Tuning. Developers can quickly fine-tune various state-of-the-art models for specific tasks using LoRA, QLoRA, and other methods with optimized performance and multimodal support.



{{< callout title="Getting Started" type="code" >}}
```bash
```bash
# Fetch axolotl examples
axolotl fetch examples

# Train a model using LoRA
axolotl train examples/llama-3/lora-1b.yml
```

```
{{< /callout >}}



## Recent Updates

Release v0.19.0 was published on September 10, 2026. Axolotl has recently added FP8 mixed precision training via torchao, TiledMLP support for single-GPU to multi-GPU training, Quantization Aware Training (QAT) support, Llama 4 support, and Sequence Parallelism (SP) support.



{{< callout title="Did You Know?" type="info" >}}
Axolotl ships with built-in documentation optimized for AI coding agents (Claude Code, Cursor, Copilot, etc.), bundled directly with the pip package.
{{< /callout >}}



## Related Tools


- [LLaMA](/tools/llama/)

- [Mistral](/tools/mistral/)

- [Mixtral](/tools/mixtral/)

- [DeepSpeed](/tools/deepspeed/)
