---
cncf_status: non-cncf
date: '2026-11-09T02:53:41.714692Z'
description: A configuration management system for platform engineering and other
  things
homepage_url: https://kapitan.dev/
layout: single
letter: K
lifecycle_stage: tech_writing
project_name: Kapitan
repo_url: https://github.com/kapicorp/kapitan
status: completed
title: Kapitan
---



## Overview

Kapitan is an open source configuration management tool for Kubernetes, Terraform, and complex infrastructure systems. It helps teams generate, organize, reuse, and validate configuration across environments using an inventory-driven model.



## Key Features


- Native secret management (GPG, HashiCorp Vault, AWS KMS, GCP KMS, Azure Key Vault)

- Remote dependencies (Git, HTTP, ORAS (OCI registry))

- GitOps-friendly: compiles to fully rendered, plain-text output

- Supports multiple templates (Jsonnet, Jinja2, Kadet, Helm, Kustomize, CUE)




## Use Cases

You manage the same application across many environments (dev, staging, prod, regions) and want a single source of truth, or you need to reuse configuration fragments across targets without copy-paste.



{{< callout title="Getting Started" type="code" >}}
```bash
git clone https://github.com/kapicorp/kapitan-reference.git kapitan-templates
cd kapitan-templates
./kapitan compile
```
{{< /callout >}}





{{< callout title="Did You Know?" type="info" >}}
Kapitan lets you model infrastructure configuration with reusable inventory classes and targets, then compile that data into manifests, scripts, documentation, and Terraform resources.
{{< /callout >}}



