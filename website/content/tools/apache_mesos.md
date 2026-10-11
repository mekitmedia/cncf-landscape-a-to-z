---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.072971'
homepage_url: https://mesos.apache.org/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Apache Mesos
repo_url: https://github.com/apache/mesos
status: completed
title: Apache Mesos
---



## Overview

A distributed systems kernel that abstracts compute resources across clusters to enable efficient resource sharing among diverse frameworks.



## Key Features


- Two-level resource offer mechanism allowing frameworks to negotiate resources.

- Scalability to tens of thousands of nodes and hundreds of thousands of tasks.

- High availability control plane using Apache ZooKeeper.

- Native containerizer supporting Docker images and Linux cgroups.




## Use Cases

Heterogeneous cluster consolidation running Hadoop, Spark, and microservices on shared pools.



{{< callout title="Getting Started" type="code" >}}
```bash
Run via Docker images (`mesosphere/mesos-master`) to inspect two-level scheduling.
```
{{< /callout >}}



## Recent Updates

Maintenance updates and security patches for distributed resource orchestration.



{{< callout title="Did You Know?" type="info" >}}
Apache Mesos is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Kubernetes](/tools/kubernetes/)

- [HashiCorp Nomad](/tools/hashicorp_nomad/)

- [Apache Hadoop YARN](/tools/apache_hadoop_yarn/)
