"""Task type configuration and definitions."""

from typing import List, Optional
from pydantic import BaseModel, Field


class TaskTypeConfig(BaseModel):
    """Configuration for a task type."""
    name: str = Field(description="Unique name of the task type")
    depends_on: List[str] = Field(default_factory=list, description="List of task types this depends on")
    agent: Optional[str] = Field(default=None, description="Agent responsible for this task")
    output_pattern: Optional[str] = Field(default=None, description="Pattern for output file location")
    description: Optional[str] = Field(default=None, description="Human-readable description")
    is_week_level: bool = Field(default=False, description="Whether this is a week-level task")


# Define available task types
# Item-level tasks (per project)
TASK_TYPE_RESEARCH = TaskTypeConfig(
    name="research",
    depends_on=[],
    agent="researcher",
    output_pattern="research/{sanitized_name}.yaml",
    description="Research project details, features, and use cases"
)

TASK_TYPE_CONTENT = TaskTypeConfig(
    name="content",
    depends_on=["research"],
    agent="writer",
    output_pattern="content/{sanitized_name}.md",
    description="Write detailed content for the project"
)

# Week-level tasks (require all items to be complete)
TASK_TYPE_BLOG_POST = TaskTypeConfig(
    name="blog_post",
    depends_on=["content"],  # All items must have content completed
    agent="writer",
    output_pattern="website/content/letters/{year}-{letter}.md",
    description="Write weekly blog post announcing all projects",
    is_week_level=True
)

# Consolidated task types dictionary
TASK_TYPES: dict[str, TaskTypeConfig] = {
    "research": TASK_TYPE_RESEARCH,
    "content": TASK_TYPE_CONTENT,
    "blog_post": TASK_TYPE_BLOG_POST,
}

# Default item-level tasks (tasks to initialize for each new item)
DEFAULT_ITEM_TASKS = ["research", "content"]

# Default week-level tasks
DEFAULT_WEEK_TASKS = ["blog_post"]


def get_task_config(task_type: str) -> TaskTypeConfig:
    """Get configuration for a task type.
    
    Args:
        task_type: Name of the task type
        
    Returns:
        TaskTypeConfig for the task
        
    Raises:
        KeyError: If task type is not defined
    """
    return TASK_TYPES[task_type]


def is_valid_task_type(task_type: str) -> bool:
    """Check if a task type is valid.
    
    Args:
        task_type: Name of the task type
        
    Returns:
        True if task type exists, False otherwise
    """
    return task_type in TASK_TYPES
