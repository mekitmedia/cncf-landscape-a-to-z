---
cncf_status: non-cncf
date: '2026-10-04T18:37:38.985232'
description: Amazon EKS Anywhere is a new deployment option for Amazon EKS that allows
  customers to create and operate Kubernetes clusters on customer-managed infrastructure,
  supported by AWS.
homepage_url: https://aws.amazon.com/eks/eks-anywhere
layout: single
letter: A
lifecycle_stage: tech_writing
project_name: Amazon Elastic Kubernetes Service Anywhere (Amazon EKS Anywhere)
repo_url: https://github.com/aws/eks-anywhere
status: completed
title: Amazon Elastic Kubernetes Service Anywhere (Amazon EKS Anywhere)
---



## Overview

An open-source deployment option from AWS that allows users to create and operate consistent on-premises Kubernetes clusters using Amazon EKS tooling.



## Key Features


- Consistent operational tooling and Kubernetes versions aligned with AWS EKS.

- Support for VMware vSphere, bare metal, Nutanix, and CloudStack.

- Integrated cluster lifecycle management using Cluster API (CAPI).

- Bundled components including Cilium CNI, CoreDNS, and Flux.




## Use Cases

Running regulated workloads on-premises while maintaining operational consistency with AWS cloud.



{{< callout title="Getting Started" type="code" >}}
```bash
Install `eksctl-anywhere` and run `eksctl anywhere create cluster`.
```
{{< /callout >}}



## Recent Updates

Expanded bare metal hardware validation and enhanced air-gapped installation support.



{{< callout title="Did You Know?" type="info" >}}
Amazon Elastic Kubernetes Service Anywhere (Amazon EKS Anywhere) is widely utilized across the cloud native and open source ecosystem.
{{< /callout >}}



## Related Tools


- [Amazon EKS-D](/tools/amazon_eks-d/)

- [Cluster API](/tools/cluster_api/)

- [KinD](/tools/kind/)


