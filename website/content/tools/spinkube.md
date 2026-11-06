---
title: "SpinKube"
date: "2024-03-12"
layout: "single"
letter: "S"
lifecycle_stage: "first_pass"
status: "completed"
project_name: "SpinKube"
homepage_url: "https://www.spinkube.dev/"
repo_url: "https://github.com/spinframework/spin-operator"
cncf_status: "sandbox"
summary: "Spin Operator is an open-source project that enables deploying Spin applications to Kubernetes by watching SpinApp Custom Resources and realizing their desired state."
key_features:
  - "Custom Resource Definitions (CRDs) for SpinApp and SpinAppExecutor"
  - "Built using the Kubebuilder framework"
  - "Provides webhook support with cert-manager integration"
recent_updates: "The project uses k3d for a lightweight Kubernetes distribution that runs on Docker for local development."
use_cases: "Deploying and managing WebAssembly (Spin) applications natively within a Kubernetes cluster."
interesting_facts: "SpinKube can be run locally using k3d or deployed to a remote Kubernetes cluster for production use cases."
get_started: "To run a local development environment, use `k3d cluster create wasm-cluster` with the specified container image and install the CRDs using `make install`."
related_tools: []
---

Spin Operator is an open-source project that enables deploying Spin applications to Kubernetes by watching SpinApp Custom Resources and realizing their desired state.

### Key Features
- Custom Resource Definitions (CRDs) for SpinApp and SpinAppExecutor
- Built using the Kubebuilder framework
- Provides webhook support with cert-manager integration

### Use Cases
Deploying and managing WebAssembly (Spin) applications natively within a Kubernetes cluster.
