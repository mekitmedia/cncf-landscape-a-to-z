---
cncf_status: graduated
date: '2026-10-04T18:37:39.350279'
description: Kubernetes-native tools to run workflows, manage clusters, and do GitOps
  right.
homepage_url: https://argoproj.github.io/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Argo
repo_url: https://github.com/argoproj/argo-cd
status: completed
title: Argo
---



## Overview

A CNCF graduated suite of open-source Kubernetes-native tools for workflows, events, continuous delivery (CD), and progressive rollouts.



## Key Features


- Argo CD: Declarative GitOps continuous delivery keeping cluster state in sync with Git.

- Argo Workflows: Kubernetes-native workflow engine for parallel compute and ML DAGs.

- Argo Rollouts: Advanced progressive delivery controller for Canary and Blue-Green deployments.

- Argo Events: Event-driven workflow automation framework triggered by webhooks, Kafka, S3.




## Use Cases

Automating GitOps continuous delivery across Kubernetes fleets and orchestrating distributed ML workflows.



{{< callout title="Getting Started" type="code" >}}
```bash
Install Argo CD via `kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`.
```
{{< /callout >}}



## Recent Updates

Graduated CNCF project, expanding multi-cluster management at scale and enterprise RBAC.



{{< callout title="Did You Know?" type="info" >}}
Argo is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Flux](/tools/flux/)

- [Tekton](/tools/tekton/)

- [Spinnaker](/tools/spinnaker/)
