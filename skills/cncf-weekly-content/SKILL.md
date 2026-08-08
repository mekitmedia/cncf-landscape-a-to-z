# Skill: CNCF Weekly Content Contributor

## Purpose
Use this skill in Claude Code, Opencode, or any other coding harness to perform the same workflow currently handled by the Pydantic AI agents (Editor → Researcher → Writer) so contributors can help without running the agent runtime.

## Required Inputs
- Repository root checkout
- Target week letter (`A`-`Z`) **or** instruction to pick the next incomplete week
- Week folder format: `<WEEK_ID>` like `00-A`, `01-B`, ..., `25-Z`
- Internet access for project research

## Files This Skill Reads
- `data/weeks/*/tracker.yaml`
- `data/weeks/*/tasks.yaml`
- `data/weeks/*/categories/*.yaml`
- Existing research files in `data/weeks/*/research/*.yaml` (if present)

## Files This Skill Writes
- `data/weeks/<WEEK_ID>/research/<SANITIZED_PROJECT_NAME>.yaml`
- `website/content/posts/<YEAR>-<WEEK_LETTER>.md`
- `data/weeks/<WEEK_ID>/tracker.yaml`

## Guardrails
- Do not invent facts; only write verifiable project details.
- Keep writes inside the three paths above.
- Preserve existing tracker fields; only update task status fields relevant to this run.
- If research is missing for a project, leave clear placeholders instead of hallucinating.

## Step-by-Step Workflow

### 1) Editor task: choose week
1. Read all week tracker files under `data/weeks/*/tracker.yaml`.
2. Select the first week with incomplete work (prefer alphabetical order).
3. If all weeks are complete, stop.

### 2) Researcher task: create/update research YAML
For each project in the selected week that still needs research:
1. Read metadata from `data/weeks/<WEEK_ID>/categories/*.yaml`.
2. Research using the project homepage, repo, release notes, and reliable sources.
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

3. Include an introduction, one section per project, and a conclusion.
4. Keep each project section factual and concise.

### 4) Tracker updates
Update `data/weeks/<WEEK_ID>/tracker.yaml`:
- Mark researched items as `research: completed`.
- Mark week `blog_post` as `completed` when the post is saved.
- If work fails, set status to `failed` with an error message.

## Suggested Prompt To Run This Skill In Any Harness

```text
Use the CNCF Weekly Content Contributor skill in this repository.
- Pick the next incomplete week from data/weeks/*/tracker.yaml.
- Complete missing research YAML files for that week.
- Generate/update website/content/posts/YYYY-L.md from research.
- Update tracker statuses accordingly.
- Do not hallucinate facts; cite only verifiable information.
- Return a summary of files changed and remaining incomplete tasks.
```

## Definition of Done
- Research YAML exists for each required project in the chosen week.
- Weekly post exists and reflects available research.
- Tracker status reflects completed/failed work accurately.
- Changes are reviewable in a single PR.
