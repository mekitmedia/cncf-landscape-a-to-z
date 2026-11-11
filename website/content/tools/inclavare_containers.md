---
cncf_status: sandbox
date: '2026-11-09T00:00:00Z'
description: Inclavare Containers provides a novel container runtime designed to launch protected containers using hardware-assisted Trusted Execution Environments (TEEs), also known as Enclaves. This approach safeguards sensitive workloads from untrusted entities like Cloud Service Providers (CSPs), ensuring confidential assets remain protected while in use.
homepage_url: https://github.com/inclavare-containers/
layout: single
letter: I
lifecycle_stage: tech_writing
project_name: Inclavare Containers
repo_url: https://github.com/inclavare-containers/inclavare-containers
status: completed
title: Inclavare Containers
---

## Overview

Inclavare Containers provides a novel container runtime designed to launch protected containers using hardware-assisted Trusted Execution Environments (TEEs), also known as Enclaves. This approach safeguards sensitive workloads from untrusted entities like Cloud Service Providers (CSPs), ensuring confidential assets remain protected while in use.

## Key Features

- Confidential computing oriented. Provides a general design for the protection of tenant’s workload.
- Create the hardware-enforced isolation between tenant’s workload and privileged software controlled by CSP.
- Remove CSP from the Trusted Computing Base (TCB) of tenant in untrusted cloud.
- Construct the general attestation infrastructure to convince users to trust the workloads running inside TEE based on hardware assisted enclave technology.
- OCI-compliant. The component `rune` is fully compliant with OCI Runtime specification.
- Cloud platform agnostic. It can be deployed in any public cloud Kubernetes platform.

## Use Cases

Helping to keep tenants' confidential data secure so they feel confident that their data is not being exposed to CSP or their own insiders, and they can easily move their trusted applications to the cloud.

{{< callout title="Getting Started" type="code" >}}
```bash
sudo make install
```
{{< /callout >}}

{{< callout title="Did You Know?" type="info" >}}
Inclavare, pronounced as `[ˈinklɑveə]`, is the Latin etymology of the word `enclave`, which means to isolate the user's sensitive workload from the untrusted and uncontrollable infrastructure.
{{< /callout >}}
