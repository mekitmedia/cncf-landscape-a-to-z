---
cncf_status: non-cncf
date: '2026-10-28T02:47:36.096265'
homepage_url: https://www.openvswitch.org/
layout: single
letter: O
lifecycle_stage: first_pass
project_name: Open vSwitch
repo_url: https://github.com/openvswitch/ovs
status: completed
title: Open vSwitch
---



## Overview

An open source multilayer software switch designed to be used as a production-quality virtual switch in virtual machine environments, supporting multiple Linux-based virtualization technologies like KVM and VirtualBox.



## Key Features


- Support for standard 802.1Q VLAN model with trunk and access ports

- Visibility and monitoring with NetFlow, sFlow, and port mirroring

- Advanced tunneling capabilities including Geneve, GRE, VXLAN, ERSPAN, GTP-U, SRv6, and Bareudp

- High-performance data path utilizing a Linux kernel module




## Use Cases

Functions as a virtual switch in VM environments, exposing standard control and visibility interfaces to the virtual networking layer, while supporting distribution across multiple physical servers.



{{< callout title="Getting Started" type="code" >}}
```bash
To install on Linux or FreeBSD, refer to the installation guide (`Documentation/intro/install/general.rst`) in the project repository.
```
{{< /callout >}}



## Recent Updates

The project is actively maintained, with recent releases addressing performance, bug fixes, and providing new features (latest version is v4.0.0).



{{< callout title="Did You Know?" type="info" >}}
Open vSwitch can be run entirely in userspace without needing a kernel module, which can make it easier to port to other environments.
{{< /callout >}}
