---
cncf_status: sandbox
date: '2026-10-16T15:41:11.837613'
description: Kubernetes performance and scale test orchestration framework written
  in golang
homepage_url: https://kube-burner.github.io/kube-burner/
layout: single
letter: K
lifecycle_stage: tech_writing
project_name: Kube-burner
repo_url: https://github.com/kube-burner/kube-burner
status: completed
title: Kube-burner
---



## Overview

Kube-burner is a comprehensive Kubernetes performance and scale test orchestration framework written in Go.



## Key Features


- Resource management: Create, delete, and patch Kubernetes resources at scale

- Observability: Prometheus metric collection and indexing

- Analysis: Built-in measurements and alerting capabilities

- Multiple build options: Standard, release, and security-hardened static binaries




## Use Cases

Useful for performing scale and performance testing of Kubernetes clusters, gathering Prometheus metrics during testing, and orchestrating complex multi-resource operations.



{{< callout title="Getting Started" type="code" >}}
```bash
Install the latest stable version using the provided script: `curl -Ls https://raw.githubusercontent.com/kube-burner/kube-burner/refs/heads/main/hack/install.sh`
```
{{< /callout >}}



## Recent Updates

Release v2.8.6 introduced outputFile support for background hooks, a baselinePhase option to vmiLatency measurement, and updated Kind support for Kubernetes 1.37.



{{< callout title="Did You Know?" type="info" >}}
Kube-burner makes extensive usage of the official k8s client library, client-go, and provides a continuous integration pipeline that automatically builds and tests the project.
{{< /callout >}}



## Related Tools


- [Kubernetes](/tools/kubernetes/)

- [Prometheus](/tools/prometheus/)
