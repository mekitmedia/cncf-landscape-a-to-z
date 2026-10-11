---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.241389'
description: A realtime distributed OLAP datastore.
homepage_url: https://pinot.apache.org/
layout: single
letter: A
lifecycle_stage: tech_writing
project_name: Apache Pinot
repo_url: https://github.com/apache/pinot
status: completed
title: Apache Pinot
---



## Overview

A real-time distributed OLAP datastore designed to execute low-latency analytical queries over streaming and historical data at massive scale.



## Key Features


- Ultra-low latency SQL queries (sub-50ms) over billions of rows.

- Pluggable indexing (inverted, star-tree, range, text, JSON, geospatial).

- Real-time streaming ingestion from Kafka, Pulsar, and Kinesis.

- Multi-stage query engine for distributed joins and window functions.




## Use Cases

Powering real-time user-facing analytics, ride-share dispatch metrics, and live anomaly detection.



{{< callout title="Getting Started" type="code" >}}
```bash
Launch quickstart cluster via `./bin/quick-start-streaming.sh` and access console at `localhost:9000`.
```
{{< /callout >}}



## Recent Updates

Added vector indexing for similarity search and enhanced distributed join optimizations.



{{< callout title="Did You Know?" type="info" >}}
Apache Pinot is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Apache Druid](/tools/apache_druid/)

- [ClickHouse](/tools/clickhouse/)

- [Apache Kafka](/tools/apache_kafka/)
