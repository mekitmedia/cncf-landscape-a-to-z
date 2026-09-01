---
name: cncf-weekly-content
description: Multi-harness skill to run the CNCF weekly Editor → Researcher → Writer workflow with batching, subagent research delegation, and contract validation.
owner: mekitmedia/cncf-landscape-a-to-z
version: 2
---

# CNCF Weekly Content Contributor

## Purpose
Use this skill in Claude Code, Codex/OpenAI, OpenCode, or other harnesses to perform the CNCF weekly Editor → Researcher → Writer workflow with strict batching, deep subagent-driven research, verifiable ground-truth links, and pre-commit contract validation.

## System Prompts Reference
The authoritative system prompts shared with Pydantic AI agents are defined in `src/agentic/prompts.py`:
- `RESEARCHER_SYSTEM_PROMPT`: Deep research guidelines and ground-truth link enforcement.
- `WRITER_SYSTEM_PROMPT`: Markdown drafting structure and factual synthesis rules.
- `EDITOR_SYSTEM_PROMPT`: Decision loop and week selection logic.

## Required Inputs
- Repository root checkout
- Target week letter (`A`-`Z`) or instruction to pick the next incomplete week
- Week folder format: `<WEEK_ID>` like `00-A`, `01-B`, ..., `25-Z`
- Configurable `BATCH_SIZE` (default: 5 projects per iteration)
- Internet access / search capabilities for project research

## Files This Skill Reads
- `src/agentic/prompts.py` (system prompt reference)
- `data/weeks/*/tracker.yaml`
- `data/weeks/*/tasks.yaml`
- `data/weeks/*/categories/*.yaml`
- `data/weeks/*/research/*.yaml` (if present)

## Files This Skill Writes
- `data/weeks/<WEEK_ID>/research/<SANITIZED_PROJECT_NAME>.yaml`
- `website/content/posts/<YEAR>-<WEEK_LETTER>.md`
- `data/weeks/<WEEK_ID>/tracker.yaml`

## Guardrails
- **Batching & Scope Limit**: Do NOT attempt to research all pending projects in a week at once if there are many. Process pending items in batches of `BATCH_SIZE` (default: 5 projects). Save research YAMLs and update `tracker.yaml` after each batch.
- **Subagent Delegation**: Delegate deep project investigation to dedicated `research` subagents whenever subagents are supported by the harness. This isolates research context and enables deep, focused lookups.
- **Ground Truth & Direct Links**: Do not invent facts or write generic summaries. Every research file MUST include verifiable release versions, exact dates, and direct URLs (`official_website`, `repo_url`, `latest_release.url`, `get_started.docs_url`, and `sources`).
- **Contract Validation**: Run `uv run python scripts/validate_contract.py` before committing. Pre-commit hooks (`.pre-commit-config.yaml`) will automatically validate modified files on git commit.
- **Path Isolation**: Keep writes strictly inside the paths listed above.
- **Tracker Integrity**: Preserve existing tracker structure; only update status fields relevant to the current batch run.
- **Placeholders Over Hallucinations**: If specific details (e.g. latest release tag) cannot be verified, provide explicit placeholders or notes rather than inventing version numbers.

## Workflow

### 1) Editor task: choose week and select batch
1. Read all week trackers in `data/weeks/*/tracker.yaml`.
2. Select the first incomplete week in alphabetical order.
3. Identify all projects in that week where `research.status == pending` and `removed == false`.
4. Select the next batch of `BATCH_SIZE` (default: 5) pending projects to research in this run.
5. If all weeks/projects are complete, stop.

### 2) Researcher task: delegate subagents for deep research
For each project in the selected batch:
1. Read metadata from `data/weeks/<WEEK_ID>/categories/*.yaml`.
2. **Invoke a `research` subagent** (or run targeted searches) specifically for the project matching `RESEARCHER_SYSTEM_PROMPT`.
   - Inspect the official homepage, GitHub repository, release notes, and documentation.
   - Extract exact version numbers, release dates, core architectural features, and primary source URLs.
3. Save one schema-compliant YAML file per project in `data/weeks/<WEEK_ID>/research/<SANITIZED_PROJECT_NAME>.yaml`.
4. Use this enhanced schema:

```yaml
project_name: ""
official_website: ""
repo_url: ""
cncf_status: "graduated | incubating | sandbox | non-cncf"
summary: ""
key_features:
  - ""
latest_release:
  version: ""
  date: "YYYY-MM-DD"
  url: ""
recent_updates: ""
use_cases: ""
interesting_facts: ""
get_started:
  command: ""
  docs_url: ""
related_tools:
  - ""
sources:
  - label: ""
    url: ""
```

### 3) Writer task: generate or incrementally update weekly post
1. Read all available research YAML files for the selected week.
2. Write or update `website/content/posts/<YEAR>-<WEEK_LETTER>.md` following `WRITER_SYSTEM_PROMPT` with frontmatter:

```yaml
---
title: "Letter <WEEK_LETTER>: CNCF Projects Starting with <WEEK_LETTER>"
date: <TIMESTAMP_ISO8601_UTC>
draft: false
---
```
Set `<YEAR>` from the run input if provided; otherwise use the repository's active post cycle year (fallback: current calendar year).

3. Include intro, one detailed section per project with ground truth links, and conclusion.
4. Keep project sections factual, structured, and hyperlinked to primary sources.

### 4) Tracker updates & Contract Validation
After completing each batch:
1. Update `data/weeks/<WEEK_ID>/tracker.yaml`:
   - Mark completed items as `research: completed` and `content: completed` (or in-progress if post is partial).
   - Update `output_file` paths and completion timestamps.
   - Mark `week_tasks.tasks.blog_post` as `completed` once all projects for the week are finished and the final post is saved.
2. Run contract validation:
   ```bash
   uv run python scripts/validate_contract.py --week <WEEK_ID>
   ```
3. Commit changes (pre-commit hook will automatically verify contract compliance).

## Suggested Prompt

```text
Use the cncf-weekly-content skill from .agents/skills.
- Pick the next incomplete week from data/weeks/*/tracker.yaml.
- Select a batch of 5 pending projects to process.
- Delegate deep research for each project to `research` subagents to gather ground truth, repository links, exact release tags, and documentation URLs.
- Save research YAML files following the enhanced schema in data/weeks/<WEEK_ID>/research/.
- Update website/content/posts/<YEAR>-<WEEK_LETTER>.md with new project sections.
- Update data/weeks/<WEEK_ID>/tracker.yaml after each batch.
- Run `uv run python scripts/validate_contract.py --week <WEEK_ID>` to verify contract compliance.
- Return a summary of completed projects in this batch, ground truth sources found, and remaining pending items.
```

## Definition of Done
- Research YAML files exist for the processed batch, containing verified facts, release numbers, and primary source links.
- Weekly post exists and reflects available research with clickable markdown links to official sites/repos/docs.
- Contract validation passes cleanly via `uv run python scripts/validate_contract.py`.
- Tracker statuses accurately reflect completed, remaining, or failed tasks.
- Progress is saved in small, reviewable commits/PRs per batch without overloading context.
