---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.919660'
homepage_url: https://github.com/GoogleChromeLabs/asyncify
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Asyncify
repo_url: https://github.com/GoogleChromeLabs/asyncify
status: completed
title: Asyncify
---



## Overview

A JavaScript wrapper intended to be used with the Asyncify feature of Binaryen. Together, they allow the use of asynchronous APIs (such as most Web APIs) from within WebAssembly written and compiled from any source language.



## Key Features


- JavaScript wrapper for Binaryen's Asyncify feature.

- Enables using asynchronous APIs (like most Web APIs) within WebAssembly.

- Supports drop-in replacement APIs for the regular WebAssembly interface with added async support.

- Wraps WebAssembly exports into async functions.




## Use Cases

Bridging asynchronous JavaScript and Web APIs with synchronous WebAssembly code, particularly when porting existing native C/C++ or Rust applications that make synchronous network requests or blocking operations to the web.



{{< callout title="Getting Started" type="code" >}}
```bash
Compile your code to WebAssembly, post-process it using `wasm-opt --asyncify`, and instantiate it in JavaScript using `Asyncify.instantiateStreaming` from `https://unpkg.com/asyncify-wasm?module`.
```
{{< /callout >}}



## Recent Updates

The repository was archived by the owner on Jul 8, 2024. It is now read-only.



{{< callout title="Did You Know?" type="info" >}}
Asyncify operates by transforming WebAssembly code post-compilation using `wasm-opt` from the Binaryen toolchain, enabling it to pause and resume execution.
{{< /callout >}}



## Related Tools


- [Binaryen](/tools/binaryen/)

- [WebAssembly](/tools/webassembly/)

- [wasm-opt](/tools/wasm-opt/)
