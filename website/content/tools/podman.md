---
cncf_status: non-cncf
date: '2026-10-05T02:43:33.555707'
get_started: Any recent Podman release should be able to run rootless without any
  additional configuration, though your operating system may require some additional
  configuration detailed in the install guide.
homepage_url: https://podman.io/
interesting_facts: Releases are predictable, with a new major or minor version released
  4 times a year, during the second week of February, May, August, and November.
key_features:
- 'Multi-format Container Image Support: Can handle different container image formats,
  including both OCI and Docker images.'
- 'Lifecycle Management: Complete management capabilities for container lifecycle,
  including creation, running, checkpointing, restoring, and removal.'
- 'Docker-compatible CLI: Offers a CLI interface that mimics Docker, allowing users
  to run containers locally and on remote systems seamlessly.'
- 'Daemonless Architecture: Operates without a manager daemon, which improves security
  and reduces resource utilization when idle.'
- 'Rootless Execution: Capable of running containers and pods without requiring root
  or elevated privileges.'
layout: single
letter: P
lifecycle_stage: first_pass
project_name: Podman
recent_updates: The latest release is v6.1.3.
related_tools:
- Skopeo
- Buildah
repo_url: https://github.com/containers/podman
status: completed
summary: Podman (the POD MANager) is a tool for managing containers and images, volumes
  mounted into those containers, and pods made from groups of containers. It runs
  containers on Linux, but can also be used on Mac and Windows systems using a Podman-managed
  virtual machine.
title: Podman
use_cases: Podman can be used to run and manage containers and images locally or on
  remote systems, and to replace Docker with a rootless, daemonless alternative.
---

This is an auto-generated tool page. For more details, see the [letter page](/letters/p/).