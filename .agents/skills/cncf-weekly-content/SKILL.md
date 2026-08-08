---
name: cncf-weekly-content
description: Multi-harness skill to run the CNCF weekly Editor → Researcher → Writer workflow without the Pydantic runtime.
owner: mekitmedia/cncf-landscape-a-to-z
version: 1
---

# CNCF Weekly Content Contributor

## Purpose
Use this skill in Claude Code, Codex/OpenAI, OpenCode, or other harnesses to perform the same workflow currently handled by the Pydantic AI agents.

## Required Inputs
- Repository root checkout
- Target week letter (`A`-`Z`) or instruction to pick the next incomplete week
- Week folder format: `<WEEK_ID>` like `00-A`, `01-B`, ..., `25-Z`
- Internet access for project research

## Files This Skill Reads
- `data/weeks/*/tracker.yaml`
- `data/weeks/*/tasks.yaml`
- `data/weeks/*/categories/*.yaml`
- `data/weeks/*/research/*.yaml` (if present)

## Files This Skill Writes
- `data/weeks/<WEEK_ID>/research/<SANITIZED_PROJECT_NAME>.yaml`
- `website/content/posts/<YEAR>-<WEEK_LETTER>.md`
- `data/weeks/<WEEK_ID>/tracker.yaml`

## Guardrails
- Do not invent facts; only write verifiable project details.
- Keep writes inside the paths listed above.
- Preserve tracker structure; only update status fields relevant to this run.
- If research is missing, leave explicit placeholders instead of hallucinating.

## Workflow

### 1) Editor task: choose week
1. Read all week trackers in `data/weeks/*/tracker.yaml`.
2. Select the first incomplete week in alphabetical order.
3. If all weeks are complete, stop.

### 2) Researcher task: create/update research YAML
For each project in the selected week that still needs research:
1. Read metadata from `data/weeks/<WEEK_ID>/categories/*.yaml`.
2. Research from homepage, repo, and reliable release/update sources.
3. Save one YAML file per project in `data/weeks/<WEEK_ID>/research/`.
4. Use this schema:

```yaml
project_name: ""
summary: ""
key_features:
  - ""
recent_updates: ""
use_cases: ""
interesting_facts: ""
get_started: ""
related_tools:
  - ""
```

### 3) Writer task: generate weekly post
1. Read all research YAML files for the selected week.
2. Write `website/content/posts/<YEAR>-<WEEK_LETTER>.md` with frontmatter:

```yaml
---
title: "Letter <WEEK_LETTER>: <PROJECT_COUNT> CNCF Projects Starting with <WEEK_LETTER>"
date: <TIMESTAMP_ISO8601_UTC>
draft: false
---
```

3. Include intro, one section per project, and conclusion.
4. Keep every project section factual and concise.
5. Set `<PROJECT_COUNT>` from the number of researched projects included in the post (typically the count of `data/weeks/<WEEK_ID>/research/*.yaml` files used).

### 4) Tracker updates
Update `data/weeks/<WEEK_ID>/tracker.yaml`:
- Mark researched items as `research: completed`.
- Mark week `blog_post` as `completed` when post is saved.
- If work fails, set status to `failed` with error details.

## Suggested Prompt

```text
Use the cncf-weekly-content skill from .agents/skills.
- Pick the next incomplete week from data/weeks/*/tracker.yaml.
- Complete missing research YAML files for that week.
- Generate/update website/content/posts/<YEAR>-<WEEK_LETTER>.md from research.
- Update tracker statuses accordingly.
- Do not hallucinate facts; use only verifiable information.
- Return a summary of changed files and remaining incomplete tasks.
```

## Definition of Done
- Required research YAML files exist for the selected week.
- Weekly post exists and reflects available research.
- Tracker statuses are accurate for completed/failed work.
- Changes are reviewable in a single PR.
