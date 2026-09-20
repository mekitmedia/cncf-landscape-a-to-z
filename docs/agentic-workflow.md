# Agentic Workflow Documentation

## 1. Overview

The content generation layer uses an AI-powered agent workflow to research CNCF projects and produce high-quality, verifiable content.

```
┌────────────────────────────────────────────────────────────┐
│                    AGENT WORKFLOW                          │
│                                                            │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │    EDITOR    │◄───────►│    WRITER    │                 │
│  │              │         │              │                 │
│  │ • Reviews    │         │ • Drafts     │                 │
│  │   grounding  │         │   Tool Pages │                 │
│  │ • Quality    │         │ • Synthesizes│                 │
│  │   gates      │         │   Blog Posts │                 │
│  │ • Tracks     │         │ • Revises    │                 │
│  │   state      │         │   drafts     │                 │
│  └──────┬───────┘         └──────▲───────┘                 │
│         │                        │                         │
│         │  Editorial Feedback    │                         │
│         │  & Iteration Loop      │                         │
│         └────────────────────────┘                         │
│                                                            │
│                  ┌──────────────┐                          │
│                  │  RESEARCHER  │                          │
│                  │ (Note-Taking)│                          │
│                  │ • Web search │                          │
│                  │ • Source URLs│                          │
│                  │ • Exact      │                          │
│                  │   quotes     │                          │
│                  └──────────────┘                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 2. Agent Roles & Responsibilities

### 2.1 Researcher Agent (`src/agentic/agents/researcher.py`)
- **Role**: Structured note-taking and evidence gathering.
- **Inputs**: Metadata from `data/weeks/<WEEK_ID>/categories/*.yaml` (name, repo URL, homepage, landscape category).
- **Outputs**: Note-taking YAML in `data/weeks/<WEEK_ID>/research/<sanitized_name>.yaml`.
- **Grounding Mandate**:
  - Extract multi-source evidence (GitHub README, release notes, documentation).
  - Capture verbatim quotes rather than unverified assertions.
  - Document version numbers, release dates, features, and use cases directly backed by quotes.

### 2.2 Grounding Validator & Critic
- **Role**: Enforce factuality before synthesis.
- **Checks**:
  - *Quote validation*: Checks that quotes exist in retrieved sources.
  - *API validation*: Verifies GitHub release tags and dates.
  - *Entailment verification*: Checks that synthesized bullet points are supported by the recorded quotes.
- See full specification in [editorial-governance-and-grounding.md](editorial-governance-and-grounding.md).

### 2.3 Writer Agent (`src/agentic/agents/writer.py`)
- **Role**: Synthesize validated research notes into target deliverables.
- **Target Deliverable 1 — Tool Pages (`website/content/tools/<tool>.md`)**:
  - Generates comprehensive reference pages with feature breakdowns, architecture overview, and getting-started guides.
- **Target Deliverable 2 — Weekly Blog Post (`website/content/posts/<YEAR>-<WEEK>.md`)**:
  - Drafts the narrative weekly post summarizing all researched projects for that letter.

### 2.4 Editor Agent (`src/agentic/agents/editor.py`)
- **Role**: Quality gatekeeper and orchestrator.
- **Responsibilities**:
  - Evaluates drafts against editorial criteria (accuracy, tone, structure, link integrity).
  - Provides targeted feedback for revisions if criteria are not met (up to 3 iteration loops).
  - Updates `data/weeks/<WEEK_ID>/tracker.yaml` task states.

---

## 3. Workflow Execution & State Management

### 3.1 Task Dependency Graph
The workflow respects the dependency graph managed in `tracker.yaml`:
1. `research` (Item level): Researcher creates `data/weeks/<WEEK_ID>/research/<item>.yaml`.
2. `content` (Item level): Writer creates tool page `website/content/tools/<item>.md`.
3. `blog_post` (Week level): Writer generates weekly post once all week items are completed.

### 3.2 Execution Options

#### Python Flow
```bash
# Option A: Run via 1Password CLI (recommended)
op run -- python src/cli.py run workflow

# Option B: Set environment variables directly
export GOOGLE_API_KEY="your_gemini_api_key"
export GEMINI_MODEL="gateway/google-vertex:gemini-2.5-flash"
export LOGFIRE_TOKEN="your_logfire_token"  # Optional for observability
python src/cli.py run workflow
```

> **Tip for Git Worktrees**: Place your local `.env` in the parent directory containing your worktrees (e.g. `../.env`). `just` and 1Password CLI walk up parent directories to locate `../.env`, sharing configuration across all worktrees cleanly.

#### Portable Skill
For contributor execution in Claude Code, Codex/OpenAI, OpenCode, or Antigravity without the Python runtime:
- Reference skill: `.agents/skills/cncf-weekly-content/SKILL.md`

---

## 4. Editorial Review Criteria & Quality Gates

All content must meet these editorial standards before approval:
- ✅ **Source Grounded**: Every technical claim is supported by a quote in research notes.
- ✅ **Deterministic Accuracy**: Release versions and dates match upstream GitHub data.
- ✅ **Tone & Style**: Discovery-focused, informative, objective, avoiding marketing fluff.
- ✅ **Completeness**: Tool pages include clear getting started instructions and feature summaries.
- ✅ **Link Integrity**: All hyperlinks return valid 200 OK statuses.

---

## 5. Troubleshooting & Diagnostics

### Common Issues
- **Research files empty or contain errors**: Check rate limits or network access; inspect error messages in YAML.
- **Low-quality output**: Inspect research notes in `data/weeks/<WEEK_ID>/research/` to verify source quote grounding before re-running.
- **Tracker out of sync**: Run ETL sync to ensure all projects are tracked in `tracker.yaml`.
