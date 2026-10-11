---
name: work-with-jules
description: Multi-harness developer skill to author atomic tasks for Google Jules, manage the file backlog queue, inspect with scripts/jules_queue.py, and leverage persistent domain memory in .Jules/.
owner: mekitmedia/cncf-landscape-a-to-z
version: 1
---

# Work with Jules: Task Delegation & Backlog Management

## Purpose
Use this skill across all agent harnesses (Claude Code, GitHub Copilot, Google Jules, Antigravity, OpenCode, Codex) to:
1. Author well-structured, atomic engineering and content tasks for Google Jules.
2. Manage and inspect the sequential task queue in `.github/prompts/tasks/`.
3. Validate task schemas and resolve prompts locally using `scripts/jules_queue.py`.
4. Consult and enrich persistent agent domain memory in `.Jules/`.
5. Review, verify, and merge autonomous pull requests created by Jules.

---

## Required Tools & Local CLI
All queue operations can be executed locally without depending on GitHub Actions:

```bash
# List all pending tasks in deterministic numerical order
uv run python scripts/jules_queue.py list

# Validate all task markdown files in the backlog against the contract
uv run python scripts/jules_queue.py validate

# Inspect the next prompt to be dispatched to Jules
uv run python scripts/jules_queue.py get-prompt --info
```

---

## Agent Domain Memory (`.Jules/`)

Before authoring tasks or reviewing code, consult the domain memory logs to understand existing lessons and guardrails:

* **`.Jules/palette.md`**: UI layout, Tailwind styling, accessibility semantics (`tabindex`, `focus-visible`), Hugo template partials.
* **`.Jules/content.md`**: CNCF project metadata schemas, GitHub release notes nuances, quote extraction and direct citation rules.
* **`.Jules/engineering.md`**: Pydantic models, CLI validators, YAML trackers, DAG projections, test suite patterns.

When Jules implements a feature or discovers an edge case, it records an entry following this format:
```markdown
## YYYY-MM-DD - <Topic Title>
**Learning:** <Key technical insight, framework quirk, or architectural nuance>
**Action:** <Canonical pattern or rule to follow in all future tasks>
```

---

## The 5 Principles of Jules Task Authoring

1. **Single Responsibility & Atomic Scope**:
   - Each task modifies or introduces **1 core component/module** accompanied by **unit tests**.
   - Keep diffs small (<150 lines) so PRs can be reviewed instantly.
2. **Explicit Technical Contracts**:
   - Provide exact function signatures, Pydantic field schemas, and error-handling requirements.
   - Reference relevant architectural docs in `docs/`.
3. **Verifiable Definition of Done**:
   - Specify exact test commands (e.g. `uv run pytest tests/test_feature.py`).
   - 100% of existing tests in the suite must pass without regressions.
4. **Memory Recording (`.Jules/engineering.md`)**:
   - Require the agent to record any architectural lessons or schema quirks in `.Jules/engineering.md`.
5. **Mandatory Self-Cleaning Final Step**:
   - Every task must instruct the agent to **delete its own prompt file** as the final step before committing.
   - When the PR merges into `main`, the task is automatically removed from the backlog on `main`.

---

## Standard Task Authoring Template

When creating a new task, save it as `.github/prompts/tasks/<XX>_<descriptive_name>.md`:

```markdown
# Task <XX>: <Concise Title>

## Objective
<1-2 sentences describing what needs to be built and why.>

---

## Technical Specifications
### 1. File: <path/to/file.py>
<Exact class, function, or model signatures.>

### 2. File: <tests/test_file.py>
<Required test assertions and edge-case coverage.>

---

## Execution Steps for Jules
1. Implement <file.py>.
2. Implement unit tests in <test_file.py>.
3. Run verification: `uv run pytest <test_file.py>`.
4. **Record Learnings (Required)**: Append any architectural insights or edge cases to `.Jules/engineering.md`.
5. **Self-Cleaning Step (Required)**: Delete this task file (`.github/prompts/tasks/<task_name>.md`) before creating the commit/PR.

---

## Definition of Done
- Implementation complete and adheres to architectural guidelines.
- 100% of test suite passes cleanly.
- Architectural learnings recorded in `.Jules/engineering.md`.
- Task prompt file deleted in the resulting PR.
```

---

## How to Dispatch Tasks

### Automated Mode (Scheduled CI)
- `.github/workflows/jules_schedule.yml` runs twice daily (`0 0,12 * * *`).
- The composite action `.github/actions/prepare-jules-task` runs `scripts/jules_queue.py get-prompt` and automatically picks the lowest-numbered pending task.
- If `.github/prompts/tasks/` is empty, it automatically falls back to `.github/prompts/jules_prompt.md`.

### Manual Dispatch via GitHub CLI (`gh`)
```bash
# Dispatch next task in backlog automatically
gh workflow run jules_schedule.yml

# Dispatch specific prompt override
gh workflow run jules_schedule.yml \
  -f custom_prompt="$(cat .github/prompts/tasks/02_pydantic_models_and_editorial_lock.md)"
```

---

## Reviewing & Merging Jules PRs
1. Verify CI checks pass (unit tests, contract validation).
2. Check that the task prompt file was deleted as part of the PR diff (self-cleaning).
3. Check that appropriate learnings were logged to `.Jules/`.
4. Merge PR into `main`. The next scheduled workflow run will automatically advance to the next task in the queue.
