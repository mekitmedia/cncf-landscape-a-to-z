---
cncf_status: non-cncf
date: '2026-10-13T22:46:33.105220'
description: Fortio is an open source load testing library, command-line tool, and
  server application written in Go. Originated as Istio's performance characterization
  tool (in particular proxy overhead), Fortio has evolved into a versatile tool for
  load testing and performance benchmarking of HTTP, gRPC, and TCP services. Among
  other options it enables users to generate a specified query-per-second (QPS) load
  and records detailed latency histograms, facilitating the analysis of performance
  metrics. The server component offers a straightforward web UI and REST API, allowing
  users to initiate tests and visualize results through graphical representations.
  Beyond load testing, Fortio provides server-side features akin to httpbin, including
  request echoing with headers, configurable latency or error responses, TCP echoing
  and proxying, HTTP fan-out, and support for gRPC echo and health checks. These capabilities
  make Fortio a versatile tool for debugging and testing high-performance services
  in cloud-native environments. As an organization set of git repositories, is also
  a growing set of reusable libraries for writing Cloud Native Go code and CLIs.
homepage_url: https://fortio.org/
layout: single
letter: F
lifecycle_stage: first_pass
project_name: Fortio
repo_url: https://github.com/fortio/fortio
status: completed
title: Fortio
---



## Overview

Fortio is a fast, small load testing library, command line tool, advanced echo server, and web UI written in Go. Originally created as Istio's load testing tool, it allows specifying a target query-per-second load and records execution time histograms and percentiles.



## Key Features


- Runs load testing at a specified query per second (qps) and records a histogram of execution time and calculates percentiles.

- Includes a simple web UI and REST API to trigger runs and see graphical representations of the results.

- Provides server-side features similar to httpbin for debugging, such as request echo back, TCP echoing, TCP proxying, and HTTP fan out.

- Functions as a reusable and embeddable Go library with minimal dependencies.




## Use Cases

Useful for benchmarking APIs, load testing web servers, and debugging service latency through its advanced echo server capabilities.



{{< callout title="Getting Started" type="code" >}}
```bash
Run the server via Docker with `docker run -p 8080:8080 -p 8079:8079 fortio/fortio server &` and initiate a test run using `docker run fortio/fortio load -logger-force-color http://www.google.com/`.
```
{{< /callout >}}



## Recent Updates

Fortio has released version v1.76.0 and now embeds the grol scripting language, accessible via `fortio script`.



{{< callout title="Did You Know?" type="info" >}}
The name Fortio comes from the Greek word φορτίο (fortio), which translates to load or burden. It originally started as Istio's load testing tool before graduating to an independent project.
{{< /callout >}}



## Related Tools


- [Istio](/tools/istio/)

- [httpbin](/tools/httpbin/)
