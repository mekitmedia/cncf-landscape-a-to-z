---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.559833'
homepage_url: https://thrift.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache Thrift
repo_url: https://github.com/apache/thrift
status: completed
title: Apache Thrift
---



## Overview

A lightweight, cross-language remote procedure call (RPC) framework with a powerful code generation engine for building scalable distributed services.



## Key Features


- Interface Definition Language (IDL) defining types and services in `.thrift` files.

- Code generation across dozens of languages (C++, Java, Python, Go, Rust, Ruby, C#).

- Multiple serialization protocols (Binary, Compact, JSON) and transport layers.

- Efficient binary serialization minimizing network payload.




## Use Cases

Inter-service communication across polyglot microservice fleets and backend data interchange.



{{< callout title="Getting Started" type="code" >}}
```bash
Define `.thrift` file, generate code via `thrift --gen py service.thrift`, and implement handlers.
```
{{< /callout >}}



## Recent Updates

Broad cross-language compiler updates, async runtime bindings, and security hardening.



{{< callout title="Did You Know?" type="info" >}}
Apache Thrift is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [gRPC](/tools/grpc/)

- [Protocol Buffers](/tools/protocol_buffers/)

- [Cap'n Proto](/tools/cap'n_proto/)
