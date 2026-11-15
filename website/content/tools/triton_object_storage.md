---
cncf_status: non-cncf
date: '2026-11-10T21:00:40.213269Z'
homepage_url: https://www.tritondatacenter.com/triton/object-storage
layout: single
letter: T
lifecycle_stage: tech_writing
project_name: Triton Object Storage
repo_url: https://github.com/TritonDataCenter/manta
status: completed
title: Triton Object Storage
---



## Overview

Manta is an HTTP-based distributed object storage system that is open source and scalable, containing all the components needed to deploy and run it.



## Key Features


- Scalable, distributed object store

- HTTP-based REST API

- Strong consistency and high availability

- Delegates to ZFS for data storage on disk

- Scales horizontally in every dimension




## Use Cases

Storing and managing large scale object data using an HTTP interface while maintaining strong consistency.



{{< callout title="Getting Started" type="code" >}}
```bash
sdc-imgadm import -m /var/tmp/my_manifest.json -f /var/tmp/my_image
```
{{< /callout >}}





{{< callout title="Did You Know?" type="info" >}}
Manta delegates to ZFS to solve the single-system data storage problem, storing block checksums separately from blocks.
{{< /callout >}}



