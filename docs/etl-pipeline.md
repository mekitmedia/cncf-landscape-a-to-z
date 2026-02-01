# ETL Pipeline Documentation

This document describes the Extract-Transform-Load (ETL) pipeline that processes the CNCF landscape data into structured, consumable formats for the agentic workflow and Hugo website.

## Overview

The ETL pipeline is a deterministic data processing system that fetches the CNCF landscape YAML, filters and organizes projects by alphabetical letter (A-Z), and generates structured output files. It runs independently from the agentic workflow and serves as the data foundation for content generation.

**Location**: `src/pipeline/` (extract.py, transform.py, load.py)
**Entry Point**: `python src/cli.py run etl`

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ETL PIPELINE FLOW                       │
│                                                              │
│  EXTRACT                   TRANSFORM                  LOAD   │
│     │                          │                        │    │
│     ├─> Fetch YAML  ──>   ├─> Filter by letter  ──>  ├─> Write YAML files    │
│     │   (HTTP/local)       │   (A-Z, 26 weeks)       │   (data/week_XX_Y/)   │
│     │                      │                          │                       │
│     │                      ├─> Exclude archived ──>  ├─> Generate summaries  │
│     │                      │   projects               │   (README.md)         │
│     │                      │                          │                       │
│     │                      ├─> Sanitize names   ──>  ├─> Create Hugo pages   │
│     │                      │   (filesystem safe)      │   (letters/Y/)        │
│     │                      │                          │                       │
│     │                      └─> Group by category ──> └─> Write indexes        │
│                                                          (stats, mappings)    │
└─────────────────────────────────────────────────────────────┘
```

## Stage 1: Extract (`src/pipeline/extract.py`)

### Purpose
Fetch the CNCF landscape YAML from upstream source (GitHub or local file).

### Input Sources
- **Default**: `https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml`
- **Custom**: Local file path via `--input_path` parameter

### Process
```python
def fetch_landscape(input_path: str = None) -> dict:
    """
    Fetches the CNCF landscape YAML file.
    
    Args:
        input_path: URL or local file path (default: GitHub master branch)
    
    Returns:
        Parsed YAML as Python dictionary
    """
```

### Output
Raw landscape dictionary containing:
- `landscape`: List of categories
  - Each category has: `name`, `subcategories`
  - Each subcategory has: `name`, `items`
  - Each item has: `name`, `repo_url`, `homepage_url`, `project`, `logo`, etc.

### Error Handling
- HTTP failures: Retry with exponential backoff
- Invalid YAML: Log error and exit
- Missing `landscape` key: Validation error

## Stage 2: Transform (`src/pipeline/transform.py`)

### Purpose
Filter, group, and sanitize landscape data into weekly batches by project name's first letter.

### Transformations

#### 1. **Letter-Based Filtering**
Projects are grouped by first letter (A-Z = 26 weeks):
```python
def group_by_letter(landscape: dict) -> dict:
    """
    Groups projects into 26 weeks based on first letter of name.
    
    Returns:
        {
            'A': {'partial': {category: [items]}, 'tasks': [names]},
            'B': {'partial': {category: [items]}, 'tasks': [names]},
            ...
        }
    """
```

**Week Mapping**:
- Week 00: Letter A
- Week 01: Letter B
- ...
- Week 25: Letter Z

#### 2. **Project Filtering**
Exclusion rules applied:
- ❌ Projects with `project: "archived"` status
- ❌ Items without `repo_url` (not open source)
- ✅ All other projects included

```python
excluded_items = []  # Saved to data/excluded_items.yaml for audit
```

#### 3. **Category Name Sanitization**
Categories sanitized for filesystem compatibility:

**Rules**:
- Lowercase conversion
- Spaces → underscores
- `&` → `and`
- Special characters removed
- Multiple underscores collapsed

**Examples**:
```
"App Definition and Development" → "app_definition_and_development"
"Observability & Analysis" → "observability_and_analysis"
"Platform/Runtime" → "platform_runtime"
"CNAI: AutoML" → "cnai_automl"
```

#### 4. **Data Structures Generated**

**Category Index** (`category_index.yaml`):
```yaml
app_definition_and_development:
  - application_definition_image_build
  - continuous_integration_delivery
  - database
  - streaming_messaging
observability_and_analysis:
  - chaos_engineering
  - logging
  - monitoring
```

**Category Item Index** (`category_item_index.yaml`):
```yaml
app_definition_and_development_application_definition_image_build:
  - Apache Airflow
  - Argo CD
  - Argo Workflows
  ...
