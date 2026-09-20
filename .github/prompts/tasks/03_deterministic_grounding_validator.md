# Task 03: Implement Deterministic Grounding Validator

## Objective
Build a fast, deterministic CLI validation script (`scripts/validate_grounding.py`) that audits research notes for authentic source quotes and link validity, runnable locally and in CI workflows.

---

## Technical Specifications

### 1. File: `scripts/validate_grounding.py`
Create a CLI tool with arguments:
- `files` (positional paths passed by pre-commit or CLI)
- `--week <WEEK_ID>` (e.g. `00-A`)
- `--all-files` (checks all `data/weeks/*/research/*.yaml`)
- `--git-diff [REF]` (checks changed files relative to git ref)

### Validation Rules:
1. **Quote Existence & Format**:
   - For every entry in `sources:`, verifies `quotes:` is a non-empty list of non-empty strings.
2. **Local Cache / Snapshot Substring Check**:
   - If a cached snapshot exists in `data/weeks/<WEEK_ID>/research/.cache/<tool>_<source_id>.txt`, use `src.utils.text_normalizer.is_quote_in_source(quote, cached_text)` to confirm the quote exists in the source.
3. **Link Syntax**:
   - Confirms `url` is a well-formed HTTP/HTTPS URL.
4. **Summary & Feature Grounding Attribution**:
   - Verifies that key claims have corresponding sources.

### 2. File: `tests/test_grounding_validator.py`
Create pytest tests verifying:
- Valid research file with valid quotes and cache passes validation.
- Missing quotes or empty source list fails with a descriptive error.
- Quote not present in the cached snapshot fails validation.

---

## Execution Steps for Jules
1. Implement `scripts/validate_grounding.py`.
2. Create `tests/test_grounding_validator.py`.
3. Run `uv run pytest tests/test_grounding_validator.py`.
4. Run `uv run python scripts/validate_grounding.py --week 00-A` to test against existing research files.
5. **Record Learnings (Required)**: Append any architectural insights or validation quirks discovered to `.Jules/engineering.md`.
6. **Self-Cleaning Step (Required)**: Delete this task file (`.github/prompts/tasks/03_deterministic_grounding_validator.md`) before committing.

