from pathlib import Path
import sys
from unittest.mock import patch, mock_open

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agentic.projections import create_tool_card, project_week_deck
from src.tracker.yaml_backend import YAMLTrackerBackend
from src.tracker.models import TaskStatus, WeekTracker, ItemTasks, TaskRecord

def test_create_tool_card():
    mock_research = {
        "project_name": "TestTool",
        "summary": " ".join(["This summary sentence stays intentionally long."] * 30),
        "cncf_status": "incubating",
        "repo_url": "https://github.com/test/tool",
        "key_features": [
            "Feature 1 is very cool",
            "Feature 2 is awesome",
            "Feature 3 is okay"
        ]
    }

    card = create_tool_card(mock_research)

    # Assert length is compact
    assert len(card.split()) <= 80
    # Assert content
    assert "TestTool" in card
    assert "incubating" in card
    assert "https://github.com/test/tool" in card
    assert "Feature 1 is very cool" in card
    assert "Feature 2 is awesome" in card
    assert "Feature 3 is okay" not in card

@patch("src.agentic.projections.glob.glob")
def test_project_week_deck(mock_glob):
    mock_glob.return_value = ["file1.yaml", "file2.yaml"]

    mock_yaml_1 = """
project_name: ToolOne
summary: Summary one.
cncf_status: sandbox
repo_url: https://url.one
key_features:
  - F1
"""
    mock_yaml_2 = """
project_name: ToolTwo
summary: Summary two.
cncf_status: graduated
repo_url: https://url.two
key_features:
  - F2
"""

    def side_effect(path, mode):
        if path == "file1.yaml":
            return mock_open(read_data=mock_yaml_1).return_value
        elif path == "file2.yaml":
            return mock_open(read_data=mock_yaml_2).return_value
        return mock_open(read_data="").return_value

    with patch("builtins.open", side_effect=side_effect):
        deck = project_week_deck("00-A")

        assert "ToolOne" in deck
        assert "ToolTwo" in deck
        assert "sandbox" in deck
        assert "graduated" in deck
        assert "F1" in deck
        assert "F2" in deck

def test_can_start_task_dag():
    tracker = WeekTracker(
        items={
            "item1": ItemTasks(
                tasks={
                    "research": TaskRecord(status=TaskStatus.COMPLETED),
                    "content": TaskRecord(status=TaskStatus.PENDING)
                }
            ),
            "item2": ItemTasks(
                tasks={
                    "research": TaskRecord(status=TaskStatus.SKIPPED),
                    "content": TaskRecord(status=TaskStatus.PENDING)
                }
            )
        }
    )

    yaml_tracker = YAMLTrackerBackend("data/weeks")

    # item1 content can start because its research is COMPLETED
    assert yaml_tracker.can_start_task("00-A", "item1", "content", tracker=tracker) is True

    # item2 content cannot start because its research is SKIPPED
    assert yaml_tracker.can_start_task("00-A", "item2", "content", tracker=tracker) is False

    # blog_post cannot start because not all items have content completed
    assert yaml_tracker.can_start_task("00-A", None, "blog_post", tracker=tracker) is False

    # item2 research becomes completed
    tracker.items["item2"].tasks["research"].status = TaskStatus.COMPLETED
    assert yaml_tracker.can_start_task("00-A", "item2", "content", tracker=tracker) is True

    # item1 and item2 content becomes completed and skipped
    tracker.items["item1"].tasks["content"].status = TaskStatus.COMPLETED
    tracker.items["item2"].tasks["content"].status = TaskStatus.SKIPPED

    # blog_post CAN start now
    assert yaml_tracker.can_start_task("00-A", None, "blog_post", tracker=tracker) is True
