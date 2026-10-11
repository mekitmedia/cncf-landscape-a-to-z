---
cncf_status: non-cncf
date: '2026-10-04T18:37:45.931505'
description: Triton is a language and compiler for parallel programming.
homepage_url: https://triton-lang.org/
layout: single
letter: T
lifecycle_stage: tech_writing
project_name: Triton
repo_url: https://github.com/triton-lang/triton
status: completed
title: Triton
---



## Overview

Triton is a language and compiler for writing highly efficient custom Deep-Learning primitives. It aims to provide an open-source environment for writing fast code at higher productivity than CUDA, but with higher flexibility than other existing DSLs.



## Key Features


- High Productivity: Provides an environment to write fast code more productively than CUDA.

- High Flexibility: Offers greater flexibility compared to other domain-specific languages (DSLs) for deep learning.

- MLIR-based Backend: Features a compiler backend rewritten to use MLIR.

- Back-to-back Matmuls: Supports kernels that contain back-to-back matmuls, enabling operations like flash attention.




## Use Cases

Writing highly efficient custom Deep-Learning primitives and optimizing deep learning workloads, such as flash attention and complex matmul operations.



{{< callout title="Getting Started" type="code" >}}
```bash
Check out the official documentation at https://triton-lang.org/ for installation instructions and tutorials, or explore the Triton puzzles to practice running the Triton interpreter without a GPU.
```
{{< /callout >}}



## Recent Updates

Version 3.8.0 includes Proton profiling improvements like CUDA graph profiling, new examples and tutorials, low-precision matmul additions, storage shape queries, performance improvements, standalone CUDA backend (can run without PyTorch), and various bug fixes.



{{< callout title="Did You Know?" type="info" >}}
Triton's foundations were described in a MAPL 2019 publication: 'Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations'.
{{< /callout >}}



## Related Tools


- [CUDA](/tools/cuda/)

- [PyTorch](/tools/pytorch/)
