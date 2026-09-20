---
cncf_status: non-cncf
date: '2026-09-20T21:46:43.958642'
description: APIClarity is a cloud API observability open-source project that provides
  functionality to discover and monitor any API traffic that interacts with modern
  applications and report suspected security weaknesses or possible abuses. Once an
  OpenAPI spec is either uploaded or reconstructed by APIClarity, it monitors for
  shadow and zombie APIs, Broken Functional-Level Authorization (BFLA), Broken Object-Level
  Authorization (BOLA), weak authentication, sensitive data leaks and data injection
  risks.
get_started: 'Install APIClarity in a Kubernetes cluster using Helm: `helm repo add
  apiclarity https://openclarity.github.io/apiclarity` followed by `helm install --values
  values.yaml --create-namespace apiclarity apiclarity/apiclarity -n apiclarity`.'
homepage_url: https://openclarity.io/
interesting_facts: Developed by Cisco (openclarity), APIClarity offers a modular architecture
  that supports a wide range of external traffic sources including Apigee X Gateway
  and BIG-IP LTM Load balancers.
key_features:
- OpenAPI automatic reconstruction based on observed API traffic
- Spec Diffs module to identify Shadow APIs, Zombie APIs, and specification deviations
- Trace Analyzer module to discover weak authentications, sensitive data leaks, and
  BOLA risks
- BFLA Detector to capture authorization models and identify Broken Function Level
  Authorization
- Fuzzer module to actively test API endpoints based on specifications
- Supports integrations with Istio Service Mesh, Kong, Tyk, Tap via DaemonSet, and
  OpenTelemetry
layout: single
letter: A
project_name: APIClarity
recent_updates: The project repository was archived by the owner on May 29, 2026,
  and is now read-only.
related_tools:
- Istio
- Kong
- Tyk
- OpenTelemetry
- Aserto
repo_url: https://github.com/openclarity/apiclarity
status: completed
summary: APIClarity is a cloud API observability open-source project that discovers
  and monitors API traffic, reporting suspected security weaknesses or possible abuses.
  It operates by capturing all API traffic or actively testing endpoints, and can
  automatically reconstruct OpenAPI specifications when none are available.
title: APIClarity
use_cases: Used by DevOps and DevSecOps teams to monitor modern applications for zombie
  APIs, shadow APIs, data injection risks, and various authorization vulnerabilities
  in Kubernetes environments.
---

This is an auto-generated tool page. For more details, see the [letter page](/letters/a/).
