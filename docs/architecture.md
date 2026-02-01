# Design Document: CNCF Landscape Content Generation

## Overview

This project automates the generation of content for a website focused on the Cloud Native Computing Foundation (CNCF) landscape. The goal is to provide weekly updates covering open source projects, prioritizing discovery through AI-powered research and iterative editorial refinement.

## System Architecture

The system is composed of two independent layers that operate sequentially:

1.  **Deterministic Layer (ETL Pipeline)**: Parses the CNCF landscape and prepares structured data
2.  **Agentic Layer (Content Generation)**: Uses AI agents with iterative editing to research and draft content

```
┌─────────────────────────────────────────────────────────────────┐
│                      ETL PIPELINE (Layer 1)                      │
│                                                                  │
│  Input: CNCF Landscape YAML                                     │
│    │                                                             │
│    ├─> Extract: Fetch from GitHub/local file                   │
│    ├─> Transform: Filter by letter, sanitize categories        │
│    └─> Load: Generate structured YAML files                    │
│                                                                  │
│  Outputs:                                                        │
│    • data/week_XX_Y/*.yaml (category files)                    │
│    • data/week_XX_Y/tasks.yaml (simple name list)              │
│    • data/week_XX_Y/README.md (summary)                        │
│    • website/content/letters/Y/ (Hugo pages)                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   AGENTIC WORKFLOW (Layer 2)                    │
│                                                                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │   Editor     │◄────►│   Writer     │◄────►│  Researcher  │ │
│  │ (Orchestrate)│      │  (Draft)     │      │  (Gather)    │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│         │                                             │         │
│         │ Iteration Loop (max 3)                     │         │
│         │  1. Writer drafts                           │         │
│         │  2. Editor reviews + feedback                │         │
│         │  3. Writer revises (if needed)              │         │
│         └─────────────────────────────────────────────┘         │
│                                                                  │
│  Inputs (Read-Only):                                            │
│    • data/week_XX_Y/*.yaml (project metadata)                  │
│    • TODO.md (progress tracking)                               │
│                                                                  │
│  Outputs (Persistent):                                          │
│    • data/week_XX_Y/research/{sanitized_name}.yaml             │
│    • website/content/posts/YYYY-Y.md (final approved post)     │
│    • TODO.md (updated with iteration history)                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS PIPELINE                     │
│                                                                  │
│  1. Workflow runs in feature branch: content/{letter}-{time}   │
│  2. Commits: research/*.yaml + posts/*.md + TODO.md            │
│  3. Opens PR with peter-evans/create-pull-request              │
│  4. Human reviews PR → approves → merges to main               │
│  5. Hugo builds + deploys website                              │
└─────────────────────────────────────────────────────────────────┘
```

## Layer 1: ETL Pipeline (Deterministic)

### Purpose
Transform the upstream CNCF landscape into consumable, organized data structures split by alphabetical letter for weekly processing.

### Input
- **Primary**: CNCF Landscape YAML from `https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml`
- **Alternative**: Local YAML file via `--input_path` parameter

### Process Flow
1. **Extract**: Fetch landscape YAML via HTTP or read from local file
2. **Transform**:
   - Filter projects by first letter of name (A-Z = 26 weeks)
   - Exclude archived projects and items without `repo_url`
   - Sanitize category names for filesystem compatibility (e.g., "App & Dev" → `app_definition_and_development`)
   - Group projects by category and subcategory
3. **Load**:
   - Generate directory: `data/week_{index:02d}_{letter}/`
   - Write category YAML files with full project metadata
   - Write `tasks.yaml` with simple project name list
   - Generate `README.md` summary using Jinja2 template
   - Create Hugo letter pages in `website/content/letters/{letter}/`

### Outputs

