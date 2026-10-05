---
cncf_status: non-cncf
date: '2026-10-04T18:37:45.915059'
description: Typhoon distributes upstream Kubernetes, architectural conventions, and
  cluster addons, much like a GNU/Linux distribution provides the Linux kernel and
  userspace components.
homepage_url: https://typhoon.psdn.io/
layout: single
letter: T
lifecycle_stage: tech_writing
project_name: Typhoon
repo_url: https://github.com/poseidon/typhoon
status: completed
title: Typhoon
---



## Overview

Typhoon is a minimal and free Kubernetes distribution.



## Key Features


- Minimal, stable base Kubernetes distribution

- Declarative infrastructure and configuration

- Ready for Ingress, Prometheus, Grafana, CSI, or other addons




## Use Cases

Practical for labs, datacenters, and clouds.



{{< callout title="Getting Started" type="code" >}}
```bash
Define a Kubernetes cluster by using the Terraform module for your chosen platform and operating system.
```
{{< /callout >}}



## Recent Updates

Add `cloud_provider` variable so "external" cloud controller managers may be used (default null).



{{< callout title="Did You Know?" type="info" >}}
Typhoon distributes upstream Kubernetes, architectural conventions, and cluster addons, much like a GNU/Linux distribution provides the Linux kernel and userspace components.
{{< /callout >}}



## Related Tools


- [Terraform](/tools/terraform/)

- [Kubespray](/tools/kubespray/)

- [kops](/tools/kops/)
