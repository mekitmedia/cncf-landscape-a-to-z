---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.753244'
homepage_url: https://rocketmq.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache RocketMQ
repo_url: https://github.com/apache/rocketmq
status: completed
title: Apache RocketMQ
---



## Overview

A distributed messaging and streaming data platform offering low latency, high throughput, high reliability, and ultra-large capacity.



## Key Features


- Strict message ordering and transactional message guarantees.

- Massive topic scalability supporting tens of thousands of topics per cluster.

- Configurable message delay and scheduled delivery.

- High availability with automatic failover via DLedger (Raft).




## Use Cases

High-volume e-commerce order processing, financial event messaging, and real-time streaming ETL.



{{< callout title="Getting Started" type="code" >}}
```bash
Start NameServer (`mqnamesrv`) and Broker (`mqbroker -n localhost:9876`) to publish messages.
```
{{< /callout >}}



## Recent Updates

RocketMQ 5.0 introduced stateless proxy architecture and unified stream-message processing.



{{< callout title="Did You Know?" type="info" >}}
Apache RocketMQ is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Apache Kafka](/tools/apache_kafka/)

- [RabbitMQ](/tools/rabbitmq/)

- [Apache Pulsar](/tools/apache_pulsar/)
