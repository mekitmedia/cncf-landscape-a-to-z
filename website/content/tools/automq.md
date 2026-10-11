---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.861315'
description: AutoMQ is a cloud-native fork of Kafka by separating storage to S3. 10x
  cost-effective. Autoscale in seconds. Single-digit ms latency.
homepage_url: https://www.automq.com
layout: single
letter: A
lifecycle_stage: first_pass
project_name: AutoMQ
repo_url: https://github.com/AutoMQ/automq
status: completed
title: AutoMQ
---



## Overview

AutoMQ is a cloud-native, diskless alternative to Apache Kafka® on S3 or any S3-compatible storage. It is designed to offer 10x cost savings, scale in seconds, and eliminate cross-AZ traffic costs while maintaining 100% Kafka compatibility.



## Key Features


- Stateless broker architecture leveraging object storage (S3) instead of local disk storage.

- 100% Apache Kafka® compatible (retention of Kafka API, protocol, and ecosystem).

- Autoscale in seconds without data rebalancing.

- Zero cross-AZ traffic costs due to its storage-compute separation and proxy layers.

- Built-in auto-balancer for automatic partition scheduling.

- Table Topic feature for automatic Kafka topic to Iceberg table conversion (Zero-ETL).




## Use Cases

Cloud-native data streaming, event-driven architectures, replacing traditional stateful Kafka clusters to reduce operational costs, real-time analytics, scaling for unpredictable traffic spikes, and integrating streams into data lakes.



{{< callout title="Getting Started" type="code" >}}
```bash
Run AutoMQ locally using Docker (`curl -O https://raw.githubusercontent.com/AutoMQ/automq/refs/tags/1.5.5/docker/docker-compose.yaml && docker compose -f docker-compose.yaml up -d`) or deploy on Kubernetes for production via helm charts.
```
{{< /callout >}}



## Recent Updates

Introduced Table Topic, a new feature combining stream and table functionalities to unify streaming and data analysis (supports Apache Iceberg and integrates with catalog services like AWS Glue and S3 tables).



{{< callout title="Did You Know?" type="info" >}}
AutoMQ replaces Kafka's classic shared-nothing architecture with a shared storage architecture using a custom S3 Storage Adapter. According to their performance benchmarks, AutoMQ can speed up partition reassignment by 300x compared to Apache Kafka, cutting an operation that traditionally took 12 minutes down to just 2.2 seconds. It also boasts a 200x efficiency improvement during catch-up reads. While AutoMQ emphasizes cost-savings and cloud scalability, evaluators often compare it with more established Kafka distributions and managed offerings.
{{< /callout >}}



## Related Tools


- [Apache Kafka](/tools/apache_kafka/)

- [MinIO](/tools/minio/)

- [Apache Iceberg](/tools/apache_iceberg/)

- [AWS MSK](/tools/aws_msk/)

- [Confluent Cloud](/tools/confluent_cloud/)

- [WarpStream](/tools/warpstream/)

- [Redpanda](/tools/redpanda/)
