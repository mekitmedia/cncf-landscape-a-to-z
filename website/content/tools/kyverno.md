---
cncf_status: graduated
date: '2026-10-24T15:00:30.042030'
homepage_url: https://kyverno.io/
layout: single
letter: K
lifecycle_stage: first_pass
project_name: Kyverno
repo_url: https://github.com/kyverno/kyverno
status: completed
title: Kyverno
---



## Overview

Kyverno is a Kubernetes-native policy engine that validates, mutates, and generates resources using admission controls and background scans.



## Key Features


- Kubernetes-native policy engine

- Validate, mutate, generate, and clean up resources

- Verify container image signatures for supply chain security

- Operate with kubectl, kustomize, and Git




## Use Cases

Enforcing Pod Security Standards, validating container image signatures, auto-labeling workloads, and auto-injecting config maps or secrets.



{{< callout title="Getting Started" type="code" >}}
```bash
Kyverno installation and reference documentation is available at kyverno.io. You can start with the Quick Start guide or try it in the Kyverno Playground.
```
{{< /callout >}}



## Recent Updates

Kyverno v1.19.2 addresses 24 published GitHub Security Advisories, including script-injection hardening and API path validation.



{{< callout title="Did You Know?" type="info" >}}
Kyverno uses policy-as-code and does not replace Kubernetes built-in policy controls but complements them with features like comprehensive reporting.
{{< /callout >}}



## Related Tools


- [Kubernetes](/tools/kubernetes/)

- [Kyverno-JSON](/tools/kyverno-json/)
