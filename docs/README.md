# CNCF Landscape A-to-Z Documentation

Welcome to the technical documentation for the CNCF Landscape A-to-Z project. This documentation covers both the deterministic ETL pipeline and the AI-powered agentic workflow for automated content generation, research note-taking, and editorial governance.

---

## 📚 Documentation Structure

```
docs/
├── 🏛️ Architecture & System Design
│   ├── architecture.md                        # Overall system architecture & 2-layer design
│   └── website-architecture.md                # Hugo 3-level content hierarchy & tool pages
│
├── ⚙️ Pipelines & Orchestration
│   ├── etl-pipeline.md                        # Deterministic CNCF extraction & taxonomy ETL
│   ├── graph-driven-orchestration.md          # Parallel graph execution & task dependencies
│   └── tracker.md                             # State tracking, task lifecycle & tracker.yaml
│
├── 🛡️ Editorial Governance & Grounding (NEW)
│   └── editorial-governance-and-grounding.md  # Provenance, quote grounding, no-vector-DB design
│
├── 🤖 Agent Workflows & Contributor Skills
│   ├── agentic-workflow.md                    # Editor, Researcher, Writer agents & iteration loop
│   └── ../.agents/skills/cncf-weekly-content/ # Multi-harness portable skill
│
└── 🔬 Explorations & Optimizations
    ├── token-optimization.md                  # Token reduction & prompt engineering
    └── iteration-and-tokens.md                # Cost vs. quality trade-offs in feedback loops
```

---

## 📖 Directory of Documentation Files

### Core Architecture & System Design

#### [architecture.md](architecture.md)
**System Architecture & Design**
- Two-layer architecture (Deterministic ETL + Agentic content generation)
- End-to-end data flow from upstream CNCF landscape to published Hugo site
- Conflict prevention through exclusive write zones
- GitHub Actions CI/CD integration and automated pull request workflow

#### [website-architecture.md](website-architecture.md)
**Website Design, Tool Pages & Content Hierarchy**
- Three-level content hierarchy (Level 1: Featured Tools → Level 2: Letter Categories → Level 3: Tool Deep Dives)
- Tool page generation (`website/content/tools/`) from research notes
- Hugo template structure, taxonomy mapping, and navigation

---

### Pipelines & State Management

#### [etl-pipeline.md](etl-pipeline.md)
**ETL Pipeline Documentation**
- Deterministic data processing (Extract, Transform, Load)
- Input sources (`landscape.yml`) and output taxonomy files (`data/weeks/<WEEK_ID>/categories/`)
- Data contracts, guarantees, sanitization, and category grouping

#### [graph-driven-orchestration.md](graph-driven-orchestration.md)
**Graph-Driven Parallel Orchestration**
- Parallel execution of independent item-level research tasks
- Embedded task dependency graph (`research` → `content` → `blog_post`)
- Batch scheduler (`get_ready_tasks`) for maximum concurrency

#### [tracker.md](tracker.md)
**Task Tracker & State Machine**
- Persistent task tracking via `data/weeks/<WEEK_ID>/tracker.yaml`
- Task types (`research`, `content`, `blog_post`), states (`PENDING`, `IN_PROGRESS`, `COMPLETED`, `FAILED`), and retry policies
- Tracker interface and synchronization with upstream ETL changes

---

### Editorial Governance & Content Quality

#### [editorial-governance-and-grounding.md](editorial-governance-and-grounding.md) *(New)*
**Editorial Governance, Provenance & Grounding Validation**
- Separation of target publications (**Tool Pages** and **Weekly Blog Posts**) from intermediate artifacts (**Research Note-Taking**)
- Multi-source provenance capturing verbatim quotes without requiring an external vector database
- Three-layer grounding verification (Substring/Fuzzy matching, GitHub Release API checks, Entailment Critic)
- Human-in-the-Loop (HITL) review gates and PR audit reporting

---

### Agent Workflows & Contributor Skills

#### [agentic-workflow.md](agentic-workflow.md)
**Agentic Workflow & Editorial Feedback Loop**
- Specialized agent roles: **Editor** (orchestration & quality review), **Researcher** (fact gathering & source extraction), **Writer** (synthesis of tool pages & blog posts)
- Iterative editorial revision cycles (up to 3 rounds)
- Prompt guidelines and editorial standards

#### [CNCF Weekly Content Skill](../.agents/skills/cncf-weekly-content/SKILL.md)
**Portable Skill for Claude Code, Codex/OpenAI, OpenCode, and Antigravity**
- Harness-agnostic skill definition allowing contributors to run the weekly workflow without the Pydantic AI runtime

---

### Explorations & Optimization History

#### [token-optimization.md](token-optimization.md) & [iteration-and-tokens.md](iteration-and-tokens.md)
**Token Optimization & Empirical Evaluations**
- Token usage benchmarks across agent roles
- Context window pruning strategies and prompt compression
- Cost-benefit analysis of multi-cycle editorial iterations

---

## 🚀 Quick Start

### 1. Deterministic ETL Run
```bash
# Extract and process CNCF landscape data into structured week buckets
python src/cli.py run etl
```

### 2. State & Task Inspection
```bash
# Check current tasks and status for Week 00-A
cat data/weeks/00-A/tracker.yaml
```

### 3. Agentic Workflow Execution

```bash
# Option A: Run via 1Password CLI (recommended)
op run -- python src/cli.py run workflow

# Option B: Set environment variables directly
export GOOGLE_API_KEY="your_gemini_api_key"
export GEMINI_MODEL="gateway/google-vertex:gemini-2.5-flash"
export LOGFIRE_TOKEN="your_logfire_token"  # Optional
python src/cli.py run workflow
```

> **Tip for Git Worktrees**: Place your local `.env` in the parent directory containing your worktrees (e.g. `../.env`). `just` and 1Password CLI walk up parent directories to locate `../.env`, sharing configuration across all worktrees cleanly.

### 4. Inspect Generated Outputs
```bash
# Inspect intermediate research notes
ls data/weeks/00-A/research/

# Inspect target blog post
cat website/content/posts/2026-A.md

# Inspect target tool pages
ls website/content/tools/
```

---

## 🤝 Key Governance & Contribution Rules

1. **Exclusive Write Zones**:
   - `data/weeks/<WEEK_ID>/categories/*.yaml` → **ETL only** (Read-only for agents)
   - `data/weeks/<WEEK_ID>/tracker.yaml` → **Tracker / Orchestrator only**
   - `data/weeks/<WEEK_ID>/research/*.yaml` → **Researcher notes only**
   - `website/content/tools/*.md` & `website/content/posts/*.md` → **Writer only**
2. **Grounding by Construction**:
   - Every claim in research notes must link to a valid source with an exact quote excerpt.
   - Never hallucinate facts or release dates; leave explicit placeholders if unverified.
3. **Documentation Hygiene**:
   - When modifying data structures or agent workflows, update the corresponding document in `docs/`.
