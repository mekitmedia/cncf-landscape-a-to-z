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
- Never skip lifecycle stages (`initial -> first_pass -> tech_writing -> approved`). CI validates state transitions on every PR.
- Keep writes inside the paths listed above.
- In first_pass research, deliver ONLY the research YAML and tracker research task update. Do NOT generate tool markdown pages in first_pass.
- Preserve tracker structure; update status fields accurately for completed items.

## Workflow Modes

### Mode A: Staged Project Lifecycle (Roulette or Ad-Hoc Mission)
When assigned a specific project (via `just roulette` or ad-hoc task), execute ONLY the targeted stage:

1. **Stage 1: First Pass (`initial -> first_pass`)**
   - Research features, recent releases, ecosystem perspectives, use cases, getting started guide, and verbatim source quotes.
   - Save or enrich research YAML at `data/weeks/<WEEK_ID>/research/<sanitized_project_name>.yaml`.
   - Update `data/weeks/<WEEK_ID>/tracker.yaml`: mark `tasks.research: completed`. Keep `tasks.content: pending`.
   - **DO NOT create `website/content/tools/<tool>.md` in this stage.**

2. **Stage 2: Tech Writing (`first_pass -> tech_writing`)**
   - Read existing verified research from `data/weeks/<WEEK_ID>/research/<sanitized_project_name>.yaml`.
   - Generate the tool markdown page at `website/content/tools/<sanitized_project_name>.md`.
   - Update `data/weeks/<WEEK_ID>/tracker.yaml`: mark `tasks.content: completed`.

3. **Stage 3: Editorial Approval (`tech_writing -> approved`)**
   - Run `uv run python scripts/validate_grounding.py` to verify quote citations.
   - Set `editorial_lock: true` in research YAML and `lifecycle_stage: approved` in tool frontmatter.

### Mode B: Full Week Compilation (Editor → Researcher → Writer)
1. Pick next incomplete week or target letter.
2. Complete missing research YAML files and tool pages for all items in that week adhering to the staged progression.
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

### Draw Single Task Mission (Recommended for Autonomous PRs):
```text
Run `just roulette` (or `uv run python -m src.cli run draw --format=prompt`) to draw the assigned project and target stage.
Execute only the assigned stage:
- If first_pass: complete research YAML at data/weeks/<WEEK_ID>/research/<project>.yaml and update tracker.yaml research status. Do NOT generate tool page markdown.
- If tech_writing: generate tool page at website/content/tools/<project>.md from research and update tracker.yaml content status.
- If approved: verify grounding quotes and set editorial_lock: true.
```

### Full Week Workflow:
```text
Use the cncf-weekly-content skill from .agents/skills.
- Pick the next incomplete week from data/weeks/*/tracker.yaml.
- Complete missing research YAML files and tool pages for that week following the staged progression.
- Generate/update website/content/posts/<YEAR>-<WEEK_LETTER>.md from research.
- Update tracker statuses accordingly.
```

## Definition of Done
- For Stage 1 (first_pass): Research YAML exists with source quotes; tracker research task is completed; content task is pending; no tool page markdown is created.
- For Stage 2 (tech_writing): Tool page markdown exists at `website/content/tools/<project>.md`; tracker content task is completed.
- For Stage 3 (approved): Grounding validation passes; editorial lock is true.
- Changes advance exactly one lifecycle step per PR.


