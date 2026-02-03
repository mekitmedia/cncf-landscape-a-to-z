"""Task tracker package for managing workflow progress.

This package provides a flexible, interface-based task tracking system
that can work with different storage backends (YAML, database, API, etc.).

Example usage:
    >>> from src.tracker import get_tracker, TaskStatus
    >>> 
    >>> tracker = get_tracker()
    >>> 
    >>> # Get pending items for research
    >>> items = tracker.get_pending_items('A', 'research')
    >>> 
    >>> # Update task status
    >>> tracker.update_task('A', 'MyProject', 'research', TaskStatus.IN_PROGRESS)
    >>> tracker.update_task('A', 'MyProject', 'research', TaskStatus.COMPLETED,
    ...                    output_file='research/myproject.yaml')
    >>> 
    >>> # Check progress
    >>> progress = tracker.get_progress('A')
    >>> print(f"Completed {progress.completed}/{progress.total} tasks")
"""

from src.tracker.interface import TrackerBackend
from src.tracker.yaml_backend import YAMLTrackerBackend
from src.tracker.models import (
    TaskStatus,
    TaskRecord,
    ItemTasks,
    WeekTasks,
    WeekTracker,
    TaskProgress,
    ReadyTask,
)
from src.tracker.config import (
    TaskTypeConfig,
    TASK_TYPES,
    DEFAULT_ITEM_TASKS,
    DEFAULT_WEEK_TASKS,
    get_task_config,
    is_valid_task_type,
)
from src.tracker.exceptions import (
    TrackerError,
    DependencyNotMetError,
    InvalidTaskTypeError,
    ItemNotFoundError,
    WeekNotFoundError,
)


def get_tracker(backend_type: str = "yaml", config=None) -> TrackerBackend:
    """Get a tracker backend instance.
    
    Args:
        backend_type: Type of backend to use ('yaml' is currently supported)
        config: Optional config to use instead of loading from environment
        
    Returns:
        TrackerBackend instance
        
    Raises:
        ValueError: If backend_type is not supported
    """
    if backend_type == "yaml":
        return YAMLTrackerBackend(config)
    else:
        raise ValueError(f"Unsupported backend type: {backend_type}")


__all__ = [
    # Factory
    "get_tracker",
    
    # Interface
    "TrackerBackend",
    
    # Models
    "TaskStatus",
    "TaskRecord",
    "ItemTasks",
    "WeekTasks",
    "WeekTracker",
    "TaskProgress",
    
    # Config
    "TaskTypeConfig",
    "TASK_TYPES",
    "DEFAULT_ITEM_TASKS",
    "DEFAULT_WEEK_TASKS",
    "get_task_config",
    "is_valid_task_type",
    
    # Exceptions
    "TrackerError",
    "DependencyNotMetError",
    "InvalidTaskTypeError",
    "ItemNotFoundError",
    "WeekNotFoundError",
    
    # Backends
    "YAMLTrackerBackend",
]
