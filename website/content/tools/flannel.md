---
title: "Flannel"
date: 2026-11-05T20:09:56Z
draft: false
layout: "single"
letter: "F"
lifecycle_stage: "initial"
status: "completed"
project_name: "Flannel"
repo_url: "https://github.com/flannel-io/flannel"
homepage_url: "https://github.com/flannel-io/flannel"
cncf_status: "non-cncf"
---

### Summary
Flannel is a network fabric designed for Kubernetes.

### Key Features
- Runs a small, single binary agent called `flanneld` on each host, and is responsible for allocating a subnet lease to each host out of a larger, preconfigured address space.
- Uses either the Kubernetes API or etcd directly to store the network configuration, the allocated subnets, and any auxiliary data (such as the host's public IP).
- Packets are forwarded using one of several backend mechanisms including VXLAN and various cloud integrations.
- Provides a layer 3 IPv4 network between multiple nodes in a cluster.
- Provides a CNI plugin for Kubernetes and a guidance on integrating with Docker.

### Use Cases
Flannel is responsible for providing a layer 3 IPv4 network between multiple nodes in a cluster.

### Interesting Facts
While the `flanneld` binary does not natively enforce Network Policies, the Flannel project provides ways to add policy support to your cluster.

### Related Tools
- Kubernetes
- etcd
- Calico
- Cilium
- K3s
- Docker

### Getting Started
For Kubernetes v1.17+

Deploying Flannel with kubectl

```bash
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```
