---
name: editorial-governance
description: Multi-harness skill to enforce verifiable source quote grounding, text normalization, editorial locking, and anti-hallucination governance across CNCF research and post generation.
owner: mekitmedia/cncf-landscape-a-to-z
version: 1
---

# CNCF Editorial Governance & Source Grounding

## Purpose
Use this skill across all agent harnesses (Claude Code, GitHub Copilot, Google Jules, Antigravity, OpenCode, Codex, Pydantic AI) to:
1. Enforce strict **verifiable source quote grounding** on all CNCF research notes.
2. Apply **canonical text normalization** (`src/utils/text_normalizer.py`) to prevent false-alarm quote rejections from Unicode formatting, em-dashes, or smart quotes.
3. Protect human-curated and reviewed content from automated overwrites via `editorial_lock`.
4. Maintain deterministic citation chains connecting research YAMLs, website tool pages, and weekly summary posts.

---

## Core Guardrails & Rules

### 1. Direct Quote Verifiability
- Never paraphrase when filling `quotes:` in `SourceEvidence`.
- Every claim in `summary`, `key_features`, or `use_cases` must be grounded by at least one exact excerpt from official project documentation, GitHub READMEs, or release notes.

### 2. Canonical Text Normalization
When comparing quotes against source text:
```python
from src.utils.text_normalizer import normalize_text, is_quote_in_source

# Strip smart quotes, convert em-dashes, unescape HTML entities, and collapse whitespace
assert is_quote_in_source(extracted_quote, raw_webpage_content)
```

### 3. Respecting Editorial Lock
When updating research files or website markdown:
- If `editorial_lock: true` is present in the file frontmatter / YAML, **do not overwrite or mutate** the content during automated workflows.
- Only update if the user or workflow explicitly sets `--force-override` or `force_override=True`.

---

## Standard Research Schema (`data/weeks/<WEEK_ID>/research/<tool>.yaml`)

```yaml
project_name: "ExampleTool"
homepage_url: "https://example.com"
repo_url: "https://github.com/example/example"
docs_url: "https://docs.example.com"
cncf_status: "incubating" # sandbox | incubating | graduated | member
editorial_lock: false
sources:
  - id: "src_github_readme"
    title: "Official GitHub README"
    url: "https://github.com/example/example"
    source_type: "github_readme" # github_readme | github_release | official_docs | cncf_landscape
    quotes:
      - "Exact verbatim quote extracted from the source document"
summary: "Concise summary grounded in the source quote above."
key_features:
  - "Feature grounded directly in verified source documentation"
recent_updates: "Highlights from the latest verified release notes"
last_researched_at: "2026-09-20T21:00:00Z"
research_version: 1
```

---

## Verification & Auditing Commands

```bash
# Validate contract compliance of research and blog post files
uv run python scripts/validate_contract.py

# Run all grounding and normalization unit tests
uv run pytest tests/test_text_normalizer.py -v
```
