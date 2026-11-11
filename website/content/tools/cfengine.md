---
cncf_status: non-cncf
date: '2026-11-04T05:48:48.813542'
homepage_url: https://cfengine.com/
layout: single
letter: C
lifecycle_stage: tech_writing
project_name: CFEngine
repo_url: https://github.com/cfengine/core
status: completed
title: CFEngine
---



## Overview

CFEngine is a configuration management system designed to provide automated configuration and maintenance of large-scale computer systems.



## Key Features


- Automated configuration and maintenance of large-scale computer systems




## Use Cases

Infrastructure automation, Security automation, and Compliance automation.



{{< callout title="Getting Started" type="code" >}}
```bash
In order to use the built cf-agent in the source tree you must add a `$HOME/.cfagent/bin/cf-promises` file:

$ pwd
<something>/core
$ echo "cd $(pwd); cf-promises/cf-promises \"$@\"" > ~/.cfagent/bin/cf-promises

```
{{< /callout >}}





{{< callout title="Did You Know?" type="info" >}}
CFEngine 3 is *not* a drop-in upgrade for CFEngine 2 installations.
{{< /callout >}}



