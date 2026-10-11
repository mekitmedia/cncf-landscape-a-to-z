---
cncf_status: non-cncf
date: '2026-10-06T03:33:59.048114'
description: Open source framework works by rapidly transferring data between nodes.
  It's often used by companies who need to handle and store big data.
homepage_url: https://hadoop.apache.org/
layout: single
letter: H
lifecycle_stage: first_pass
project_name: Hadoop HDFS
repo_url: https://github.com/apache/hadoop
status: completed
title: Hadoop HDFS
---



## Overview

The Hadoop Distributed File System (HDFS) is a highly fault-tolerant distributed file system designed to run on commodity hardware, providing high throughput access to application data and suitable for applications with large data sets.



## Key Features


- Highly fault-tolerant and designed to be deployed on low-cost hardware.

- Provides high throughput access to application data, suited for batch processing rather than interactive use.

- Tuned to support large files, scaling to hundreds of nodes and tens of millions of files in a single instance.

- Simplifies data coherency issues with a write-once-read-many access model for files.




## Use Cases

HDFS is primary distributed storage used by Hadoop applications. A MapReduce application or a web crawler application fits perfectly with its write-once-read-many model.



{{< callout title="Getting Started" type="code" >}}
```bash
The command `bin/hdfs dfs -help` lists the commands supported by Hadoop shell to interact with HDFS.
```
{{< /callout >}}



## Recent Updates

The most recent tag is `release-3.5.0-RC2`, released in March 2026.



{{< callout title="Did You Know?" type="info" >}}
HDFS was originally built as infrastructure for the Apache Nutch web search engine project.
{{< /callout >}}



## Related Tools


- [Apache Spark](/tools/apache_spark/)

- [Apache Flink](/tools/apache_flink/)

- [Apache Hadoop](/tools/apache_hadoop/)
