---
cncf_status: non-cncf
date: '2026-10-04T18:37:44.832280'
description: Scripting languages that support Wasm
homepage_url: https://github.com/second-state/wasmedge-quickjs
layout: single
letter: W
lifecycle_stage: tech_writing
project_name: WasmEdge-Quickjs
repo_url: https://github.com/second-state/wasmedge-quickjs
status: completed
title: WasmEdge-Quickjs
---



## Overview

WasmEdge-Quickjs is a high-performance, secure, extensible, and OCI-compliant JavaScript runtime designed to run JavaScript in WebAssembly using WasmEdge.



## Key Features


- Provides a standard JavaScript runtime within WebAssembly.

- Optimized for Linux x86_64 with pre-AOT-compiled binaries, but can be AOT compiled for other OS and CPU architectures.

- Includes Node API extensions for enhanced compatibility and functionality.




## Use Cases

Ideal for developers who need to run JavaScript securely within a WebAssembly environment (WasmEdge), enabling cross-platform execution.



{{< callout title="Getting Started" type="code" >}}
```bash
To get started, clone the repository, build the project using Cargo targeting `wasm32-wasi`, and execute your JavaScript files with the WasmEdge runtime.
```
{{< /callout >}}



## Recent Updates

The latest release (v0.6.1-alpha) provides pre-AOT-compiled binaries optimized for Linux x86_64 and node API extensions.



{{< callout title="Did You Know?" type="info" >}}
WebAssembly bytecode files provided in the release can be AOT compiled with `wasmedgec` on a target platform to optimize them for a different OS/CPU.
{{< /callout >}}



## Related Tools


- [WasmEdge](/tools/wasmedge/)

- [WebAssembly](/tools/webassembly/)

- [QuickJS](/tools/quickjs/)
