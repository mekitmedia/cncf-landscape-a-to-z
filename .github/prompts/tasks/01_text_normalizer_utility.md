# Task 01: Implement Canonical Text Normalization Utility

## Objective
Implement a robust, standalone text normalization utility (`src/utils/text_normalizer.py`) and unit tests (`tests/test_text_normalizer.py`) to prevent false-alarm quote rejections caused by Unicode smart quotes, em-dashes, HTML entities, and formatting differences.

---

## Technical Specifications

### 1. File: `src/utils/text_normalizer.py`
Create `src/utils/text_normalizer.py` with the following functions:
- `canonical_normalize(text: str) -> str`:
  - Decodes HTML entities using `html.unescape(text)`.
  - Normalizes Unicode characters using `unicodedata.normalize('NFKD', text)`.
  - Standardizes typographic quotes: replaces `“`, `”`, `„`, `«`, `»`, `'`, `‘`, `’` with standard ASCII quotes.
  - Standardizes dashes: replaces em-dash `—`, en-dash `–`, and minus `−` with ASCII hyphen `-`.
  - Collapses multiple whitespace characters and newlines (`\r`, `\n`, `\t`, non-breaking spaces `\u00a0`) into a single space.
  - Converts to lowercase and strips leading/trailing whitespace.
- `is_quote_in_source(quote: str, source_text: str) -> bool`:
  - Returns `True` if `canonical_normalize(quote)` is a substring of `canonical_normalize(source_text)`.

### 2. File: `tests/test_text_normalizer.py`
Create comprehensive pytest tests in `tests/test_text_normalizer.py`:
- Test HTML entity unescaping (e.g. `&amp;`, `&quot;`, `&lt;`).
- Test curly/smart quote and em-dash standardization.
- Test multi-line text with whitespace and newline variations.
- Test `is_quote_in_source()` matching positive and negative cases.

---

## Execution Steps for Jules
1. Create `src/utils/text_normalizer.py` (ensure `src/utils/__init__.py` exists).
2. Create `tests/test_text_normalizer.py`.
3. Run `uv run pytest tests/test_text_normalizer.py` to ensure all tests pass.
4. **Self-Cleaning Step (Required)**: Delete this task file (`.github/prompts/tasks/01_text_normalizer_utility.md`) so that merging the PR leaves the backlog clean.
