# Engineering & Architecture Domain Memory Log

This file records insights, learnings, and canonical actions discovered during engineering, schema modeling, CLI tooling, and testing tasks.

## 2026-09-20 - Standalone Utilities and Zero-Dependency Normalization
**Learning:** Utilities that normalize text or validate schemas should minimize heavy runtime dependencies so they can be executed in isolated CLI scripts and lightweight validators.
**Action:** Place core pure-Python algorithms in `src/utils/` and ensure they have 100% pytest test coverage in `tests/`.

## 2026-09-20 - Deterministic Grounding Validator
**Learning:** YAML research files must include non-empty summary and key_features; source quotes should be validated as substrings of cached snapshots after canonical normalization.
**Action:** Keep grounding validation deterministic by checking sources/url/quotes shape and using canonical_normalize-based substring matching when cache snapshots are present.

## 2026-09-20 - Tool Card and DAG Validation
**Learning:** Tool card projections should enforce a hard word cap in tests with intentionally long summaries, while tracker DAG checks should keep item-level prerequisites strict and only allow `SKIPPED` to satisfy week-level rollups.
**Action:** Keep `create_tool_card` capped, test it with long summaries, and validate dependency behavior via `can_start_task(...)` for both item-level and week-level tasks.

## 2026-10-22 - Gather Research Results for Blog Post Tasks
**Learning:** In the parallel orchestration flow (`src/agentic/flow.py`), the `writer` tasks need the research results of the week to draft the weekly post. Passing an empty list `[]` to `write_weekly_post` creates a blog post with no research content.
**Action:** Use `load_week_research(task.week_letter)` from `src.agentic.runner` to gather research results before drafting the weekly post.

## 2026-10-24 - Prefect Testing and Subprocess Ephemeral Servers
**Learning:** Prefect tests spawn ephemeral servers which can cause "ValueError: I/O operation on closed file." or timeout crashes inside the API server subprocess termination code when pytest exits or the flow lacks an API environment setup.
**Action:** Always inject `prefect_test_harness()` from `prefect.testing.utilities` into a session-scoped pytest fixture (e.g. `tests/conftest.py`) or use the `PREFECT_TEST_MODE=1` environment variable during automated test execution. We also added `PREFECT_LOGGING_TO_API_WHEN_MISSING_FLOW=ignore` to silence noise.

## 2026-10-31 - Resilient Multiline Regex Matching for Cross-Platform Line Endings
**Learning:** Hardcoding `\n` in multiline regex operations (like frontmatter extraction using `re.search`) causes scripts to fail on Windows or when handling CRLF (`\r\n`) formatted files, resulting in flaky schema validation.
**Action:** Always use `\r?\n` in Python regex patterns dealing with text boundaries instead of `\n` alone to ensure correct parsing regardless of file line endings.
