---
cncf_status: non-cncf
date: '2026-10-29T03:09:19.674453+00:00'
description: KubeLinter analyzes Kubernetes YAML files, Helm charts, and Kustomize manifests, and checks them against a variety of best practices, with a focus on production readiness and security.
homepage_url: https://docs.kubelinter.io/
layout: single
letter: K
lifecycle_stage: first_pass
project_name: KubeLinter
repo_url: https://github.com/stackrox/kube-linter
status: completed
title: KubeLinter
---

## Overview

KubeLinter analyzes Kubernetes YAML files, Helm charts, and Kustomize manifests, and checks them against a variety of best practices, with a focus on production readiness and security.

## Key Features

- Analyzes Kubernetes YAML files, Helm charts, and Kustomize manifests
- Runs sensible default checks for security misconfigurations and DevOps best practices
- Configurable to enable, disable, and create custom checks depending on organizational policies
- Reports recommendations for how to resolve potential issues when a lint check fails
- Supports generating multiple output formats (e.g., SARIF, JSON) in a single run

## Use Cases

Teams checking early and often for security misconfigurations and DevOps best practices in their Kubernetes deployments.

{{< callout title="Getting Started" type="code" >}}
```bash
Run `kube-linter lint /path/to/your/yaml.yaml` to test your YAML files.
```
{{< /callout >}}

## Recent Updates

Supports generating multiple output formats in a single run. Created by StackRox and powered by Red Hat.

{{< callout title="Did You Know?" type="info" >}}
KubeLinter returns a non-zero exit code when a lint check fails. It was created by StackRox and is now powered by Red Hat.
{{< /callout >}}