| File/Directory | Purpose | Format | Update Strategy |
|---------------|---------|--------|-----------------|
| `data/categories.yaml` | Full category taxonomy | YAML | Regenerate on each run |
| `data/category_index.yaml` | Category→path mappings | YAML | Regenerate on each run |
| `data/category_item_index.yaml` | Category→items index | YAML | Regenerate on each run |
| `data/stats_*.yaml` | Various statistics | YAML | Regenerate on each run |
| `data/excluded_items.yaml` | Non-OSS projects | YAML | Regenerate on each run |
| `data/week_XX_Y/*.yaml` | Category project details | YAML | Regenerate on each run |
| `data/week_XX_Y/tasks.yaml` | Simple project names | YAML | Regenerate on each run |
| `data/week_XX_Y/README.md` | Week summary | Markdown | Regenerate on each run |
| `website/content/letters/Y/` | Hugo letter pages | Markdown | Regenerate on each run |

### File Naming Conventions
- **Week directories**: `week_{index:02d}_{letter}` (e.g., `week_00_A`, `week_25_Z`)
- **Category files**: `{sanitized_category}_{sanitized_subcategory}.yaml`
- **Sanitization rules**: lowercase, spaces→underscores, special chars→underscores

### Execution
```bash
# Run ETL pipeline
python src/cli.py run etl

# With custom input
python src/cli.py run etl --input_path ./landscape.yml --output_dir ./custom_data
```

## Layer 2: Agentic Workflow (AI-Powered)

### Purpose
Generate high-quality, well-researched blog posts through an iterative editorial process with AI agents playing distinct roles.

### Agent Roles

#### 1. Editor Agent (Orchestrator)
**Responsibility**: Decides which week to process and manages the content iteration cycle

**Tools**:
- `check_existing_post(letter)`: Verifies if `website/content/posts/YYYY-{letter}.md` exists
- `read_todo()`: Reads `TODO.md` for progress tracking
- `write_todo(content)`: Updates `TODO.md` with decisions and iteration history
- `list_week_projects(letter)`: Reads project count from `data/week_XX_Y/tasks.yaml`

**Decision Flow**:
1. Check `TODO.md` for completed/in-progress weeks
2. Select next letter (A→Z sequential priority)
3. Orchestrate Writer-Editor iteration loop (max 3 iterations)
4. On approval: commit all files and mark week complete in `TODO.md`

**Editorial Review Criteria**:
- Technical accuracy of project descriptions
- Consistent tone (engaging, discovery-focused)
- Completeness (all key sections present)
- Proper markdown formatting
- No hallucinations or outdated information

#### 2. Researcher Agent (Data Gatherer)
**Responsibility**: Deep-dive research on individual projects using web search and documentation

**Tools**:
- `web_search(query, max_results=3)`: DuckDuckGo search for project information

**Input**: `ProjectMetadata(name, repo_url, homepage)`

**Output**: `ResearchOutput` persisted to `data/week_XX_Y/research/{sanitized_name}.yaml`
```yaml
project_name: "Apache Kafka"
summary: "Distributed event streaming platform for high-throughput data pipelines"
key_features:
  - "Pub/sub messaging with persistent storage"
  - "Scalable to trillions of events per day"
  - "Real-time stream processing with Kafka Streams"
recent_updates: "Kafka 3.6 released with KRaft mode generally available"
use_cases: "Event sourcing, log aggregation, real-time analytics, CDC"
interesting_facts: "Used by 80% of Fortune 100 companies"
```

**Process**:
- Runs in parallel for all projects in a week (using Prefect `task.map`)
- Searches for: latest releases, community discussions, use cases, architecture details
- Handles failures gracefully: saves error message in research file for debugging

#### 3. Writer Agent (Content Creator)
**Responsibility**: Synthesizes research into engaging blog posts, revises based on Editor feedback

**Input**: 
- List of `ResearchOutput` objects (read from `data/week_XX_Y/research/*.yaml`)
- Optional: `EditorFeedback` from previous iteration

**Output**: `BlogPostDraft(title, content_markdown)`

