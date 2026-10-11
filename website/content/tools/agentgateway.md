---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.121719'
description: Next Generation Agentic Proxy for AI Agents and MCP servers
homepage_url: https://agentgateway.dev/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Agentgateway
repo_url: https://github.com/agentgateway/agentgateway
status: completed
title: Agentgateway
---



## Overview

Agentgateway is an open source proxy built on AI-native protocols that provides drop-in security, observability, and governance for agent-to-LLM, agent-to-tool, and agent-to-agent communication.



## Key Features


- LLM Gateway: Route traffic to major LLM providers through a unified OpenAI-compatible API with budget controls, load balancing, and failover.

- MCP Gateway: Connect LLMs to tools and external data sources via MCP with tool federation, OpenAPI integration, and OAuth authentication.

- A2A Gateway: Secure agent-to-agent communication using A2A with capability discovery and task collaboration.

- Inference Routing: Intelligent routing to self-hosted models using Kubernetes Inference Gateway extensions based on GPU utilization, KV cache, and queue depth.

- Guardrails: Multi-layered content filtering with regex, OpenAI moderation, AWS Bedrock Guardrails, Google Model Armor, and custom webhooks.

- Security & Observability: Auth (JWT, API keys, OAuth), fine-grained RBAC with CEL policy engine, rate limiting, TLS, and OpenTelemetry metrics/logs/tracing.




## Use Cases

Routing and securing traffic between AI agents, LLMs, and external tools/services. Providing a unified gateway for agent-to-agent and agent-to-tool communications with embedded security, routing logic, and observability out-of-the-box.



{{< callout title="Getting Started" type="code" >}}
```bash
Check the standalone or Kubernetes quickstart guides on agentgateway.dev to deploy the proxy using a flat YAML config or the built-in Kubernetes controller.
```
{{< /callout >}}



## Recent Updates

Release v1.5.0 introduces numerous enhancements including support for forward proxy authentication, limit on authorized models per API key, connecting tunneling through dynamic proxy backends, and API-key scoped budgets for LLM traffic. It also includes UI fixes and various security refinements.



{{< callout title="Did You Know?" type="info" >}}
Agentgateway describes itself as the first complete connectivity solution for Agentic AI.
{{< /callout >}}



## Related Tools


- [Model Context Protocol (MCP)](/tools/model_context_protocol_(mcp)/)

- [Envoy Proxy](/tools/envoy_proxy/)
