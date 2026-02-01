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

## 🚀 Quick Start

### Running the Complete Workflow

```bash
# 1. Run ETL to process CNCF landscape data
python src/cli.py run etl

# 2. Verify data generated
ls data/week_*

# 3. Run agentic workflow (Editor selects next week automatically)
python src/cli.py run workflow

# 4. Check outputs
cat TODO.md                           # Progress tracking
ls data/week_00_A/research/           # Research files
cat website/content/posts/2026-A.md   # Final blog post
```

### Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Required environment variables
export GOOGLE_API_KEY="your_gemini_api_key"
export LOGFIRE_TOKEN="your_logfire_token"  # Optional
export GEMINI_MODEL="gemini-2.0-flash-exp"
```

## 🗂️ Key Concepts

### Data Flow

```
CNCF Landscape (upstream)
    ↓
ETL Pipeline
    ↓
data/week_XX_Y/*.yaml (project metadata)
    ↓
Agentic Workflow (reads)
    ├─> data/week_XX_Y/research/*.yaml (persisted research)
    └─> website/content/posts/*.md (final blog posts)
    └─> TODO.md (state tracking)
```

### Conflict Prevention

The system is designed with **exclusive write zones** to prevent conflicts:

| Directory | ETL | Agentic | Purpose |
|-----------|-----|---------|---------|
| `data/week_XX_Y/*.yaml` | ✅ Write | ❌ Read-only | Project metadata |
| `data/week_XX_Y/research/` | ❌ Never | ✅ Write | Research persistence |
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
ls -d data/week_* | wc -l              # Should be 26 (A-Z)
python -c "import yaml; yaml.safe_load(open('data/week_00_A/tasks.yaml'))"

# Check agentic outputs
cat TODO.md                             # Progress and iteration history
ls data/week_00_A/research/             # Research files present?
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
