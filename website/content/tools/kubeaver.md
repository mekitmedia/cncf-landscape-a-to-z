---
cncf_status: non-cncf
date: '2026-11-03T17:02:13.974565'
description: Deploy a highly available Kubernetes cluster in offline environments.
homepage_url: https://github.com/eb-k8s/kubeaver
layout: single
letter: K
lifecycle_stage: tech_writing
project_name: Kubeaver
repo_url: https://github.com/eb-k8s/kubeaver
status: completed
title: Kubeaver
---



## Overview

Kubeaver is a tool for quickly deploying high-availability Kubernetes (K8s) clusters, supporting offline and online methods. The project is based on kubespray, leveraging Ansible to automate deployment tasks, and provides a user-friendly graphical user interface.



## Key Features


- Cluster Management

- Deploy Cluster (Offline Cluster Deployment)

- Task Management

- Task Time Statistics

- Task Real-time Output

- Node Management

- Offline Package Management

- Host Management




## Use Cases

Quickly deploying high-availability Kubernetes clusters in offline or online environments.



{{< callout title="Getting Started" type="code" >}}
```bash
tar xzvf kubeaver-offline-installer-1.0.0.tgz

cd kubeaver-offline-installer-1.0.0

./start.sh
```
{{< /callout >}}





{{< callout title="Did You Know?" type="info" >}}
Kubeaver is based on kubespray and leverages Ansible to automate deployment tasks. It is also a CNCF conformance-certified installer.
{{< /callout >}}



