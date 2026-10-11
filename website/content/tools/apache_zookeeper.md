---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.653766'
homepage_url: https://zookeeper.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache Zookeeper
repo_url: https://github.com/apache/zookeeper
status: completed
title: Apache Zookeeper
---



## Overview

A centralized service for maintaining configuration information, naming, providing distributed synchronization, and group services across distributed systems.



## Key Features


- Hierarchical key-value namespace structured like a filesystem (znodes).

- Zab (ZooKeeper Atomic Broadcast) consensus ensuring sequential consistency.

- Watch mechanisms notifying clients asynchronously of data changes.

- Ephemeral and sequential nodes enabling distributed locks and leader election.




## Use Cases

Leader election in distributed databases, cluster membership tracking, and configuration management.



{{< callout title="Getting Started" type="code" >}}
```bash
Configure `zoo.cfg`, start via `./bin/zkServer.sh start`, and test with `./bin/zkCli.sh`.
```
{{< /callout >}}



## Recent Updates

ZooKeeper 3.9 added TLS certificate auto-reloading and Prometheus metrics integration.



{{< callout title="Did You Know?" type="info" >}}
Apache Zookeeper is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [etcd](/tools/etcd/)

- [Consul](/tools/consul/)

- [Chubby](/tools/chubby/)
