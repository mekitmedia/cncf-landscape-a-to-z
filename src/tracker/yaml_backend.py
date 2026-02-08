"""YAML-based tracker backend implementation."""

import os
import yaml
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from src.config import load_config, week_id
from src.tracker.models import (
    WeekTracker,
    ItemTasks,
    WeekTasks,
    TaskRecord,
    TaskProgress,
    TaskStatus,
)
from src.tracker.config import (
    get_task_config,
    is_valid_task_type,
    DEFAULT_ITEM_TASKS,
    DEFAULT_WEEK_TASKS,
)
from src.tracker.exceptions import (
    DependencyNotMetError,
    InvalidTaskTypeError,
    ItemNotFoundError,
    WeekNotFoundError,
)
from src.tracker.models import ReadyTask


class YAMLTrackerBackend:
    """YAML file-based tracker backend."""
    
    def __init__(self, config=None):
        """Initialize YAML tracker backend."""
        self.cfg = config or load_config()
    
    def _get_tracker_path(self, week_letter: str) -> Path:
        """Get path to tracker file for a week.
        
        Args:
            week_letter: Letter of the week (A-Z)
            
        Returns:
            Path to tracker.yaml file
        """
        week_dir = self.cfg.weeks_dir / week_id(week_letter)
        return week_dir / "tracker.yaml"
    
    def _get_tasks_path(self, week_letter: str) -> Path:
        """Get path to tasks.yaml file for a week.
        
        Args:
            week_letter: Letter of the week (A-Z)
            
        Returns:
            Path to tasks.yaml file
        """
        week_dir = self.cfg.weeks_dir / week_id(week_letter)
        return week_dir / "tasks.yaml"
    
    def tracker_exists(self, week_letter: str) -> bool:
        """Check if tracker exists for a week."""
        return self._get_tracker_path(week_letter).exists()
    
    def load_tracker(self, week_letter: str) -> WeekTracker:
        """Load tracker data for a specific week."""
        tracker_path = self._get_tracker_path(week_letter)
        
        if not tracker_path.exists():
            # Initialize from tasks.yaml if it exists
            if self._get_tasks_path(week_letter).exists():
                return self._initialize_from_tasks(week_letter)
            else:
                raise WeekNotFoundError(f"No tracker or tasks found for week {week_letter}")
        
        with open(tracker_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return WeekTracker(**data)
    
    def save_tracker(self, week_letter: str, tracker: WeekTracker) -> None:
        """Save tracker data for a specific week."""
        tracker_path = self._get_tracker_path(week_letter)
        
        # Ensure directory exists
        tracker_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to dict and save atomically
        data = tracker.model_dump(mode='json')
        
        # Write to temp file first, then rename (atomic on POSIX)
        temp_path = tracker_path.with_suffix('.yaml.tmp')
        with open(temp_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        temp_path.replace(tracker_path)
    
    def _initialize_from_tasks(self, week_letter: str) -> WeekTracker:
        """Initialize tracker from tasks.yaml file.
        
        Args:
            week_letter: Letter of the week (A-Z)
            
        Returns:
            Newly initialized WeekTracker
        """
        tasks_path = self._get_tasks_path(week_letter)
        
        with open(tasks_path, 'r', encoding='utf-8') as f:
            item_names = yaml.safe_load(f) or []
        
        # Initialize tracker with all items
        tracker = WeekTracker(
            items={},
            week_tasks=WeekTasks(),
            metadata={
                "created_at": datetime.now().isoformat(),
                "week_letter": week_letter,
            }
        )
        
        # Add each item with default tasks
        for item_name in item_names:
            tracker.items[item_name] = self._create_default_item_tasks()
        
        # Add week-level tasks
        for task_type in DEFAULT_WEEK_TASKS:
            tracker.week_tasks.tasks[task_type] = TaskRecord(
                status=TaskStatus.PENDING,
                agent=get_task_config(task_type).agent
            )
        
        # Save initialized tracker
        self.save_tracker(week_letter, tracker)
        
        return tracker
    
    def _create_default_item_tasks(self) -> ItemTasks:
        """Create default tasks for a new item.
        
        Returns:
            ItemTasks with default pending tasks
        """
        tasks = {}
        for task_type in DEFAULT_ITEM_TASKS:
            config = get_task_config(task_type)
            tasks[task_type] = TaskRecord(
                status=TaskStatus.PENDING,
                agent=config.agent
            )
        
        return ItemTasks(tasks=tasks)
    
    def get_pending_items(self, week_letter: str, task_type: str) -> List[str]:
        """Get list of items with pending tasks of a specific type."""
        if not is_valid_task_type(task_type):
            raise InvalidTaskTypeError(f"Invalid task type: {task_type}")
        
        tracker = self.load_tracker(week_letter)
        
        pending_items = []
        for item_name, item_tasks in tracker.items.items():
            # Skip removed items
            if item_tasks.removed:
                continue
            
            # Check if task exists and is pending
            task_record = item_tasks.get(task_type)
            if task_record and task_record.status == TaskStatus.PENDING:
                # Check if dependencies are met
                if self._check_dependencies(tracker, item_name, task_type):
                    pending_items.append(item_name)
        
        return pending_items
    
    def can_start_task(self, week_letter: str, item: Optional[str], task_type: str) -> bool:
        """Check if a task can be started (dependencies met)."""
        if not is_valid_task_type(task_type):
            return False
        
        tracker = self.load_tracker(week_letter)
        
        return self._check_dependencies(tracker, item, task_type)
    
    def _check_dependencies(
        self,
        tracker: WeekTracker,
        item: Optional[str],
        task_type: str
    ) -> bool:
        """Check if dependencies are met for a task.
        
        Args:
            tracker: WeekTracker instance
            item: Item name (None for week-level tasks)
            task_type: Type of task to check
            
        Returns:
            True if dependencies are met, False otherwise
        """
        config = get_task_config(task_type)
        
        # Week-level task
        if item is None or config.is_week_level:
            # Check if all items have completed the dependent task
            for dep_task_type in config.depends_on:
                for item_name, item_tasks in tracker.items.items():
                    if item_tasks.removed:
                        continue
                    
                    dep_task = item_tasks.get(dep_task_type)
                    if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                        return False
            return True
        
        # Item-level task
        if item not in tracker.items:
            return False
        
        item_tasks = tracker.items[item]
        
        # Check each dependency
        for dep_task_type in config.depends_on:
            dep_task = item_tasks.get(dep_task_type)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def update_task(
        self,
        week_letter: str,
        item: Optional[str],
        task_type: str,
        status: TaskStatus,
        **metadata
    ) -> None:
        """Update task status and metadata."""
        if not is_valid_task_type(task_type):
            raise InvalidTaskTypeError(f"Invalid task type: {task_type}")
        
        tracker = self.load_tracker(week_letter)
        config = get_task_config(task_type)
        
        # Determine if week-level or item-level task
        is_week_task = item is None or config.is_week_level
        
        if is_week_task:
            # Week-level task
            if task_type not in tracker.week_tasks.tasks:
                tracker.week_tasks.tasks[task_type] = TaskRecord(agent=config.agent)
            
            task_record = tracker.week_tasks.tasks[task_type]
        else:
            # Item-level task
            if item not in tracker.items:
                raise ItemNotFoundError(f"Item not found: {item}")
            
            if task_type not in tracker.items[item].tasks:
                tracker.items[item].tasks[task_type] = TaskRecord(agent=config.agent)
            
            task_record = tracker.items[item].tasks[task_type]
        
        # Check dependencies if transitioning to IN_PROGRESS
        if status == TaskStatus.IN_PROGRESS:
            if not self._check_dependencies(tracker, item, task_type):
                deps = ", ".join(config.depends_on)
                raise DependencyNotMetError(
                    f"Cannot start task '{task_type}' for {'week' if is_week_task else item}: "
                    f"dependencies not met ({deps})"
                )
        
        # Update task record
        task_record.status = status
        
        if status == TaskStatus.IN_PROGRESS and task_record.started_at is None:
            task_record.started_at = datetime.now()
        
        if status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED):
            task_record.completed_at = datetime.now()
        
        # Update metadata
        for key, value in metadata.items():
            if hasattr(task_record, key):
                setattr(task_record, key, value)
        
        # Save updated tracker
        self.save_tracker(week_letter, tracker)
    
    def sync_with_etl(self, week_letter: str, items: List[str]) -> None:
        """Synchronize tracker with ETL output."""
        changes_detected = False

        # Load or initialize tracker
        if self.tracker_exists(week_letter):
            tracker = self.load_tracker(week_letter)
        else:
            changes_detected = True
            tracker = WeekTracker(
                items={},
                week_tasks=WeekTasks(),
                metadata={
                    "created_at": datetime.now().isoformat(),
                    "week_letter": week_letter,
                }
            )
            
            # Initialize week-level tasks
            for task_type in DEFAULT_WEEK_TASKS:
                tracker.week_tasks.tasks[task_type] = TaskRecord(
                    status=TaskStatus.PENDING,
                    agent=get_task_config(task_type).agent
                )
        
        # Check for missing metadata or mismatched count
        if "last_synced" not in tracker.metadata or tracker.metadata.get("etl_item_count") != len(items):
            changes_detected = True

        # Add new items from ETL and restore removed items
        for item_name in items:
            if item_name not in tracker.items:
                tracker.items[item_name] = self._create_default_item_tasks()
                changes_detected = True
            elif getattr(tracker.items[item_name], "removed", False):
                # Item was removed but is now back in ETL
                tracker.items[item_name].removed = False
                changes_detected = True
        
        # Mark removed items (preserve history)
        etl_items_set = set(items)
        for item_name in tracker.items:
            if item_name not in etl_items_set:
                if not getattr(tracker.items[item_name], "removed", False):
                    tracker.items[item_name].removed = True
                    changes_detected = True
        
        if changes_detected:
            # Update metadata
            tracker.metadata["last_synced"] = datetime.now().isoformat()
            tracker.metadata["etl_item_count"] = len(items)

            # Save updated tracker
            self.save_tracker(week_letter, tracker)
    
    def get_progress(self, week_letter: str, task_type: Optional[str] = None) -> TaskProgress:
        """Get progress statistics for a week."""
        tracker = self.load_tracker(week_letter)
        
        # Count tasks by status
        counts = {
            TaskStatus.PENDING: 0,
            TaskStatus.IN_PROGRESS: 0,
            TaskStatus.COMPLETED: 0,
            TaskStatus.FAILED: 0,
            TaskStatus.SKIPPED: 0,
        }
        
        # Count item-level tasks
        for item_name, item_tasks in tracker.items.items():
            if item_tasks.removed:
                continue
            
            for task_name, task_record in item_tasks.tasks.items():
                if task_type is None or task_name == task_type:
                    counts[task_record.status] += 1
        
        # Count week-level tasks if not filtering by task type
        if task_type is None:
            for task_record in tracker.week_tasks.tasks.values():
                counts[task_record.status] += 1
        
        total = sum(counts.values())
        
        return TaskProgress(
            total=total,
            pending=counts[TaskStatus.PENDING],
            in_progress=counts[TaskStatus.IN_PROGRESS],
            completed=counts[TaskStatus.COMPLETED],
            failed=counts[TaskStatus.FAILED],
            skipped=counts[TaskStatus.SKIPPED],
        )
    
    def get_ready_tasks(self, limit: Optional[int] = None) -> List[ReadyTask]:
        """Get all ready tasks across all weeks (graph-aware).
        
        Returns pending tasks where all dependencies are met, respecting the task dependency graph.
        This enables parallel execution: researcher can work on any research tasks,
        writer can work on any blog_post tasks where research is complete, etc.
        
        Args:
            limit: Maximum number of tasks to return (None for unlimited)
            
        Returns:
            List of ReadyTask objects ready for execution, sorted by week then task type
        """
        ready_tasks = []
        
        # Check all weeks A-Z
        for char_code in range(ord('A'), ord('Z') + 1):
            letter = chr(char_code)
            if not self.tracker_exists(letter):
                continue
            
            try:
                tracker = self.load_tracker(letter)
            except WeekNotFoundError:
                continue
            
            # Check item-level tasks
            for item_name, item_tasks in tracker.items.items():
                if item_tasks.removed:
                    continue
                
                for task_type, task_record in item_tasks.tasks.items():
                    # Only include pending tasks where dependencies are met
                    if task_record.status == TaskStatus.PENDING:
                        if self.can_start_task(letter, item_name, task_type):
                            config = get_task_config(task_type)
                            ready_tasks.append(ReadyTask(
                                week_letter=letter,
                                item_name=item_name,
                                task_type=task_type,
                                agent=config.agent
                            ))
            
            # Check week-level tasks
            for task_type, task_record in tracker.week_tasks.tasks.items():
                if task_record.status == TaskStatus.PENDING:
                    if self.can_start_task(letter, None, task_type):
                        config = get_task_config(task_type)
                        ready_tasks.append(ReadyTask(
                            week_letter=letter,
                            item_name=None,
                            task_type=task_type,
                            agent=config.agent
                        ))
        
        # Sort by week, then task type for deterministic ordering
        ready_tasks.sort(key=lambda t: (t.week_letter, t.task_type, t.item_name or ""))
        
        # Apply limit if specified
        if limit is not None:
            ready_tasks = ready_tasks[:limit]
        
        return ready_tasks
