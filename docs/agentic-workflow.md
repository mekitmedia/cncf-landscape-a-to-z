# Agentic Workflow Documentation

This document describes the AI-powered agent workflow that generates weekly content for the CNCF Landscape A-to-Z website through iterative editorial refinement.

## Overview

The content generation uses a **trio of AI agents** orchestrated by **Prefect** to research CNCF projects and produce high-quality blog posts through an iterative editorial process. The workflow is located in `src/agentic/flow.py` and implements an Editor-Writer feedback loop with persistent research artifacts.

## Architecture

### Agent Roles

The workflow uses three specialized AI agents powered by Google Gemini via Pydantic AI:

```
┌────────────────────────────────────────────────────────────┐
│                    AGENT WORKFLOW                          │
│                                                            │
│  ┌──────────────┐         ┌──────────────┐               │
│  │   EDITOR     │◄───────►│   WRITER     │               │
│  │              │         │              │               │
│  │ • Selects    │         │ • Drafts     │               │
│  │   week       │         │   content    │               │
│  │ • Reviews    │         │ • Revises    │               │
│  │   drafts     │         │   based on   │               │
│  │ • Approves/  │         │   feedback   │               │
│  │   Rejects    │         │              │               │
│  │ • Tracks     │         │              │               │
│  │   progress   │         │              │               │
│  └──────┬───────┘         └──────▲───────┘               │
│         │                        │                        │
│         │  Iteration Loop        │                        │
│         │  (max 3 cycles)        │                        │
│         └────────────────────────┘                        │
│                                                            │
│                  ┌──────────────┐                         │
│                  │  RESEARCHER  │                         │
│                  │              │                         │
│                  │ • Gathers    │                         │
│                  │   project    │                         │
│                  │   info       │                         │
│                  │ • Web search │                         │
│                  │ • Persists   │                         │
│                  │   research   │                         │
│                  └──────────────┘                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### 1. Editor Agent (`src/agentic/agents/editor.py`)

**Role**: Orchestrator and quality gatekeeper

**Responsibilities**:
- Selects which letter/week to process next (A→Z sequential)
- Manages the iteration loop between Writer and Editor
- Reviews drafts against editorial criteria
- Provides structured feedback to Writer for revisions
- Approves final drafts for publication
- Tracks progress in `TODO.md`

**Tools**:
- `check_existing_post(letter: str) -> bool`: Checks if `website/content/posts/YYYY-{letter}.md` exists
- `read_todo() -> str`: Reads `TODO.md` for progress tracking and history
- `write_todo(content: str)`: Updates `TODO.md` with decisions and iteration logs
- `list_week_projects(letter: str) -> int`: Counts projects in `data/week_XX_Y/tasks.yaml`

**Decision Process**:
```python
1. Read TODO.md to check completed/in-progress weeks
2. Select next letter based on:
   - Priority: Sequential A→Z
   - Skip: Already completed weeks
   - Skip: Weeks currently in progress
3. Initiate research phase for selected week
4. Enter iteration loop:
   - Review Writer's draft
   - Check against editorial criteria (see below)
   - If approved: proceed to commit
   - If rejected: provide structured feedback → Writer revises
   - Max 3 iterations, then auto-approve
5. On approval:
   - Save post to website/content/posts/
   - Update TODO.md with completion status
   - Commit all changes
```

**Editorial Review Criteria**:
- ✅ **Technical Accuracy**: Descriptions match project reality, no hallucinations
- ✅ **Tone Consistency**: Engaging, discovery-focused, not dry or overly promotional
- ✅ **Completeness**: All sections present (What/Why/Features/Get Started)
- ✅ **Recent Information**: Updates reflect current state, not outdated
- ✅ **Markdown Quality**: Proper formatting, no broken links, consistent structure
- ✅ **Balance**: Equal coverage across projects, no favoritism

### 2. Researcher Agent (`src/agentic/agents/researcher.py`)

**Role**: Information gatherer and fact finder

**Responsibilities**:
- Deep-dive research on individual CNCF projects
- Web search for latest updates, community discussions, use cases
- Extract key features, architecture details, and interesting facts
- Persist research to YAML files for Writer consumption and audit trail

**Tools**:
- `web_search(query: str, max_results: int = 3) -> List[str]`: DuckDuckGo search

**Input**: 
```python
ProjectMetadata(
    name="Apache Kafka",
    repo_url="https://github.com/apache/kafka",
    homepage="https://kafka.apache.org/"
)
```

**Process**:
1. Receive project metadata from `data/week_XX_Y/{category}.yaml`
2. Perform web searches:
   - "{project_name} latest release updates"
   - "{project_name} use cases real world"
   - "{project_name} key features architecture"
3. Synthesize findings into structured output
4. Handle errors gracefully (API failures, rate limits)
5. Save to `data/week_XX_Y/research/{sanitized_name}.yaml`

**Output**: `ResearchOutput` (persisted as YAML)
```yaml
project_name: "Apache Kafka"
summary: "Distributed event streaming platform for high-throughput data pipelines"
key_features:
  - "Pub/sub messaging with persistent storage"
  - "Horizontally scalable to trillions of events per day"
  - "Real-time stream processing with Kafka Streams API"
  - "Exactly-once semantics and strong ordering guarantees"
