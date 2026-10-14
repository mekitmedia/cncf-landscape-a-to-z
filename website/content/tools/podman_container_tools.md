---
cncf_status: sandbox
date: '2026-10-14T02:28:19.065749'
description: A set of tools providing full management of container lifecycle, including
  Podman, Buildah, and Skopeo, which manage containers and images without requiring
  a daemon or root privileges.
homepage_url: https://podman.io/
layout: single
letter: P
lifecycle_stage: first_pass
project_name: Podman Container Tools
repo_url: https://github.com/podman-container-tools/podman
status: completed
title: Podman Container Tools
---



## Overview

Podman is a tool used to manage OCI containers, images, volumes, and pods created from grouped containers.



## Key Features


- Support for multiple container image formats, including OCI and Docker images.

- Full management of container lifecycle, including creation (both from an image and from an exploded root filesystem), running, checkpointing and restoring (via CRIU), and removal.

- Support for pods, groups of containers that share resources and are managed together.

- Support for running containers and pods without root or other elevated privileges.

- No manager daemon, for improved security and lower resource utilization at idle.




## Use Cases

Running containers on Linux, Mac and Windows systems using a Podman-managed virtual machine; managing container images and volumes; creating and managing pods.



{{< callout title="Getting Started" type="code" >}}
```bash
Any recent Podman release should be able to run rootless without any additional configuration, though your operating system may require some additional configuration detailed in the [install guide](https://podman.io/getting-started/installation).
```
{{< /callout >}}



## Recent Updates

v6.1.4 was released on 2026-10-12.



{{< callout title="Did You Know?" type="info" >}}
Podman is based on libpod, a library for container lifecycle management that is also contained in this repository. The libpod library provides APIs for managing containers, pods, container images, and volumes.
{{< /callout >}}



## Related Tools


- [Buildah](/tools/buildah/)

- [Skopeo](/tools/skopeo/)
