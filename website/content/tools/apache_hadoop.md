---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.534467'
homepage_url: https://hadoop.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache Hadoop
repo_url: https://github.com/apache/hadoop
status: completed
title: Apache Hadoop
---



## Overview

A foundational open-source framework that allows for the distributed processing and storage of large data sets across clusters of computers.



## Key Features


- HDFS (Hadoop Distributed File System) for fault-tolerant distributed storage.

- YARN for cluster resource negotiation and workload scheduling.

- Hadoop MapReduce for parallel data computation.

- Ecosystem compatibility with Hive, Spark, and cloud object stores.




## Use Cases

Batch data warehousing, historical log archiving, and petabyte-scale data pipelines.



{{< callout title="Getting Started" type="code" >}}
```bash
Configure `core-site.xml`, format namenode with `hdfs namenode -format`, and run `start-dfs.sh`.
```
{{< /callout >}}



## Recent Updates

HDFS erasure coding cutting storage overhead by 50% and GPU scheduling in YARN.



{{< callout title="Did You Know?" type="info" >}}
Apache Hadoop is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Apache Spark](/tools/apache_spark/)

- [Apache Hive](/tools/apache_hive/)

- [Ceph](/tools/ceph/)
