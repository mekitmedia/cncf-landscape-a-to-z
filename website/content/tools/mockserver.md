---
title: MockServer
date: 2026-11-01
layout: single
letter: M
lifecycle_stage: initial
status: pending
project_name: MockServer
homepage_url: https://www.mock-server.com
repo_url: https://github.com/mock-server/mockserver-monorepo
cncf_status: non-cncf
summary: MockServer allows you to mock, record, and chaos-test HTTP(S) dependencies, acting as either a mock server or proxy without requiring per-protocol configurations.
key_features:
  - 'Universal Protocol Support: Automatically handles HTTP/1.1, HTTPS, HTTP/2, gRPC, and WebSockets on a single port.'
  - 'Mocking & Proxying: Return custom responses or proxy traffic to inspect and alter requests in-flight.'
  - 'Built-in Chaos Engineering: Inject delays, connection drops, and random errors to evaluate resilience.'
  - 'Generative AI API Mocking: Native support for mocking chat-completion APIs from major AI providers like OpenAI and Anthropic.'
recent_updates: See the changelog for details on what shipped in recent versions.
use_cases: Useful for mocking out third-party APIs during development and executing chaos tests against remote microservices.
interesting_facts: MockServer includes an MCP server so AI coding assistants can drive MockServer directly.
get_started: "Run the official Docker container locally via: docker run -d --rm -p 1080:1080 mockserver/mockserver"
related_tools:
  - ""
---
