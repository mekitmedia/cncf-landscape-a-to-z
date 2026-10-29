---
cncf_status: non-cncf
date: '2026-10-23T02:15:14.610519'
description: InfluxDB is an open source time series database written in Rust, using
  Apache Arrow, Apache Parquet, and Apache DataFusion as its foundational building
  blocks.
homepage_url: https://github.com/influxdata/influxdb
layout: single
letter: I
lifecycle_stage: tech_writing
project_name: Influxdb
repo_url: https://github.com/influxdata/influxdb
status: completed
title: Influxdb
---



## Overview

InfluxDB is a scalable, open-source time series database designed for real-time events, analytics, and monitoring, powered by Apache Arrow, DataFusion, and Parquet.



## Key Features


- Diskless architecture with object storage support (or local disk with no dependencies)

- Fast query response times (under 10ms for last-value queries, or 30ms for distinct metadata)

- Embedded Python VM for plugins and triggers

- Parquet file persistence

- Compatibility with InfluxDB 1.x and 2.x write APIs

- SQL query engine with support for FlightSQL and HTTP query API




## Use Cases

Monitoring sensor data, server monitoring, application performance monitoring, network monitoring, financial market and trading analytics, and behavioral analytics.



{{< callout title="Getting Started" type="code" >}}
```bash
Start InfluxDB using Docker:

docker run -p 8086:8086 -v influxdb2:/var/lib/influxdb2 influxdb:2.0

```
{{< /callout >}}



## Recent Updates

v3.12.1 brings faster startup after large file removals, a fix for catalog loading failures after upgrades, and ensures acknowledged writes are not lost after forced snapshots and restarts.



{{< callout title="Did You Know?" type="info" >}}
InfluxDB 3 Core utilizes a diskless architecture and is built using Rust, Apache Arrow, DataFusion, and persists data in Apache Parquet formats.
{{< /callout >}}



## Related Tools


- [Prometheus](/tools/prometheus/)

- [Grafana](/tools/grafana/)
