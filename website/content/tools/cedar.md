---
cncf_status: sandbox
date: '2026-10-04T18:37:42.774046'
description: Cedar is an open source authorization policy language that enables developers
  to express fine-grained permissions as easy-to-understand policies enforced in their
  applications, and decouple access control from application logic. Cedar is designed
  to be ergonomic, fast, safe, and analyzable using automated reasoning. Cedar's simple
  and intuitive syntax supports common authorization use-cases with readable policies,
  naturally expressing concepts from role-based, attribute-based, and relation-based
  access control models. Cedar's policy structure enables authorization requests to
  be decided quickly. Its policy validator uses optional typing to help policy writers
  avoid mistakes, but not get in their way. Cedar's design has been finely balanced
  to allow for a sound, complete, and decidable logical encoding, which enables precise
  automated analysis of Cedar policies, e.g., to ensure that policy refactoring preserves
  existing permissions. Cedar's language specification has been formally verified
  using a theorem prover to satisfy key security properties like `deny trumps allow,`
  and its implementation in Rust undergoes rigorous differential random testing against
  its formal specification. By combining mathematical rigor with developer-friendly
  design, Cedar offers a practical approach to secure, maintainable authorization
  for modern applications.
homepage_url: https://cedarpolicy.com
layout: single
letter: C
lifecycle_stage: tech_writing
project_name: Cedar
repo_url: https://github.com/cedar-policy/cedar
status: completed
title: Cedar
---



## Overview

Cedar is an open-source policy language developed for defining and enforcing fine-grained access control across applications. It allows developers to decouple authorization logic from application code, supporting common models like Role-Based Access Control (RBAC) and Attribute-Based Access Control (ABAC).



## Key Features


- Expressive Language: Designed to natively support authorization concepts, making it straightforward to write policies for both simple and complex access control scenarios.

- Performant Evaluation: Optimized for speed and scalability, the authorization engine provides bounded latency for real-time access decisions.

- Analyzable Policies: Integration with Automated Reasoning tools allows developers to mathematically prove that security models operate as intended and analyze policies for potential optimization.




## Use Cases

Developers use Cedar to separate authorization policies from business logic, ensuring that access decisions can be independently verified, analyzed, and updated without requiring code changes.



{{< callout title="Getting Started" type="code" >}}
```bash
To get started, depend on the `cedar-policy` crate by running `cargo add cedar-policy`. You can also use the CLI to interact with Cedar.
```
{{< /callout >}}



## Recent Updates

The latest release (v4.13.0) introduces pre-built binaries for multiple platforms, an integrated `cedar license` subcommand, and significant performance optimizations to `EntityUid::from_str()` which parses and renders much faster.



{{< callout title="Did You Know?" type="info" >}}
Cedar includes a built-in validator that cross-checks policies against a declared authorization schema to catch inconsistencies early.
{{< /callout >}}



## Related Tools


- [Open Policy Agent (OPA)](/tools/open_policy_agent_(opa)/)

- [Zanzibar](/tools/zanzibar/)
