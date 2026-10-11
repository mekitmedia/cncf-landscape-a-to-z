---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.969401'
description: Graph database optimized for fast analysis and real-time data processing.
  It is provided as an extension to PostgreSQL.
homepage_url: https://age.apache.org/
layout: single
letter: A
lifecycle_stage: tech_writing
project_name: Apache AGE
repo_url: https://github.com/apache/age
status: completed
title: Apache AGE
---



## Overview

Apache AGE is a PostgreSQL Graph database extension that leverages graph data structures to analyze and use relationships and patterns in data. It adds graph data processing and analytics capability to relational databases.



## Key Features


- Provides graph database functionality as a PostgreSQL extension.

- Read and write graph data in nodes and edges within an existing relational database.

- Supports variable length and edge traversal algorithms.

- Uses its own set of SQL extensions, similar to Cypher, while allowing native SQL queries.




## Use Cases

Useful for those who want to leverage the flexibility of graph databases while maintaining PostgreSQL's advanced SQL querying capabilities and robust transaction support.



{{< callout title="Getting Started" type="code" >}}
```bash
Install as a PostgreSQL extension and begin modeling data as nodes and edges following the tutorial at https://age.apache.org/age-manual/master/intro/setup.html.
```
{{< /callout >}}



## Recent Updates

Compatible with PostgreSQL 16.



{{< callout title="Did You Know?" type="info" >}}
AGE stands for A Graph Extension. It transforms a standard relational PostgreSQL database into a powerful graph database without the need for a separate data store.
{{< /callout >}}



## Related Tools


- [PostgreSQL](/tools/postgresql/)

- [Neo4j](/tools/neo4j/)
