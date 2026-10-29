---
cncf_status: sandbox
date: '2026-10-27T15:20:44.206499'
description: A secure-by-default agent execution runtime for running millions of sandboxes.
homepage_url: https://github.com/agent-substrate/substrate
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Agent Substrate
repo_url: https://github.com/agent-substrate/substrate
status: completed
title: Agent Substrate
---



## Overview

A security-hardened, zero-trust runtime for sandboxed agents, engineered to safely run millions of agents and tools with 10x higher density than standard containers.



## Key Features


- Always sandboxed, VM-grade boundaries with gVisor or Cloud Hypervisor

- Per-agent cryptographic identity using SPIFFE X.509 certificates

- Zero credentials in the sandbox via atenet-egress

- Default-deny networking with private network stacks

- Pluggable policy at the edge for external PEP




## Use Cases

Running autonomous, untrusted, mostly-idle AI agents on standard Kubernetes.



{{< callout title="Getting Started" type="code" >}}
```bash
Follow the Quickstart Guide in the GitHub repository.
```
{{< /callout >}}



## Recent Updates

Initial release of Agent Substrate featuring zero-trust sandboxing for millions of agents on Kubernetes.



{{< callout title="Did You Know?" type="info" >}}
Built for 10x higher density than standard containers, delivering fast resume operations in less than 400ms.
{{< /callout >}}
