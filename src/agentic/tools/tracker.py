from pydantic_ai import RunContext
from src.tracker import get_tracker, TaskStatus
import logging

logger = logging.getLogger(__name__)

def update_tracker_status(ctx: RunContext, item_name: str, task_type: str, status: str, week_letter: str) -> str:
    """Update the tracker status for a task."""
    try:
        tracker = get_tracker()
        task_status = TaskStatus(status.lower())
        tracker.update_task(week_letter, item_name, task_type, task_status)
        return f"Updated {item_name} {task_type} to {status}"
    except Exception as e:
        logger.error(f"Failed to update tracker: {e}")
        return f"Failed to update tracker: {e}"

def check_tracker_progress(ctx: RunContext, week_letter: str) -> str:
    """Checks the tracker progress for a specific week."""
    # Validate input to prevent path traversal
    if not (len(week_letter) == 1 and 'A' <= week_letter <= 'Z'):
        return "Invalid week letter provided"
    
    try:
        tracker = get_tracker()
        if not tracker.tracker_exists(week_letter):
            return f"No tracker found for week {week_letter}. ETL may not have run yet."
        
        progress = tracker.get_progress(week_letter, "research")
        blog_progress = tracker.get_progress(week_letter, "blog_post")
        
        return f"Week {week_letter} progress:\n" \
               f"- Research: {progress.completed}/{progress.total} completed ({progress.completion_percentage:.1f}%)\n" \
               f"- Blog post: {'Completed' if blog_progress.completed > 0 else 'Not started'}"
    except Exception as e:
        return f"Error checking tracker for {week_letter}: {e}"
