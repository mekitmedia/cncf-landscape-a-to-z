---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.351323'
homepage_url: https://carbondata.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache CarbonData
repo_url: https://github.com/apache/carbondata
status: completed
title: Apache CarbonData
---



## Overview

An indexed columnar data format for fast analytics on big data platforms, optimized for multi-dimensional point lookups and aggregations.



## Key Features


- Multi-level indexing (min/max, inverted index, B-tree) for rapid point queries.

- Columnar storage with advanced encoding and compression.

- Integration with Spark, Presto, and Hive.

- Support for ACID transactions and lakehouse mutations.




## Use Cases

Interactive analytics on massive datasets mixing full table scans and single-record filters.



{{< callout title="Getting Started" type="code" >}}
```bash
Include `carbondata-spark` dependency and write DataFrames using `.write.format('carbondata')`.
```
{{< /callout >}}



## Recent Updates

Enhanced secondary index support and Spark 3.x compatibility.



{{< callout title="Did You Know?" type="info" >}}
Apache CarbonData is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Apache Parquet](/tools/apache_parquet/)

- [Apache Iceberg](/tools/apache_iceberg/)

- [Apache ORC](/tools/apache_orc/)
