---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.225034'
description: Open source, distributed, versioned, column-oriented store modeled after
  Google's Bigtable.
homepage_url: https://hbase.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache HBase
repo_url: https://github.com/apache/hbase
status: completed
title: Apache HBase
---



## Overview

An open-source, distributed, versioned, column-oriented store modeled after Google's Bigtable, providing random real-time read/write access to big data on HDFS.



## Key Features


- Linear horizontal scalability across commodity servers.

- Strictly consistent read and write operations at scale.

- Automatic sharding and region failover handling.

- Integration with Hadoop, Spark, and Apache Phoenix for SQL.




## Use Cases

Serving high-volume user activity logs, real-time messaging backends, and sparse key-value data.



{{< callout title="Getting Started" type="code" >}}
```bash
Download release, start standalone mode via `./bin/start-hbase.sh`, and query via `./bin/hbase shell`.
```
{{< /callout >}}



## Recent Updates

Optimized off-heap memory management and container-native deployment patterns.



{{< callout title="Did You Know?" type="info" >}}
Apache HBase is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Apache Cassandra](/tools/apache_cassandra/)

- [Apache Hadoop](/tools/apache_hadoop/)

- [Apache Phoenix](/tools/apache_phoenix/)
