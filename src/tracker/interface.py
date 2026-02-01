"""Protocol interface for tracker backends."""

from typing import Protocol, List, Dict, Any, Optional
from src.tracker.models import WeekTracker, TaskProgress, TaskStatus


class TrackerBackend(Protocol):
    """Protocol defining the interface for tracker storage backends.
    
    This allows for multiple implementations (YAML, database, API, etc.)
    while maintaining a consistent interface for the business logic.
    """
    
    def load_tracker(self, week_letter: str) -> WeekTracker:
        """Load tracker data for a specific week.
        
        Args:
            week_letter: Letter of the week (A-Z)
            
        Returns:
            WeekTracker instance with current state
            
        Raises:
            WeekNotFoundError: If week tracker doesn't exist
        """
        ...
    
    def save_tracker(self, week_letter: str, tracker: WeekTracker) -> None:
        """Save tracker data for a specific week.
        
        Args:
            week_letter: Letter of the week (A-Z)
            tracker: WeekTracker instance to save
        """
        ...
    
    def get_pending_items(self, week_letter: str, task_type: str) -> List[str]:
        """Get list of items with pending tasks of a specific type.
        
        Args:
            week_letter: Letter of the week (A-Z)
            task_type: Type of task to check
            
        Returns:
            List of item names with pending tasks
        """
        ...
    
    def can_start_task(self, week_letter: str, item: str, task_type: str) -> bool:
        """Check if a task can be started (dependencies met).
        
        Args:
            week_letter: Letter of the week (A-Z)
            item: Name of the item (or None for week-level tasks)
            task_type: Type of task to check
            
        Returns:
            True if dependencies are met, False otherwise
        """
        ...
    
    def update_task(
        self,
        week_letter: str,
        item: Optional[str],
        task_type: str,
        status: TaskStatus,
        **metadata
    ) -> None:
        """Update task status and metadata.
        
        Args:
            week_letter: Letter of the week (A-Z)
            item: Name of the item (None for week-level tasks)
            task_type: Type of task to update
            status: New status for the task
            **metadata: Additional metadata (output_file, error_message, etc.)
            
        Raises:
            ItemNotFoundError: If item doesn't exist
            InvalidTaskTypeError: If task type is invalid
            DependencyNotMetError: If trying to start task with unmet dependencies
        """
        ...
    
    def sync_with_etl(self, week_letter: str, items: List[str]) -> None:
        """Synchronize tracker with ETL output.
        
        - Add new items from ETL with default tasks
        - Mark removed items (preserve history)
        - Update tracker metadata
        
        Args:
            week_letter: Letter of the week (A-Z)
            items: List of item names from ETL
        """
        ...
    
    def get_progress(self, week_letter: str, task_type: Optional[str] = None) -> TaskProgress:
        """Get progress statistics for a week.
        
        Args:
            week_letter: Letter of the week (A-Z)
            task_type: Specific task type to check (None for all tasks)
            
        Returns:
            TaskProgress with statistics
        """
        ...
    
    def tracker_exists(self, week_letter: str) -> bool:
        """Check if tracker exists for a week.
        
        Args:
            week_letter: Letter of the week (A-Z)
            
        Returns:
            True if tracker exists, False otherwise
        """
        ...
