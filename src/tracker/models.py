"""Pydantic models for task tracking."""

from enum import Enum
from typing import Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    """Status of a task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TaskRecord(BaseModel):
    """Record of a single task execution."""
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current status of the task")
    started_at: Optional[datetime] = Field(default=None, description="When the task was started")
    completed_at: Optional[datetime] = Field(default=None, description="When the task was completed")
    output_file: Optional[str] = Field(default=None, description="Relative path to output file")
    error_message: Optional[str] = Field(default=None, description="Error message if task failed")
    retry_count: int = Field(default=0, description="Number of times task was retried")
    agent: Optional[str] = Field(default=None, description="Agent that executed the task")
    
    model_config = ConfigDict(use_enum_values=True)


class ItemTasks(BaseModel):
    """Collection of tasks for a single item."""
    tasks: Dict[str, TaskRecord] = Field(default_factory=dict, description="Map of task_type to TaskRecord")
    removed: bool = Field(default=False, description="Whether item was removed from ETL")
    
    def __getitem__(self, task_type: str) -> TaskRecord:
        """Allow dict-like access to tasks."""
        return self.tasks[task_type]
    
    def __setitem__(self, task_type: str, record: TaskRecord):
        """Allow dict-like assignment to tasks."""
        self.tasks[task_type] = record
    
    def get(self, task_type: str, default=None) -> Optional[TaskRecord]:
        """Get task record with default."""
        return self.tasks.get(task_type, default)


class WeekTasks(BaseModel):
    """Week-level tasks that depend on all items being completed."""
    tasks: Dict[str, TaskRecord] = Field(default_factory=dict, description="Map of task_type to TaskRecord")
    
    def __getitem__(self, task_type: str) -> TaskRecord:
        """Allow dict-like access to tasks."""
        return self.tasks[task_type]
    
    def __setitem__(self, task_type: str, record: TaskRecord):
        """Allow dict-like assignment to tasks."""
        self.tasks[task_type] = record
    
    def get(self, task_type: str, default=None) -> Optional[TaskRecord]:
        """Get task record with default."""
        return self.tasks.get(task_type, default)


class WeekTracker(BaseModel):
    """Complete tracker state for a week."""
    items: Dict[str, ItemTasks] = Field(default_factory=dict, description="Map of item_name to ItemTasks")
    week_tasks: WeekTasks = Field(default_factory=WeekTasks, description="Week-level tasks")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = ConfigDict(use_enum_values=True)


class TaskProgress(BaseModel):
    """Progress statistics for tasks."""
    total: int = Field(description="Total number of tasks")
    pending: int = Field(description="Number of pending tasks")
    in_progress: int = Field(description="Number of tasks in progress")
    completed: int = Field(description="Number of completed tasks")
    failed: int = Field(description="Number of failed tasks")
    skipped: int = Field(description="Number of skipped tasks")
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total == 0:
            return 0.0
        return (self.completed / self.total) * 100


class ReadyTask(BaseModel):
    """A task that is ready to be executed (all dependencies met)."""
    week_letter: str = Field(description="Week letter (A-Z)")
    item_name: Optional[str] = Field(default=None, description="Item name (None for week-level tasks)")
    task_type: str = Field(description="Type of task (research, content, blog_post, etc.)")
    agent: Optional[str] = Field(default=None, description="Agent assigned to this task type")
    
    model_config = ConfigDict(use_enum_values=True)
