---
cncf_status: sandbox
date: '2026-10-04T18:37:43.087333'
description: Clusterpedia is used for complex resources search across multiple clusters,
  support simultaneous search of a single kind of resource  or multiple kinds of resources
  existing in multiple clusters.
homepage_url: https://clusterpedia.io
layout: single
letter: C
lifecycle_stage: tech_writing
project_name: Clusterpedia
repo_url: https://github.com/clusterpedia-io/clusterpedia
status: completed
title: Clusterpedia
---



## Overview

Clusterpedia is a multi-cluster encyclopedia designed to synchronize, search for, and easily control multi-cluster resources.



## Key Features


- Automatic synchronization of clusters managed by multi-cloud platforms.

- Advanced retrieval features and complete compatibility with Kubernetes OpenAPI.

- Supports importing Kubernetes 1.10+ clusters.

- Automatic conversion and retrieval of multi-version Kube resources.

- A single API endpoint to retrieve different resource types.

- Flexible synchronization policies, including wildcards and custom resources support.

- Unified search entry point for master and multi-cluster resources using Aggregated API.

- Low memory footprint and weak network optimization.

- Pluggable storage layer architecture without dependency on specific database components.




## Use Cases

Operators and platform engineers use Clusterpedia to efficiently synchronize and retrieve multi-cluster resources with rich search conditions (like multi-cluster label selectors, owner names, and complex queries), and they can manage varied multi-cloud resources from a unified endpoint that mirrors the Kubernetes master cluster API.



{{< callout title="Getting Started" type="code" >}}
```bash
Clusterpedia can be integrated into your multi-cluster setup using various tools or deployed as a standalone platform to begin synchronizing and searching your resources across clusters.
```
{{< /callout >}}



## Recent Updates

Clusterpedia continues to improve its core capabilities to synchronize, search for, and control multi-cluster resources across a variety of multi-cloud platforms like Cluster API, Karmada, Clusternet, vCluster, and KubeVela.



{{< callout title="Did You Know?" type="info" >}}
Clusterpedia is inspired by Wikipedia, where it acts as a central encyclopedia for multi-cluster data and envisions a future where it can not only view but control and edit resources directly.
{{< /callout >}}



## Related Tools


- [Cluster API](/tools/cluster_api/)

- [Karmada](/tools/karmada/)

- [Clusternet](/tools/clusternet/)

- [vCluster](/tools/vcluster/)

- [KubeVela](/tools/kubevela/)


