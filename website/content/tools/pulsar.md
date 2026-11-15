---
cncf_status: non-cncf
date: '2026-10-31 00:00:00+00:00'
homepage_url: https://pulsar.apache.org/
layout: single
letter: P
lifecycle_stage: tech_writing
project_name: Pulsar
repo_url: https://github.com/apache/pulsar
status: completed
title: Pulsar
---



## Overview

Apache Pulsar is a distributed pub-sub messaging platform designed for flexibility and ease of use, featuring an intuitive client API and a robust messaging model.



## Key Features


- Horizontally scalable architecture capable of handling millions of independent topics and messages per second

- Provides strong ordering and consistency guarantees with low latency durable storage

- Supports both topic and queue semantics

- Includes a built-in load balancer and is designed for hosted services with multi-tenant capabilities, authentication, authorization, and quotas

- Features geo-replication, transparent handling of partitioned topics, and transparent batching of messages




## Use Cases

Ideal for scenarios requiring high-throughput, low-latency messaging, distributed event streaming, and multi-tenant architectures where strong isolation and scalability are critical.



{{< callout title="Getting Started" type="code" >}}
```bash
To get started with Pulsar, visit the official website to download the latest release or use the Docker image via `docker pull apachepulsar/pulsar-all`. Detailed setup and configuration guides are available in the documentation at https://pulsar.apache.org/.
```
{{< /callout >}}



## Recent Updates

Apache Pulsar continues to receive updates with bug fixes and improvements, notably recommending specific Java versions (like 17 or 21) for optimal performance and stability, and providing helm charts and various client libraries across multiple languages.



{{< callout title="Did You Know?" type="info" >}}
Pulsar was originally developed by Yahoo! and was designed to solve the challenges they faced with existing messaging systems, particularly around multi-tenancy and geo-replication.
{{< /callout >}}



