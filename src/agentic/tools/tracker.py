from pydantic_ai import RunContext
from pydantic import BaseModel, Field
from src.tracker import get_tracker, TaskStatus, ReadyTask
from src.agentic.deps import AgentDeps
import logging
from typing import List

logger = logging.getLogger(__name__)

def update_tracker_status(ctx: RunContext[AgentDeps], item_name: str, task_type: str, status: str, week_letter: str) -> str:
    """Update the tracker status for a task."""
    try:
        tracker = get_tracker(config=ctx.deps.config)
        task_status = TaskStatus(status.lower())
        tracker.update_task(week_letter, item_name, task_type, task_status)
        return f"Updated {item_name} {task_type} to {status}"
    except Exception as e:
        logger.error(f"Failed to update tracker: {e}")
        return f"Failed to update tracker: {e}"

def check_tracker_progress(ctx: RunContext[AgentDeps], week_letter: str) -> str:
    """Checks the tracker progress for a specific week."""
    # Validate input to prevent path traversal
    if not (len(week_letter) == 1 and 'A' <= week_letter <= 'Z'):
        return "Invalid week letter provided"
    
    try:
        tracker = get_tracker(config=ctx.deps.config)
        if not tracker.tracker_exists(week_letter):
            return f"No tracker found for week {week_letter}. ETL may not have run yet."
        
        progress = tracker.get_progress(week_letter, "research")
        blog_progress = tracker.get_progress(week_letter, "blog_post")
        
        return f"Week {week_letter} progress:\n" \
               f"- Research: {progress.completed}/{progress.total} completed ({progress.completion_percentage:.1f}%)\n" \
               f"- Blog post: {'Completed' if blog_progress.completed > 0 else 'Not started'}"
    except Exception as e:
        return f"Error checking tracker for {week_letter}: {e}"


# Explicit input/output models for gateway compatibility
class GetAllWeeksStatusInput(BaseModel):
    only_incomplete: bool = True
    """If True, return only incomplete weeks; if False, return all weeks A-Z."""

class GetAllWeeksStatusOutput(BaseModel):
    status: str

def get_all_weeks_status(ctx: RunContext[AgentDeps], data: GetAllWeeksStatusInput) -> GetAllWeeksStatusOutput:
    """Gets status for weeks A-Z. By default, returns only incomplete weeks to reduce context.
    
    Args:
        data: GetAllWeeksStatusInput with only_incomplete flag
        
    Returns:
        GetAllWeeksStatusOutput with formatted status string
    """
    try:
        tracker = get_tracker(config=ctx.deps.config)
        results = []
        incomplete_count = 0
        
        for char_code in range(ord('A'), ord('Z') + 1):
            letter = chr(char_code)
            if tracker.tracker_exists(letter):
                # Check research progress
                res_progress = tracker.get_progress(letter, "research")
                # Check blog post progress
                blog_progress = tracker.get_progress(letter, "blog_post")
                
                # Determine if this week is complete
                is_completed = blog_progress.completed > 0
                
                # Format status
                if is_completed:
                    status = "✅ Blog Completed"
                elif res_progress.completion_percentage > 0:
                    status = f"🏗️ In Progress ({res_progress.completion_percentage:.1f}%)"
                else:
                    status = "📝 Not Started"
                
                # Only add incomplete weeks if flag is set
                if not is_completed:
                    results.append(f"Week {letter}: {status}")
                    incomplete_count += 1
                elif not data.only_incomplete:
                    results.append(f"Week {letter}: {status}")
            elif not data.only_incomplete:
                results.append(f"Week {letter}: ❌ ETL required")
        
        if not results:
            return GetAllWeeksStatusOutput(status="All weeks are complete!")
        
        header = f"Incomplete weeks ({incomplete_count}):" if data.only_incomplete else "Week status:"
        return GetAllWeeksStatusOutput(status=header + "\n" + "\n".join(results))
    except Exception as e:
        return GetAllWeeksStatusOutput(status=f"Error getting overview: {e}")


# Graph-aware task discovery for parallel execution
class GetReadyTasksInput(BaseModel):
    agent_type: str = Field(default="", description="Filter by agent: 'researcher', 'writer', 'editor', or empty for all")
    limit: int = Field(default=5, description="Maximum tasks to return (1-20)")

class TaskData(BaseModel):
    week_letter: str
    item_name: str | None = None
    task_type: str
    agent: str

class GetReadyTasksOutput(BaseModel):
    tasks: List[TaskData]
    total_available: int
    message: str

def get_ready_tasks(ctx: RunContext[AgentDeps], data: GetReadyTasksInput) -> GetReadyTasksOutput:
    """Get tasks ready for execution (respecting dependency graph).
    
    Returns pending tasks where all dependencies are met. This enables parallel execution:
    - Researcher can work on any 'research' tasks
    - Writer can work on 'blog_post' tasks once all research in that week completes
    - Editor can work on 'blog_post' tasks once they're written and ready for review
    
    Args:
        data: GetReadyTasksInput with optional agent filter and limit
        
    Returns:
        GetReadyTasksOutput with list of ready tasks and metadata
    """
    try:
        tracker = get_tracker(config=ctx.deps.config)
        
        # Get all ready tasks (respects dependency graph via can_start_task)
        ready_list = tracker.get_ready_tasks(limit=None)
        
        # Filter by agent if specified
        agent_filter = data.agent_type.strip().lower()
        if agent_filter:
            ready_list = [t for t in ready_list if t.agent.lower() == agent_filter]
        
        # Apply limit (1-20)
        limit = max(1, min(data.limit, 20))
        limited_tasks = ready_list[:limit]
        
        # Convert to output format
        tasks = [
            TaskData(
                week_letter=t.week_letter,
                item_name=t.item_name,
                task_type=t.task_type,
                agent=t.agent
            )
            for t in limited_tasks
        ]
        
        if not tasks:
            message = "No ready tasks available."
        elif agent_filter and len(tasks) < len(ready_list):
            message = f"Showing {len(tasks)} ready {agent_filter} tasks (out of {len(ready_list)} total ready)"
        else:
            message = f"Found {len(tasks)} ready task(s)"
        
        return GetReadyTasksOutput(
            tasks=tasks,
            total_available=len(ready_list),
            message=message
        )
    except Exception as e:
        logger.error(f"Error getting ready tasks: {e}")
        return GetReadyTasksOutput(
            tasks=[],
            total_available=0,
            message=f"Error getting ready tasks: {e}"
        )

