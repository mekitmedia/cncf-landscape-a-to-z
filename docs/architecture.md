# System Architecture: CNCF Landscape A-to-Z

## 1. Overview

The CNCF Landscape A-to-Z project automates discovery and technical content generation for hundreds of cloud-native projects in the CNCF landscape. The system operates on a weekly cadence (organized alphabetically from Week `00-A` to `25-Z`).

The architecture is built on two primary layers:
1. **Deterministic Layer (ETL Pipeline)**: Ingests, filters, and groups CNCF landscape data into structured, version-controlled files.
2. **Agentic Layer (Content Generation & Governance)**: Orchestrates AI agents to perform grounded research note-taking, generate individual Tool Pages, and draft weekly narrative Blog Posts.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DETERMINISTIC LAYER (ETL)                    │
│                                                                  │
│  Upstream: CNCF Landscape YAML (landscape.yml)                  │
│    │                                                             │
│    ├─> Extract: Ingest raw landscape data                       │
│    ├─> Transform: Filter OSS, categorize, group by letter (A-Z)  │
│    └─> Load: Generate structured YAML files                     │
│                                                                  │
│  Outputs:                                                        │
│    • data/weeks/<WEEK_ID>/categories/*.yaml (project metadata)   │
│    • data/weeks/<WEEK_ID>/tracker.yaml (state machine & graph)   │
│    • data/weeks/<WEEK_ID>/README.md (week statistics)            │
│    • website/content/letters/<LETTER>/_index.md (Hugo listing)   │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENTIC LAYER (Content & Governance)               │
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐   │
│  │    Editor    │◄────►│    Writer    │◄────►│  Researcher  │   │
│  │ (Governance) │      │  (Synthesis) │      │ (Note-Taking)│   │
│  └──────────────┘      └──────────────┘      └──────────────┘   │
│                                                                  │
│  Research Note-Taking:                                          │
│    • data/weeks/<WEEK_ID>/research/<tool>.yaml                  │
│      (Verbatim source quotes, release dates, features)           │
│                                                                  │
│  Grounding Validation:                                          │
│    • Quote substring validation & GitHub API release checks     │
│    • Entailment Critic (verifies claims against quotes)         │
│                                                                  │
│  Target Deliverables:                                            │
│    • website/content/tools/<tool>.md (Tool deep dives)          │
│    • website/content/posts/<YEAR>-<LETTER>.md (Weekly blog)     │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS & HUGO                       │
│                                                                  │
│  1. CI runs automated grounding & link integrity linters        │
│  2. Opens PR with editorial health metrics                      │
│  3. Human Editor reviews and merges to main                     │
│  4. Hugo deploys static site (Homepage, Letters, Tools, Posts)   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Layer 1: ETL Pipeline (Deterministic)

### Purpose
Extracts data from the official CNCF landscape repository, categorizes projects alphabetically (A–Z), and establishes the baseline metadata and initial task tracker for each week.

### Inputs & Outputs
- **Input**: Upstream `https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml`
- **Output Directories**:
  - `data/index/`: Taxonomy indices, category mappings, and statistics
  - `data/weeks/<WEEK_ID>/categories/*.yaml`: Sanitized project metadata
  - `data/weeks/<WEEK_ID>/tracker.yaml`: Initialized task dependency graph
  - `data/weeks/<WEEK_ID>/README.md`: Human-readable letter summary

---

## 3. Layer 2: Content Generation & Editorial Governance

### Target Content vs. Note-Taking Artifacts
- **Intermediate Working Memory**: `data/weeks/<WEEK_ID>/research/*.yaml`
  - Acts as structured **note-taking** by the Researcher agent.
  - Contains multi-source provenance, verbatim quotes, and extracted facts.
  - Kept in Git without an external vector database to maximize auditability and transparency.
- **Target Deliverable 1: Tool Pages (`website/content/tools/*.md`)**:
  - Comprehensive reference pages for individual projects with specs, features, and getting started guides.
- **Target Deliverable 2: Weekly Blog Posts (`website/content/posts/<YEAR>-<LETTER>.md`)**:
  - Editorial weekly articles summarizing projects, trends, and release updates.

### Multi-Agent Workflow
1. **Researcher Agent**:
   - Fetches repository READMEs, release notes, and official documentation.
   - Extracts verbatim quotes and records them in structured research notes.
2. **Grounding Validator / Critic**:
   - Performs deterministic verification (quote substring checks, GitHub release API verification).
   - Validates that synthesized statements are directly entailed by the cited quotes.
3. **Writer Agent**:
   - Synthesizes research notes into individual tool markdown pages and weekly blog posts.
4. **Editor Agent & Governance**:
   - Enforces editorial guidelines, reviews drafts, and updates `tracker.yaml`.

---

## 4. Exclusive Write Zones (Conflict Prevention)

To prevent race conditions and merge conflicts across workflows, each component has an exclusive write boundary:

| Path | ETL Pipeline | Researcher | Writer / Script | Editor / Orchestrator |
|---|---|---|---|---|
| `data/index/*.yaml` | ✅ Write | ❌ Read-only | ❌ Read-only | ❌ Read-only |
| `data/weeks/*/categories/*.yaml` | ✅ Write | ❌ Read-only | ❌ Read-only | ❌ Read-only |
| `data/weeks/*/research/*.yaml` | ❌ Never | ✅ Write | ❌ Read-only | ❌ Read-only |
| `data/weeks/*/tracker.yaml` | ❌ Init only | ❌ Read-only | ❌ Read-only | ✅ Write |
| `website/content/tools/*.md` | ❌ Never | ❌ Never | ✅ Write | ❌ Read-only |
| `website/content/posts/*.md` | ❌ Never | ❌ Never | ✅ Write | ✅ Review/Approve |

---

## 5. Execution Modes

1. **Python Orchestrator**: Run locally or in CI via `python src/cli.py run workflow` (supports parallel graph scheduling).
2. **Portable Harness Skill**: Contributor execution via `.agents/skills/cncf-weekly-content/SKILL.md` across coding harnesses (Claude Code, Google Jules, Copilot, Codex/OpenAI, OpenCode, Antigravity).
3. **Automated CI / PR Workflow**: Scheduled GitHub Actions run ETL and content workflows, generating PRs with automated grounding audits.
