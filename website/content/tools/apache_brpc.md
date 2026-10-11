---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.575800'
homepage_url: https://brpc.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache bRPC
repo_url: https://github.com/apache/brpc
status: completed
title: Apache bRPC
---



## Overview

An industrial-grade, high-performance RPC framework built in C++ and used extensively in mission-critical, latency-sensitive distributed services.



## Key Features


- Ultra-high performance with lock-free concurrency (bthread M:N user-space threading).

- Multi-protocol support: Baidu-std, gRPC, HTTP/HTTPS, Redis, Memcached, Thrift.

- Built-in diagnostic web services (bvar, /status, /vars, /rpcz) for live profiling.

- Advanced traffic management: backup requests, circuit breaking, locality routing.




## Use Cases

High-concurrency search engines, ad-serving ranking systems, and real-time AI inference pipelines.



{{< callout title="Getting Started" type="code" >}}
```bash
Clone repository, build via CMake, and implement services using Protocol Buffers and C++.
```
{{< /callout >}}



## Recent Updates

Graduated to Apache Top-Level Project with RDMA network acceleration and gRPC interoperability.



{{< callout title="Did You Know?" type="info" >}}
Apache bRPC is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [gRPC](/tools/grpc/)

- [Apache Thrift](/tools/apache_thrift/)

- [Dubbo](/tools/dubbo/)
