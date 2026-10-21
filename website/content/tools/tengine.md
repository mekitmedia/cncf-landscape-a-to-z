---
cncf_status: non-cncf
date: '2026-10-21T02:16:03.369895'
homepage_url: https://tengine.taobao.org/
layout: single
letter: T
lifecycle_stage: first_pass
project_name: Tengine
repo_url: https://github.com/alibaba/tengine
status: completed
title: Tengine
---



## Overview

Tengine is a high-performance web server and reverse proxy originated by Taobao, the largest e-commerce website in Asia.



## Key Features


- All features of nginx-1.31.5 are inherited, i.e., it is 100% compatible with nginx.

- HTTP/3 support (QUIC v1 and draft-29) with xquic, including connection management and multiplexing for lower latency and higher resilience to packet loss on unstable networks.

- NTLS/TLCP (dual-certificate TLS, GM/T 0024) support with the Chinese SM2/SM3/SM4 algorithms via Tongsuo.

- Dynamically configure the servers, locations and upstreams without reloading or restarting worker processes with tengine-ingress, the Kubernetes Ingress controller for Tengine.

- High-speed UDP transmission with kernel-bypass.

- Active health checks of upstream servers can be performed.

- Dynamic scripting language (Lua) support, which is very efficient and makes it easy to extend core functionalities.




## Use Cases

Serving as a high-performance web server and reverse proxy, Kubernetes Ingress controller, HTTP/3 and UDP load balancer, and for WAF implementation using input body filters.



{{< callout title="Getting Started" type="code" >}}
```bash
docker pull ghcr.io/alibaba/tengine:latest
```
{{< /callout >}}



## Recent Updates

Tengine-3.1.0 was released on 2023-10-27.



{{< callout title="Did You Know?" type="info" >}}
Tengine has proven to be very stable and efficient on some of the top 100 websites in the world, including taobao.com and tmall.com.
{{< /callout >}}



## Related Tools


- [nginx](/tools/nginx/)

- [kubernetes](/tools/kubernetes/)

- [tongsuo](/tools/tongsuo/)
