# Research Note: Flux D2 Reference Architecture

## Overview
The Flux D2 architecture introduces the concept of **Gitless GitOps**, transitioning from reconciling manifests hosted directly in Git repositories to using **OCI (Open Container Initiative) Artifacts** stored in container registries. These artifacts are built from manifests tracked in Git during the Continuous Integration (CI) process.

## Key Advantages of OCI Artifacts (Gitless GitOps)
- **Enhanced Security & Access Control**: Leverages workload identities (e.g., GitHub Actions OIDC, AWS IAM roles) instead of persistent secrets or Personal Access Tokens (PATs) for downloading manifests, preventing direct interaction between Kubernetes clusters and Git manifests.
- **Rich Metadata & Provenance**: OCI artifacts natively support attaching metadata like signatures, Software Bill of Materials (SBOMs), and Vulnerability Exploitability eXchange (VEX) documents.
- **Improved Verification**: Flux's `OCIRepository` can be configured to verify signed OCI artifacts (e.g., using cosign). This decouples manifest signature verification from source authenticity verification (which is handled by a hardened CI workflow).
- **Reduced Control Duplication**: OCI is the standard for containers; using it for configurations unifies technologies and practices for software distribution.

## Repository Structure
The D2 Reference Architecture splits desired state across three primary repositories, which will be published as OCI artifacts:
1. **`d2-fleet`**: Defines the desired state of the Kubernetes clusters and tenants in the fleet.
2. **`d2-infra`**: Defines the desired state of the cluster add-ons and the monitoring stack.
3. **`d2-apps`**: Defines the desired state of the applications deployed across environments.

## Conclusion
Moving towards the D2 Reference Architecture will significantly harden our deployment pipeline. By utilizing OCI artifacts built via trusted CI pipelines, we can take advantage of workload identity federation and cosign signatures to ensure only verified, authentic manifests are reconciled by Flux in our clusters.