recent_updates: "Kafka 3.7 released with KRaft mode fully replacing ZooKeeper, improved tiered storage"
use_cases: "Event sourcing, log aggregation, real-time analytics, CDC, microservices communication"
interesting_facts: "Used by 80% of Fortune 100, processes trillions of messages daily at LinkedIn"
```

**Parallelization**: Uses Prefect `task.map()` to research multiple projects concurrently (respects API rate limits)

**Error Handling**: If research fails (network, API timeout), saves error message in YAML for debugging:
```yaml
project_name: "Example Project"
summary: "Research failed: API timeout after 30s"
key_features: []
recent_updates: ""
use_cases: ""
interesting_facts: "Error logged for manual investigation"
```

### 3. Writer Agent (`src/agentic/agents/writer.py`)

**Role**: Content creator and reviser

**Responsibilities**:
- Synthesize research into engaging blog posts
- Follow consistent structure and tone
- Revise drafts based on Editor feedback
- Maintain quality across iterations

**Input**:
- **Iteration 1**: List of `ResearchOutput` objects from `data/week_XX_Y/research/*.yaml`
- **Iteration 2+**: Previous draft + `EditorFeedback` object

**Output**: `BlogPostDraft`
```python
BlogPostDraft(
    title="Letter B: 54 Projects Starting with B",
    content_markdown="..." # Full markdown content
)
```

**Content Structure**:
```markdown
---
title: "Letter {X}: {N} Projects Starting with {X}"
date: YYYY-MM-DDTHH:MM:SSZ
draft: false
---

# Introduction
Brief overview of the letter's theme and project count. Hook to engage readers.

# Project 1: {Project Name}

## What is it?
2-3 sentence clear explanation of the project's purpose and core functionality.

## Why it matters
Value proposition: what problem does it solve, who benefits, why should readers care.

## Key Features
- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description
- Feature 4: Brief description (if applicable)

## Recent Updates
Latest releases, major changes, roadmap items from research.

## Use Cases
Common scenarios where this project excels, with concrete examples.

## Get Started
```bash
# Quick installation/usage example
kubectl apply -f example.yaml
```

---

[Repeat for all projects]

# Conclusion
Wrap-up highlighting themes, patterns, or standout projects from the week.
```

**Revision Process**:
- **Iteration 1**: Fresh draft from research, following structure template
- **Iteration 2**: Read feedback → identify sections to revise → rewrite those sections while maintaining consistency
- **Iteration 3**: Final revision attempt → incorporate any remaining feedback → polish

**Style Guidelines**:
- **Tone**: Conversational but technical, enthusiastic about discovery
- **Audience**: Developers and operators familiar with cloud-native concepts
- **Length**: ~150-300 words per project (scales with research depth)
- **Voice**: Active voice, direct language, avoid jargon overload

## Workflow Execution Flow

### Complete Week Processing Cycle

```
START: Editor selects letter (e.g., "C")
  │
  ├─> Load projects from data/week_02_C/*.yaml (48 projects)
  │
  ├─> RESEARCH PHASE (Parallel)
  │   ├─> Researcher: Project 1 → save to data/week_02_C/research/project_1.yaml
  │   ├─> Researcher: Project 2 → save to data/week_02_C/research/project_2.yaml
  │   └─> ... (all 48 projects in parallel)
  │
  ├─> ITERATION PHASE (Sequential)
  │   │
  │   ├─> Iteration 1:
  │   │   ├─> Writer: Read all 48 research/*.yaml files
  │   │   ├─> Writer: Draft complete blog post
  │   │   ├─> Editor: Review draft
  │   │   ├─> Editor Decision:
  │   │   │   ├─> APPROVED → Go to PUBLISH
  │   │   │   └─> REJECTED → Generate feedback → Iteration 2
  │   │
  │   ├─> Iteration 2 (if rejected):
  │   │   ├─> Writer: Read research + previous draft + feedback
  │   │   ├─> Writer: Revise specific sections per feedback
  │   │   ├─> Editor: Review revised draft
  │   │   ├─> Editor Decision:
  │   │   │   ├─> APPROVED → Go to PUBLISH
  │   │   │   └─> REJECTED → Generate feedback → Iteration 3
  │   │
  │   └─> Iteration 3 (if still rejected):
  │       ├─> Writer: Final revision attempt
  │       ├─> Editor: Review
  │       └─> AUTO-APPROVE (max iterations reached)
  │
  └─> PUBLISH PHASE
      ├─> Editor: Save to website/content/posts/2026-C.md
      ├─> Editor: Update TODO.md with completion status
      ├─> Git: Commit all files (research/*.yaml + post + TODO.md)
      └─> END: Week C complete
```

## File Naming & Persistence

### Sanitization Rules

All filenames are sanitized for cross-platform filesystem compatibility:

```python
def sanitize_filename(name: str) -> str:
    """
    Convert project name to filesystem-safe filename.
    
    Rules:
    - Lowercase
    - Spaces → underscores
    - Forward slashes → underscores
    - Hyphens → underscores
    - Remove special characters: ()[]{}!@#$%^&*
    - Collapse multiple underscores to single
    
    Examples:
    - "Apache Kafka" → "apache_kafka"
    - "Kong/Insomnia" → "kong_insomnia"
    - "cert-manager" → "cert_manager"
    - "Dapr (Distributed Application Runtime)" → "dapr_distributed_application_runtime"
    """
    sanitized = name.lower()
    sanitized = sanitized.replace(' ', '_').replace('/', '_').replace('-', '_')
    sanitized = re.sub(r'[()[\]{}!@#$%^&*]', '', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized)  # Collapse multiple underscores
    return sanitized.strip('_')
```

### File Locations

#### Research Files (Persistent)
- **Location**: `data/week_XX_Y/research/`
- **Pattern**: `{sanitized_name}.yaml`
- **Lifecycle**: Created once per project, retained permanently
- **Purpose**: Audit trail, debugging, re-runs without re-researching

**Example**:
```
data/week_00_A/research/
├── apache_airflow.yaml
├── apache_kafka.yaml
├── argo_cd.yaml
├── argo_workflows.yaml
└── aws_controllers_for_kubernetes.yaml
```

#### Final Posts (Published)
- **Location**: `website/content/posts/`
- **Pattern**: `YYYY-{letter}.md` (e.g., `2026-A.md`)
- **Lifecycle**: Created on Editor approval, permanent
- **Access Control**: Only Editor agent can write/overwrite

#### Progress Tracking (Version Controlled)
- **Location**: `TODO.md` (repository root)
- **Lifecycle**: Updated on each workflow run, committed to git
- **Purpose**: Cross-run state, iteration history, human visibility

## Input/Output Mapping

### Agentic Workflow Inputs (Read-Only)

| File/Directory | Content | Used By | Purpose |
|---------------|---------|---------|---------|
| `data/week_XX_Y/*.yaml` | Full project metadata (name, repo_url, homepage, logos, etc.) | Researcher | Extract ProjectMetadata for research |
| `data/week_XX_Y/tasks.yaml` | Simple list of project names | Editor | Count projects, determine workload |
| `TODO.md` | Progress tracking, iteration history | Editor | Determine next week, check completion status |

### Agentic Workflow Outputs (Write)

| File/Directory | Content | Written By | Update Strategy |
|---------------|---------|------------|-----------------|
| `data/week_XX_Y/research/{name}.yaml` | ResearchOutput per project | Researcher | Create once, retain permanently |
| `website/content/posts/YYYY-{letter}.md` | Final approved blog post | Editor | Create/overwrite on approval only |
| `TODO.md` | Progress and iteration logs | Editor | Append iteration details, update completion status |

## Running the Workflow

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY="your_gemini_api_key"
export LOGFIRE_TOKEN="your_logfire_token"  # Optional for observability
export GEMINI_MODEL="gemini-2.0-flash-exp"  # Or gemini-1.5-pro
```

### Local Execution

```bash
# Process one week (Editor selects automatically)
python src/cli.py run workflow

# Process with limit (for testing/gradual rollout)
python src/cli.py run workflow --limit 10  # Only process first 10 projects

# Local mode (no Prefect Cloud)
python src/cli.py run workflow --local
```

## Modifying Agent Behavior

### Adjusting Editorial Criteria
Edit `src/agentic/agents/editor.py`:
```python
EDITORIAL_CRITERIA = """
Review drafts for:
1. Technical accuracy (no hallucinations, current information)
2. Tone consistency (engaging, discovery-focused, not promotional)
3. Completeness (all sections: What/Why/Features/GetStarted)
4. Markdown quality (formatting, links, structure)
5. Balance (equal coverage, no favoritism)
6. [ADD YOUR CUSTOM CRITERIA HERE]
"""
```

### Changing Writer Style
Edit `src/agentic/agents/writer.py`:
```python
WRITER_SYSTEM_PROMPT = """
You are a technical writer creating engaging content about CNCF projects.

Style Guidelines:
- Tone: [Conversational/Formal/Technical]
- Length: [150-300 words per project]
- Structure: [Custom structure here]
- Voice: [Active/Passive]
"""
```

## Troubleshooting

### Common Issues

**Issue**: "TODO.md not found"
- **Cause**: First run, file doesn't exist yet
- **Solution**: Editor will create it automatically with initial structure

**Issue**: Research files empty or contain errors
- **Cause**: API rate limiting, network timeout, invalid search results
- **Solution**: Check Logfire/console logs, retry specific projects, increase timeout

**Issue**: Writer produces low-quality content
- **Cause**: Poor research input, unclear prompts, model limitations
- **Solution**: Inspect research/*.yaml files, improve Researcher prompts, try different model (gemini-1.5-pro)

### Manual Intervention

If the workflow produces unsatisfactory results:

1. **Keep research files**: Already saved in `data/week_XX_Y/research/`
2. **Edit draft manually**: Modify `website/content/posts/YYYY-{letter}.md`
3. **Update TODO.md**: Mark as "manually completed"
4. **Commit changes**: Git commit with note about manual edits
5. **Continue**: Next run will pick up next letter automatically
