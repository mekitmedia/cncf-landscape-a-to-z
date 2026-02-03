"""Unit tests for the tracker package."""

import pytest
import tempfile
import shutil
import os
import yaml
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tracker.models import (
    TaskStatus,
    TaskRecord,
    ItemTasks,
    WeekTasks,
    WeekTracker,
    TaskProgress,
)
from src.tracker.config import (
    TaskTypeConfig,
    TASK_TYPES,
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
from src.tracker.yaml_backend import YAMLTrackerBackend
from src.tracker import get_tracker


def test_task_status_enum():
    """Test TaskStatus enum values."""
    assert TaskStatus.PENDING == "pending"
    assert TaskStatus.IN_PROGRESS == "in_progress"
    assert TaskStatus.COMPLETED == "completed"
    assert TaskStatus.FAILED == "failed"
    assert TaskStatus.SKIPPED == "skipped"


def test_task_record_creation():
    """Test TaskRecord model creation and validation."""
    record = TaskRecord(
        status=TaskStatus.PENDING,
        agent="test_agent"
    )
    assert record.status == TaskStatus.PENDING
    assert record.agent == "test_agent"
    assert record.started_at is None
    assert record.completed_at is None
    assert record.error_message is None
    assert record.output_file is None


def test_task_record_with_timestamps():
    """Test TaskRecord with timestamp fields."""
    now = datetime.now()
    record = TaskRecord(
        status=TaskStatus.COMPLETED,
        agent="test_agent",
        started_at=now,
        completed_at=now,
        error_message="Test error",
        output_file="/path/to/file"
    )
    assert record.status == TaskStatus.COMPLETED
    assert record.agent == "test_agent"
    assert record.started_at == now
    assert record.completed_at == now
    assert record.error_message == "Test error"
    assert record.output_file == "/path/to/file"


def test_item_tasks_creation():
    """Test ItemTasks model creation."""
    item_tasks = ItemTasks()
    assert item_tasks.tasks == {}
    # Test that we can access tasks via dict-like interface
    item_tasks["research"] = TaskRecord(status=TaskStatus.PENDING)
    assert item_tasks["research"].status == TaskStatus.PENDING
    item_tasks["content"] = TaskRecord(status=TaskStatus.PENDING)
    assert item_tasks["content"].status == TaskStatus.PENDING


def test_week_tasks_creation():
    """Test WeekTasks model creation."""
    week_tasks = WeekTasks()
    assert week_tasks.tasks == {}
    # Test that we can access tasks via dict-like interface
    week_tasks["blog_post"] = TaskRecord(status=TaskStatus.PENDING)
    assert week_tasks["blog_post"].status == TaskStatus.PENDING


def test_week_tracker_creation():
    """Test WeekTracker model creation."""
    tracker = WeekTracker(
        items={},
        week_tasks=WeekTasks(),
        metadata={"test": "data"}
    )
    assert tracker.items == {}
    assert isinstance(tracker.week_tasks, WeekTasks)
    assert tracker.metadata == {"test": "data"}


def test_task_progress_calculation():
    """Test TaskProgress calculation."""
    # Test with no items
    progress = TaskProgress(total=0, pending=0, in_progress=0, completed=0, failed=0, skipped=0)
    assert progress.total == 0
    assert progress.completed == 0
    assert progress.completion_percentage == 0.0

    # Test with items
    progress = TaskProgress(total=10, pending=3, in_progress=2, completed=3, failed=1, skipped=1)
    assert progress.total == 10
    assert progress.completed == 3
    assert progress.completion_percentage == 30.0


def test_task_type_config_creation():
    """Test TaskTypeConfig creation."""
    config = TaskTypeConfig(
        name="test_task",
        depends_on=["dep1", "dep2"],
        agent="test_agent",
        output_pattern="/path/{name}",
        description="Test task",
        is_week_level=False
    )
    assert config.name == "test_task"
    assert config.depends_on == ["dep1", "dep2"]
    assert config.agent == "test_agent"
    assert config.output_pattern == "/path/{name}"
    assert config.description == "Test task"
    assert config.is_week_level == False


def test_get_task_config():
    """Test get_task_config function."""
    config = get_task_config("research")
    assert config.name == "research"
    assert config.agent == "researcher"
    assert config.depends_on == []

    config = get_task_config("content")
    assert config.name == "content"
    assert config.agent == "writer"
    assert config.depends_on == ["research"]

    config = get_task_config("blog_post")
    assert config.name == "blog_post"
    assert config.agent == "writer"
    assert config.depends_on == ["content"]
    assert config.is_week_level == True


def test_is_valid_task_type():
    """Test is_valid_task_type function."""
    assert is_valid_task_type("research") == True
    assert is_valid_task_type("content") == True
    assert is_valid_task_type("blog_post") == True
    assert is_valid_task_type("invalid") == False


def test_tracker_exists():
    """Test tracker_exists method."""
    import shutil
    backend = YAMLTrackerBackend()
    # Override config for testing
    backend.cfg = MagicMock()
    backend.cfg.weeks_dir = Path("/tmp/test_weeks")

    # Ensure directory doesn't exist
    week_dir = Path("/tmp/test_weeks") / "00-A"
    if week_dir.exists():
        shutil.rmtree(week_dir)

    # Test when file doesn't exist
    assert backend.tracker_exists("A") == False

    # Create the directory and file
    week_dir.mkdir(parents=True, exist_ok=True)
    tracker_file = week_dir / "tracker.yaml"
    tracker_file.write_text("test: data")

    assert backend.tracker_exists("A") == True

    # Cleanup
    shutil.rmtree("/tmp/test_weeks")


def test_load_tracker_nonexistent():
    """Test loading a nonexistent tracker."""
    backend = YAMLTrackerBackend()
    # Override config for testing
    backend.cfg = MagicMock()
    backend.cfg.weeks_dir = Path("/tmp/test_weeks")

    # Ensure no tracker files exist
    week_dir = Path("/tmp/test_weeks") / "00-A"
    if week_dir.exists():
        import shutil
        shutil.rmtree(week_dir)

    with pytest.raises(WeekNotFoundError):
        backend.load_tracker("A")


def test_initialize_from_tasks():
    """Test initializing tracker from tasks."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker manually
        tracker = WeekTracker(
            items={
                "Item 1": ItemTasks(),
                "Item 2": ItemTasks()
            },
            week_tasks=WeekTasks(),
            metadata={}
        )
        backend.save_tracker("A", tracker)

        # Check tracker was created
        assert backend.tracker_exists("A")
        loaded_tracker = backend.load_tracker("A")
        assert "Item 1" in tracker.items
        assert "Item 2" in tracker.items

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")


def test_save_and_load_tracker():
    """Test saving and loading tracker."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker
        tracker = WeekTracker(
            items={
                "Item 1": ItemTasks(),
                "Item 2": ItemTasks()
            },
            week_tasks=WeekTasks(),
            metadata={"created_at": datetime.now().isoformat()}
        )

        backend.save_tracker("A", tracker)
        loaded_tracker = backend.load_tracker("A")

        assert "Item 1" in loaded_tracker.items
        assert "Item 2" in loaded_tracker.items
        assert loaded_tracker.metadata["created_at"] is not None

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")


def test_get_pending_items():
    """Test getting pending items."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker with mixed status
        tracker = WeekTracker(
            items={
                "Item 1": backend._create_default_item_tasks(),
                "Item 2": backend._create_default_item_tasks()
            },
            week_tasks=WeekTasks(),
            metadata={}
        )
        # Mark Item 1 research as completed
        tracker.items["Item 1"]["research"].status = TaskStatus.COMPLETED

        backend.save_tracker("A", tracker)

        pending = backend.get_pending_items("A", "research")
        assert "Item 2" in pending
        assert "Item 1" not in pending

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")


def test_can_start_task_no_dependencies():
    """Test can_start_task with no dependencies."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker
        tracker = WeekTracker(
            items={"Item 1": ItemTasks()},
            week_tasks=WeekTasks(),
            metadata={}
        )
        backend.save_tracker("A", tracker)

        assert backend.can_start_task("A", "Item 1", "research") == True

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")


def test_can_start_task_with_dependencies():
    """Test can_start_task with dependencies."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker
        tracker = WeekTracker(
            items={"Item 1": ItemTasks()},
            week_tasks=WeekTasks(),
            metadata={}
        )
        backend.save_tracker("A", tracker)

        # Content depends on research
        assert backend.can_start_task("A", "Item 1", "content") == False

        # Mark research as completed
        tracker.items["Item 1"]["research"] = TaskRecord(status=TaskStatus.COMPLETED)
        backend.save_tracker("A", tracker)

        assert backend.can_start_task("A", "Item 1", "content") == True

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")


def test_can_start_week_task():
    """Test can_start_task for week-level tasks."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker with one item
        tracker = WeekTracker(
            items={"Item 1": ItemTasks()},
            week_tasks=WeekTasks(),
            metadata={}
        )
        backend.save_tracker("A", tracker)

        # Blog post requires all content tasks to be completed
        assert backend.can_start_task("A", None, "blog_post") == False

        # Mark content as completed
        tracker.items["Item 1"]["content"] = TaskRecord(status=TaskStatus.COMPLETED)
        backend.save_tracker("A", tracker)

        assert backend.can_start_task("A", None, "blog_post") == True

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")


def test_update_task():
    """Test updating task status."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker
        tracker = WeekTracker(
            items={"Item 1": ItemTasks()},
            week_tasks=WeekTasks(),
            metadata={}
        )
        backend.save_tracker("A", tracker)

        # Update task
        backend.update_task("A", "Item 1", "research", TaskStatus.IN_PROGRESS)

        loaded_tracker = backend.load_tracker("A")
        assert loaded_tracker.items["Item 1"]["research"].status == TaskStatus.IN_PROGRESS
        assert loaded_tracker.items["Item 1"]["research"].started_at is not None

        # Update to completed
        backend.update_task("A", "Item 1", "research", TaskStatus.COMPLETED)

        loaded_tracker = backend.load_tracker("A")
        assert loaded_tracker.items["Item 1"]["research"].status == TaskStatus.COMPLETED
        assert loaded_tracker.items["Item 1"]["research"].completed_at is not None

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")


def test_update_task_dependency_check():
    """Test update_task with dependency checking."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker
        tracker = WeekTracker(
            items={"Item 1": ItemTasks()},
            week_tasks=WeekTasks(),
            metadata={}
        )
        backend.save_tracker("A", tracker)

        # Try to update content without research completed
        with pytest.raises(DependencyNotMetError):
            backend.update_task("A", "Item 1", "content", TaskStatus.IN_PROGRESS)

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")


def test_update_task_invalid_type():
    """Test update_task with invalid task type."""
    with patch('src.config.load_config') as mock_load_config:
        mock_cfg = MagicMock()
        mock_cfg.weeks_dir = Path("/tmp/test_weeks")
        mock_load_config.return_value = mock_cfg

        backend = YAMLTrackerBackend()

        # Create week directory
        week_dir = Path("/tmp/test_weeks") / "00-A"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Create tracker
        tracker = WeekTracker(
            items={"Item 1": ItemTasks()},
            week_tasks=WeekTasks(),
            metadata={}
        )
        backend.save_tracker("A", tracker)

        # Try to update invalid task type
        with pytest.raises(InvalidTaskTypeError):
            backend.update_task("A", "Item 1", "invalid_task", TaskStatus.IN_PROGRESS)

        # Cleanup
        shutil.rmtree("/tmp/test_weeks")
