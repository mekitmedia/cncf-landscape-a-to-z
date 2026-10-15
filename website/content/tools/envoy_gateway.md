---
cncf_status: non-cncf
date: '2026-10-15T15:58:09.885478'
description: Part of the Envoy project, Envoy Gateway is the control plane for dynamically
  managing Envoy Proxy, aimed at significantly decreasing the barrier to entry when
  using it for Gateway (sometimes known as "north-south") use cases.
homepage_url: https://gateway.envoyproxy.io
layout: single
letter: E
lifecycle_stage: first_pass
project_name: Envoy Gateway
repo_url: https://github.com/envoyproxy/gateway
status: completed
title: Envoy Gateway
---



## Overview

Envoy Gateway is an open source project for managing Envoy Proxy as a standalone or Kubernetes-based application gateway. It utilizes Gateway API resources to dynamically provision and configure managed Envoy Proxies.



## Key Features


- Manages Envoy Proxy as a standalone or Kubernetes-based application gateway

- Uses Gateway API resources to dynamically provision and configure managed Envoy Proxies

- Supports HTTP Routing, Traffic Splitting, Secure Gateways, Global Rate Limit, and gRPC Routing




## Use Cases

Providing an open source application gateway using Envoy Proxy with dynamic configuration via the Kubernetes Gateway API.



{{< callout title="Getting Started" type="code" >}}
```bash
To clean up the quickstart, you can run 'helm uninstall eg -n envoy-gateway-system'.
```
{{< /callout >}}



## Recent Updates

The project recently published the v1.9.2 release.



{{< callout title="Did You Know?" type="info" >}}
The quickstart configures the gateway using Kubernetes Gateway API resources Gateway and HTTPRoute to direct incoming requests over HTTP to the backend service.
{{< /callout >}}



## Related Tools


- [Envoy Proxy](/tools/envoy_proxy/)

- [Kubernetes Gateway API](/tools/kubernetes_gateway_api/)
