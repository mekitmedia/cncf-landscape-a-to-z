# Graph-Driven Parallel Orchestration

## Overview

This document describes the refactored orchestration system that enables **parallel execution** of research and writing tasks while respecting embedded task dependencies.

### Previous Architecture

The original workflow was **sequential per-week**:
```
Editor picks Week A → Researchers research items → Writers write blog → Editor picks Week B → ...
```

**Limitation**: Only one week could be processed at a time, despite research tasks being independent across weeks.

### New Architecture

The refactored workflow is **graph-aware and parallel**:
```
┌─────────────────────────────────────────────────┐
│  Orchestrator: get_ready_tasks()                │
│  (respects dependency graph, returns batch)     │
└─────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
   Ready Research         Ready blog_post
   (any week)            (once research ✓)
        │                       │
   Researchers ║          Writers
   work in ║║║║║║         work in ║║║║
   parallel ║║║║║║        parallel ║║║║
```

## Key Components

### 1. Task Dependency Graph

Embedded in tracker:
- **Item-level**: `research` → `content` (content can't start until research completes)
- **Week-level**: `research` (all items) → `blog_post` (blog can't start until all research done)

Checked via `tracker.can_start_task(week, item, task_type)` which validates:
- Task status is `PENDING`
- All dependencies are satisfied

### 2. ReadyTask Model

```python
class ReadyTask(BaseModel):
    week_letter: str              # Week letter (A-Z)
    item_name: str | None         # None for week-level tasks
    task_type: str                # 'research', 'content', 'blog_post'
    agent: str                    # Agent assigned ('researcher', 'writer', 'editor')
```

Represents a task that:
- Is in `PENDING` status
- Has all dependencies met (can_start_task returns True)
- Is ready for immediate execution

### 3. get_ready_tasks() Method

**Location**: `src/tracker/yaml_backend.py`

**Signature**:
```python
def get_ready_tasks(self, limit: Optional[int] = None) -> List[ReadyTask]
```

**Algorithm**:
1. Iterate through all weeks (A-Z)
2. For each week, check all pending tasks
3. Call `can_start_task()` for each pending task
4. Include only tasks where dependencies are met
5. Sort by week, task type for deterministic ordering
6. Return up to `limit` tasks

**Complexity**: O(weeks × items × task_types)

### 4. get_ready_tasks() Tool

**Location**: `src/agentic/tools/tracker.py`

**Signature**:
```python
def get_ready_tasks(ctx: RunContext[AgentDeps], data: GetReadyTasksInput) -> GetReadyTasksOutput
```

**Input**:
```python
class GetReadyTasksInput(BaseModel):
    agent_type: str = ""  # Filter: 'researcher', 'writer', 'editor', or ""
    limit: int = 5        # Max tasks (1-20)
```

**Output**:
```python
class GetReadyTasksOutput(BaseModel):
    tasks: List[TaskData]     # Ready tasks
    total_available: int      # Total ready tasks (before limit)
    message: str              # Status message
```

Available as a tool to **all agents** for discovering independent work.

### 5. Updated Agents

#### Researcher Agent
- **Input**: `ReadyTask` (or original `ProjectMetadata` for compatibility)
- **Tools**: `get_ready_tasks("researcher", limit=5)` + research tools
- **Output**: `ResearchOutput` (unchanged)
- **System Prompt**: Can now discover and pick research tasks independently

#### Writer Agent
- **Input**: `ReadyTask` for `blog_post` tasks
- **Tools**: `get_ready_tasks("writer", limit=5)` + writing tools
- **Output**: `BlogPostDraft` (unchanged)
- **System Prompt**: Can now pick blog_post tasks once research is complete

#### Editor Agent
- **Role**: Evolving to quality reviewer (currently unchanged for backward compatibility)
- **Future**: Review completed blog posts instead of selecting weeks

## Two Orchestration Modes

### Mode 1: Sequential (Legacy)
**Function**: `weekly_content_flow(limit=None)`

- **Invokes**: Editor Agent → gets next week decision
- **Processes**: All items for that week
- **Flow**: Sequential per-week
- **Use Case**: Backward compatibility, debugging

**Still supported** and functional.

### Mode 2: Parallel (New)
**Function**: `parallel_orchestration_flow(max_rounds=10, batch_size=5)`

- **Does NOT invoke Editor**: Uses task queue directly
- **Per Round**:
  1. Get batch of ready researcher tasks
  2. Get batch of ready writer tasks
  3. Execute research tasks in parallel
  4. Execute writer tasks in parallel
  5. Save results
  6. Loop until no more ready tasks
- **Use Case**: Maximize throughput, enable independent parallel work

**New feature** for efficient large-scale processing.

## Task Dependency Graph Examples

### Example 1: Week A, 3 items

```
Initial State:
├─ Week A
│  ├─ Item A1: research=PENDING, content=PENDING
│  ├─ Item A2: research=PENDING, content=PENDING
│  └─ Item A3: research=PENDING, content=PENDING
│  └─ blog_post=PENDING

Ready Tasks Initially: [research(A1), research(A2), research(A3)]

After researching A1:
├─ Item A1: research=COMPLETED ✓, content=PENDING
│  → content(A1) becomes ready!

Ready Tasks Now: [research(A2), research(A3), content(A1)]

After researching A2, A3 and researching A2 content:
├─ Item A2: research=COMPLETED ✓, content=COMPLETED ✓
├─ Item A3: research=COMPLETED ✓, content=PENDING
├─ All research done ✓
│  → blog_post(A) becomes ready!

Ready Tasks Now: [content(A1), content(A3), blog_post(A)]
```

### Example 2: Multiple Weeks Running in Parallel

```
Round 1:
  Researchers: [research(A1), research(A2), research(B1), research(B2), research(C1)]
  Writers:     []  (no week has all research done yet)
  
Round 2 (after Round 1 completes):
  Researchers: [research(A3), research(B3), research(C2), research(D1), research(D2)]
  Writers:     [blog_post(A)]  (Week A all research done!)
  
Round 3:
  Researchers: [research(C3), research(D3), research(E1), research(E2), research(E3)]
  Writers:     [blog_post(B), blog_post(C)]  (Weeks B, C all research done!)
```

## Tracker Method: can_start_task()

**Location**: `src/tracker/yaml_backend.py` (and interface)

**Purpose**: Core dependency checking logic

**Algorithm**:
```
if task_type in ["research", "content"]:
    # Item-level task: check item not removed
    if item.removed:
        return False
    # Check if item task exists and pending
    if task not in item.tasks or task.status != PENDING:
        return False
    # Check dependencies
    if task_type == "research":
        return True  # Always ready (no dependencies)
    elif task_type == "content":
        return item.research_task.status == COMPLETED
        
elif task_type == "blog_post":
    # Week-level task: check all items have research done
    for item in week.items:
        if item.research_task.status != COMPLETED:
            return False
    return week.blog_post_task.status == PENDING
```

**Key Insight**: This logic determines which tasks appear in `get_ready_tasks()`.

## Integration Points

### With Tracker System
- `tracker.get_ready_tasks()` queries all tasks
- `tracker.can_start_task()` validates each task
- `tracker.update_task()` marks tasks complete (moves to next ready state)

### With Agents
- `get_ready_tasks()` tool available to all agents
- Agents can discover independent work
- Agents can pick any ready task, not just assigned week

### With Orchestrator
- `parallel_orchestration_flow()` uses task queues
- Dispatches batches of ready tasks
- Parallelizes execution across agents

### With Web UI
- Task queue visible in UI (if exposed via tools)
- Real-time updates as tasks complete
- Enables flexible assignment UI

## Configuration

### Task Types
Defined in `src/tracker/config.py`:
```python
TASK_CONFIG = {
    "research": TaskConfig(agent="researcher", ...),
    "content": TaskConfig(agent="writer", ...),
    "blog_post": TaskConfig(agent="writer", ...),
}
```

### Orchestration Parameters
In `src/agentic/flow.py`:
```python
await parallel_orchestration_flow(
    max_rounds=10,      # Prevent infinite loops
    batch_size=5        # Tasks per agent per round
)
```

## Monitoring & Logging

All operations log to Prefect task logger:

```
=== Orchestration Round 1 ===
Getting 5 ready tasks for researcher
Found 5 ready tasks for researcher
Dispatching 5 research tasks
Research completed for item X
[... parallel execution ...]
Round 1 complete
```

Use Prefect UI to monitor:
- Flow runs
- Task parallelism
- Task completion timeline
- Failed tasks

## Future Enhancements

1. **Editor as Reviewer**: Change editor role from selector to quality reviewer
2. **Dynamic Batch Sizing**: Adjust batch_size based on available agents
3. **Priority Queue**: Order tasks by week (A → Z) within each type
4. **Rate Limiting**: Add delays for API rate limits (search, fetch, model APIs)
5. **Error Recovery**: Automatic retry for transient failures
6. **Incremental Checkpointing**: Save state between rounds for resumability

## Migration Guide

### From Sequential to Parallel

**Old Code**:
```python
await weekly_content_flow(limit=100)
```

**New Code**:
```python
# For parallel execution:
await parallel_orchestration_flow(max_rounds=20, batch_size=5)

# Or keep sequential for backward compatibility:
await weekly_content_flow(limit=100)
```

### For Agents

**Old Agent Code** (week-based):
```python
# Receives ProjectMetadata with week_letter
async def research_item(item: ProjectMetadata, week_letter: str) -> ResearchOutput:
```

**New Agent Code** (can work with ReadyTask):
```python
# Can still receive ProjectMetadata (backward compatible)
# Or can discover ready tasks:
async def agent_invocation(...):
    ready = await tool.get_ready_tasks("researcher", limit=5)
    for task in ready:
        # Pick and work on task
        # task has: week_letter, item_name, task_type, agent
```

## Troubleshooting

### No Ready Tasks Found
**Symptom**: `get_ready_tasks()` returns empty list

**Causes**:
1. All tasks completed ✓
2. All pending tasks have unmet dependencies
   - Check `can_start_task()` logic
   - Verify task status in tracker

**Debug**:
```python
tracker = get_tracker()
# Check pending tasks
pending = tracker.get_progress(week_letter, "research")
# Check if dependencies met
can_start = tracker.can_start_task(week_letter, item_name, task_type)
```

### Tasks Not Progressing
**Symptom**: Ready tasks list doesn't change between rounds

**Causes**:
1. Agent not updating tracker status
   - Must call `update_tracker_status()` when done
2. Orchestrator not reloading tracker
   - Each round should reload state

**Debug**:
```python
# Check tracker file for updated status
cat data/weeks/{XX}-{Letter}/tracker.yaml
# Should show COMPLETED status after agent finishes
```

### Dependencies Not Respected
**Symptom**: blog_post tasks appear ready before research done

**Cause**: `can_start_task()` logic bug

**Debug**:
```python
# Check can_start_task directly
can_start = tracker.can_start_task(week_letter, None, "blog_post")
# Should be False if any research is PENDING
```

## API Reference

### ReadyTask
```python
@dataclass
class ReadyTask:
    week_letter: str              # 'A', 'B', ..., 'Z'
    item_name: str | None         # None for week-level tasks
    task_type: str                # 'research', 'content', 'blog_post'
    agent: str                    # 'researcher', 'writer', 'editor'
```

### get_ready_tasks() Tool
```python
# In agent
result = await tool.get_ready_tasks(GetReadyTasksInput(
    agent_type="researcher",  # Optional filter
    limit=5                   # Max tasks
))

# result.tasks: List[TaskData] with ready tasks
# result.total_available: int, total ready before limit
# result.message: str, status message
```

### Parallel Flow
```python
# In main script
await parallel_orchestration_flow(
    max_rounds=10,       # Max orchestration rounds
    batch_size=5         # Tasks per agent per round
)
```

## Related Documentation

- [ETL Pipeline](etl-pipeline.md) - Data ingestion
- [Agentic Workflow](agentic-workflow.md) - Agent roles and interactions
- [Tracker](tracker.md) - Task tracking system
- [Architecture](architecture.md) - Overall system design
