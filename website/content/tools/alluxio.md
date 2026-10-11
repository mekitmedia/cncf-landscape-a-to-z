---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.175796'
homepage_url: https://www.alluxio.io/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Alluxio
repo_url: https://github.com/alluxio/alluxio
status: completed
title: Alluxio
---



## Overview

An open-source data orchestration layer that bridges analytical and AI compute frameworks with distributed and cloud storage systems.



## Key Features


- Memory-speed distributed caching across storage tiers (RAM, NVMe, SSD).

- Unified namespace aggregating AWS S3, HDFS, GCS, and Ceph.

- Transparent acceleration for PyTorch, TensorFlow, Spark, and Presto/Trino.

- Native Kubernetes CSI driver for container mounts.




## Use Cases

Accelerating distributed machine learning training over remote object stores and reducing cloud egress costs.



{{< callout title="Getting Started" type="code" >}}
```bash
Deploy Alluxio on Kubernetes via Helm and mount object store buckets to `alluxio://` URIs.
```
{{< /callout >}}



## Recent Updates

Enterprise AI and community editions focused on high-concurrency LLM training I/O caching.



{{< callout title="Did You Know?" type="info" >}}
Alluxio is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Apache Spark](/tools/apache_spark/)

- [Trino](/tools/trino/)

- [JuiceFS](/tools/juicefs/)
