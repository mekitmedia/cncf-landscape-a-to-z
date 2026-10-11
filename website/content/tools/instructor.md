---
cncf_status: non-cncf
date: '2026-10-07T03:00:30.491619'
description: structured outputs for llms
homepage_url: https://python.useinstructor.com/
layout: single
letter: I
lifecycle_stage: first_pass
project_name: Instructor
repo_url: https://github.com/567-labs/instructor
status: completed
title: Instructor
---



## Overview

Instructor is a library for structured extraction, getting reliable JSON from any LLM, built on Pydantic for validation, type safety, and IDE support.



## Key Features


- Provides automatic validation, retries, streaming, and nested object support without manual schema writing.

- Works with every major provider including OpenAI, Anthropic, Google, and local models like Ollama using the same API.

- Stream partial objects as they're generated.

- Automatically retries failed validations with the error message.




## Use Cases

Extract complex, nested data structures from natural language with automatic validation and retries, streamlining structured data extraction.



{{< callout title="Getting Started" type="code" >}}
```bash
Install Instructor via pip `pip install instructor`, define a Pydantic model for your data, and use `instructor.from_provider()` to extract structured data from any LLM.
```
{{< /callout >}}



## Recent Updates

The most recent tag is v1.17.0.



{{< callout title="Did You Know?" type="info" >}}
Instructor is trusted by over 100,000 developers, has over 3 million monthly downloads, and is used by teams at OpenAI, Google, Microsoft, and AWS.
{{< /callout >}}



## Related Tools


- [LangChain](/tools/langchain/)

- [LlamaIndex](/tools/llamaindex/)

- [PydanticAI](/tools/pydanticai/)
