# Task 04: Implement Tool Card Projections and Graph DAG Enforcement

## Objective
Implement a lightweight Tool Card projection utility to prevent context window explosion when synthesizing large weeks (e.g. 69+ tools in Week 00-A) and strictly enforce the task dependency order in the orchestrator.

---

## Technical Specifications

### 1. File: `src/agentic/projections.py` (or `src/tracker/projections.py`)
Create a helper to project full research notes into concise **80-word Tool Cards**:
- `create_tool_card(research_data: dict) -> str`:
  - Extracts project name, 1-line summary, CNCF status, top 2 key features, and repo URL.
  - Returns a compact markdown bullet (~80 words / ~100 tokens).
- `project_week_deck(week_id: str) -> str`:
  - Reads all completed research files in `data/weeks/<WEEK_ID>/research/*.yaml` and compiles them into a compact deck.
  - For a 70-tool week, this keeps total input token count under 8,000 tokens.

### 2. File: `src/tracker/yaml_backend.py` (DAG Enforcement)
Update `can_start_task()`:
- `can_start_task(week_id, item_name, "content")` requires `research` status to be `completed`.
- `can_start_task(week_id, None, "blog_post")` requires all items in the week to have `content` (tool page) status `completed` (or explicitly verified) before weekly blog post generation can begin.

### 3. File: `tests/test_tool_card_dag.py`
Create pytest tests verifying:
- `create_tool_card` produces bounded, compact output from long research files.
- `can_start_task("blog_post")` blocks if any item tool page is incomplete.

---

## Execution Steps for Jules
1. Implement `src/agentic/projections.py`.
2. Update DAG dependency rules in `src/tracker/yaml_backend.py`.
3. Create `tests/test_tool_card_dag.py`.
4. Run `uv run pytest`.
5. **Self-Cleaning Step (Required)**: Delete this task file (`.github/prompts/tasks/04_tool_card_projection_and_dag.md`) before committing.
