---
title: Amazon Elastic Kubernetes Service Distro (Amazon EKS-D)
project_name: Amazon Elastic Kubernetes Service Distro (Amazon EKS-D)
date: 2026-11-05
layout: single
letter: A
lifecycle_stage: approved
status: completed
repo_url: https://github.com/aws/eks-distro
homepage_url: https://aws.amazon.com/eks/eks-distro
cncf_status: non-cncf
summary: Amazon EKS Distro (EKS-D) is a Kubernetes distribution based on and used by Amazon Elastic Kubernetes Service (EKS) to create reliable and secure Kubernetes clusters. It provides the same versions of Kubernetes and its dependencies deployed by Amazon EKS, including upstream updates and extended security patching support.
key_features:
- Provides the same software that powers thousands of clusters on Amazon EKS
- Includes the latest upstream Kubernetes updates
- Offers extended security patching support
- Follows the same Kubernetes version release cycle as Amazon EKS
- Everything required to build the components from source is included in the repository
recent_updates: Metrics-server and CSI sidecar projects are being deprecated from EKS-D (starting Jan 2025 and Mar 2025 respectively). EKS-D has discontinued support for Kubernetes v1.18 - v1.28, recommending users to update to supported versions (v1.29+).
use_cases: Creating reliable and secure Kubernetes clusters locally or on other infrastructures using the same Kubernetes versions and dependencies as Amazon EKS.
interesting_facts: EKS-D is the actual distribution powering tens of thousands of Kubernetes clusters on Amazon EKS.
get_started: Full documentation for releases can be found on https://distro.eks.amazonaws.com. You can download the release manifests directly from the repository or website to deploy the specific Kubernetes versions.
related_tools:
- Kubernetes
- Amazon EKS
---
