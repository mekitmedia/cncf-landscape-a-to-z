---
cncf_status: non-cncf
date: '2026-10-22T16:20:10.014524'
homepage_url: https://docs.prefect.io/
layout: single
letter: P
lifecycle_stage: tech_writing
project_name: Prefect
repo_url: https://github.com/PrefectHQ/prefect
status: completed
title: Prefect
---



## Overview

Prefect is a workflow orchestration framework for building resilient, dynamic data pipelines in Python, allowing teams to confidently automate data processes.



## Key Features


- Scheduling, caching, retries, and event-based automations

- Prefect flow and task decorators

- Self-hosted server or managed Prefect Cloud dashboard




## Use Cases

Building resilient data pipelines that react to the world around them and recover from unexpected changes, elevating simple Python scripts into production workflows.



{{< callout title="Getting Started" type="code" >}}
```bash
Prefect requires Python 3.11+. To install the latest version, run:

pip install -U prefect

Then create and run a Python file that uses Prefect `flow` and `task` decorators.

```
{{< /callout >}}



## Recent Updates

Added Python 3.15 support, dropped Python 3.10 support, and deprecated Pendulum datetime behavior on Python 3.11-3.12.



{{< callout title="Did You Know?" type="info" >}}
Prefect requires Python 3.11+ and provides simple Python decorators to orchestrate and observe your workflow.
{{< /callout >}}



## Related Tools


- [Apache Airflow](/tools/apache_airflow/)

- [Dagster](/tools/dagster/)

- [Luigi](/tools/luigi/)
