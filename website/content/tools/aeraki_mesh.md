---
cncf_status: sandbox
date: '2026-10-04T18:37:39.544435'
description: Aeraki Mesh allows you to manage any layer-7 traffic in a service mesh
homepage_url: https://www.aeraki.net/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Aeraki Mesh
repo_url: https://github.com/aeraki-mesh/aeraki
status: completed
title: Aeraki Mesh
---



## Overview

A CNCF sandbox project providing a non-intrusive, extendable way to manage any layer-7 traffic in a service mesh, extending beyond HTTP/gRPC.



## Key Features


- Extends Istio to support various layer-7 protocols like Dubbo, Thrift, Kafka, Redis.

- Uses MetaProtocol Proxy for unified traffic management.

- Dynamic route updates through Aeraki MetaRDS.

- Provides request-level metrics, distributed tracing, and access logs for all supported protocols.

- Supports advanced traffic management like load balancing, circuit breaking, traffic splitting, and rate limiting.




## Use Cases

Ideal for microservices architectures that use a mix of protocols (RPC, messaging, caching, databases) and need a unified service mesh to manage all of them, rather than just HTTP traffic.



{{< callout title="Getting Started" type="code" >}}
```bash
Visit the Aeraki Mesh quickstart guide on aeraki.net to deploy it alongside an Istio installation, or install it via Helm.
```
{{< /callout >}}



## Recent Updates

Aeraki Mesh continues to expand its protocol support and improve integration with Envoy and Istio. It allows users to write custom codecs to support proprietary layer-7 protocols.



{{< callout title="Did You Know?" type="info" >}}
Aeraki (Air-rah-ki) is the Greek word for 'breeze'. It avoids reinventing the wheel by letting existing tools handle HTTP while it manages other layer-7 protocols.
{{< /callout >}}



## Related Tools


- [Istio](/tools/istio/)

- [Envoy](/tools/envoy/)

- [Linkerd](/tools/linkerd/)
