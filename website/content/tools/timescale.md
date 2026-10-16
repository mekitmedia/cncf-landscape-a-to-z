---
cncf_status: non-cncf
date: '2026-10-15T02:23:08.019251'
description: PostgreSQL for time‑series. TimescaleDB is the leading open-source relational
  database for time-series data. Fully managed or self‑hosted.
homepage_url: https://www.timescale.com
layout: single
letter: T
lifecycle_stage: tech_writing
project_name: Timescale
repo_url: https://github.com/timescale/timescaledb
status: completed
title: Timescale
---



## Overview

TimescaleDB is a PostgreSQL extension for high-performance real-time analytics on time-series and event data.



## Key Features


- PostgreSQL extension designed for time-series and event data.

- Supports high-performance real-time analytics.

- Provides columnstore capabilities for hypertables.

- Offers instant analytical query performance.




## Use Cases

Ideal for handling IoT sensor data, event data, and requiring high-performance real-time analytics over time-series data.



{{< callout title="Getting Started" type="code" >}}
```bash
Start TimescaleDB locally using Docker:

docker run -d --name timescaledb \
    -p 6543:5432 \
    -e POSTGRES_PASSWORD=password \
    timescale/timescaledb-ha:pg18

Connect using psql:

psql -h localhost -p 6543 -U postgres

Create a hypertable:

CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    sensor_id TEXT NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    pressure DOUBLE PRECISION
) WITH (
    tsdb.hypertable
);

```
{{< /callout >}}



## Recent Updates

TimescaleDB release 2.30.2.



{{< callout title="Did You Know?" type="info" >}}
Exposes PostgreSQL on a non-standard port (6543) by default in local installations to avoid conflicts with existing PostgreSQL instances.
{{< /callout >}}
