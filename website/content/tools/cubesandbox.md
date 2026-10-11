---
cncf_status: non-cncf
date: '2026-10-04T18:37:42.624954'
description: A high-performance sandbox infrastructure for AI Agent execution with
  60ms startup and 5MB memory footprint.
homepage_url: https://cubesandbox.com
layout: single
letter: C
lifecycle_stage: tech_writing
project_name: CubeSandbox
repo_url: https://github.com/TencentCloud/CubeSandbox
status: completed
title: CubeSandbox
---



## Overview

CubeSandbox is a high-performance, out-of-the-box secure sandbox service for AI Agents built on RustVMM and KVM, compatible with the E2B SDK.



## Key Features


- Sub-60ms cold start speed for rapid sandbox creation

- Hardware-level isolation with dedicated OS kernels in MicroVMs

- E2B SDK compatibility for drop-in migration from E2B Cloud

- High-density deployment with <5MB memory overhead per sandbox

- eBPF-based inter-sandbox isolation and network security




## Use Cases

AI Agent code execution, browser automation, OpenClaw integration, and RL training workloads requiring secure, isolated execution environments.



{{< callout title="Getting Started" type="code" >}}
```bash
Deploy CubeSandbox via one-click Terraform on cloud VMs, on bare-metal, or in a dev-environment, then use the built-in WebUI for visual management.
```
{{< /callout >}}



## Recent Updates

Version 0.7.1 introduced end-to-end high availability for control-plane services, including a standalone template-center service and active/standby deployment for lifecycle management.



{{< callout title="Did You Know?" type="info" >}}
It can create a hardware-isolated, fully serviceable sandbox in under 60ms with less than 5MB of memory overhead, enabling thousands of instances per server.
{{< /callout >}}



## Related Tools


- [E2B](/tools/e2b/)

- [Kata Containers](/tools/kata_containers/)

- [Cloud Hypervisor](/tools/cloud_hypervisor/)
