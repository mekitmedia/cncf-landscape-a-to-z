---
cncf_status: non-cncf
date: '2026-10-28T17:38:40.036200'
homepage_url: https://wasmedge.org/docs/develop/rust/wasinn/openvino
layout: single
letter: W
lifecycle_stage: tech_writing
project_name: WASI NN for OpenVINO
repo_url: https://github.com/WebAssembly/wasi-nn
status: completed
title: WASI NN for OpenVINO
---



## Overview

WASI NN for OpenVINO provides a WASI API for performing machine learning inference from WebAssembly using the OpenVINO backend.



## Key Features


- Provides an easy-to-use API for performing ML inference from WebAssembly using existing models.

- Designed to be framework- and model-agnostic, supporting multiple ML frameworks and model formats.

- Enables execution of machine learning models with hardware acceleration for maximum performance.




## Use Cases

Performing AI inference with OpenVINO models in WebAssembly environments, such as road segmentation or image classification.



{{< callout title="Getting Started" type="code" >}}
```bash
Check out the official WasmEdge documentation and the wasi-nn bindings repository to use WASI NN for OpenVINO.
```
{{< /callout >}}



## Recent Updates

wasi-nn is currently in Phase 2 and is advancing towards Phase 4, which requires at least two complete independent implementations.



{{< callout title="Did You Know?" type="info" >}}
WASI NN does not support training models in the near term because its primary focus is ML inference, which has clear performance advantages over training models natively.
{{< /callout >}}