**Content Structure**:
```markdown
---
title: "Letter {X}: {N} Projects Starting with {X}"
date: YYYY-MM-DDTHH:MM:SSZ
draft: false
---

# Introduction
Hook paragraph highlighting the letter's theme and project count.

# Project 1: {Name}
## What is it?
Clear 2-3 sentence explanation of the project.

## Why it matters
Value proposition and problem it solves.

## Key Features
- Feature 1
- Feature 2
- Feature 3

## Get Started
Brief installation/usage example.

---

[Repeat for all projects]

# Conclusion
Summary of the week's discoveries.
```

**Revision Process**:
- On iteration 1: Write fresh draft from research
- On iteration 2+: Read previous draft + Editor feedback → revise specific sections
- Maintains consistent voice across revisions

### Iteration Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ WEEK PROCESSING CYCLE                                           │
│                                                                  │
│  1. Editor selects letter (e.g., "B")                           │
│  2. Load projects from data/week_01_B/*.yaml                   │
│  3. Researcher: Parallel research all projects                  │
│     └─> Save to data/week_01_B/research/{name}.yaml           │
│                                                                  │
│  4. ITERATION LOOP (max 3):                                     │
│     ┌────────────────────────────────────────────────┐         │
│     │ Iteration 1:                                     │         │
│     │   • Writer reads all research files             │         │
│     │   • Drafts complete blog post                   │         │
│     │   • Editor reviews draft                        │         │
│     │   • If approved → DONE                          │         │
│     │   • If rejected → provide structured feedback   │         │
│     │                                                  │         │
│     │ Iteration 2:                                     │         │
│     │   • Writer reads: research + feedback + draft   │         │
│     │   • Revises specific sections per feedback      │         │
│     │   • Editor reviews revised draft                │         │
│     │   • If approved → DONE                          │         │
│     │   • If rejected → provide feedback (iteration 3)│         │
│     │                                                  │         │
│     │ Iteration 3:                                     │         │
│     │   • Writer final revision attempt               │         │
│     │   • Editor reviews                              │         │
│     │   • Auto-approve after max iterations           │         │
│     └────────────────────────────────────────────────┘         │
│                                                                  │
│  5. Editor saves approved post:                                 │
│     • website/content/posts/YYYY-B.md                          │
│     • Updates TODO.md with completion status                   │
│                                                                  │
│  6. All changes committed to feature branch                     │
└─────────────────────────────────────────────────────────────────┘
```

### Data Models

```python
class ProjectMetadata(BaseModel):
    name: str
    repo_url: Optional[str] = None
    homepage: Optional[str] = None

class ResearchOutput(BaseModel):
    project_name: str
    summary: str
    key_features: List[str]
    recent_updates: str
    use_cases: str
    interesting_facts: Optional[str] = None

class EditorFeedback(BaseModel):
    iteration: int
    approved: bool
    feedback: str  # Structured feedback on specific sections to improve
    review_timestamp: str

class BlogPostDraft(BaseModel):
    title: str
    content_markdown: str
```

### File Naming Conventions

#### Research Files
- **Location**: `data/week_XX_Y/research/`
- **Pattern**: `{sanitized_project_name}.yaml`
- **Sanitization**: `name.lower().replace(' ', '_').replace('/', '_').replace('-', '_')`
- **Examples**:
  - "Apache Kafka" → `apache_kafka.yaml`
  - "Kong/Insomnia" → `kong_insomnia.yaml`
  - "cert-manager" → `cert_manager.yaml`

#### Draft Files (during iterations)
- **Location**: `data/week_XX_Y/` (temporary)
- **Pattern**: `draft.md` (single file, overwritten each iteration)
- **Lifecycle**: Exists only in feature branch, deleted after approval

#### Final Posts
- **Location**: `website/content/posts/`
- **Pattern**: `YYYY-{letter}.md` (e.g., `2026-A.md`)
- **Overwrite Policy**: Only Editor can write/overwrite these files

### Inputs (Read-Only for Agentic Layer)

| File/Directory | Purpose | Read By |
|---------------|---------|---------|
| `data/week_XX_Y/*.yaml` | Project metadata (repo_url, homepage, etc.) | Researcher |
| `data/week_XX_Y/tasks.yaml` | List of project names for the week | Editor |
| `TODO.md` | Progress tracking, iteration history | Editor |

### Outputs (Written by Agentic Layer)

| File/Directory | Purpose | Written By | Update Strategy |
|---------------|---------|------------|-----------------|
| `data/week_XX_Y/research/{name}.yaml` | Individual project research | Researcher | Create once per project |
| `data/week_XX_Y/draft.md` | Temporary draft during iterations | Writer | Overwrite each iteration |
| `website/content/posts/YYYY-{letter}.md` | Final approved blog post | Editor | Create/overwrite on approval |
| `TODO.md` | Progress and iteration history | Editor | Append iteration logs |

## Conflict Prevention & Data Integrity

### Exclusive Write Zones
Each workflow has exclusive ownership of specific directories to prevent conflicts:

| Directory | ETL (Write) | Agentic (Write) | Agentic (Read) |
|-----------|-------------|-----------------|----------------|
| `data/week_XX_Y/*.yaml` | ✅ Regenerate | ❌ Never | ✅ Read-only |
| `data/week_XX_Y/research/` | ❌ Never | ✅ Create | ✅ Read |
| `website/content/letters/` | ✅ Regenerate | ❌ Never | ❌ Never |
| `website/content/posts/` | ❌ Never | ✅ Editor only | ✅ Read |
| `TODO.md` | ❌ Never | ✅ Editor only | ✅ Read |

### Safe Concurrent Execution Rules
1. **ETL runs first**: Always execute ETL pipeline before agentic workflow
2. **Feature branch isolation**: Agentic workflow runs in dedicated feature branch
3. **No file locking needed**: Exclusive write zones eliminate race conditions
4. **Read-only data**: Agentic layer never modifies ETL outputs

### Update Strategies

#### ETL Pipeline
- **Strategy**: Full regeneration on each run
- **Rationale**: Upstream CNCF landscape is source of truth
- **Impact**: Overwrites `data/` and `website/content/letters/` completely
- **Schedule**: Weekly via GitHub Actions (Monday 00:00 UTC)

#### Agentic Workflow
- **Strategy**: Selective write with Editor approval
- **Rationale**: Research is expensive (API costs), posts require editorial review
- **Impact**: Adds research files, creates/updates posts only after iteration approval
- **Schedule**: After ETL completes, manual trigger via workflow_dispatch

#### Research Files
- **Persistence**: Permanent (not regenerated unless project researched again)
- **Benefits**: 
  - Debugging: Inspect what Researcher found
  - Audit trail: Track AI research quality over time
  - Re-runs: Writer can revise posts without re-researching

#### TODO.md Management
- **Version control**: Tracked in git (not .gitignored)
- **Purpose**: 
  - Progress tracking across workflow runs
  - Iteration history (what feedback was given, how many iterations)
  - Completed weeks (prevent duplicate work)
- **Structure**:
```markdown
# CNCF Landscape A-to-Z Progress

## Completed Weeks
- [x] Week 00 (A) - 61 projects - 2 iterations - Approved 2026-01-15
- [x] Week 01 (B) - 54 projects - 1 iteration - Approved 2026-01-22

## In Progress
- [ ] Week 02 (C) - 48 projects - Iteration 1 in progress

## Iteration History
### Week 01 (B) - 2026-01-22
- Iteration 1: Editor feedback: "Add more recent updates for Backstage and Buildpacks"
- Iteration 2: Writer revised → Approved

## Pending Weeks
- [ ] Week 03 (D) - 52 projects
- [ ] Week 04 (E) - 43 projects
[... through Z]
```

## GitHub Actions Pipeline

### Workflow: ETL Data Update (`.github/workflows/update_data.yml`)
**Trigger**: Schedule (weekly Monday) OR manual workflow_dispatch

**Steps**:
1. Checkout repository
2. Install Python + dependencies
3. Run `python src/cli.py run etl`
4. Create PR with updated `data/` files
5. Human reviews PR → merges to main

### Workflow: Agentic Content Generation (`.github/workflows/agents.yml`)
**Trigger**: Manual workflow_dispatch with `limit` parameter

**Steps**:
1. Checkout repository (main branch)
2. Create feature branch: `content/{letter}-{timestamp}`
3. Install Python + dependencies
4. Run `python src/cli.py run workflow --limit={input}`
5. Commit changes:
   - `data/week_XX_Y/research/*.yaml` (new research files)
   - `website/content/posts/YYYY-{letter}.md` (final post)
   - `TODO.md` (updated progress)
6. Open PR using `peter-evans/create-pull-request`:
   - Title: "Weekly Content: Letter {X} ({N} projects)"
   - Body: PR template with iteration summary, project list, editorial notes
   - Branch: `content/{letter}-{timestamp}`
   - Base: `main`
7. Human reviews PR:
   - Check post quality (technical accuracy, tone, completeness)
   - Review TODO.md iteration history
   - Inspect research files if needed
8. Human approves + merges PR
9. Hugo deployment workflow triggers on merge to main

### PR Template for Content PRs
```markdown
## Weekly Content: Letter {X}

### Summary
- **Projects researched**: {count}
- **Iterations**: {iteration_count}
- **Editor approval**: ✅ Approved on iteration {N}

### Projects Included
{list of project names}

### Iteration History
{summary from TODO.md}

### Editorial Notes
{Editor's final approval reasoning}

### Checklist
- [ ] Technical accuracy verified
- [ ] Tone is engaging and discovery-focused
- [ ] All key sections present (What/Why/Features/GetStarted)
- [ ] Markdown formatting correct
- [ ] Research files committed for audit trail
- [ ] TODO.md updated with completion status
```

## Deployment Pipeline

```
PR Merge → Main Branch
    ↓
Hugo Build Workflow (.github/workflows/deploy.yml)
    ↓
Build Hugo Site (website/)
    ├─> Reads data/ for Hugo data templates
    ├─> Reads website/content/posts/ for blog posts
    └─> Reads website/content/letters/ for letter pages
    ↓
Deploy to GitHub Pages / Netlify
```

## Execution Guide

### Full Weekly Cycle
```bash
# 1. Run ETL to fetch latest CNCF data
python src/cli.py run etl

# 2. Verify data generated
ls data/week_*

# 3. Run agentic workflow (limit optional)
python src/cli.py run workflow --limit 50

# 4. Review TODO.md for iteration history
cat TODO.md

# 5. Inspect research files
ls data/week_*/research/

