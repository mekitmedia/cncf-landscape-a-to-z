---
cncf_status: non-cncf
date: '2026-10-25T01:59:28.203301'
description: Parseable is an open source, column-oriented data lake platform purpose-built
  for observability. It stores telemetry in Apache Parquet on object storage and provides
  SQL and PromQL queries, along with major observability features like agent observability,
  alerting, dashboards, anomaly detection, and APM, all within a single binary.
homepage_url: https://www.parseable.io
layout: single
letter: P
lifecycle_stage: tech_writing
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


