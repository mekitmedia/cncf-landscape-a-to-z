---
cncf_status: non-cncf
date: '2026-10-31T02:57:09.636283'
description: A toolkit to run Ray applications on Kubernetes
homepage_url: https://github.com/ray-project/kuberay
layout: single
letter: K
lifecycle_stage: first_pass
project_name: Kuberay
repo_url: https://github.com/ray-project/kuberay
status: completed
title: Kuberay
---



## Overview

KubeRay is an open-source Kubernetes operator designed to streamline the deployment and management of Ray applications on Kubernetes, offering components like RayCluster, RayJob, and RayService.



## Key Features


- **RayCluster**: Fully manages the lifecycle of RayCluster, handling creation/deletion, autoscaling, and ensuring fault tolerance.

- **RayJob**: Automatically creates a RayCluster, submits a job upon cluster readiness, and can be configured to delete the cluster once the job concludes.

- **RayService**: Offers zero-downtime upgrades and high availability for RayCluster and Ray Serve deployment graphs.




## Use Cases

Simplifying the deployment, lifecycle management, autoscaling, and fault tolerance of distributed applications and machine learning workloads using Ray on Kubernetes.



{{< callout title="Getting Started" type="code" >}}
```bash
Refer to the Quick Start guides in the Ray documentation for RayCluster, RayJob, and RayService to begin deploying workloads on Kubernetes using KubeRay.
```
{{< /callout >}}



## Recent Updates

Starting from KubeRay v1.4.0, an experimental KubeRay Dashboard has been introduced to enable users to view and manage KubeRay resources.



{{< callout title="Did You Know?" type="info" >}}
KubeRay provides a kubectl plugin (`kubectl ray`) starting from version 1.3.0 to simplify common workflows for deploying Ray on Kubernetes, catering to users less familiar with Kubernetes native commands.
{{< /callout >}}



## Related Tools


- [Kubernetes](/tools/kubernetes/)

- [Ray](/tools/ray/)

- [Volcano](/tools/volcano/)

- [Kueue](/tools/kueue/)
