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
- `data/adhoc_tasks.yaml` (if present, for prioritized ad-hoc tasks)
- `data/weeks/*/tracker.yaml`
- `data/weeks/*/tasks.yaml`
- `data/weeks/*/categories/*.yaml`
- `data/weeks/*/research/*.yaml` (if present)

## Files This Skill Writes
- `data/weeks/<WEEK_ID>/research/<SANITIZED_PROJECT_NAME>.yaml`
- `website/content/tools/<SANITIZED_PROJECT_NAME>.md` (Hugo tool page)
- `website/content/posts/<YEAR>-<WEEK_LETTER>.md`
- `data/weeks/<WEEK_ID>/tracker.yaml`

## Guardrails
- Do not invent facts; only write verifiable project details.
- Research files are structured note-taking artifacts: ground claims in verifiable source quotes.
- Keep writes inside the paths listed above.
- Always generate both the research YAML and the tool markdown page for an assigned project.
- Preserve tracker structure; update status fields accurately for completed items.

## Workflow Modes

### Mode A: Single Project Vertical Slice (Roulette or Ad-Hoc Mission)
When assigned a specific project (via `just roulette` or ad-hoc task):
1. Read project metadata from `data/weeks/<WEEK_ID>/categories/*.yaml` and any existing research in `data/weeks/<WEEK_ID>/research/`.
2. Research features, recent releases, ecosystem perspectives, use cases, and getting started guide.
3. Save or enrich research YAML at `data/weeks/<WEEK_ID>/research/<sanitized_project_name>.yaml` using the schema below.
4. Generate the tool markdown page at `website/content/tools/<sanitized_project_name>.md` (or run `uv run python -m src.pipeline.tool_pages`).
5. Update `data/weeks/<WEEK_ID>/tracker.yaml` marking `research` and `content` tasks as `completed`.

### Mode B: Full Week Compilation (Editor → Researcher → Writer)
1. Pick next incomplete week or target letter.
2. Complete missing research YAML files and tool pages for all items in that week.
3. Write/update weekly summary post `website/content/posts/<YEAR>-<WEEK_LETTER>.md`.
4. Update week `blog_post` status to `completed` in `tracker.yaml`.

## Research YAML Schema (Structured Note-Taking)

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

## Weekly Post Generation (Writer)
1. Read research YAML files for the selected week.
2. Write `website/content/posts/<YEAR>-<WEEK_LETTER>.md` with frontmatter (initialized as draft):

```yaml
---
title: "Cruising through the '<WEEK_LETTER>'s: <Curated Subtitle or Themes>"
date: <TIMESTAMP_ISO8601_UTC>
draft: true
letter: "<WEEK_LETTER>"
---
```

## Suggested Prompts

### Draw Single Task Mission (Recommended for Jules / Autonomous PRs):
```text
Run `just roulette` (or `uv run python -m src.cli run draw --format=prompt`) to draw the assigned project.
Execute the vertical slice:
- Complete research YAML at data/weeks/<WEEK_ID>/research/<project>.yaml
- Generate tool page at website/content/tools/<project>.md
- Update tracker.yaml
```

### Full Week Workflow:
```text
Use the cncf-weekly-content skill from .agents/skills.
- Pick the next incomplete week from data/weeks/*/tracker.yaml.
- Complete missing research YAML files and tool pages for that week.
- Generate/update website/content/posts/<YEAR>-<WEEK_LETTER>.md from research.
- Update tracker statuses accordingly.
```

## Definition of Done
- Research YAML exists for the project.
- Tool page markdown exists at `website/content/tools/<project>.md`.
- Tracker statuses are accurate for completed/failed work.
- Changes are reviewable in a single PR.


