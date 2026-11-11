---
cncf_status: non-cncf
date: '2026-11-07T23:53:10.351931Z'
description: MockServer mocks, records, and chaos-tests any HTTP(S) dependency your application talks to — one binary, no per-protocol setup.
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

MockServer mocks, records, and chaos-tests any HTTP(S) dependency your application talks to — one binary, no per-protocol setup.

## Key Features

- One port, every protocol — HTTP/1.1, HTTPS, HTTP/2, gRPC & gRPC-Web, WebSockets and raw TCP are auto-detected from the first bytes of each connection.
- Mock, proxy, or both — return canned/templated/callback responses, or sit as a proxy (port forwarding, HTTP proxy, HTTPS tunneling, SOCKS) and record, inspect, and modify real traffic in flight
- Chaos engineering built in — inject latency, dropped connections, and errors on demand to see how your application copes when a dependency misbehaves.
- Mock AI too — chat-completion APIs for OpenAI, Anthropic, Gemini, Bedrock, Azure OpenAI and Ollama (including streaming), plus a built-in MCP server so AI coding assistants can drive MockServer directly.
- Generate mocks, don't hand-write them — from an OpenAPI/Swagger spec
- Fits your stack — Java, JavaScript/Node, Python, Ruby, Go, .NET, Rust, and PHP clients, plus JUnit and Spring support

## Use Cases

Mocking and recording HTTP(S) dependencies, chaos testing applications, generating mocks from OpenAPI specifications, and proxying traffic to inspect TLS-encrypted exchanges.

{{< callout title="Getting Started" type="code" >}}
```bash
brew install mockserver
mockserver run --port 1080
```
{{< /callout >}}

{{< callout title="Did You Know?" type="info" >}}
MockServer supports mocking AI chat-completion APIs and includes a built-in MCP server so AI coding assistants can drive MockServer directly.
{{< /callout >}}
