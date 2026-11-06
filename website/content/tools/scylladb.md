---
title: "ScyllaDB"
date: 2026-11-06T08:00:00Z
draft: false
layout: "single"
project_name: "ScyllaDB"
homepage_url: "https://github.com/scylladb/scylladb"
repo_url: "https://github.com/scylladb/scylladb"
cncf_status: "none"
letter: "S"
lifecycle_stage: "initial"
status: "completed"
summary: "Scylla is a real-time big data database that is API-compatible with Apache Cassandra and Amazon DynamoDB, embracing a shared-nothing approach for increased performance."
key_features:
  - "API compatibility with Apache Cassandra and Amazon DynamoDB."
  - "Shared-nothing architecture for increased throughput and storage capacity."
  - "Order-of-magnitude performance improvements and reduced hardware costs."
recent_updates: "Release scylla-2026.4.0-rc2-candidate-20261105094225."
use_cases: "Replacing Cassandra or DynamoDB setups for real-time big data workloads with reduced hardware costs and higher performance."
interesting_facts: "ScyllaDB is built to be fairly fussy about its build environment, requiring recent versions of the C++23 compiler, but offers a frozen toolchain Docker image for easy compilation."
get_started: "Run Scylla with Docker: `docker run --name scylla -d -p 8000:8000 scylladb/scylla:latest --alternator-port=8000 --alternator-write-isolation=always`"
related_tools:
  - "Alternator"
---

# ScyllaDB

Scylla is a real-time big data database that is API-compatible with Apache Cassandra and Amazon DynamoDB, embracing a shared-nothing approach for increased performance.
