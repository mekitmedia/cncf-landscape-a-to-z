from pydantic_ai import RunContext
from src.tracker import get_tracker, TaskStatus
from src.agentic.deps import AgentDeps
import logging

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

def get_all_weeks_status(ctx: RunContext[AgentDeps]) -> str:
    """Gets an overview of the status for all weeks A-Z."""
    try:
        tracker = get_tracker(config=ctx.deps.config)
        results = []
        for char_code in range(ord('A'), ord('Z') + 1):
            letter = chr(char_code)
            if tracker.tracker_exists(letter):
                # Check research progress
                res_progress = tracker.get_progress(letter, "research")
                # Check blog post progress
                blog_progress = tracker.get_progress(letter, "blog_post")
                
                if blog_progress.completed > 0:
                    status = "✅ Blog Completed"
                elif res_progress.completion_percentage > 0:
                    status = f"🏗️ Research in Progress ({res_progress.completion_percentage:.1f}%)"
                else:
                    status = "📝 ETL Done, Not Started"
                results.append(f"Week {letter}: {status}")
            else:
                results.append(f"Week {letter}: ❌ Not Started (ETL required)")
        return "\n".join(results)
    except Exception as e:
        return f"Error getting overview: {e}"
