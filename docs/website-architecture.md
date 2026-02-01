# Website Architecture

This document describes the complete website implementation architecture, including the three-level content hierarchy, integration with ETL and agentic workflows, and the data flow from project research to published content.

## Table of Contents

1. [Three-Level Content Hierarchy](#three-level-content-hierarchy)
2. [Data Flow Architecture](#data-flow-architecture)
3. [Components](#components)
4. [Integration Points](#integration-points)
5. [Template System](#template-system)
6. [Navigation & Discovery](#navigation--discovery)
7. [Implementation Phases](#implementation-phases)
8. [File Structure](#file-structure)

## Three-Level Content Hierarchy

The website implements a progressive disclosure model with three levels of content depth:

### Level 1: Featured Tools (Homepage)
- **Purpose**: Hand-picked highlights from the CNCF registry
- **Location**: `website/themes/cncf-theme/layouts/_default/list.html`
- **Content**: 6 featured projects per letter, displayed on alphabet buttons
- **Data Source**: ETL output with `featured: true` flag
- **Selection Logic**: Top 6 items per category sorted by CNCF status (graduated > incubating > sandbox)

### Level 2: All Tools with Abstracts (Letter Pages)
- **Purpose**: Comprehensive view of all projects for a letter
- **Location**: `website/themes/cncf-theme/layouts/letters/list.html`
- **Content**: All projects organized by category with research summaries
- **Data Source**: ETL output + research YAML files from agentic workflow
- **Features**:
  - Category grouping (e.g., "App Definition and Development")
  - Project status badges (Graduated, Incubating, Sandbox)
  - Research summary (first 2 key features when available)
  - Links to GitHub repository and official website
  - "Details" button linking to individual tool page

### Level 3: Individual Tool Deep Dives
- **Purpose**: Complete research and information for a single project
- **Location**: `website/themes/cncf-theme/layouts/tools/single.html`
- **Content**: Comprehensive project information including:
  - Full summary and description
  - Complete list of key features
  - Use cases and recent updates
  - Interesting facts about the project
  - Getting started guide (code examples when available)
  - Related tools (cross-references)
- **Data Source**: Research YAML files + ETL project metadata
- **Navigation**: Breadcrumb navigation back to letter pages

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ CNCF Landscape Data (landscape.yml)                              │
└─────────────────┬──────────────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  ETL Pipeline       │
        │ (src/pipeline/)     │
        ├─────────────────────┤
        │ Extract: landscape  │
        │ Transform: by letter│
        │ Load: YAML files    │
        └────────┬────────────┘
                 │
                 ▼
    ┌────────────────────────────┐
    │ data/week_XX_Y/            │
    ├────────────────────────────┤
    │ ├─ category_*.yaml         │ ← Projects with metadata
    │ ├─ tasks.yaml              │
    │ └─ README.md               │
    └────────────────┬───────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────────┐    ┌───────────────────────┐
│ Hugo Build       │    │ Agentic Workflow      │
│ (reads data/)    │    │ (src/agentic/)        │
│                  │    ├───────────────────────┤
│ .Site.Data reads │    │ 1. Research Agent     │
│ week_XX_Y YAML   │    │ 2. Writer Agent       │
│ renders templates│    │ 3. Editor Agent       │
└────────┬─────────┘    │                       │
         │              │ ▼ (saves research)    │
         │              │                       │
         │              └──┬────────────────────┘
         │                 │
         │                 ▼
         │    ┌─────────────────────────────┐
         │    │ data/week_XX_Y/research/    │
         │    ├─────────────────────────────┤
         │    │ ├─ {sanitized_name}.yaml    │ ← Research data
         │    │ ├─ {sanitized_name}.yaml    │
         │    │ └─ ...                      │
         │    └──────────┬──────────────────┘
         │               │
         │               ▼
         │    ┌─────────────────────────────┐
         │    │ generate_tool_pages.py      │
         │    │ (scripts/)                  │
         │    │                             │
         │    │ Converts research YAML      │
         │    │ → Hugo tool pages           │
         │    └──────────┬──────────────────┘
         │               │
         │               ▼
         │    ┌──────────────────────────────┐
         │    │ website/content/tools/       │
         │    ├──────────────────────────────┤
         │    │ ├─ {sanitized_name}.md       │
         │    │ ├─ {sanitized_name}.md       │
         │    │ └─ ...                       │
         │    └──────────┬───────────────────┘
         │               │
         └───────────────┴──────────┐
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │ Hugo Rendered Site      │
                        ├─────────────────────────┤
                        │ ├─ index.html (Level 1) │
                        │ ├─ /letters/ (Level 2)  │
                        │ ├─ /tools/ (Level 3)    │
                        │ └─ posts/ (Blog)        │
                        └─────────────────────────┘
```

## Components

### ETL Pipeline (src/pipeline/)

The ETL pipeline transforms CNCF landscape data into Hugo-friendly YAML files.

**Output Structure**:
```yaml
# data/week_00_A/app_definition_and_development_database.yaml
- name: "Apache Kafka"
  repo_url: "https://github.com/apache/kafka"
  homepage_url: "https://kafka.apache.org"
  project: "graduated"
  featured: true
  logo: "apache-kafka.svg"
  description: "Event streaming platform"
  twitter: "..."
  crunchbase: "..."
```

**Key Changes**:
- Added `featured: boolean` flag (set by featured selection logic)
- Added `description: string` field (from CNCF data)
- Organized by letter (A-Z) in week directories

### Research Persistence (Agentic Workflow)

The agentic workflow now saves research to YAML files in `data/week_XX_Y/research/`.

**Research Output Structure**:
```yaml
# data/week_00_A/research/apache_kafka.yaml
project_name: "Apache Kafka"
summary: "Distributed event streaming platform for high-throughput, low-latency data pipelines"
key_features:
  - "Scalable distributed architecture"
  - "High throughput and low latency"
  - "Durable message storage"
recent_updates: "Version 3.x with KRaft consensus for easier deployment"
use_cases: "Event sourcing, real-time analytics, log aggregation"
interesting_facts: "Used by 80% of Fortune 100 companies"
get_started: |
  docker run -d -p 9092:9092 apache/kafka:latest
  # Create topic and produce messages
related_tools:
  - "Apache Flink"
  - "Apache Spark"
  - "Pulsar"
```

**Saving Process** (in `src/agentic/flow.py`):
```python
@task
async def save_research(week_letter: str, research: ResearchOutput):
    """Save individual research file to data/week_XX_Y/research/{sanitized_name}.yaml"""
    week_index = ord(week_letter) - ord('A')
    research_dir = f"data/week_{week_index:02d}_{week_letter}/research"
    sanitized_name = research.project_name.lower().replace(" ", "_").replace("&", "and")
    filename = f"{research_dir}/{sanitized_name}.yaml"
    
    os.makedirs(research_dir, exist_ok=True)
    research_dict = research.model_dump(exclude_none=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(research_dict, f, default_flow_style=False, allow_unicode=True)
```

### Tool Page Generation (scripts/generate_tool_pages.py)

This script generates individual tool pages from research YAML files.

**Process**:
1. Discovers research YAML files in `data/week_XX_Y/research/`
2. Reads research data and cross-references ETL for project URLs
3. Generates Hugo markdown files in `website/content/tools/`
4. Each file has research data in YAML front matter

**Generated Page Example**:
```markdown
---
title: Apache Kafka
project_name: Apache Kafka
letter: A
cncf_status: graduated
layout: single
date: 2025-02-01T10:30:00
summary: "..."
key_features: [...]
repo_url: "https://github.com/apache/kafka"
homepage_url: "https://kafka.apache.org"
---

This is an auto-generated tool page...
```

## Template System

### Homepage (_default/list.html)

Features alphabet navigation with letter buttons. Clicking a letter now properly navigates to the letter page.

**Key Updates**:
- Fixed `handleLetterClick()` to navigate: `window.location.href = '/letters/{letter}/'`
- Fixed prev/next buttons to navigate to actual pages
- Displays featured tools grid (via `tools-grid.html` partial)

### Letter Page (letters/list.html)

Displays all projects for a letter organized by category.

**Features**:
- Category groupings
- Project metadata (status, name, URLs)
- Research integration:
  - Loads research data alongside ETL data
  - Displays research summary as description
  - Shows first 2 key features
  - "Details" link to full tool page

**Template Logic**:
```hugo
{{ $sanitizedName := .name | lower | replaceRE " " "_" | replaceRE "&" "and" | ... }}
{{ $projectResearch := index $researchData $sanitizedName }}
{{ if $projectResearch.summary }}
  <p>{{ $projectResearch.summary }}</p>
{{ end }}
```

### Tool Deep Dive (tools/single.html)

Comprehensive single tool page with full research information.

**Sections**:
1. **Header**: Project name, CNCF status, links to repo and website
2. **Overview**: Full summary/description
3. **Key Features**: Complete list with checkmarks
4. **Use Cases**: Common applications
5. **Getting Started**: Code examples and quick start guide
6. **Recent Updates**: Latest developments
7. **Interesting Facts**: Additional context
8. **Related Tools**: Cross-references in sidebar
9. **Navigation**: Breadcrumb and back links

## Integration Points

### 1. Hugo Configuration (hugo.toml)

```toml
dataDir = "../data"
```

Hugo automatically loads all YAML files from the data directory as `.Site.Data`, making them accessible in templates via `index .Site.Data "week_00_A"`.

### 2. Front Matter for Letter Pages

Each letter page includes `data_key` parameter in front matter:

```markdown
---
title: "Week 1: Letter A"
letter: "A"
week: 0
data_key: "week_00_A"
layout: "list"
---
```

Templates use this to load: `{{ $weekData := index .Site.Data $dataKey }}`

### 3. Research Data Loading

Research data is loaded in letter templates:

```hugo
{{ $researchData := index .Site.Data (printf "%s_research" $dataKey) }}
```

This requires Hugo dataDir to include a `week_XX_Y_research` directory structure (separate from projects).

### 4. Featured Selection in Homepage

The `tools-grid.html` partial now filters for featured items:

```hugo
{{ range (first 6 (where $weekData.featured_items "featured" true)) }}
  <!-- display featured tool card -->
{{ end }}
```

## Navigation & Discovery

### User Journey

1. **Land on Homepage**: See alphabet with current letter highlighted
2. **Click Letter**: Navigate to `/letters/{letter}/`
3. **See Letter Page**: Browse all projects in categories
4. **Click "Details"**: Navigate to `/tools/{sanitized_name}/`
5. **Read Full Info**: View complete research and links
6. **Explore Related**: Click related tools to discover more

### Navigation Elements

- **Homepage**: Alphabet navigation, featured tools grid
- **Letter Pages**: Category groupings, "Details" links, prev/next buttons
- **Tool Pages**: Breadcrumb navigation, related tools sidebar, back link

## Implementation Phases

### Phase 1: Critical (MVP)
✅ Fix homepage navigation to actually navigate pages
✅ Persist research files to filesystem
✅ Create letter detail template with research
✅ Create tool deep dive template
✅ Enhance research model with new fields

### Phase 2: Important (Data Quality)
- Add featured flag to ETL output
- Add description field to ETL
- Enhance research model (get_started, related_tools)
- Generate tool pages from research

### Phase 3: Enhancement (UX)
- Add breadcrumb navigation
- Implement search functionality
- Add filtering by category or status
- Add tags and cross-references
- Implement related tools recommendations

## File Structure

```
website/
├── hugo.toml                           # Hugo config with dataDir = "../data"
├── content/
│   ├── letters/
│   │   ├── _index.md                  # All letters page
│   │   └── A/_index.md                # Letter A page with data_key
│   │       B/_index.md
│   │       ... (C-Z)
│   ├── tools/
│   │   ├── apache_kafka.md            # Generated from research YAML
│   │   ├── kubernetes.md
│   │   └── ... (all tools)
│   └── posts/
│       ├── 2025-A.md                  # Generated by agentic workflow
│       └── ... (blog posts)
└── themes/cncf-theme/
    └── layouts/
        ├── _default/
        │   └── list.html              # Homepage (fixed navigation)
        ├── letters/
        │   └── list.html              # Letter pages (with research)
        ├── tools/
        │   └── single.html            # Tool pages (NEW)
        └── partials/
            ├── nav.html
            ├── hero.html
            ├── tools-grid.html        # Featured tools (updated)
            ├── letter-footer.html
            └── ...

data/
├── week_00_A/
│   ├── app_definition_and_development_database.yaml  # Projects
│   ├── app_definition_and_development_*.yaml
│   ├── tasks.yaml
│   └── research/
│       ├── apache_kafka.yaml          # Research (persisted by agentic)
│       ├── kubernetes.yaml
│       └── ...
├── week_01_B/
│   └── ... (same structure)
└── ... (week_02_C through week_25_Z)

src/
├── pipeline/
│   ├── extract.py
│   ├── transform.py    # Updated: featured flag, description
│   └── load.py
└── agentic/
    ├── flow.py         # Updated: save_research task
    ├── models.py       # Updated: get_started, related_tools
    └── agents/

scripts/
└── generate_tool_pages.py  # Generate tool pages from research
```

## API Contracts

### Research YAML Format

```yaml
project_name: string
summary: string (max 200 chars)
key_features: [string] (list of 3-5 features)
recent_updates: string (max 200 chars)
use_cases: string (max 200 chars)
interesting_facts: string (optional, max 200 chars)
get_started: string (optional, code/commands)
related_tools: [string] (optional, list of project names)
```

### ETL Output Format

```yaml
name: string
repo_url: string (URL)
homepage_url: string (URL)
project: string (graduated|incubating|sandbox|archived)
featured: boolean (true if in top 6 per category)
description: string (optional)
logo: string (optional, filename)
twitter: string (optional, handle)
crunchbase: string (optional, slug)
```

### URL Patterns

- Homepage: `/`
- Letter page: `/letters/{letter}/` (A-Z)
- Tool page: `/tools/{sanitized_name}/` where sanitized_name is lowercase with spaces/& replaced
- Blog posts: `/posts/{year}-{letter}/` or `/posts/`

## Monitoring & Maintenance

### Data Validation

- Verify all research YAML files parse correctly
- Check featured selection counts (should be 0-6 per category)
- Validate project URLs resolve (occasional automated checks)

### Tool Page Generation

Run before each site build:
```bash
python scripts/generate_tool_pages.py
```

Can be integrated into GitHub Actions deploy workflow.

### ETL Pipeline Monitoring

- Ensure all 26 weeks generate successfully
- Verify YAML output format compliance
- Check featured flag distribution (should be relatively even across categories)

## Future Enhancements

1. **Search**: Implement site search over project names and descriptions
2. **Filtering**: Add category and status filters on letter pages
3. **Recommendations**: Use related_tools to suggest discovery paths
4. **Statistics**: Show category statistics and trending projects
5. **Comparison**: Compare two tools side-by-side
6. **Feedback**: Allow user feedback on research quality
7. **Analytics**: Track which projects are most explored
8. **Caching**: Implement aggressive caching for research data

