---
cncf_status: non-cncf
date: '2026-10-04T18:37:39.269140'
homepage_url: https://arc.codes/docs/en/get-started/quickstart
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Architect
repo_url: https://github.com/architect/functions
status: completed
title: Architect
---



## Overview

A simple, declarative open-source framework for building serverless applications on AWS with fast local development and plain text architecture manifests.



## Key Features


- Concise `app.arc` manifest defining HTTP routes, scheduled jobs, queues, and tables in plain text.

- Fast local development sandbox simulating API Gateway, Lambda, and DynamoDB without Docker.

- Direct code generation into standard AWS CloudFormation templates with zero boilerplate.

- First-class support for JavaScript/TypeScript, Python, Ruby, and Go.




## Use Cases

Rapidly developing, testing, and deploying serverless web apps and event-driven APIs on AWS.



{{< callout title="Getting Started" type="code" >}}
```bash
Install via `npm i -g @architect/architect`, run `arc init myapp`, and launch `arc sandbox`.
```
{{< /callout >}}



## Recent Updates

Enhanced HTTP API support, Node.js ES modules, and fine-grained Lambda bundling.



{{< callout title="Did You Know?" type="info" >}}
Architect is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [AWS SAM](/tools/aws_sam/)

- [Serverless Framework](/tools/serverless_framework/)

- [SST](/tools/sst/)
