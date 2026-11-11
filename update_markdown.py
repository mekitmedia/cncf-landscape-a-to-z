import os
from datetime import datetime, timezone

now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

content = f"""---
cncf_status: non-cncf
date: '{now}'
description: SigLens is an observability DB uniquely suited for logs, metrics and traces with zero external dependencies.
homepage_url: https://www.siglens.com/
layout: single
letter: S
lifecycle_stage: tech_writing
project_name: SigLens
repo_url: https://github.com/siglens/siglens
status: completed
title: SigLens
---

## Overview

SigLens is an observability DB uniquely suited for logs, metrics and traces with zero external dependencies.

## Key Features

- Multiple Ingestion formats: Open Telemetry, Elastic, Splunk HEC, Loki
- Multiple Query Languages: Splunk SPL, SQL
- Simple architecture, easy to get started
"""

os.makedirs('website/content/tools', exist_ok=True)
with open('website/content/tools/siglens.md', 'w') as f:
    f.write(content)
