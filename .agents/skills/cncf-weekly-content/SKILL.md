---
name: cncf-weekly-content
description: Multi-harness skill to run the CNCF weekly Editor → Researcher → Writer workflow without the Pydantic runtime.
owner: mekitmedia/cncf-landscape-a-to-z
version: 1
---

# CNCF Weekly Content Contributor

## Purpose
Use this skill across all agent harnesses (Claude Code, GitHub Copilot, Google Jules, Codex/OpenAI, OpenCode, Antigravity, and Pydantic AI) to perform the CNCF Landscape A-to-Z content workflow.

Modular role prompts are maintained in:
- Content Manager: `prompts/content_manager.md`
- Managing Editor: `prompts/editor.md`
- Software Researcher: `prompts/researcher.md`
- Technical Writer: `prompts/writer.md`
- Unified Jules Agent: `prompts/jules.md`

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
- `website/content/tools/<SANITIZED_PROJECT_NAME>.md` (optional / tool page generation)
- `website/content/posts/<YEAR>-<WEEK_LETTER>.md`
- `data/weeks/<WEEK_ID>/tracker.yaml`

## Guardrails
- Do not invent facts; only write verifiable project details.
- Research files are structured note-taking artifacts: ground every claim in verifiable source quotes.
- Keep writes inside the paths listed above.
- Preserve tracker structure; only update status fields relevant to this run.
- If research is missing, leave explicit placeholders instead of hallucinating.

## Workflow

### 1) Editor task: choose week
1. Read all week trackers in `data/weeks/*/tracker.yaml`.
2. Select the first incomplete week in alphabetical order.
3. If all weeks are complete, stop.

### 2) Researcher task: create or enrich research YAML (Structured Note-Taking)
Research is a continuous endeavor. For each project in the selected week:
1. Read existing metadata from `data/weeks/<WEEK_ID>/categories/*.yaml` and any existing research file in `data/weeks/<WEEK_ID>/research/`.
2. Do not overwrite rich data with shallower summaries; enrich missing citations, releases, and ecosystem perspectives.
3. Conduct deep live grounding from official homepages, repositories, documentation, and release notes.
4. Save one YAML file per project in `data/weeks/<WEEK_ID>/research/<sanitized_project_name>.yaml`.
5. Use this rich schema with source quotes for grounding:

```yaml
project_name: ""
homepage_url: ""
repo_url: ""
docs_url: ""
cncf_status: "" # sandbox | incubating | graduated | member
latest_release:
  version: ""
  date: ""
  release_notes_url: ""
summary: ""
key_features:
  - ""
recent_updates: ""
use_cases: ""
ecosystem_perspectives:
  strengths: ""
  considerations: ""
  community_discussions:
    - ""
interesting_facts: ""
get_started: ""
related_tools:
  - ""
sources:
  - id: "src_readme"
    title: ""
    url: ""
    source_type: "github_readme" # github_readme | github_release | official_docs | cncf_landscape
    quotes:
      - "Exact quote or excerpt from the official source"
last_researched_at: "<TIMESTAMP_ISO8601_UTC>"
research_version: 1
```

### 3) Writer task: generate weekly post
1. Read all research YAML files for the selected week.
2. Write `website/content/posts/<YEAR>-<WEEK_LETTER>.md` with frontmatter (always initialized as draft):

```yaml
---
title: "Cruising through the '<WEEK_LETTER>'s: <Curated Subtitle or Themes>"
date: <TIMESTAMP_ISO8601_UTC>
draft: true
letter: "<WEEK_LETTER>"
---
```
Set `<YEAR>` from the run input if provided; otherwise use the repository's active post cycle year (fallback: current calendar year).

3. Include intro, curated featured tools section, and conclusion.
4. Keep project sections concise and curated. Avoid shadowing persistent `/tools/` or `/letters/` pages.
5. Provide markdown hyperlinks to project websites, GitHub repositories, documentation, and site letter/tool pages.
6. For letters with large numbers of tools (e.g. A or C), remain concise and encourage readers to explore the full catalog via persistent pages.

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
