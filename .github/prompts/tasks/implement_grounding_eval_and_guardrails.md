# Task: Implement Grounding Validation & Edge-Case Safeguards

## Objective
Implement the deterministic grounding evaluation framework, text normalization utilities, editorial lock protocol, and DAG dependency protections in the CNCF Landscape A-to-Z repository as specified in `docs/editorial-governance-and-grounding.md` and `docs/model-capabilities-and-judge-design.md`.

---

## Background & Architecture Reference
Before writing code, review the architectural contracts in:
- `docs/editorial-governance-and-grounding.md` (Specifically Section 4 & Section 4.3)
- `docs/model-capabilities-and-judge-design.md`
- `scripts/validate_contract.py`

---

## Detailed Tasks to Implement

### 1. Text Normalization Utility (`src/utils/text_normalizer.py`)
Create a robust text normalization utility to prevent false-alarm quote rejections:
- `canonical_normalize(text: str) -> str`:
  - Unescape HTML entities (`html.unescape`).
  - Normalize unicode characters (NFKD, normalize smart quotes `“”"` and typographic dashes `—–-`).
  - Collapse multiple whitespaces and newlines into a single space.
  - Convert to lowercase and strip.
- `is_quote_in_source(quote: str, source_text: str) -> bool`:
  - Returns `True` if `canonical_normalize(quote)` is contained in `canonical_normalize(source_text)`.

### 2. Update Pydantic Models (`src/agentic/models.py`)
Enhance `ResearchOutput` and supporting models:
- Add `SourceEvidence` model:
  ```python
  class SourceEvidence(BaseModel):
      id: str
      title: Optional[str] = None
      url: str
      source_type: str  # "github_readme" | "github_release" | "official_docs" | "cncf_landscape"
      quotes: List[str] = Field(default_factory=list, description="Verbatim quotes from the source")
  ```
- Update `ResearchOutput` to include:
  - `sources: List[SourceEvidence] = Field(default_factory=list)`
  - `editorial_lock: bool = Field(default=False, description="True if locked against automated overwrites")`
  - `locked_by: Optional[str] = None`
  - `locked_at: Optional[str] = None`

### 3. Editorial Lock Guardrail in Tracker & Runner
- In `src/tracker/yaml_backend.py` (and agent execution flows):
  - Check if target research file or tool page has `editorial_lock: true`.
  - If locked and `--force-unlock` is not supplied, skip writing and log an informational message.

### 4. Deterministic Grounding Validator (`scripts/validate_grounding.py`)
Implement a CLI validation script (runnable in CI and pre-commit):
- Scans `data/weeks/*/research/*.yaml`.
- Verifies that every research note with `sources` contains valid non-empty `quotes`.
- If local cached text exists in `data/weeks/<WEEK_ID>/research/.cache/`, verifies `is_quote_in_source(quote, cached_text)`.
- Flags empty or suspicious ungrounded claims.
- CLI arguments: `--week <WEEK_ID>`, `--all-files`, `--git-diff <REF>`.

### 5. Add Test Suite (`tests/test_grounding_eval.py`)
Create comprehensive pytest tests:
- Test `canonical_normalize` with smart quotes, HTML entities, and varied newlines.
- Test `is_quote_in_source` matching.
- Test `SourceEvidence` validation in `ResearchOutput`.
- Test editorial lock guardrail skipping.
- Ensure 100% of tests in `uv run pytest` pass cleanly.

---

## Definition of Done
- `src/utils/text_normalizer.py` implemented and unit tested.
- `src/agentic/models.py` updated with `SourceEvidence` and `editorial_lock`.
- `scripts/validate_grounding.py` implemented and integrated with CI checks.
- All existing tests in `uv run pytest` continue to pass without regressions.
- Changes are self-contained and reviewable in a single PR.
