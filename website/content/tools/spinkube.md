---
cncf_status: sandbox
date: '2024-03-12'
description: Open source platform for efficiently running (containerless) Spin-based
  WebAssembly (Wasm) applications on Kubernetes.
homepage_url: https://www.spinkube.dev/
layout: single
letter: S
lifecycle_stage: tech_writing
project_name: SpinKube
repo_url: https://github.com/spinframework/spin-operator
status: completed
title: SpinKube
---



## Overview

Spin Operator is an open-source project that enables deploying Spin applications to Kubernetes by watching SpinApp Custom Resources and realizing their desired state.



## Key Features


- Custom Resource Definitions (CRDs) for SpinApp and SpinAppExecutor

- Built using the Kubebuilder framework

- Provides webhook support with cert-manager integration




## Use Cases

Deploying and managing WebAssembly (Spin) applications natively within a Kubernetes cluster.



{{< callout title="Getting Started" type="code" >}}
```bash
To run a local development environment, use `k3d cluster create wasm-cluster` with the specified container image and install the CRDs using `make install`.
```
{{< /callout >}}



## Recent Updates

The project uses k3d for a lightweight Kubernetes distribution that runs on Docker for local development.



{{< callout title="Did You Know?" type="info" >}}
SpinKube can be run locally using k3d or deployed to a remote Kubernetes cluster for production use cases.
{{< /callout >}}



