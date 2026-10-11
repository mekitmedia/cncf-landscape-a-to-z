---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.666030'
description: Enterprise-grade, commercial-friendly agentic workflow platform for building
  next-generation SuperAgents with multi-agent orchestration capabilities.
homepage_url: http://astron.ai/
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Astron Agent
repo_url: https://github.com/iflytek/astron-agent
status: completed
title: Astron Agent
---



## Overview

Astron Agent is an enterprise-grade, commercial-friendly agentic workflow development platform that integrates AI workflow orchestration, model management, AI and MCP tool integration, RPA automation, and team collaboration features.



## Key Features


- AI workflow orchestration and model management

- AI and MCP tool integration

- Native intelligent RPA integration for connecting enterprise systems

- High-availability deployment architecture

- Enterprise-grade open ecosystem compatible with various industry models




## Use Cases

Building scalable, production-ready intelligent agent applications. Orchestrating complex multi-agent workflows. Automating enterprise processes using intelligent RPA. Developing AI foundation for organizations with team collaboration.



{{< callout title="Getting Started" type="code" >}}
```bash
Deploy using Docker Compose: `git clone https://github.com/iflytek/astron-agent.git && cd docker/astronAgent && docker compose -f docker-compose-with-auth.yaml up -d`. Access the Casdoor Admin Interface at `http://localhost:8000` (default login: admin/123). Access the Application Frontend at `http://localhost/`
```
{{< /callout >}}



## Recent Updates

Released v1.1.2 Security Release addressing unsafe workflow code-node execution. Migrated to built-in isolated LangChain/Pyodide executor by default for local code execution. Added Langfuse integration and end-to-end agent traces. Strengthened authentication on internal Workflow and Tenant service APIs.



{{< callout title="Did You Know?" type="info" >}}
Built on the same core technology as the iFLYTEK Astron Agent Platform. Deeply compatible with Model Context Protocol (MCP) and various industry models. Released under the permissive Apache 2.0 License allowing free commercial use.
{{< /callout >}}



## Related Tools


- [SkillHub](/tools/skillhub/)

- [AstronRPA](/tools/astronrpa/)

- [LangChain](/tools/langchain/)

- [Casdoor](/tools/casdoor/)