```

**Statistics**:
- `stats_per_category.yaml`: Count of subcategories per category
- `stats_per_category_per_week.yaml`: Distribution across weeks
- `stats_by_status.yaml`: Breakdown by CNCF project status (graduated/incubating/sandbox)

### Output
Transformed data structure ready for loading:
```python
{
    'landscape_by_letter': {
        'A': {
            'partial': {
                'app_definition_and_development_database': [
                    {
                        'name': 'Apache Cassandra',
                        'repo_url': 'https://github.com/apache/cassandra',
                        'homepage_url': 'https://cassandra.apache.org',
                        'logo': 'apache-cassandra.svg',
                        'project': 'graduated',
                        ...
                    }
                ]
            },
            'tasks': ['Apache Airflow', 'Apache Kafka', ...]
        }
    },
    'indexes': {...},
    'stats': {...},
    'excluded': [...]
}
```

## Stage 3: Load (`src/pipeline/load.py`)

### Purpose
Write transformed data to filesystem in structured YAML files and generate Hugo pages.

### Output Files

#### 1. **Week Directories** (`data/week_XX_Y/`)

Structure for each week:
```
data/week_00_A/
├── app_definition_and_development_application_definition_image_build.yaml
├── app_definition_and_development_continuous_integration_delivery.yaml
├── app_definition_and_development_database.yaml
├── cnai_automl.yaml
├── observability_and_analysis_logging.yaml
├── tasks.yaml  # Simple list of project names
└── README.md   # Generated summary
```

**Category Files** (e.g., `app_definition_and_development_database.yaml`):
```yaml
- name: Apache Cassandra
  repo_url: https://github.com/apache/cassandra
  homepage_url: https://cassandra.apache.org
  logo: apache-cassandra.svg
  twitter: https://twitter.com/cassandra
  crunchbase: https://www.crunchbase.com/organization/apache
  project: graduated
  item: null

- name: Apache CouchDB
  repo_url: https://github.com/apache/couchdb
  homepage_url: https://couchdb.apache.org
  ...
```

**tasks.yaml** (simple name list for quick lookup):
```yaml
- Apache Airflow
- Apache Kafka
- Argo CD
- Argo Workflows
- AWS Controllers for Kubernetes
...
```

**README.md** (generated summary using Jinja2 template):
```markdown
# Week 00 (A) - CNCF Landscape Projects

Total projects: 61

## Projects by Category

- **App Definition And Development Application Definition Image Build**: 5 projects
- **App Definition And Development Database**: 12 projects
- **Observability And Analysis Logging**: 8 projects
...
```

#### 2. **Root-Level Index Files** (`data/`)

**categories.yaml** (full taxonomy):
```yaml
- name: App Definition and Development
  subcategories:
    - name: Application Definition & Image Build
      items:
        - name: Buildpacks
          repo_url: https://github.com/buildpacks/pack
          ...
```

**category_index.yaml** (name→path mapping):
```yaml
app_definition_and_development:
  - application_definition_image_build
  - continuous_integration_delivery
  - database
```

**category_item_index.yaml** (category→items):
```yaml
app_definition_and_development_database:
  - Apache Cassandra
  - Apache CouchDB
  - Vitess
```

**excluded_items.yaml** (audit trail):
```yaml
- name: SomeCommercialProduct
  reason: No repo_url (not open source)
- name: ArchivedProject
  reason: Project status is archived
```

#### 3. **Hugo Letter Pages** (`website/content/letters/Y/`)

Each letter gets a Hugo page:
```
website/content/letters/A/_index.md
website/content/letters/B/_index.md
...
website/content/letters/Z/_index.md
```

**Generated content** (`A/_index.md`):
```markdown
---
title: "Letter A"
weight: 1
---

Projects starting with the letter **A** in the CNCF Landscape.

**Total projects**: 61

