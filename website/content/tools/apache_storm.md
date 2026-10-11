---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.788408'
homepage_url: https://storm.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache Storm
repo_url: https://github.com/apache/storm
status: completed
title: Apache Storm
---



## Overview

A distributed, real-time computation system for processing unbounded streams of data reliably with high speed and low latency.



## Key Features


- Real-time stream abstraction with Spouts and Bolts in Topologies.

- Guaranteed message processing semantics (at-least-once or Trident exactly-once).

- Fault-tolerant worker management with automatic task restarts.

- Multi-language support authoring logic in any language via standard I/O.




## Use Cases

Real-time stream analytics, online machine learning scoring, and continuous ETL computation.



{{< callout title="Getting Started" type="code" >}}
```bash
Start Nimbus (`storm nimbus`) and Supervisor (`storm supervisor`) and submit topologies via `storm jar`.
```
{{< /callout >}}



## Recent Updates

Migrated internal daemons to pure Java and added resource-aware scheduling.



{{< callout title="Did You Know?" type="info" >}}
Apache Storm is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Apache Flink](/tools/apache_flink/)

- [Apache Spark Streaming](/tools/apache_spark_streaming/)

- [Apache Samza](/tools/apache_samza/)
