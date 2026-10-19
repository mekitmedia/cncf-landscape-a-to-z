---
cncf_status: non-cncf
date: '2026-10-19T02:10:36.948997'
description: 'SpiceDB is an open source database optimized for storing and querying
  authorization data. SpiceDB sets the standard for scalable authorization by remaining
  true to the design of the system powering permissions at Google: Zanzibar. While
  SpiceDB is a general purpose solution, it is often used to secure access to Retrieval-Augmented
  Generation (RAG) systems for AI workloads.

  '
homepage_url: https://authzed.com/spicedb
layout: single
letter: S
lifecycle_stage: tech_writing
project_name: SpiceDB
repo_url: https://github.com/authzed/spicedb
status: completed
title: SpiceDB
---



## Overview

SpiceDB is an open source authorization system inspired by Google's Zanzibar, offering a mature and scalable solution.



## Key Features


- Built by cloud-native ecosystem pioneers, offering robust engineering

- Mature, feature-complete implementation based on Google's Zanzibar paper

- Highly scalable to millions of queries per second with a 5ms p95 latency

- Per-request consistency configuration ensuring both correctness and performance

- Supports caveated relationships, blending ABAC and ReBAC concepts

- Schema design tooling with real-time validation for CI/CD pipelines

- Reverse indexing functionality to query subject permissions and resource accessibility




## Use Cases

Platform and product teams use SpiceDB to definitively answer access control questions like whether a specific subject can perform a certain action on a given resource.



{{< callout title="Getting Started" type="code" >}}
```bash
docker run --rm -p 50051:50051 -p 8443:8443 authzed/spicedb serve --http-enabled true --grpc-preshared-key "somerandomkeyhere"
```
{{< /callout >}}



## Recent Updates

SpiceDB v1.56.2 was released on 2026-09-11



{{< callout title="Did You Know?" type="info" >}}
The original inspiration for SpiceDB came from Google's 2019 paper on Zanzibar, their globally consistent authorization system.
{{< /callout >}}



## Related Tools


- [kubernetes](/tools/kubernetes/)
