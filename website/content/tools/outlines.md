---
cncf_status: non-cncf
date: '2026-10-24T02:28:30.214480'
description: Structured Outputs
homepage_url: https://dottxt-ai.github.io/outlines/
layout: single
letter: O
lifecycle_stage: tech_writing
project_name: Outlines
repo_url: https://github.com/dottxt-ai/outlines
status: completed
title: Outlines
---



## Overview

Outlines is a library that provides guaranteed structured generation directly from large language models, mitigating parsing errors.



## Key Features


- Works with any model - Same code runs across OpenAI, Ollama, vLLM, and more

- Simple integration - Just pass your desired output type: `model(prompt, output_type)`

- Guaranteed valid structure - No more parsing headaches or broken JSON

- Provider independence - Switch models without changing code




## Use Cases

Customer support triage, e-commerce product categorization, parsing event details with incomplete data, categorizing documents into predefined types, and dynamically generating prompts.



{{< callout title="Getting Started" type="code" >}}
```bash
Getting started with outlines is simple:

pip install outlines
```
{{< /callout >}}



## Recent Updates

Added support for PEP 604 unions (`int | str`) as output types. Fixed handling of nullable object type in additionalProperties pass. Fixed rejecting negative counts.



{{< callout title="Did You Know?" type="info" >}}
Outlines provides structured outputs for LLMs and is trusted by NVIDIA, Cohere, HuggingFace, vLLM.
{{< /callout >}}



## Related Tools


- [OpenAI](/tools/openai/)

- [Ollama](/tools/ollama/)
