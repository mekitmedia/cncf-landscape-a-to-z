---
cncf_status: sandbox
date: '2026-10-25T15:17:38.722669'
description: An early-stage event processing system for unstructured data with rich
  support for structural pattern-matching, filtering and transformation
homepage_url: https://www.tremor.rs/
layout: single
letter: T
lifecycle_stage: tech_writing
project_name: Tremor
repo_url: https://github.com/tremor-rs/tremor-runtime
status: completed
title: Tremor
---



## Overview

Tremor is an event- or stream-processing engine designed to handle high-volumetric data efficiently in terms of resources and latency.



## Key Features


- Event and stream-processing system optimized for high-volumetric data.

- Supports structured and binary data (schemaless and strictly schematic).

- Troy language for configuring pipelines and routing.

- Connects with Kafka, Influx compatible stores, Open telemetry, S3, and more.




## Use Cases

Applying traffic-shaping to a high volume of incoming events, distributing events based on their contents, protecting a downstream system from overload, and performing ETL like tasks on data.



{{< callout title="Getting Started" type="code" >}}
```bash
To run tremor locally and introspect its docker environment, do the following:

make image
docker run tremorproject/tremor:latest

Tremor is configured using .troy files written in our own Troy language.

```
{{< /callout >}}



## Recent Updates

v0.12.5 Release Notes: Add dynamic metrics configuration to control output. Fix issue where some log messages were dropped during shutdown. Enhance performance of the Kafka connector under high load.



{{< callout title="Did You Know?" type="info" >}}
Tremor is designed to perform well for high-volumetric data both in terms of consumption of memory and CPU resources and in terms of latency, while providing insightful metrics and helpful error messages at runtime.
{{< /callout >}}



## Related Tools


- [Kafka](/tools/kafka/)

- [Elasticsearch](/tools/elasticsearch/)

- [S3](/tools/s3/)
