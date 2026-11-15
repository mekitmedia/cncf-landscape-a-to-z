---
cncf_status: non-cncf
date: '2026-11-06 08:00:00+00:00'
description: NoSQL data store using the seastar framework, compatible with Apache
  Cassandra.
homepage_url: https://github.com/scylladb/scylladb
layout: single
letter: S
lifecycle_stage: tech_writing
project_name: ScyllaDB
repo_url: https://github.com/scylladb/scylladb
status: completed
title: ScyllaDB
---



## Overview

Scylla is a real-time big data database that is API-compatible with Apache Cassandra and Amazon DynamoDB, embracing a shared-nothing approach for increased performance.



## Key Features


- API compatibility with Apache Cassandra and Amazon DynamoDB.

- Shared-nothing architecture for increased throughput and storage capacity.

- Order-of-magnitude performance improvements and reduced hardware costs.




## Use Cases

Replacing Cassandra or DynamoDB setups for real-time big data workloads with reduced hardware costs and higher performance.



{{< callout title="Getting Started" type="code" >}}
```bash
Run Scylla with Docker: `docker run --name scylla -d -p 8000:8000 scylladb/scylla:latest --alternator-port=8000 --alternator-write-isolation=always`
```
{{< /callout >}}



## Recent Updates

Release scylla-2026.4.0-rc2-candidate-20261105094225.



{{< callout title="Did You Know?" type="info" >}}
ScyllaDB is built to be fairly fussy about its build environment, requiring recent versions of the C++23 compiler, but offers a frozen toolchain Docker image for easy compilation.
{{< /callout >}}



## Related Tools


- [Alternator](/tools/alternator/)


