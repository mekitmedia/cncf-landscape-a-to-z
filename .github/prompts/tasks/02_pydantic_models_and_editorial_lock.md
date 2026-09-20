# Task 02: Enhance Research Models with Source Evidence and Editorial Lock

## Objective
Update Pydantic models in `src/agentic/models.py` to support multi-source verbatim quotes and the `editorial_lock` guardrail to prevent automated runs from stomping on manual human edits.

---

## Technical Specifications

### 1. File: `src/agentic/models.py`
1. Define `SourceEvidence` model:
   ```python
   class SourceEvidence(BaseModel):
       id: str
       title: Optional[str] = None
       url: str
       source_type: str = Field(
           default="official_docs",
           description="Source category: github_readme | github_release | official_docs | cncf_landscape"
       )
       quotes: List[str] = Field(
           default_factory=list,
           description="Verbatim text excerpts extracted from the source"
       )
   ```
2. Update `ResearchOutput` model:
   - Add `sources: List[SourceEvidence] = Field(default_factory=list)`
   - Add `editorial_lock: bool = Field(default=False, description="Set to True to prevent automated overwrites")`
   - Add `locked_by: Optional[str] = None`
   - Add `locked_at: Optional[str] = None`

### 2. File: `src/tracker/yaml_backend.py` (or runner flow)
- In the task execution flow before saving research outputs or tool pages, check if target file exists and contains `editorial_lock: true`.
- If `editorial_lock: true` and `force_override=False`, skip overwriting and log: `f"Skipping {item_name}: Protected by editorial lock"`.

### 3. File: `tests/test_editorial_lock.py`
Create tests verifying:
- `ResearchOutput` can parse and dump `SourceEvidence` with verbatim quotes.
- `ResearchOutput` preserves `editorial_lock: true` and lock metadata.
- Execution guard correctly skips locked items.

---

## Execution Steps for Jules
1. Update `src/agentic/models.py`.
2. Update `src/tracker/yaml_backend.py` or research persistence handlers to respect `editorial_lock`.
3. Create `tests/test_editorial_lock.py`.
4. Run `uv run pytest` to ensure all 54+ tests pass.
5. **Self-Cleaning Step (Required)**: Delete this task file (`.github/prompts/tasks/02_pydantic_models_and_editorial_lock.md`) before committing.
