---
cncf_status: non-cncf
date: '2026-11-05'
description: Amazon Elastic Kubernetes Service Distro (Amazon EKS-D) is a Kubernetes
  distribution based on and used by Amazon Elastic Kubernetes Service (EKS) to create
  reliable and secure Kubernetes clusters.
homepage_url: https://aws.amazon.com/eks/eks-distro
layout: single
letter: A
lifecycle_stage: tech_writing
project_name: Amazon Elastic Kubernetes Service Distro (Amazon EKS-D)
repo_url: https://github.com/aws/eks-distro
status: completed
title: Amazon Elastic Kubernetes Service Distro (Amazon EKS-D)
---



## Overview

Amazon EKS Distro (EKS-D) is a Kubernetes distribution based on and used by Amazon Elastic Kubernetes Service (EKS) to create reliable and secure Kubernetes clusters. It provides the same versions of Kubernetes and its dependencies deployed by Amazon EKS, including upstream updates and extended security patching support.



## Key Features


- Provides the same software that powers thousands of clusters on Amazon EKS

- Includes the latest upstream Kubernetes updates

- Offers extended security patching support

- Follows the same Kubernetes version release cycle as Amazon EKS

- Everything required to build the components from source is included in the repository




## Use Cases

Creating reliable and secure Kubernetes clusters locally or on other infrastructures using the same Kubernetes versions and dependencies as Amazon EKS.



{{< callout title="Getting Started" type="code" >}}
```bash
Full documentation for releases can be found on https://distro.eks.amazonaws.com. You can download the release manifests directly from the repository or website to deploy the specific Kubernetes versions.
```
{{< /callout >}}



## Recent Updates

Metrics-server and CSI sidecar projects are being deprecated from EKS-D (starting Jan 2025 and Mar 2025 respectively). EKS-D has discontinued support for Kubernetes v1.18 - v1.28.



{{< callout title="Did You Know?" type="info" >}}
EKS-D is the actual distribution powering tens of thousands of Kubernetes clusters on Amazon EKS.
{{< /callout >}}



## Related Tools


- [Kubernetes](/tools/kubernetes/)

- [Amazon EKS](/tools/amazon_eks/)