# 6. Review generated post
cat website/content/posts/2026-B.md
```

### Local Development
```bash
# Set environment variables
export GOOGLE_API_KEY=your_key_here
export LOGFIRE_TOKEN=your_token_here  # Optional
export GEMINI_MODEL=gemini-2.0-flash-exp

# Run single letter with limit
python src/cli.py run workflow --limit 10

# Run in local mode (uses local data, no Prefect Cloud)
python src/cli.py run workflow --local
```

## Next Steps & Future Enhancements

### Phase 1: Core Implementation (Current)
- ✅ ETL pipeline with letter-based splitting
- ✅ Agentic workflow with Editor/Researcher/Writer agents
- ✅ Prefect orchestration
- 🔄 Research file persistence
- 🔄 Editorial iteration loop
- 🔄 TODO.md version control

### Phase 2: Quality Improvements
- [ ] Structured data output (JSON frontmatter for Hugo data templates)
- [ ] Enhanced Writer prompts for consistent style
- [ ] Research result caching (avoid re-researching same projects)
- [ ] Rate limiting and retry logic for API calls
- [ ] Visual regression tests (Playwright) in PR checks

### Phase 3: Advanced Features
- [ ] Multi-model support (Gemini, Claude, GPT-4)
- [ ] Human-in-the-loop for iteration 2+ (Slack integration)
- [ ] Newsletter generation (email template from blog post)
- [ ] Analytics integration (track which projects get most attention)
- [ ] Community contributions (allow PRs with additional project research)
