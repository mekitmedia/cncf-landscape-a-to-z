"""Unit tests for the tracker package."""

import unittest
import tempfile
import shutil
import os
import yaml
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

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


class TestTaskModels(unittest.TestCase):
    """Test Pydantic models for task tracking."""

    def test_task_status_enum(self):
        """Test TaskStatus enum values."""
        self.assertEqual(TaskStatus.PENDING, "pending")
        self.assertEqual(TaskStatus.IN_PROGRESS, "in_progress")
        self.assertEqual(TaskStatus.COMPLETED, "completed")
        self.assertEqual(TaskStatus.FAILED, "failed")
        self.assertEqual(TaskStatus.SKIPPED, "skipped")

    def test_task_record_creation(self):
        """Test TaskRecord model creation and validation."""
        record = TaskRecord(
            status=TaskStatus.PENDING,
            agent="researcher"
        )
        self.assertEqual(record.status, TaskStatus.PENDING)
        self.assertEqual(record.agent, "researcher")
        self.assertIsNone(record.started_at)
        self.assertIsNone(record.completed_at)

    def test_task_record_with_timestamps(self):
        """Test TaskRecord with timestamps."""
        started = datetime.now()
        completed = datetime.now()

        record = TaskRecord(
            status=TaskStatus.COMPLETED,
            started_at=started,
            completed_at=completed,
            output_file="research/test.yaml",
            agent="researcher"
        )

        self.assertEqual(record.status, TaskStatus.COMPLETED)
        self.assertEqual(record.started_at, started)
        self.assertEqual(record.completed_at, completed)
        self.assertEqual(record.output_file, "research/test.yaml")

    def test_item_tasks_creation(self):
        """Test ItemTasks model."""
        tasks = ItemTasks()
        self.assertEqual(len(tasks.tasks), 0)
        self.assertFalse(tasks.removed)

        # Test dict-like access
        tasks["research"] = TaskRecord(status=TaskStatus.PENDING)
        self.assertEqual(tasks["research"].status, TaskStatus.PENDING)
        self.assertEqual(tasks.get("research").status, TaskStatus.PENDING)
        self.assertIsNone(tasks.get("nonexistent"))

    def test_week_tasks_creation(self):
        """Test WeekTasks model."""
        tasks = WeekTasks()
        self.assertEqual(len(tasks.tasks), 0)

        # Test dict-like access
        tasks["blog_post"] = TaskRecord(status=TaskStatus.PENDING)
        self.assertEqual(tasks["blog_post"].status, TaskStatus.PENDING)

    def test_week_tracker_creation(self):
        """Test WeekTracker model."""
        tracker = WeekTracker()
        self.assertEqual(len(tracker.items), 0)
        self.assertIsInstance(tracker.week_tasks, WeekTasks)
        self.assertEqual(len(tracker.metadata), 0)

    def test_task_progress_calculation(self):
        """Test TaskProgress completion percentage calculation."""
        progress = TaskProgress(
            total=10,
            pending=3,
            in_progress=2,
            completed=4,
            failed=1,
            skipped=0
        )

        self.assertEqual(progress.total, 10)
        self.assertEqual(progress.completed, 4)
        self.assertEqual(progress.completion_percentage, 40.0)

        # Test zero total
        empty_progress = TaskProgress(total=0, pending=0, in_progress=0, completed=0, failed=0, skipped=0)
        self.assertEqual(empty_progress.completion_percentage, 0.0)


class TestTaskConfig(unittest.TestCase):
    """Test task type configuration."""

    def test_task_type_config_creation(self):
        """Test TaskTypeConfig model."""
        config = TaskTypeConfig(
            name="test_task",
            depends_on=["research"],
            agent="writer",
            output_pattern="content/{sanitized_name}.md",
            description="Test task",
            is_week_level=False
        )

        self.assertEqual(config.name, "test_task")
        self.assertEqual(config.depends_on, ["research"])
        self.assertEqual(config.agent, "writer")
        self.assertEqual(config.output_pattern, "content/{sanitized_name}.md")
        self.assertEqual(config.description, "Test task")
        self.assertFalse(config.is_week_level)

    def test_get_task_config(self):
        """Test get_task_config function."""
        config = get_task_config("research")
        self.assertEqual(config.name, "research")
        self.assertEqual(config.depends_on, [])
        self.assertEqual(config.agent, "researcher")

        config = get_task_config("blog_post")
        self.assertEqual(config.name, "blog_post")
        self.assertEqual(config.depends_on, ["content"])
        self.assertTrue(config.is_week_level)

    def test_is_valid_task_type(self):
        """Test is_valid_task_type function."""
        self.assertTrue(is_valid_task_type("research"))
        self.assertTrue(is_valid_task_type("content"))
        self.assertTrue(is_valid_task_type("blog_post"))
        self.assertFalse(is_valid_task_type("invalid_task"))


