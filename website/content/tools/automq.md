---
cncf_status: non-cncf
date: '2026-09-20T21:46:43.949480'
description: AutoMQ is a cloud-native fork of Kafka by separating storage to S3. 10x
  cost-effective. Autoscale in seconds. Single-digit ms latency.
get_started: Run AutoMQ locally using Docker (`curl -O https://raw.githubusercontent.com/AutoMQ/automq/refs/tags/1.5.5/docker/docker-compose.yaml
  && docker compose -f docker-compose.yaml up -d`) or deploy on Kubernetes for production
  via helm charts.
homepage_url: https://www.automq.com
interesting_facts: AutoMQ replaces Kafka's classic shared-nothing architecture with
  a shared storage architecture using a custom S3 Storage Adapter. According to their
  performance benchmarks, AutoMQ can speed up partition reassignment by 300x compared
  to Apache Kafka, cutting an operation that traditionally took 12 minutes down to
  just 2.2 seconds. It also boasts a 200x efficiency improvement during catch-up reads.
  While AutoMQ emphasizes cost-savings and cloud scalability, evaluators often compare
  it with more established Kafka distributions and managed offerings.
key_features:
- Stateless broker architecture leveraging object storage (S3) instead of local disk
  storage.
- 100% Apache Kafka® compatible (retention of Kafka API, protocol, and ecosystem).
- Autoscale in seconds without data rebalancing.
- Zero cross-AZ traffic costs due to its storage-compute separation and proxy layers.
- Built-in auto-balancer for automatic partition scheduling.
- Table Topic feature for automatic Kafka topic to Iceberg table conversion (Zero-ETL).
layout: single
letter: A
project_name: AutoMQ
recent_updates: Introduced Table Topic, a new feature combining stream and table functionalities
  to unify streaming and data analysis (supports Apache Iceberg and integrates with
  catalog services like AWS Glue and S3 tables).
related_tools:
- Apache Kafka
- MinIO
- Apache Iceberg
- AWS MSK
- Confluent Cloud
- WarpStream
- Redpanda
repo_url: https://github.com/AutoMQ/automq
status: completed
summary: AutoMQ is a cloud-native, diskless alternative to Apache Kafka® on S3 or
  any S3-compatible storage. It is designed to offer 10x cost savings, scale in seconds,
  and eliminate cross-AZ traffic costs while maintaining 100% Kafka compatibility.
title: AutoMQ
use_cases: Cloud-native data streaming, event-driven architectures, replacing traditional
  stateful Kafka clusters to reduce operational costs, real-time analytics, scaling
  for unpredictable traffic spikes, and integrating streams into data lakes.
---

This is an auto-generated tool page. For more details, see the [letter page](/letters/a/).
