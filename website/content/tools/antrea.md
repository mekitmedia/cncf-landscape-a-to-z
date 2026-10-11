---
cncf_status: sandbox
date: '2026-10-04T18:37:38.996718'
description: Kubernetes networking based on Open vSwitch
homepage_url: https://antrea.io/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Antrea
repo_url: https://github.com/antrea-io/antrea
status: completed
title: Antrea
---



## Overview

A CNCF Container Network Interface (CNI) plugin based on Open vSwitch (OVS) providing high-performance pod networking and security policies.



## Key Features


- Open vSwitch (OVS) data plane supporting Linux, Windows, and hardware offload.

- Rich network policy enforcement with Antrea Tiering and ClusterNetworkPolicies.

- WireGuard and IPsec pod-to-pod traffic encryption.

- Built-in network observability (traceflow, flow aggregator).




## Use Cases

Enterprise Kubernetes networking across heterogeneous Linux/Windows clusters with encrypted traffic.



{{< callout title="Getting Started" type="code" >}}
```bash
Deploy Antrea on Kubernetes via official manifests: `kubectl apply -f https://github.com/antrea-io/antrea/releases/latest/download/antrea.yml`.
```
{{< /callout >}}



## Recent Updates

Introduced advanced egress gateway enhancements and optimized Cilium service mesh interoperability.



{{< callout title="Did You Know?" type="info" >}}
Antrea is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Calico](/tools/calico/)

- [Cilium](/tools/cilium/)

- [Flannel](/tools/flannel/)
