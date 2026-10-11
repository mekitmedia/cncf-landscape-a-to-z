---
cncf_status: non-cncf
date: '2026-10-04T18:37:42.350602'
description: A free and open source, distributed, wide-column store, NoSQL database
  management system designed to handle large amounts of data across many commodity
  servers, providing high availability with no single point of failure.
homepage_url: https://cassandra.apache.org/
layout: single
letter: C
lifecycle_stage: tech_writing
project_name: Cassandra
repo_url: https://github.com/apache/cassandra
status: completed
title: Cassandra
---



## Overview

Apache Cassandra is an open source transactional distributed database designed for managing massive amounts of data across commodity hardware or cloud infrastructure, offering linear scalability and proven fault-tolerance without compromising performance.



## Key Features


- Distributed Database: Highly-scalable partitioned row store.

- Partitioning: Distributes data across multiple machines transparently, automatically repartitioning as nodes are added or removed.

- Row Store & CQL: Organizes data by rows and columns, similar to relational databases, queryable using the Cassandra Query Language (CQL).




## Use Cases

Ideal for applications requiring massive scale, high availability, and no single point of failure.



{{< callout title="Getting Started" type="code" >}}
```bash
Download the archive, extract it, and start the server using `bin/cassandra -f`. You can then interact with it using `bin/cqlsh`.
```
{{< /callout >}}



## Recent Updates

Cassandra 5.0.9 released with ongoing enhancements.



{{< callout title="Did You Know?" type="info" >}}
Cassandra's partitioning allows it to automatically repartition data as machines are dynamically added and removed from the cluster.
{{< /callout >}}



## Related Tools


- [ScyllaDB](/tools/scylladb/)

- [HBase](/tools/hbase/)

- [MongoDB](/tools/mongodb/)