See the [full list](/data/week_00_A/tasks.yaml) or explore by category.
```

### File Writing Strategy

**Mode**: Overwrite/regenerate on each run
- **Rationale**: ETL is deterministic; upstream landscape is source of truth
- **Impact**: Any manual edits to `data/` will be lost on next ETL run
- **Safety**: Keep manual edits in separate directories outside `data/`

```python
def to_yaml(data: dict, path: str):
    """
    Saves dictionary to YAML file.
    Creates parent directories if needed.
    Overwrites existing files.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w+') as file:
        yaml.dump(data, file)
```

## Input/Output Summary

### ETL Pipeline Inputs

| Source | Type | Purpose |
|--------|------|---------|
| CNCF Landscape YAML (upstream) | HTTP/File | Primary data source |
| Command-line parameters | CLI args | Configuration (input path, output dir) |
| Jinja2 templates (`src/templates/`) | Templates | README.md generation |

### ETL Pipeline Outputs

| File/Directory | Purpose | Consumers | Update Strategy |
|---------------|---------|-----------|-----------------|
| `data/week_XX_Y/*.yaml` | Category project details | Agentic Researcher | Full regeneration |
| `data/week_XX_Y/tasks.yaml` | Simple project name list | Agentic Editor | Full regeneration |
| `data/week_XX_Y/README.md` | Week summary for humans | Documentation | Full regeneration |
| `data/categories.yaml` | Full category taxonomy | Hugo templates | Full regeneration |
| `data/category_index.yaml` | Category→path mapping | Hugo templates | Full regeneration |
| `data/category_item_index.yaml` | Category→items index | Hugo templates | Full regeneration |
| `data/stats_*.yaml` | Various statistics | Analytics/Hugo | Full regeneration |
| `data/excluded_items.yaml` | Audit trail of exclusions | Manual review | Full regeneration |
| `website/content/letters/Y/` | Hugo letter pages | Hugo site | Full regeneration |

### Data Contracts

**ETL guarantees for downstream consumers**:
1. ✅ All projects in `tasks.yaml` have corresponding entries in category YAML files
2. ✅ Every project has `name` field (required)
3. ✅ Projects without `repo_url` are excluded (open source only)
4. ✅ Archived projects are excluded
5. ✅ Category filenames are filesystem-safe (sanitized)
6. ✅ Week directories follow `week_{index:02d}_{letter}` pattern
7. ✅ All YAML files are valid and parseable

**What ETL does NOT guarantee**:
- ❌ Project `homepage_url` may be null
- ❌ Project `twitter`, `crunchbase` may be null
- ❌ Project `logo` path may be missing
- ❌ Project `project` status may be null (non-CNCF projects)

## Configuration

### Command-Line Options

```bash
# Default: Fetch from GitHub, output to data/
python src/cli.py run etl

# Custom input file
python src/cli.py run etl --input_path ./landscape.yml

# Custom output directory
python src/cli.py run etl --output_dir ./custom_data

# Both custom
python src/cli.py run etl --input_path ./landscape.yml --output_dir ./output
```

### Environment Variables
None required. ETL is fully deterministic and self-contained.

### Configurable Templates

**README.md template** (`src/templates/weekly_summary.md.j2`):
```jinja2
# Week {{ week_name }} - CNCF Landscape Projects

Total projects: {{ total_items }}

## Projects by Category

{% for category, count in items_per_category.items() %}
- **{{ category }}**: {{ count }} projects
{% endfor %}
```

Modify this template to change week summary format.

## Execution

### Manual Execution

```bash
# Ensure requirements installed
pip install -r requirements.txt

# Run ETL pipeline
python src/cli.py run etl

# Verify outputs
ls data/week_*
head data/week_00_A/tasks.yaml
cat data/categories.yaml
```

### GitHub Actions Execution

**Workflow**: `.github/workflows/update_data.yml`

**Trigger**: 
- Weekly schedule (Monday 00:00 UTC)
- Manual workflow_dispatch
- PR changes to pipeline code

**Steps**:
1. Checkout repository
2. Install Python + dependencies
3. Run `python src/cli.py run etl`
4. Detect changes to `data/` directory
5. Create PR with updated data files
6. Human reviews + merges PR

### CI/CD Integration

```yaml
# .github/workflows/update_data.yml (excerpt)
- name: Run ETL Pipeline
  run: PYTHONPATH=. python src/cli.py run etl

- name: Create Pull Request
  if: github.event_name == 'schedule'
  uses: peter-evans/create-pull-request@v6
  with:
    commit-message: "ci: Update data (scheduled)"
    title: "Scheduled Data Update"
    body: "Weekly data update generated by GitHub Actions."
    branch: "data-update-automated"
    base: "main"
```

## Data Flow & Conflict Prevention

### Exclusive Write Zones

| Directory | ETL (Write) | Agentic (Write) | Agentic (Read) | Hugo (Read) |
|-----------|-------------|-----------------|----------------|-------------|
| `data/week_XX_Y/*.yaml` | ✅ Full regen | ❌ Never | ✅ Yes | ✅ Yes |
| `data/week_XX_Y/research/` | ❌ Never | ✅ Append | ✅ Yes | ❌ No |
| `data/*.yaml` (indexes) | ✅ Full regen | ❌ Never | ❌ No | ✅ Yes |
| `website/content/letters/` | ✅ Full regen | ❌ Never | ❌ No | ✅ Yes |
| `website/content/posts/` | ❌ Never | ✅ Editor only | ❌ No | ✅ Yes |

### Safe Concurrent Execution

**Recommended**: Run ETL before Agentic workflow
```bash
# Correct order
python src/cli.py run etl      # ETL writes data/
python src/cli.py run workflow  # Agentic reads data/
```

**Conflict Risk**: Running simultaneously
- ETL regenerates `data/week_XX_Y/*.yaml` while Agentic reads them
- **Impact**: Agentic may read partial/corrupt YAML files
- **Mitigation**: Use file locking OR schedule workflows at different times

**GitHub Actions Strategy**: Sequential execution
1. ETL workflow creates PR with updated data
2. Human reviews + merges ETL PR
3. Agentic workflow triggered after merge (reads stable data)

## Monitoring & Debugging

### Verification Commands

```bash
# Count week directories (should be 26: A-Z)
ls -d data/week_* | wc -l

# Check project count per week
for dir in data/week_*; do
  echo "$dir: $(grep '^- ' $dir/tasks.yaml | wc -l) projects"
done

# Verify YAML validity
python -c "import yaml; yaml.safe_load(open('data/week_00_A/tasks.yaml'))"

# Check for duplicates
cat data/week_*/tasks.yaml | sort | uniq -d

# Inspect excluded items
cat data/excluded_items.yaml
```

### Common Issues

**Issue**: Fewer than 26 week directories generated
- **Cause**: No projects starting with certain letters (rare)
- **Check**: Verify upstream landscape has projects for all letters

**Issue**: Projects missing `repo_url`
- **Cause**: Upstream data quality issue
- **Resolution**: Added to `excluded_items.yaml` automatically

**Issue**: Duplicate project names
- **Cause**: Same project in multiple categories
- **Expected**: Projects can appear in multiple subcategories (not a bug)

**Issue**: Hugo pages not rendering
- **Cause**: Invalid markdown syntax in generated `_index.md`
- **Check**: Verify Jinja2 template syntax

### Logging

ETL pipeline uses structured logging (`src/logger.py`):
```python
logger.info(f"Fetching landscape from {url}")
logger.info(f"Found {len(projects)} projects for letter {letter}")
logger.warning(f"Excluded {len(excluded)} items without repo_url")
```

Check console output for processing details.

## Schema Reference

### Project Object Schema

Full project object from category YAML files:

```yaml
name: str                    # Required: Project name
repo_url: str | null         # GitHub/GitLab repository URL
homepage_url: str | null     # Official website
logo: str | null             # Filename in CNCF landscape assets
twitter: str | null          # Twitter profile URL
crunchbase: str | null       # Crunchbase organization URL
project: str | null          # CNCF status: graduated, incubating, sandbox
item: str | null             # Additional item metadata (rarely used)
```

### tasks.yaml Schema

Simple list of strings:
```yaml
- Apache Airflow
- Apache Kafka
- Argo CD
```

## Performance Considerations

### Optimization Strategies

1. **Single-pass processing**: Transform stage processes all letters in one pass
2. **In-memory aggregation**: No disk I/O until Load stage
3. **Parallel-safe**: Multiple workers could process different letters (not implemented)

### Typical Execution Times

- **Extract**: ~2-5 seconds (HTTP fetch + YAML parse)
- **Transform**: ~1-3 seconds (filtering, grouping, sanitization)
- **Load**: ~5-10 seconds (writing 100+ YAML files)
- **Total**: ~10-20 seconds for full ETL run

### Scalability

Current implementation handles:
- ✅ ~1500 projects in CNCF landscape
- ✅ ~50 categories and subcategories
- ✅ 26 week directories

Future-proof for:
- ✅ 10,000+ projects (linear scaling)
- ✅ 100+ categories
- ❌ Real-time updates (designed for batch processing)

## Future Enhancements

### Phase 1: Data Quality
- [ ] Schema validation (ensure all required fields present)
- [ ] Duplicate detection and deduplication
- [ ] Broken link checking for `repo_url` and `homepage_url`
- [ ] Logo asset verification

### Phase 2: Enrichment
- [ ] Fetch GitHub stars, forks, last commit date
- [ ] Calculate project "health score"
- [ ] Extract README.md summaries for better descriptions
- [ ] Sentiment analysis on community discussions

### Phase 3: Performance
- [ ] Incremental updates (only process changed projects)
- [ ] Parallel processing for letter groups
- [ ] Caching layer for expensive operations
- [ ] Database backend (PostgreSQL) for complex queries