class TestYAMLTrackerBackend(unittest.TestCase):
    """Test YAML tracker backend functionality."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.weeks_dir = Path(self.test_dir) / "weeks"
        self.weeks_dir.mkdir()

        # Mock config
        self.mock_config = MagicMock()
        self.mock_config.weeks_dir = self.weeks_dir

        with patch('src.tracker.yaml_backend.load_config', return_value=self.mock_config):
            self.backend = YAMLTrackerBackend()

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    def test_tracker_exists(self):
        """Test tracker_exists method."""
        # Test non-existent tracker
        self.assertFalse(self.backend.tracker_exists("A"))

        # Create tracker file
        week_dir = self.weeks_dir / "00-A"
        week_dir.mkdir()
        (week_dir / "tracker.yaml").write_text("items: {}")

        self.assertTrue(self.backend.tracker_exists("A"))

    def test_load_tracker_nonexistent(self):
        """Test loading non-existent tracker raises error."""
        with self.assertRaises(WeekNotFoundError):
            self.backend.load_tracker("A")

    def test_initialize_from_tasks(self):
        """Test initializing tracker from tasks.yaml."""
        # Create tasks.yaml
        week_dir = self.weeks_dir / "00-A"
        week_dir.mkdir()
        tasks_file = week_dir / "tasks.yaml"
        tasks_file.write_text(yaml.dump(["Item 1", "Item 2"]))

        tracker = self.backend.load_tracker("A")

        # Check tracker was created
        self.assertIn("Item 1", tracker.items)
        self.assertIn("Item 2", tracker.items)
        self.assertIn("blog_post", tracker.week_tasks.tasks)

        # Check default tasks were created
        item1_tasks = tracker.items["Item 1"]
        self.assertIn("research", item1_tasks.tasks)
        self.assertIn("content", item1_tasks.tasks)
        self.assertEqual(item1_tasks.tasks["research"].status, TaskStatus.PENDING)
        self.assertEqual(item1_tasks.tasks["research"].agent, "researcher")

    def test_save_and_load_tracker(self):
        """Test saving and loading tracker."""
        tracker = WeekTracker(
            items={
                "TestItem": ItemTasks(tasks={
                    "research": TaskRecord(status=TaskStatus.COMPLETED, agent="researcher")
                })
            },
            week_tasks=WeekTasks(tasks={
                "blog_post": TaskRecord(status=TaskStatus.PENDING, agent="writer")
            }),
            metadata={"test": "value"}
        )

        # Save tracker
        self.backend.save_tracker("A", tracker)

        # Load tracker
        loaded_tracker = self.backend.load_tracker("A")

        # Verify data
        self.assertIn("TestItem", loaded_tracker.items)
        self.assertEqual(loaded_tracker.items["TestItem"].tasks["research"].status, TaskStatus.COMPLETED)
        self.assertEqual(loaded_tracker.week_tasks.tasks["blog_post"].status, TaskStatus.PENDING)
        self.assertEqual(loaded_tracker.metadata["test"], "value")

    def test_get_pending_items(self):
        """Test getting pending items for a task type."""
        tracker = WeekTracker(items={
            "Item1": ItemTasks(tasks={
                "research": TaskRecord(status=TaskStatus.COMPLETED)
            }),
            "Item2": ItemTasks(tasks={
                "research": TaskRecord(status=TaskStatus.PENDING)
            }),
            "Item3": ItemTasks(tasks={
                "research": TaskRecord(status=TaskStatus.PENDING)
            }, removed=True)  # Removed item should be ignored
        })

        self.backend.save_tracker("A", tracker)

        pending = self.backend.get_pending_items("A", "research")
        self.assertEqual(set(pending), {"Item2"})

    def test_can_start_task_no_dependencies(self):
        """Test can_start_task for task with no dependencies."""
        tracker = WeekTracker(items={
            "Item1": ItemTasks(tasks={
                "research": TaskRecord(status=TaskStatus.PENDING)
            })
        })

        self.backend.save_tracker("A", tracker)

        self.assertTrue(self.backend.can_start_task("A", "Item1", "research"))

    def test_can_start_task_with_dependencies(self):
        """Test can_start_task for task with dependencies."""
        tracker = WeekTracker(items={
            "Item1": ItemTasks(tasks={
                "research": TaskRecord(status=TaskStatus.COMPLETED),
                "content": TaskRecord(status=TaskStatus.PENDING)
            })
        })

        self.backend.save_tracker("A", tracker)

        # Content depends on research, which is completed
        self.assertTrue(self.backend.can_start_task("A", "Item1", "content"))

        # Test unmet dependency
        tracker.items["Item1"].tasks["research"].status = TaskStatus.PENDING
        self.backend.save_tracker("A", tracker)
        self.assertFalse(self.backend.can_start_task("A", "Item1", "content"))

    def test_can_start_week_task(self):
        """Test can_start_task for week-level tasks."""
        tracker = WeekTracker(
            items={
                "Item1": ItemTasks(tasks={
                    "content": TaskRecord(status=TaskStatus.COMPLETED)
                }),
                "Item2": ItemTasks(tasks={
                    "content": TaskRecord(status=TaskStatus.COMPLETED)
                })
            },
            week_tasks=WeekTasks(tasks={
                "blog_post": TaskRecord(status=TaskStatus.PENDING)
            })
        )

        self.backend.save_tracker("A", tracker)

        # Blog post requires all items to have completed content
        self.assertTrue(self.backend.can_start_task("A", None, "blog_post"))

        # Test unmet dependency
        tracker.items["Item1"].tasks["content"].status = TaskStatus.PENDING
        self.backend.save_tracker("A", tracker)
        self.assertFalse(self.backend.can_start_task("A", None, "blog_post"))

    def test_update_task(self):
        """Test updating task status."""
        tracker = WeekTracker(items={
            "Item1": ItemTasks(tasks={
                "research": TaskRecord(status=TaskStatus.PENDING, agent="researcher")
            })
        })

        self.backend.save_tracker("A", tracker)

        # Update to in progress
        self.backend.update_task("A", "Item1", "research", TaskStatus.IN_PROGRESS)
        updated_tracker = self.backend.load_tracker("A")

        task = updated_tracker.items["Item1"].tasks["research"]
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        self.assertIsNotNone(task.started_at)

        # Update to completed with metadata
        self.backend.update_task(
            "A", "Item1", "research", TaskStatus.COMPLETED,
            output_file="research/item1.yaml"
        )
        updated_tracker = self.backend.load_tracker("A")

        task = updated_tracker.items["Item1"].tasks["research"]
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.completed_at)
        self.assertEqual(task.output_file, "research/item1.yaml")

    def test_update_task_dependency_check(self):
        """Test that update_task enforces dependencies."""
        tracker = WeekTracker(items={
            "Item1": ItemTasks(tasks={
                "research": TaskRecord(status=TaskStatus.PENDING),
                "content": TaskRecord(status=TaskStatus.PENDING)
            })
        })

        self.backend.save_tracker("A", tracker)

        # Try to start content without research completed
        with self.assertRaises(DependencyNotMetError):
            self.backend.update_task("A", "Item1", "content", TaskStatus.IN_PROGRESS)

    def test_update_task_invalid_type(self):
        """Test updating invalid task type."""
        tracker = WeekTracker()
        self.backend.save_tracker("A", tracker)

        with self.assertRaises(InvalidTaskTypeError):
            self.backend.update_task("A", "Item1", "invalid_task", TaskStatus.PENDING)

    def test_sync_with_etl(self):
        """Test syncing tracker with ETL output."""
        # Initial tracker
        tracker = WeekTracker(items={
            "OldItem": ItemTasks(tasks={
                "research": TaskRecord(status=TaskStatus.COMPLETED)
            })
        })
        self.backend.save_tracker("A", tracker)

        # Sync with new ETL items (OldItem removed, NewItem added)
        self.backend.sync_with_etl("A", ["NewItem"])

        updated_tracker = self.backend.load_tracker("A")

        # Old item should be marked as removed
        self.assertTrue(updated_tracker.items["OldItem"].removed)

        # New item should be added with default tasks
        self.assertIn("NewItem", updated_tracker.items)
        self.assertIn("research", updated_tracker.items["NewItem"].tasks)
        self.assertIn("content", updated_tracker.items["NewItem"].tasks)

    def test_get_progress(self):
        """Test getting progress statistics."""
        tracker = WeekTracker(
            items={
                "Item1": ItemTasks(tasks={
                    "research": TaskRecord(status=TaskStatus.COMPLETED),
                    "content": TaskRecord(status=TaskStatus.PENDING)
                }),
                "Item2": ItemTasks(tasks={
                    "research": TaskRecord(status=TaskStatus.FAILED),
                    "content": TaskRecord(status=TaskStatus.SKIPPED)
                })
            },
            week_tasks=WeekTasks(tasks={
                "blog_post": TaskRecord(status=TaskStatus.IN_PROGRESS)
            })
        )

        self.backend.save_tracker("A", tracker)

        # Get progress for all tasks
        progress = self.backend.get_progress("A")
        self.assertEqual(progress.total, 5)  # 4 item tasks + 1 week task
        self.assertEqual(progress.completed, 1)
        self.assertEqual(progress.failed, 1)
        self.assertEqual(progress.skipped, 1)
        self.assertEqual(progress.in_progress, 1)
        self.assertEqual(progress.pending, 1)

        # Get progress for specific task type
        research_progress = self.backend.get_progress("A", "research")
        self.assertEqual(research_progress.total, 2)
        self.assertEqual(research_progress.completed, 1)
        self.assertEqual(research_progress.failed, 1)


class TestTrackerFactory(unittest.TestCase):
    """Test tracker factory function."""

    def test_get_tracker_yaml(self):
        """Test getting YAML tracker."""
        tracker = get_tracker("yaml")
        self.assertIsInstance(tracker, YAMLTrackerBackend)

    def test_get_tracker_default(self):
        """Test getting default tracker."""
        tracker = get_tracker()
        self.assertIsInstance(tracker, YAMLTrackerBackend)

    def test_get_tracker_invalid(self):
        """Test getting invalid tracker type."""
        with self.assertRaises(ValueError):
            get_tracker("invalid_type")


class TestTrackerIntegration(unittest.TestCase):
    """Integration tests for tracker functionality."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.weeks_dir = Path(self.test_dir) / "weeks"
        self.weeks_dir.mkdir()

        # Mock config
        self.mock_config = MagicMock()
        self.mock_config.weeks_dir = self.weeks_dir

    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)

    @patch('src.tracker.yaml_backend.load_config')
    def test_full_workflow_simulation(self, mock_load_config):
        """Test a full workflow simulation."""
        mock_load_config.return_value = self.mock_config

        backend = YAMLTrackerBackend()

        # Step 1: Initialize from ETL
        backend.sync_with_etl("A", ["Project1", "Project2"])

        # Step 2: Check initial state
        pending = backend.get_pending_items("A", "research")
        self.assertEqual(set(pending), {"Project1", "Project2"})

        # Step 3: Start research on first project
        backend.update_task("A", "Project1", "research", TaskStatus.IN_PROGRESS)

        # Step 4: Complete research
        backend.update_task(
            "A", "Project1", "research", TaskStatus.COMPLETED,
            output_file="research/project1.yaml"
        )

        # Step 5: Check that content can now start
        self.assertTrue(backend.can_start_task("A", "Project1", "content"))

        # Step 6: Start content
        backend.update_task("A", "Project1", "content", TaskStatus.IN_PROGRESS)

        # Step 7: Check progress
        progress = backend.get_progress("A")
        self.assertEqual(progress.completed, 1)  # research completed
        self.assertEqual(progress.in_progress, 1)  # content in progress

        # Step 8: Complete content
        backend.update_task("A", "Project1", "content", TaskStatus.COMPLETED)

        # Step 9: Check that blog post still can't start (Project2 not done)
        self.assertFalse(backend.can_start_task("A", None, "blog_post"))

        # Step 10: Complete Project2 research and content
        backend.update_task("A", "Project2", "research", TaskStatus.COMPLETED)
        backend.update_task("A", "Project2", "content", TaskStatus.COMPLETED)

        # Step 11: Now blog post can start
        self.assertTrue(backend.can_start_task("A", None, "blog_post"))

        # Step 12: Complete blog post
        backend.update_task("A", None, "blog_post", TaskStatus.COMPLETED)

        # Step 13: Final progress check
        final_progress = backend.get_progress("A")
        self.assertEqual(final_progress.total, 5)  # 4 item tasks + 1 week task
        self.assertEqual(final_progress.completed, 5)
        self.assertEqual(final_progress.completion_percentage, 100.0)


if __name__ == '__main__':
    unittest.main()