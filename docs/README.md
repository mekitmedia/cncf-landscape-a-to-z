# CNCF Landscape A-to-Z Documentation

Welcome to the technical documentation for the CNCF Landscape A-to-Z project. This documentation covers both the deterministic ETL pipeline and the AI-powered agentic workflow for automated content generation.

## 📚 Documentation Overview

This project automates the generation of weekly content about CNCF landscape projects through two independent workflows:

1. **ETL Pipeline** - Deterministic data processing that extracts, transforms, and loads CNCF landscape data
2. **Agentic Workflow** - AI agents (Editor, Researcher, Writer) that research projects and generate blog posts through iterative editorial refinement

## 📖 Documentation Files

### [architecture.md](architecture.md)
**System Architecture & Design**

Complete system design including:
- Two-layer architecture (ETL + Agentic)
- Data flow diagrams and workflow visualization
- Iteration workflow (Editor-Writer feedback loop)
- Conflict prevention through exclusive write zones
- GitHub Actions integration and PR workflow
- Future enhancement roadmap

**Start here if you're new to the project** or need to understand the overall system design.

---

### [etl-pipeline.md](etl-pipeline.md)
**ETL Pipeline Documentation**

Comprehensive guide to the deterministic data processing pipeline:
- Extract, Transform, Load stages in detail
- Input sources and output file structures
- Data contracts and guarantees
- File naming conventions and sanitization rules
- Command-line usage and CI/CD integration
- Monitoring, debugging, and performance optimization

**Read this when:**
- Setting up or modifying the ETL pipeline
- Understanding data folder structure
- Debugging data processing issues
- Adding new data transformations

---

### [agentic-workflow.md](agentic-workflow.md)
**Agentic Workflow Documentation**

Deep dive into the AI-powered content generation system:
- Agent trio roles (Editor, Researcher, Writer)
- Editorial iteration loop (up to 3 revision cycles)
- Research persistence and file management
- TODO.md state tracking (version controlled)
- Input/output mapping for each agent
- Modifying agent behavior and prompts
- Troubleshooting and manual intervention

**Read this when:**
- Running or debugging the agentic workflow
- Adjusting agent prompts or editorial criteria
- Understanding the iteration and approval process
- Implementing research persistence features

---

### Harness Skill: `.agents/skills/cncf-weekly-content/SKILL.md`
**Contributor Skill for Any Coding Harness**

Portable skill instructions that mirror the current Pydantic AI Editor, Researcher, and Writer responsibilities so contributors can execute the workflow with Claude Code, Opencode, or other harnesses.

**Read this when:**
- You want to contribute content updates without using the Pydantic AI runtime
- You need a single prompt/playbook that works across coding harnesses

---

### [tracker.md](tracker.md)
**Task Tracker System**

Comprehensive guide to the task tracking and state management system:
- Task types, states, and dependency management
- Data models and storage architecture
- Integration with agentic workflow
- Progress tracking and error handling
- Synchronization with ETL pipeline
- Configuration and extensibility
- Troubleshooting and debugging

**Read this when:**
- Understanding how tasks are tracked and managed
- Working with task dependencies and state
- Debugging workflow progress issues
- Adding new task types or modifying tracking behavior
- Implementing custom tracker backends

---

### [website-architecture.md](website-architecture.md)
**Website Design & Integration**

Complete guide to the website implementation and data integration:
- Three-level content hierarchy (Featured → All → Details)
- Data flow from ETL through research to rendered pages
- Hugo template system and content generation
- Research persistence and file organization
- Tool page generation from research YAML
- Navigation patterns and user discovery flows
- Integration between workflows and website
- Implementation phases and roadmap

**Read this when:**
- Building or modifying website features
- Understanding how research feeds into website content
- Implementing new templates or pages
- Generating tool pages from research data
- Troubleshooting website content display

---

## 🚀 Quick Start

### Running the Complete Workflow

```bash
# 1. Run ETL to process CNCF landscape data
python src/cli.py run etl

# 2. Verify data generated
ls data/weeks/*

# 3. Run agentic workflow (Editor selects next week automatically)
python src/cli.py run workflow

# 4. Check outputs
cat TODO.md                           # Progress tracking
ls data/weeks/00-A/research/          # Research files
cat website/content/posts/2026-A.md   # Final blog post
```

### Environment Setup

```bash
# Option A: Run via 1Password CLI (recommended)
op run -- python src/cli.py run workflow

# Option B: Set environment variables directly
export GOOGLE_API_KEY="your_gemini_api_key"
export GEMINI_MODEL="gateway/google-vertex:gemini-2.5-flash"
export LOGFIRE_TOKEN="your_logfire_token"  # Optional
```

## 🗂️ Key Concepts

### Data Flow

```
CNCF Landscape (upstream)
    ↓
ETL Pipeline
    ↓
data/weeks/XX-L/*.yaml (project metadata)
    ↓
Agentic Workflow (reads)
    ├─> Tracker System (data/weeks/XX-L/tracker.yaml)
    │   ├─> Task state management and dependencies
    │   ├─> Progress tracking and error handling
    │   └─> Synchronization with ETL changes
    ├─> data/weeks/XX-L/research/*.yaml (persisted research)
    ├─> website/content/posts/*.md (final blog posts)
    └─> TODO.md (state tracking)
```

### Conflict Prevention

The system is designed with **exclusive write zones** to prevent conflicts:

