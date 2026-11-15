---
cncf_status: non-cncf
date: '2026-11-05 20:09:56+00:00'
homepage_url: https://github.com/flannel-io/flannel
layout: single
letter: F
lifecycle_stage: tech_writing
project_name: Flannel
repo_url: https://github.com/flannel-io/flannel
status: completed
title: Flannel
---



## Overview

Flannel is a network fabric designed for Kubernetes.



## Key Features


- Runs a small, single binary agent called `flanneld` on each host, and is responsible for allocating a subnet lease to each host out of a larger, preconfigured address space.

- Uses either the Kubernetes API or etcd directly to store the network configuration, the allocated subnets, and any auxiliary data (such as the host's public IP).

- Packets are forwarded using one of several backend mechanisms including VXLAN and various cloud integrations.

- Provides a layer 3 IPv4 network between multiple nodes in a cluster.

- Provides a CNI plugin for Kubernetes and a guidance on integrating with Docker.




## Use Cases

Flannel is responsible for providing a layer 3 IPv4 network between multiple nodes in a cluster.



{{< callout title="Getting Started" type="code" >}}
```bash
For Kubernetes v1.17+, apply the Flannel manifest with kubectl to deploy the network plugin on your cluster.
```
{{< /callout >}}





{{< callout title="Did You Know?" type="info" >}}
While the `flanneld` binary does not natively enforce Network Policies, the Flannel project provides ways to add policy support to your cluster.
{{< /callout >}}



## Related Tools


- [Kubernetes](/tools/kubernetes/)

- [etcd](/tools/etcd/)

- [Calico](/tools/calico/)

- [Cilium](/tools/cilium/)

- [K3s](/tools/k3s/)

- [Docker](/tools/docker/)


