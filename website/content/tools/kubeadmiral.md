---
cncf_status: non-cncf
date: '2026-10-23T16:03:23.466101'
description: KubeAdmiral is a multi-cluster scheduling and orchestration system for
  Kubernetes.
homepage_url: https://github.com/kubewharf/kubeadmiral
layout: single
letter: K
lifecycle_stage: first_pass
project_name: KubeAdmiral
repo_url: https://github.com/kubewharf/kubeadmiral
status: completed
title: KubeAdmiral
---



## Overview

KubeAdmiral is a multi-cluster management system for Kubernetes, developed from Kubernetes Federation v2, extending its API for native compatibility and enhanced resource management.



## Key Features


- A new scheduling framework with a rich set of scheduling plugins.

- Override policies.

- Automatic propagation of dependencies with follower scheduling.

- Status aggregation of member cluster resources.

- Scalability, stability and user experience enhancements




## Use Cases

Managing Kubernetes resources across multiple clusters, migrating from single-cluster to multi-cluster setups, and implementing custom override policies and automatic failover.



{{< callout title="Getting Started" type="code" >}}
```bash
If you wish to see how KubeAdmiral works, you can easily start a cluster that includes the KubeAdmiral control plane on your local machine.


$ git clone https://github.com/kubewharf/kubeadmiral
$ cd kubeadmiral
$ make local-up
```
{{< /callout >}}



## Recent Updates

Released v1.0.0, a production-ready version with unified management of multi-clusters, multi-cluster application propagation, scheduling framework enhancement, unified federated type, failover, and status collection for member cluster resources.



{{< callout title="Did You Know?" type="info" >}}
KubeAdmiral is a continuation of Kubernetes Federation v2 and refers to Karmada for some of its architecture and API design.
{{< /callout >}}



## Related Tools


- [Kubernetes](/tools/kubernetes/)

- [Karmada](/tools/karmada/)
