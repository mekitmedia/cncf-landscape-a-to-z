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
- Keep writes inside the paths listed above.
- Always generate both the research YAML and the tool markdown page for an assigned project.
- Preserve tracker structure; update status fields accurately for completed items.

## Workflow Modes

### Mode A: Single Project Vertical Slice (Roulette or Ad-Hoc Mission)
When assigned a specific project (via `just roulette` or ad-hoc task):
1. Read project metadata from `data/weeks/<WEEK_ID>/categories/*.yaml`.
2. Research features, updates, use cases, and getting started guide.
3. Save research YAML to `data/weeks/<WEEK_ID>/research/<SANITIZED_NAME>.yaml`.
4. Generate the tool markdown page at `website/content/tools/<SANITIZED_NAME>.md` (or run `uv run python -m src.pipeline.tool_pages`).
5. Update `data/weeks/<WEEK_ID>/tracker.yaml` marking `research` and `content` tasks as `completed`.

### Mode B: Full Week Compilation (Editor → Researcher → Writer)
1. Pick next incomplete week or target letter.
2. Complete missing research YAML files and tool pages for all items in that week.
3. Write/update weekly summary post `website/content/posts/<YEAR>-<WEEK_LETTER>.md`.
4. Update week `blog_post` status to `completed` in `tracker.yaml`.

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

