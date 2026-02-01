# Task Tracker System

## Overview

The Task Tracker is a flexible, interface-based system for managing workflow progress and task dependencies in the CNCF Landscape A-to-Z project. It provides persistent state tracking for the agentic workflow, ensuring tasks are executed in the correct order and progress is maintained across workflow runs.

## Architecture

The tracker system follows a clean architecture pattern with:

- **Interface Layer** (`TrackerBackend`) - Defines the contract for tracker implementations
- **Backend Layer** - Concrete implementations (currently YAML-based file storage)
- **Model Layer** - Pydantic models for type safety and validation
- **Configuration Layer** - Task type definitions and dependency management

## Core Concepts

### Task Types

The system defines three main task types:

| Task Type | Level | Dependencies | Agent | Description |
|-----------|-------|--------------|-------|-------------|
| `research` | Item | None | Researcher | Research project details, features, and use cases |
| `content` | Item | `research` | Writer | Write detailed content for the project |
| `blog_post` | Week | `content` | Writer | Write weekly blog post announcing all projects |

### Task States

Tasks can be in one of five states:

- `PENDING` - Task is ready to be started
- `IN_PROGRESS` - Task is currently being executed
- `COMPLETED` - Task finished successfully
- `FAILED` - Task failed with an error
- `SKIPPED` - Task was skipped (not currently used)

### Data Model

```python
# Task execution record
TaskRecord:
  status: TaskStatus
  started_at: Optional[datetime]
  completed_at: Optional[datetime]
  output_file: Optional[str]  # Relative path to output
  error_message: Optional[str]
  retry_count: int
  agent: Optional[str]  # Agent that executed the task

# Collection of tasks for one item (project)
ItemTasks:
  tasks: Dict[str, TaskRecord]  # task_type -> TaskRecord
  removed: bool  # Whether item was removed from ETL

# Week-level tasks
WeekTasks:
  tasks: Dict[str, TaskRecord]  # task_type -> TaskRecord

# Complete tracker state for a week
WeekTracker:
  items: Dict[str, ItemTasks]  # item_name -> ItemTasks
  week_tasks: WeekTasks
  metadata: Dict[str, Any]
```

## Usage

### Basic Usage

```python
from src.tracker import get_tracker, TaskStatus

# Get tracker instance
tracker = get_tracker()  # Returns YAMLTrackerBackend

# Check if tracker exists for a week
if tracker.tracker_exists('A'):
    print("Week A tracker exists")

# Get pending items for research
pending_items = tracker.get_pending_items('A', 'research')
print(f"Items needing research: {pending_items}")

# Update task status
tracker.update_task('A', 'MyProject', 'research', TaskStatus.IN_PROGRESS)
tracker.update_task('A', 'MyProject', 'research', TaskStatus.COMPLETED,
                   output_file='research/myproject.yaml')

# Check progress
progress = tracker.get_progress('A')
print(f"Completed {progress.completed}/{progress.total} tasks")
```

### Integration with Agentic Workflow

The tracker is deeply integrated with the agentic workflow:

```python
# In research_item() function
tracker = get_tracker()

# Mark research as in progress
tracker.update_task(week_letter, item.name, "research", TaskStatus.IN_PROGRESS)

try:
    # Do research work...
    result = await researcher_agent.run("Research the project", deps=item)

    # Mark as completed with output file
    tracker.update_task(week_letter, item.name, "research", TaskStatus.COMPLETED,
                       output_file=f"research/{sanitized_name}.yaml")
except Exception as e:
    # Mark as failed
    tracker.update_task(week_letter, item.name, "research", TaskStatus.FAILED,
                       error_message=str(e))
```

## File Storage

The YAML backend stores tracker data in the following structure:

```
data/weeks/
├── 00-A/
│   ├── tracker.yaml      # WeekTracker data
│   └── tasks.yaml        # Legacy tasks file (for migration)
├── 01-B/
│   └── tracker.yaml
└── ...
```

### Tracker File Format

```yaml
# data/weeks/00-A/tracker.yaml
items:
  ProjectA:
    tasks:
      research:
        status: completed
        started_at: "2026-02-01T10:00:00"
        completed_at: "2026-02-01T10:05:00"
        output_file: research/projecta.yaml
        agent: researcher
      content:
        status: pending
        agent: writer
    removed: false
  ProjectB:
    tasks:
      research:
        status: in_progress
        started_at: "2026-02-01T10:10:00"
        agent: researcher
    removed: false

week_tasks:
  tasks:
    blog_post:
      status: pending
      agent: writer

metadata:
  created_at: "2026-02-01T09:00:00"
  week_letter: A
  last_synced: "2026-02-01T10:00:00"
  etl_item_count: 2
```

