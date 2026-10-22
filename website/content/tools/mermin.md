---
cncf_status: non-cncf
date: '2026-10-22T02:09:08.375627'
description: Mermin is a Kubernetes-native network observability tool that uses eBPF
  exports OpenTelemetry Flow Traces, to provide deep visibility into your cluster’s
  network communications with zero application changes required.
homepage_url: https://github.com/elastiflow/mermin
layout: single
letter: M
lifecycle_stage: first_pass
project_name: Mermin
repo_url: https://github.com/elastiflow/mermin
status: completed
title: Mermin
---



## Overview

Mermin is a powerful, Kubernetes-native network observability tool that utilizes eBPF to capture network traffic efficiently and exports it as Flow Traces through the OpenTelemetry Protocol (OTLP). It offers comprehensive visibility into cluster network communications without requiring any changes to the application code.



## Key Features


- Uses eBPF to auto-instrument the network layer without sidecars or application changes.

- Captures granular, bidirectional network flows instead of just aggregated metrics or full packet captures.

- Enriches flows with native Kubernetes metadata, showing communications between Pods, Services, and Deployments.

- Exports network traffic as standard OpenTelemetry Flow Traces via OTLP to seamlessly integrate with existing observability backends.

- Deploys simply as a DaemonSet for low-overhead, kernel-level traffic capture suitable for always-on production environments.




## Use Cases

Ideal for bridging the gap between application performance monitoring and IP-level network statistics, allowing teams to correlate slow network spans in traces with actual network flow data and pinpoint network congestion back to specific services.



{{< callout title="Getting Started" type="code" >}}
```bash
Deploy Mermin via Helm using `helm repo add elastiflow https://elastiflow.github.io/mermin` followed by `helm install mermin elastiflow/mermin --namespace mermin --create-namespace`.
```
{{< /callout >}}



## Recent Updates

Mermin aggregates packets into flows with connection state tracking and enriches them with Kubernetes context before converting them to OpenTelemetry trace spans.



{{< callout title="Did You Know?" type="info" >}}
Mermin's approach to network observability sits in a 'sweet spot'—it avoids the high storage and querying costs of raw PCAP files while providing the rich connection context (like timing and directionality) that simple network metrics lack.
{{< /callout >}}



## Related Tools


- [Jaeger](/tools/jaeger/)

- [Tempo](/tools/tempo/)

- [Istio](/tools/istio/)
