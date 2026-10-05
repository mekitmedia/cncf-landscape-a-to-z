---
cncf_status: sandbox
date: '2026-10-04T18:37:39.401846'
description: A Kubernetes Resource Interface for the Edge
homepage_url: https://docs.akri.sh
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Akri
repo_url: https://github.com/project-akri/akri
status: completed
title: Akri
---



## Overview

Akri (A Kubernetes Resource Interface for the Edge) is a Cloud Native Computing Foundation (CNCF) Sandbox project that easily exposes heterogeneous leaf devices—such as IP cameras, USB sensors, and OPC UA equipment—as resources in a Kubernetes cluster.



## Key Features


- Automated discovery of IoT edge devices (ONVIF, udev, OPC UA, etc.)

- Exposes devices as Kubernetes Custom Resources (CRDs)

- Extends the Kubernetes device plugin framework for the edge

- Schedules workloads automatically on nodes where devices are detected

- Supports high availability and device failover




## Use Cases

Simplifying edge computing deployments by automating the connection of cameras in retail, sensors in warehouses, and OPC UA equipment in industrial environments to Kubernetes clusters.



{{< callout title="Getting Started" type="code" >}}
```bash
Install Akri using its Helm charts (`helm install akri akri-helm-charts/akri`), apply an Akri Configuration (like ONVIF or udev) to your cluster, and deploy pods requesting those resources. See documentation at https://project-akri.github.io/akri/ and learn more about real-world discovery setups at https://oneuptime.com/blog/post/2026-02-09-akri-iot-device-discovery/view.
```
{{< /callout >}}



## Recent Updates

Akri continues to grow its ecosystem of discovery handlers, enabling support for a wider array of industrial and edge protocols, and it remains an active CNCF Sandbox project.



{{< callout title="Did You Know?" type="info" >}}
Akri means 'edge' in Greek and acts as an acronym for 'A Kubernetes Resource Interface.' It was originally created by Microsoft to make Kubernetes a viable edge computing solution. Perspectives vary on its complexity, with some engineers highlighting how it drastically reduces the manual effort of maintaining dynamic hardware configurations (e.g. automatically recovering workloads when devices fail over), while others point out a steep learning curve related to writing custom discovery handlers for proprietary edge protocols.
{{< /callout >}}



## Related Tools


- [K3s](/tools/k3s/)

- [MicroK8s](/tools/microk8s/)

- [KubeEdge](/tools/kubeedge/)