## Dependency Management

The tracker enforces task dependencies automatically:

### Item-Level Dependencies

- `content` tasks depend on `research` completion
- Tasks can only start when all dependencies are `COMPLETED`

### Week-Level Dependencies

- `blog_post` depends on ALL items having `content` completed
- Week tasks require all relevant item tasks to be done first

### Dependency Checking

```python
# Check if a task can start
can_start = tracker.can_start_task('A', 'MyProject', 'content')
# Returns True only if 'research' is COMPLETED

can_start = tracker.can_start_task('A', None, 'blog_post')
# Returns True only if ALL items have 'content' COMPLETED
```

## Synchronization with ETL

The tracker synchronizes with ETL pipeline output:

```python
# After ETL runs, sync tracker with new/removed items
tracker.sync_with_etl('A', ['ProjectA', 'ProjectB', 'ProjectC'])

# This will:
# - Add new items with default pending tasks
# - Mark removed items (preserve history)
# - Update metadata
```

## Progress Tracking

Get detailed progress statistics:

```python
# Overall progress for a week
progress = tracker.get_progress('A')
print(f"Total: {progress.total}")
print(f"Completed: {progress.completed}")
print(f"Pending: {progress.pending}")
print(f"In Progress: {progress.in_progress}")
print(f"Failed: {progress.failed}")
print(f"Completion: {progress.completion_percentage:.1f}%")

# Progress for specific task type
research_progress = tracker.get_progress('A', 'research')
```

## Error Handling

The tracker includes comprehensive error handling:

```python
from src.tracker.exceptions import (
    WeekNotFoundError,
    ItemNotFoundError,
    InvalidTaskTypeError,
    DependencyNotMetError
)

try:
    tracker.update_task('A', 'NonExistentItem', 'research', TaskStatus.IN_PROGRESS)
except ItemNotFoundError:
    print("Item not found in tracker")

try:
    tracker.update_task('A', 'MyProject', 'invalid_task', TaskStatus.IN_PROGRESS)
except InvalidTaskTypeError:
    print("Invalid task type")

try:
    tracker.update_task('A', 'MyProject', 'content', TaskStatus.IN_PROGRESS)
except DependencyNotMetError:
    print("Dependencies not met - research must complete first")
```

## Configuration

Task types are configured in `src/tracker/config.py`:

```python
TASK_TYPE_RESEARCH = TaskTypeConfig(
    name="research",
    depends_on=[],  # No dependencies
    agent="researcher",
    output_pattern="research/{sanitized_name}.yaml",
    description="Research project details, features, and use cases"
)

TASK_TYPE_CONTENT = TaskTypeConfig(
    name="content",
    depends_on=["research"],  # Depends on research
    agent="writer",
    output_pattern="content/{sanitized_name}.md",
    description="Write detailed content for the project"
)
```

## Extensibility

The tracker system is designed for extensibility:

### Adding New Task Types

1. Define the task in `config.py`
2. Add to `TASK_TYPES` dictionary
3. Update `DEFAULT_ITEM_TASKS` or `DEFAULT_WEEK_TASKS` as needed

### Adding New Backends

1. Implement the `TrackerBackend` interface
2. Add to the `get_tracker()` factory function
3. Ensure all methods handle the data models correctly

### Custom Storage

The interface allows for different storage backends:
- Database storage (PostgreSQL, MongoDB)
- API-based storage
- In-memory storage for testing
- Cloud storage (S3, GCS)

## Troubleshooting

### Common Issues

**Tracker not found for week**
- Ensure ETL pipeline has run for that week
- Check that `data/weeks/XX-Y/tracker.yaml` exists

**Task dependencies not met**
- Check that prerequisite tasks are COMPLETED
- Use `tracker.get_progress()` to see overall status

**File permission errors**
- Ensure write access to `data/weeks/` directory
- Check that parent directories exist

### Debugging

```python
# Load and inspect tracker state
tracker = get_tracker()
week_tracker = tracker.load_tracker('A')

# Check specific item tasks
item_tasks = week_tracker.items['MyProject']
print(f"Research status: {item_tasks['research'].status}")
print(f"Content status: {item_tasks['content'].status}")

# Check week tasks
print(f"Blog post status: {week_tracker.week_tasks['blog_post'].status}")
```

## Future Enhancements

- **Retry Logic**: Automatic retry for failed tasks
- **Parallel Execution**: Support for concurrent task execution
- **Notifications**: Integration with notification systems
- **Metrics**: Detailed execution time and success rate tracking
- **Rollback**: Ability to revert task state changes
- **Audit Trail**: Complete history of all state changes</content>
<parameter name="filePath">/workspaces/cncf-landscape-a-to-z/docs/tracker.md