| Directory/File | ETL | Agentic | Purpose |
|---------------|-----|---------|---------|
| `data/weeks/XX-L/*.yaml` | ✅ Write | ❌ Read-only | Project metadata |
| `data/weeks/XX-L/tracker.yaml` | ❌ Never | ✅ Write | Task state tracking |
| `data/weeks/XX-L/research/` | ❌ Never | ✅ Write | Research persistence |
| `website/content/letters/` | ✅ Write | ❌ Never | Hugo letter pages |
| `website/content/posts/` | ❌ Never | ✅ Write (Editor only) | Blog posts |
| `TODO.md` | ❌ Never | ✅ Write (Editor only) | Progress tracking |

### Workflow Execution Order

1. **ETL runs first** (weekly schedule or manual) → Creates PR with updated data
2. **Human reviews and merges** ETL PR
3. **Agentic workflow runs** (manual trigger) → Reads stable data from main branch
4. **Editor orchestrates** iteration loop (max 3 cycles)
5. **PR opens for human review** with research files, blog post, and TODO.md updates
6. **Human approves and merges** content PR
7. **Hugo deploys** updated website

## 🔍 Finding What You Need

### I want to...

- **Understand the overall system** → Read [architecture.md](architecture.md)
- **Set up the ETL pipeline** → See [etl-pipeline.md](etl-pipeline.md) "Configuration" section
- **Run the agentic workflow** → See [agentic-workflow.md](agentic-workflow.md) "Running the Workflow"
- **Modify agent behavior** → See [agentic-workflow.md](agentic-workflow.md) "Modifying Agent Behavior"
- **Debug data processing** → See [etl-pipeline.md](etl-pipeline.md) "Monitoring & Debugging"
- **Understand file naming** → See [agentic-workflow.md](agentic-workflow.md) "File Naming & Persistence"
- **Prevent workflow conflicts** → See [architecture.md](architecture.md) "Conflict Prevention"
- **Track progress across runs** → See [agentic-workflow.md](agentic-workflow.md) "TODO.md Structure"
- **Understand website architecture** → Read [website-architecture.md](website-architecture.md)
- **Generate tool pages** → See [website-architecture.md](website-architecture.md) "Tool Page Generation"
- **Work with Hugo templates** → See [website-architecture.md](website-architecture.md) "Template System"
- **Integrate research with website** → See [website-architecture.md](website-architecture.md) "Integration Points"

## 🏗️ Project Structure Reference

```
cncf-landscape-a-to-z/
├── data/                          # ETL outputs (regenerated weekly)
│   ├── week_00_A/                 # Week directories (A-Z)
│   │   ├── *.yaml                 # Category project files (ETL writes)
│   │   ├── tasks.yaml             # Simple project list (ETL writes)
│   │   ├── README.md              # Week summary (ETL writes)
│   │   └── research/              # Research persistence (Agentic writes)
│   │       └── *.yaml             # Individual project research
│   ├── categories.yaml            # Full taxonomy (ETL writes)
│   ├── category_index.yaml        # Mappings (ETL writes)
│   └── stats_*.yaml               # Statistics (ETL writes)
├── website/
│   └── content/
│       ├── letters/               # Letter pages (ETL writes)
│       │   └── A/, B/, ... Z/
│       └── posts/                 # Blog posts (Agentic writes, Editor only)
│           └── 2026-A.md, etc.
├── TODO.md                        # Progress tracking (Agentic writes, versioned)
├── src/
│   ├── pipeline/                  # ETL implementation
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py
│   └── agentic/                   # Agentic workflow implementation
│       ├── agents/                # Agent implementations
│       ├── flow.py                # Prefect orchestration
│       ├── models.py              # Data models
│       └── tools.py               # Agent tools
└── docs/                          # Documentation (you are here!)
    ├── README.md                  # This file
    ├── architecture.md            # System design
    ├── etl-pipeline.md            # ETL pipeline docs
    └── agentic-workflow.md        # Agentic workflow docs
```

## 🤝 Contributing

When making changes to the workflows:

1. **Update documentation** - Keep docs in sync with code changes
2. **Test both workflows** - Ensure ETL and Agentic don't conflict
3. **Preserve exclusive write zones** - Don't introduce shared write access
4. **Document breaking changes** - Update architecture.md if data contracts change
5. **Maintain TODO.md format** - Keep iteration history structure consistent

## 📋 Troubleshooting

### Quick Diagnostics

```bash
# Verify ETL outputs
ls -d data/weeks/* | wc -l             # Should be 26 (A-Z)
python -c "import yaml; yaml.safe_load(open('data/weeks/00-A/tasks.yaml'))"

# Check agentic outputs
cat TODO.md                             # Progress and iteration history
ls data/weeks/00-A/research/            # Research files present?
cat website/content/posts/2026-A.md     # Final post generated?

# Test workflows independently
python src/cli.py run etl --output_dir /tmp/test_data
python src/cli.py run workflow --limit 5  # Small test batch
```

### Common Issues

- **"TODO.md not found"** → First run; Editor creates it automatically
- **Research files empty** → API rate limiting; check Logfire logs
- **Conflicts between workflows** → Ensure ETL runs before Agentic
- **Low-quality content** → Inspect research/*.yaml files, adjust prompts

See individual documentation files for detailed troubleshooting.

## 🔗 Additional Resources

- **CNCF Landscape**: https://landscape.cncf.io
- **Prefect Documentation**: https://docs.prefect.io
- **Pydantic AI**: https://ai.pydantic.dev
- **Hugo Documentation**: https://gohugo.io/documentation

## 📝 Documentation Maintenance

This documentation is maintained alongside the codebase. When making changes:

- Update [architecture.md](architecture.md) for design/architectural changes
- Update [etl-pipeline.md](etl-pipeline.md) for ETL modifications
- Update [agentic-workflow.md](agentic-workflow.md) for agentic workflow changes
- Update this README.md if adding new documentation files or major sections

Last updated: February 1, 2026
