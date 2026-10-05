---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.589742'
description: Cost-efficient and pluggable Infrastructure components for GenAI inference.
homepage_url: https://aibrix.github.io/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: AIBrix
repo_url: https://github.com/vllm-project/aibrix
status: completed
title: AIBrix
---



## Overview

AIBrix is an open-source, cost-efficient, scalable, and pluggable cloud-native infrastructure for GenAI applications, tailored specifically to enterprise needs for deploying, managing, and scaling large language model (LLM) inference.



## Key Features


- High-Density LoRA Management: Streamlined support for lightweight, low-rank adaptations of models.

- LLM Gateway and Routing: Efficiently manage and direct traffic across multiple models and replicas.

- LLM App-Tailored Autoscaler: Dynamically scale inference resources based on real-time demand.

- Unified AI Runtime: A versatile sidecar enabling metric standardization, model downloading, and management.

- Distributed Inference: Scalable architecture to handle large workloads across multiple nodes.

- Distributed KV Cache: Enables high-capacity, cross-engine KV reuse.

- Cost-efficient Heterogeneous Serving: Enables mixed GPU inference to reduce costs with SLO guarantees.

- GPU Hardware Failure Detection: Proactive detection of GPU hardware issues.




## Use Cases

Optimizing GenAI inference deployment via Kubernetes for cost efficiency and scalability, managing high-density LoRA adaptations, and performing distributed LLM inference.



{{< callout title="Getting Started" type="code" >}}
```bash
Clone the repository and install dependencies and AIBrix CRDs using `kubectl apply -k` or install a stable distribution using provided manifests from the releases page.
```
{{< /callout >}}



## Recent Updates

v0.7.0 was released on June 16, 2026, introducing Management Console, Self-Hosted Batch, KV-Centric Disaggregation, and a Highly-Available Gateway. v0.6.0 was released on March 5, 2026.



{{< callout title="Did You Know?" type="info" >}}
AIBrix co-delivered a keynote at KubeCon North America 2025 and KubeCon EU 2025 (with Google) focusing on LLM-aware load balancing in Kubernetes.
{{< /callout >}}



## Related Tools


- [vLLM](/tools/vllm/)
