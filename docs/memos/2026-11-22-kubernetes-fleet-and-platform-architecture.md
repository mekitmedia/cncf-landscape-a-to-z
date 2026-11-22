# Internal Editorial Memo: Modern Kubernetes Fleet & Platform Architecture

- **Date**: 2026-11-22
- **Status**: Seed / Idea Backlog
- **Target Projects**:
  - [Cozystack](https://cozystack.io/) (`cozystack/cozystack`) — CNCF Sandbox
  - [Clusterpedia](https://clusterpedia.io/) (`clusterpedia-io/clusterpedia`) — CNCF Sandbox
  - [Clusternet](https://clusternet.io/) (`clusternet/clusternet`) — CNCF Sandbox
  - [Capsule](https://projectcapsule.dev/) (`projectcapsule/capsule`) — CNCF Sandbox
- **Core Theme**: Next-generation Kubernetes infrastructure platforms: from bare-metal cloud provisioning to hierarchical multi-tenancy, edge fleet dispatch, and cross-cluster resource discovery.

---

## 1. Why These 4 Tools Belong Together

A common challenge in platform engineering is balancing **cost**, **isolation**, and **scale**:
- Giving every team a dedicated Kubernetes cluster leads to cluster sprawl, high control-plane overhead, and fragmented management.
- Cramming all workloads into a single flat cluster creates security risks, noisy neighbor issues, and operational bottlenecks.
- Managing geographically dispersed or edge clusters makes querying and observability painfully slow and complex.

These 4 tools form a complete, end-to-end open-source platform stack addressing every layer of this challenge:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        4. Unified Fleet Discovery                      │
│      Clusterpedia (Global Search, OpenAPI-compatible Aggregated API)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────┴────────────────────────────────────┐
│                        3. Fleet Dispatch & Scheduling                  │
│        Clusternet (Push/Pull Multi-Cluster Orchestration & Edge)       │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
┌───────────────────┴───────────────┐  ┌─────────────┴───────────────────┐
│     Cluster A (Multi-Tenant)      │  │      Cluster B (Edge Fleet)     │
│  2. In-Cluster Tenancy: Capsule   │  │   2. Workload Nodes / Tenants   │
│  (Tenant CRD, Namespaces, Quotas) │  │                                 │
└───────────────────┬───────────────┘  └─────────────┬───────────────────┘
                    │                                │
┌───────────────────┴────────────────────────────────┴───────────────────┐
│                    1. Bare-Metal Cloud Platform / PaaS                 │
│       Cozystack (Managed K8s, KubeVirt VMs, LINSTOR/Ceph, REST API)    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tool Breakdown & Technical Highlights

### 1. [Cozystack](https://cozystack.io/) (Infrastructure Layer)
- **Repo**: [github.com/cozystack/cozystack](https://github.com/cozystack/cozystack)
- **CNCF Status**: Sandbox
- **What it does**: Turns bare-metal servers or commodity hardware into an intelligent private/public cloud platform using standard Kubernetes primitives.
- **Why it matters**: It provides out-of-the-box Kubernetes-as-a-Service, VM hosting via KubeVirt, Software-Defined Storage (LINSTOR / Ceph), and DBaaS without the heavyweight complexity of legacy OpenStack.
- **Angle to explore**: "Building your own AWS on bare metal with open-source cloud-native building blocks."

### 2. [Capsule](https://projectcapsule.dev/) (Tenancy & Isolation Layer)
- **Repo**: [github.com/projectcapsule/capsule](https://github.com/projectcapsule/capsule)
- **CNCF Status**: Sandbox
- **What it does**: Solves Kubernetes multi-tenancy without requiring a separate cluster per team or client.
- **Why it matters**: Groups multiple namespaces under a single `Tenant` abstraction. Tenant owners can self-serve namespaces without `cluster-admin` privileges, while cluster operators enforce aggregate resource quotas, allowed node selectors, ingress hostnames, and storage classes.
- **Angle to explore**: "Slaying cluster sprawl: How hierarchical multi-tenancy saves infrastructure bills while giving developers autonomy."

### 3. [Clusternet](https://clusternet.io/) (Fleet Orchestration Layer)
- **Repo**: [github.com/clusternet/clusternet](https://github.com/clusternet/clusternet)
- **CNCF Status**: Sandbox
- **What it does**: Coordinates and schedules applications across massive fleets of Kubernetes clusters spanning public clouds, private data centers, and edge devices.
- **Why it matters**: Supports both push and pull modes (critical for edge clusters behind NAT/firewalls) and schedules standard, unmodified Kubernetes manifests directly without forcing users into proprietary wrappers.
- **Angle to explore**: "Managing edge and hybrid cloud fleets like visiting the web: Scalable scheduling across thousands of disconnected nodes."

### 4. [Clusterpedia](https://clusterpedia.io/) (Fleet Discovery Layer)
- **Repo**: [github.com/clusterpedia-io/clusterpedia](https://github.com/clusterpedia-io/clusterpedia)
- **CNCF Status**: Sandbox
- **What it does**: The "Wikipedia for Kubernetes clusters" — a synchronized encyclopedia and multi-cluster resource search engine.
- **Why it matters**: Querying 50+ clusters with `kubectl` sequentially causes API timeouts and throttling. Clusterpedia synchronizes and indexes cluster resources into a pluggable database and serves them through a single OpenAPI-compatible endpoint. You can run complex cross-cluster queries, label selectors, and watches through familiar `kubectl` commands.
- **Angle to explore**: "Where is that pod? Querying and auditing 100 clusters with a single `kubectl` command."

---

## 3. Potential Content Formats & Editorial Angles

### Article / Video Idea 1: "The Self-Hosted Cloud Blueprint"
- **Format**: Architectural deep dive / Long-form guide
- **Hook**: How small-to-mid engineering teams can run their own resilient, multi-tenant cloud on bare metal or hybrid hosting without paying the hyperscaler tax.
- **Flow**: Cozystack for the hardware/cluster lifecycle $\rightarrow$ Capsule for internal team isolation $\rightarrow$ Clusternet for multi-region failover.

### Article / Video Idea 2: "Multi-Tenancy vs. Multi-Cluster: Stop Choosing, Do Both"
- **Format**: Practical comparison & design patterns
- **Hook**: When to isolate using namespaces (Capsule), when to spin up dedicated virtual clusters (vCluster), and when to go multi-cluster (Clusternet).
- **Key Takeaway**: Use Capsule *inside* regional clusters to maximize node density, and Clusternet *between* regions/edges for geographic resilience.

### Article / Video Idea 3: "Fleet Observability: Taming Multi-Cluster Chaos with Clusterpedia"
- **Format**: Hands-on tutorial
- **Hook**: Step-by-step setup integrating Clusternet and Clusterpedia to deploy across multiple clusters and search global resources using standard `kubectl`.

---

## 4. Hands-On Lab / Verification Ideas
- [ ] Spin up 3 local KinD / k3d clusters.
- [ ] Install Clusternet-hub on Cluster 1 and agents on Clusters 2 & 3.
- [ ] Deploy Capsule on Cluster 2 to configure two isolated tenants (`team-alpha`, `team-beta`).
- [ ] Connect Clusterpedia to index all resources across both worker clusters and verify querying via `kubectl --cluster=clusterpedia get pods -A`.
