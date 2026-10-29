---
cncf_status: non-cncf
date: '2026-10-25T01:59:28.203301'
description: Parseable is a free and open source log storage and observability platform.
  Written in Rust, Parseable can be deployed on natively on Kubernetes. It ingests
  log data via HTTP POST calls and exposes a query API to search and analyze logs.
  It is compatible with logging agents like FluentBit, LogStash, FileBeat among others.
homepage_url: https://www.parseable.io
layout: single
letter: P
lifecycle_stage: first_pass
project_name: Parseable
repo_url: https://github.com/parseablehq/parseable
status: completed
title: Parseable
---



## Overview

Parseable is an open source, columnar data lake platform purpose-built for observability.



## Key Features


- Data lake architecture with stateless compute over object storage

- Fully featured with alerting, dashboards, anomaly detection, and APM in a single binary

- Agent ready with support for both AI agents and LLMs

- OpenTelemetry native with no custom plugins required




## Use Cases

Sending logs, metrics, and traces via popular logging agents, OpenTelemetry, Kafka, eBPF, or other integrations, and utilizing native observability features like PromQL & SQL within a single binary.



{{< callout title="Getting Started" type="code" >}}
```bash
Download and run the Parseable binary on your laptop:

```bash
curl -fsSL https://logg.ing/install | bash
```

```
{{< /callout >}}



## Recent Updates

Added process CPU limit metric, aborted hot-tier tasks on tenant deletion, added checklist to home API, fixed failed alert evaluation, added tool executer API for external MCP server, and exposed read-only tools.



{{< callout title="Did You Know?" type="info" >}}
Parseable operates as a single binary, providing a fully featured observability platform without needing to stitch together multiple tools.
{{< /callout >}}



## Related Tools


- [OpenTelemetry](/tools/opentelemetry/)

- [Kafka](/tools/kafka/)
