---
cncf_status: sandbox
date: '2026-10-04T18:37:38.825414'
description: Apicurio Registry is an open-source registry for API and schema artifacts
  (OpenAPI, AsyncAPI, Avro, Protobuf, JSON Schema, GraphQL and more) and AI agent
  artifacts (A2A Agent Cards, MCP tool definitions, prompt templates, model schemas),
  with immutable versioning, validity and compatibility rules, role-based access control,
  and standards-based discovery through AI Catalog and ARD well-known endpoints.
homepage_url: https://www.apicur.io
layout: single
letter: A
lifecycle_stage: tech_writing
project_name: Apicurio Registry
repo_url: https://github.com/Apicurio/apicurio-registry
status: completed
title: Apicurio Registry
---



## Overview

A CNCF sandbox schema and API registry providing centralized management, storage, and evolution tracking for schemas and API contracts.



## Key Features


- Comprehensive format support: OpenAPI, AsyncAPI, Avro, Protobuf, JSON Schema, GraphQL.

- Schema validation and compatibility rules preventing breaking changes in event streams.

- Pluggable storage backends (PostgreSQL, Kafka Streams, In-Memory).

- Integration with Kafka client serializers/deserializers (SerDes).




## Use Cases

Managing schema evolution in event-driven Kafka architectures and governing enterprise API contracts.



{{< callout title="Getting Started" type="code" >}}
```bash
Run via Docker: `docker run -it -p 8080:8080 apicurio/apicurio-registry-mem:latest`.
```
{{< /callout >}}



## Recent Updates

Apicurio Registry 3.0 modernized UI and decoupled storage connector architecture.



{{< callout title="Did You Know?" type="info" >}}
Apicurio Registry is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Confluent Schema Registry](/tools/confluent_schema_registry/)

- [Buf](/tools/buf/)

- [SchemaHero](/tools/schemahero/)
