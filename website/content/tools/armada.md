---
cncf_status: sandbox
date: '2026-10-04T18:37:39.089558'
description: Armada is a multi-Kubernetes cluster batch job scheduler
homepage_url: https://armadaproject.io/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Armada
repo_url: https://github.com/armadaproject/armada
status: completed
title: Armada
---



## Overview

Armada is a multi-Kubernetes cluster batch job meta-scheduler designed to handle massive-scale workloads. Built on top of Kubernetes, Armada enables organizations to distribute millions of batch jobs per day across tens of thousands of nodes spanning multiple clusters, making it an ideal solution for high-throughput computational workloads.



## Key Features


- Multi-cluster orchestration to schedule jobs across many Kubernetes clusters seamlessly

- High-throughput queueing capable of handling millions of queued jobs

- Advanced batch scheduling including fair queuing, gang scheduling, preemption, and resource limits

- Enterprise-grade reliability with secure, highly available components designed for production use

- Support for external storage backends (e.g., PostgreSQL and Redis) for high-throughput batch job queueing and scheduling




## Use Cases

High-Performance Computing (HPC) such as Machine Learning Training, Scientific Computing, and Financial Modeling. Data Processing Pipelines like ETL Workloads, Data Analytics, and Backup/Archival. CI/CD and Development for Build Systems, Integration Testing, and Deployment Automation.



{{< callout title="Getting Started" type="code" >}}
```bash
Users can try Armada locally by following the quickstart guide on the Armada project website.
```
{{< /callout >}}



## Recent Updates

Armada is actively maintained as a CNCF Sandbox project and used in production environments, such as G-Research where it processes millions of jobs daily.



{{< callout title="Did You Know?" type="info" >}}
G-Research, a leading quantitative research company, uses Armada in production to process millions of jobs per day and manage tens of thousands of nodes.
{{< /callout >}}



## Related Tools


- [Kubernetes](/tools/kubernetes/)

- [Agones](/tools/agones/)

- [Apache Mesos](/tools/apache_mesos/)
