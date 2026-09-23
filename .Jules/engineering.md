# Jules Engineering & Architecture Memory Log

This file records insights, learnings, and canonical actions discovered during engineering, schema modeling, CLI tooling, and testing tasks.

## 2026-09-20 - Standalone Utilities and Zero-Dependency Normalization
**Learning:** Utilities that normalize text or validate schemas should minimize heavy runtime dependencies so they can be executed in isolated CLI scripts and lightweight validators.
**Action:** Place core pure-Python algorithms in `src/utils/` and ensure they have 100% pytest test coverage in `tests/`.

## 2026-09-20 - Atomic Task Self-Cleaning
**Learning:** Leaving completed task prompt files in `.github/prompts/tasks/` leads to ambiguous queue state and stale prompt pollution.
**Action:** When implementing a task from `.github/prompts/tasks/`, always delete the task prompt file as the final step in the PR branch before committing.

## 2026-09-20 - Deterministic Grounding Validator
**Learning:** YAML research files must include non-empty summary and key_features; source quotes should be validated as substrings of cached snapshots after canonical normalization.
**Action:** Keep grounding validation deterministic by checking sources/url/quotes shape and using canonical_normalize-based substring matching when cache snapshots are present.
## 2026-09-20 - Tool Card and DAG Validation
**Learning:** Tool card projections should enforce a hard word cap in tests with intentionally long summaries, while tracker DAG checks should keep item-level prerequisites strict and only allow `SKIPPED` to satisfy week-level rollups.
**Action:** Keep `create_tool_card` capped, test it with long summaries, and validate dependency behavior via `can_start_task(...)` for both item-level and week-level tasks.
