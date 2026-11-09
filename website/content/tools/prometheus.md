---
cncf_status: graduated
date: '2026-11-09T22:36:44.667796Z'
description: Prometheus is a cloud-native systems and service monitoring system that collects metrics, evaluates rule expressions, and can trigger alerts.
homepage_url: https://prometheus.io/
layout: single
letter: P
lifecycle_stage: tech_writing
project_name: Prometheus
repo_url: https://github.com/prometheus/prometheus
status: completed
title: Prometheus
---

## Overview

Prometheus is a cloud-native systems and service monitoring system that collects metrics, evaluates rule expressions, and can trigger alerts.

## Key Features

- A multi-dimensional data model (time series defined by metric name and set of key/value dimensions)
- PromQL, a powerful and flexible query language to leverage this dimensionality
- No dependency on distributed storage; single server nodes are autonomous
- An HTTP pull model for time series collection
- Pushing time series is supported via an intermediary gateway for batch jobs
- Targets are discovered via service discovery or static configuration
- Multiple modes of graphing and dashboarding support
- Support for hierarchical and horizontal federation

{{< callout title="Getting Started" type="code" >}}
```bash
docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus
```
{{< /callout >}}
