---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.591655'
homepage_url: https://avro.apache.org/
layout: single
letter: A
lifecycle_stage: tech_writing
project_name: Avro
repo_url: https://github.com/apache/avro
status: completed
title: Avro
---



## Overview

Apache Avro is a data serialization system that provides rich data structures, a compact, fast, binary data format, and simple integration with dynamic languages.



## Key Features


- Rich data structures defined using JSON.

- Compact, fast, binary data format.

- Container file format for storing persistent data.

- Remote procedure call (RPC).

- Simple integration with dynamic languages with no code generation required to read or write data files.




## Use Cases

Often used as the leading serialization format for record data and the first choice for streaming data pipelines, commonly integrating with Apache Hadoop and Apache Kafka.



{{< callout title="Getting Started" type="code" >}}
```bash
Get started by defining a schema in JSON format, then generate code or dynamically (de)serialize data using one of the many supported language SDKs (Java, Python, C++, etc).
```
{{< /callout >}}



## Recent Updates

The 1.12.2 release includes a broad round of hardening against malformed and adversarial input across the Java and Python SDKs, plus security fixes in C#, C++, and JavaScript.



{{< callout title="Did You Know?" type="info" >}}
Avro relies on schemas that are always present when data is read, permitting data to be written with no per-value overheads, making serialization both fast and small.
{{< /callout >}}



## Related Tools


- [Apache Hadoop](/tools/apache_hadoop/)

- [Apache Kafka](/tools/apache_kafka/)

- [Apache Thrift](/tools/apache_thrift/)
