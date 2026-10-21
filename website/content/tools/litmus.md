---
cncf_status: incubating
date: '2026-10-20T16:18:07.522745'
description: Litmus is an open source Chaos Engineering platform that enables teams
  to identify weaknesses & potential outages in infrastructures by inducing chaos
  tests in a controlled way
homepage_url: https://litmuschaos.io/
layout: single
letter: L
lifecycle_stage: first_pass
project_name: Litmus
repo_url: https://github.com/litmuschaos/litmus
status: completed
title: Litmus
---



## Overview

Litmus is a tool for Cloud-Native Chaos Engineering that lets teams test and improve infrastructure resilience by introducing controlled faults.



## Key Features


- Chaos Control Plane: Centralized management using chaos-center

- Chaos Execution Plane: Operators and agents that execute faults in Kubernetes

- ChaosExperiment: Reusable templates defining fault configurations

- ChaosEngine: Links application workloads to specific ChaosExperiments

- ChaosResult: Captures and holds the outcome of experiment runs




## Use Cases

- **For Developers**: To run chaos experiments during application development as an extension of unit testing or integration testing.
- **For CI/CD pipeline builders**: To run chaos as a pipeline stage to find bugs when the application is subjected to fail paths in a pipeline.
- **For SREs**: To plan and schedule chaos experiments into the application and/or surrounding infrastructure. This practice identifies the weaknesses
  in the deployment system and increases resilience.



{{< callout title="Getting Started" type="code" >}}
```bash
helm repo add litmuschaos https://litmuschaos.github.io/litmus-helm/
helm install chaos litmuschaos/litmus --namespace=litmus --set portal.frontend.service.type=NodePort
```
{{< /callout >}}



## Recent Updates

Litmus v3.33.0 was released on 2026-10-15



{{< callout title="Did You Know?" type="info" >}}
Litmus adopts a "Kubernetes-native" approach to define chaos intent in a declarative manner via Kubernetes custom resources (CRs).
{{< /callout >}}



## Related Tools


- [kubernetes](/tools/kubernetes/)
