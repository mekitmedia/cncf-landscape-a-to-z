---
cncf_status: non-cncf
date: '2026-10-04T18:37:49.261732'
description: PolarDB is a cloud native SQL Database.
homepage_url: https://openpolardb.com/home
layout: single
letter: P
lifecycle_stage: tech_writing
project_name: PolarDB
repo_url: https://github.com/polardb/polardbx-sql
status: completed
title: PolarDB
---



## Overview

PolarDB-X is a cloud native distributed SQL Database designed for high concurrency, massive storage and complex querying scenarios. It has a shared-nothing architecture in which computing is decoupled from storage. It supports horizontal scaling, distributed transactions and Hybrid Transactional and Analytical Processing (HTAP) workloads, and is characterized by enterprise-class, cloud native, high availability, highly compatible with MySQL and its ecosystem.



## Key Features


- Horizontal Scalability: Designed with Shared-nothing architecture, supporting multiple Hash and Range data sharding algorithms and achieving transparent horizontal scaling through implicit primary key sharding and dynamic scheduling of data shard.

- Distributed Transactions: Adopts MVCC + TSO approach and 2PC protocol to implement distributed transactions. Transactions meet ACID characteristics, support RC/RR isolation levels, and achieve high performance through optimizations such as one-stage commit, read-only transaction, and asynchronous commit.

- HTAP: Supports analytical queries through native MPP capability, and achieves strong isolation of OLTP and OLAP traffic through CPU quota constraint, memory pooling, storage resource separation, etc.




## Use Cases

PolarDB-X is ideal for solving database scalability bottlenecks in core transaction systems, handling high concurrency, massive storage, and complex querying scenarios, as originally created for Alibaba Tmall's 'Double Eleven'.



{{< callout title="Getting Started" type="code" >}}
```bash
To get started with PolarDB-X, explore the documentation on the official website or repository, and use the K8S Operator for deployment.
```
{{< /callout >}}



## Recent Updates

Recent updates include externalized column storage (phase 1) to offload large LONGTEXT/LONGBLOB columns, various AI embedding and text-processing functions (AI_EMBEDDING, AI_EXTRACT, AI_TEXT2SQL), and an NL2SQL agent with conversation and transaction support.



{{< callout title="Did You Know?" type="info" >}}
PolarDB-X was originally created to solve the database's scalability bottleneck of Alibaba Tmall's 'Double Eleven' core transaction system.
{{< /callout >}}



## Related Tools


- [MySQL](/tools/mysql/)

- [TiDB](/tools/tidb/)

- [CockroachDB](/tools/cockroachdb/)
