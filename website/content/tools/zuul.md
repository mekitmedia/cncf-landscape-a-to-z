---
cncf_status: non-cncf
date: '2026-11-09T21:33:01.239963Z'
description: Zuul is an open source CI/CD and project gating system designed to assist developers in taking a change from proposal through deployment.
homepage_url: https://zuul-ci.org
layout: single
letter: Z
lifecycle_stage: tech_writing
project_name: Zuul
repo_url: https://opendev.org/zuul/zuul
status: completed
title: Zuul
---

## Overview

Zuul is an open source CI/CD and project gating system designed to assist developers in taking a change from proposal through deployment, testing the future state of code repositories.

## Key Features

- Project gating to prevent merging broken code
- CI/CD using Ansible playbooks
- Testing cross-project dependencies in parallel
- Multi-node environment testing and orchestration
- Integration with Gerrit and GitHub code review systems

## Use Cases

Maintaining evergreen builds by automatically merging changes only if they pass tests, and testing cross-project changes together.

{{< callout title="Getting Started" type="code" >}}
```bash
git clone https://opendev.org/zuul/zuul
cd zuul/doc/source/examples
docker compose -p zuul-tutorial up
```
{{< /callout >}}

{{< callout title="Did You Know?" type="info" >}}
Zuul's functionality now incorporates Nodepool, meaning it natively handles resource provisioning across various cloud providers.
{{< /callout >}}
