---
title: "CubeSandbox"
date: 2026-09-23T18:00:00Z
draft: false
weight: 1
cncf_status: non-cncf
category: ai_native_infra_workload_runtime
week: 2
is_research_in_progress: false
homepage_url: https://cubesandbox.com
repo_url: https://github.com/TencentCloud/CubeSandbox
summary: CubeSandbox is a high-performance, out-of-the-box secure sandbox service for AI Agents built on RustVMM and KVM, compatible with the E2B SDK.
key_features:
  - Sub-60ms cold start speed for rapid sandbox creation
  - Hardware-level isolation with dedicated OS kernels in MicroVMs
  - E2B SDK compatibility for drop-in migration from E2B Cloud
  - High-density deployment with <5MB memory overhead per sandbox
  - eBPF-based inter-sandbox isolation and network security
recent_updates: Version 0.7.1 introduced end-to-end high availability for control-plane services, including a standalone template-center service and active/standby deployment for lifecycle management.
use_cases: AI Agent code execution, browser automation, OpenClaw integration, and RL training workloads requiring secure, isolated execution environments.
interesting_facts: It can create a hardware-isolated, fully serviceable sandbox in under 60ms with less than 5MB of memory overhead, enabling thousands of instances per server.
get_started: Deploy CubeSandbox via one-click Terraform on cloud VMs, on bare-metal, or in a dev-environment, then use the built-in WebUI for visual management.
related_tools:
  - E2B
  - Kata Containers
  - Cloud Hypervisor
---

# CubeSandbox
CubeSandbox is a high-performance, out-of-the-box secure sandbox service for AI Agents built on RustVMM and KVM, compatible with the E2B SDK.
