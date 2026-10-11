---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.366669'
description: Open Source CI/CD platform with advanced features and architecture. Powerful,
  reproducible and containerized workflows (called Runs), git based workflow (integrates
  with all the primary git repositories like GitHub, GitLab, Gitea), restart Runs
  from failed tasks, user direct runs (test your local changes to a remote Agola server
  with just one command), distributed and high available by design and runs everywhere
  (Kubernetes, docker, IaaS, bare metal).
homepage_url: https://agola.io
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Agola
repo_url: https://github.com/agola-io/agola
status: completed
title: Agola
---



## Overview

A cloud-native CI/CD system designed to run workflows across multiple execution environments including Kubernetes, containers, and virtual machines.



## Key Features


- Container-native workflow execution in Kubernetes pods.

- User-driven pipelines configured via YAML manifests.

- Multi-source authentication (GitHub, GitLab, Gitea).

- Distributed microservices architecture.




## Use Cases

Building flexible internal CI/CD pipelines running inside isolated Kubernetes pods.



{{< callout title="Getting Started" type="code" >}}
```bash
Deploy Agola on Kubernetes via Helm charts and trigger builds with the `agola` CLI.
```
{{< /callout >}}



## Recent Updates

Enhanced token security and modern Kubernetes executor integrations.



{{< callout title="Did You Know?" type="info" >}}
Agola is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Tekton](/tools/tekton/)

- [Argo Workflows](/tools/argo_workflows/)

- [Drone](/tools/drone/)
