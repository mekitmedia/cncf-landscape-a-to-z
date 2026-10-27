---
cncf_status: sandbox
date: '2026-10-26T02:00:23.763885'
description: An Envoy-powered, Kubernetes-native API Gateway that integrates Kubernetes
  Gateway API with a control plane for API connectivity in any cloud environment.
homepage_url: https://kgateway.dev/
layout: single
letter: K
lifecycle_stage: first_pass
project_name: Kgateway
repo_url: https://github.com/kgateway-dev/kgateway
status: completed
title: Kgateway
---



## Overview

Kgateway is the most mature and widely deployed gateway in the market today. Built on open source and open standards, kgateway is a resilient and performance-oriented control plane that implements the Kubernetes Gateway API for Envoy.



## Key Features


- Powered by Envoy and programmed with the Gateway API, kgateway is a world-leading Cloud Native API Gateway.

- With a control plane that scales from lightweight microgateway deployments between services to massively parallel centralized gateways handling billions of API calls, kgateway brings omni-directional API connectivity to any cloud and any environment.

- Route to backends implemented as microservices, serverless functions or legacy apps. Gradually migrate from legacy code while maintaining existing systems.

- Multiple personas and teams can work with kgateway to express their APIs, with concepts like route delegation and composable policies.




## Use Cases

Next-Gen API Gateway, Hybrid Application Migration, Complex Tenancy Environments



{{< callout title="Getting Started" type="code" >}}
```bash
Try installing this release:
helm install kgateway-crds oci://cr.kgateway.dev/kgateway-dev/charts/kgateway-crds --version v2.4.7 --namespace kgateway-system --create-namespace
helm install kgateway oci://cr.kgateway.dev/kgateway-dev/charts/kgateway --version v2.4.7 --namespace kgateway-system --create-namespace

```
{{< /callout >}}



## Recent Updates

v2.4.7 Release Notes: Fixed PreferNetwork and other network-aware traffic distribution splitting traffic across networks when the gateway or backend pods have no topology.istio.io/network label. Bump envoy to v1.38.7.



{{< callout title="Did You Know?" type="info" >}}
The project was launched in 2018 as Gloo by Solo.io and has been production-ready since 2019.
{{< /callout >}}



## Related Tools


- [Envoy](/tools/envoy/)

- [Kubernetes](/tools/kubernetes/)
