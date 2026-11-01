---
cncf_status: non-cncf
date: '2026-11-01T10:44:09.994107'
description: Mocking, debugging proxy and chaos engineering for HTTP, gRPC, GraphQL,
  LLM, MCP, Kafka, TCP and more.
homepage_url: https://www.mock-server.com
layout: single
letter: M
lifecycle_stage: tech_writing
project_name: MockServer
repo_url: https://github.com/mock-server/mockserver-monorepo
status: completed
title: MockServer
---



## Overview

MockServer allows you to mock, record, and chaos-test HTTP(S) dependencies, acting as either a mock server or proxy without requiring per-protocol configurations.



## Key Features


- Universal Protocol Support: Automatically handles HTTP/1.1, HTTPS, HTTP/2, gRPC, and WebSockets on a single port.

- Mocking & Proxying: Return custom responses or proxy traffic to inspect and alter requests in-flight.

- Built-in Chaos Engineering: Inject delays, connection drops, and random errors to evaluate resilience.

- Generative AI API Mocking: Native support for mocking chat-completion APIs from major AI providers like OpenAI and Anthropic.




## Use Cases

Useful for mocking out third-party APIs during development and executing chaos tests against remote microservices.



{{< callout title="Getting Started" type="code" >}}
```bash
Run the official Docker container locally via: docker run -d --rm -p 1080:1080 mockserver/mockserver
```
{{< /callout >}}



## Recent Updates

See the changelog for details on what shipped in recent versions.



{{< callout title="Did You Know?" type="info" >}}
MockServer includes an MCP server so AI coding assistants can drive MockServer directly.
{{< /callout >}}



