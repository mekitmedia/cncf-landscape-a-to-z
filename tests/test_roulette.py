from datetime import datetime, timezone, timedelta
from pathlib import Path
import pytest
import yaml

from src.roulette import (
    calculate_project_weight,
    get_all_candidates,
    check_adhoc_tasks,
    draw_task,
    DrawnTask,
)
from src.pipeline.tool_pages import generate_single_tool_page


@pytest.fixture(autouse=True)
def setup_test_data():
    """Setup mock week data in test directory."""
    from src.config import load_config
    cfg = load_config()

    # Create week 00-A with a sample category and item
    week_a_cat = cfg.weeks_dir / "00-A" / "categories"
    week_a_cat.mkdir(parents=True, exist_ok=True)
    week_a_research = cfg.weeks_dir / "00-A" / "research"
    week_a_research.mkdir(parents=True, exist_ok=True)

    sample_items = [
        {
            "name": "Akri",
            "project": "sandbox",
            "repo_url": "https://github.com/project-akri/akri",
            "homepage_url": "https://akri.sh",
        },
        {
            "name": "Argo CD",
            "project": "graduated",
            "repo_url": "https://github.com/argoproj/argo-cd",
            "homepage_url": "https://argoproj.github.io/cd/",
        },
    ]

    with (week_a_cat / "provisioning.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(sample_items, f)

    # Also create sample research for Akri
    sample_research = {
        "project_name": "Akri",
        "summary": "A Kubernetes Resource Interface for the Edge",
        "key_features": ["Expose leaf devices as Kubernetes resources"],
    }
    with (week_a_research / "akri.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(sample_research, f)

    yield cfg


def test_calculate_project_weight():
    now = datetime(2026, 9, 23, 12, 0, 0, tzinfo=timezone.utc)

    # 1. Unresearched item gets base weight 100.0
    weight_unresearched = calculate_project_weight(
        has_research=False,
        last_updated=None,
        cncf_status="sandbox",
        now=now,
    )
    assert weight_unresearched == 100.0

    # 2. Researched 14 days ago (2 weeks ago)
    two_weeks_ago = now - timedelta(days=14)
    weight_graduated = calculate_project_weight(
        has_research=True,
        last_updated=two_weeks_ago,
        cncf_status="graduated",
        now=now,
    )
    assert weight_graduated == pytest.approx(3.0)

    # 3. Researched yesterday (1 day ago)
    yesterday = now - timedelta(days=1)
    weight_sandbox = calculate_project_weight(
        has_research=True,
        last_updated=yesterday,
        cncf_status="sandbox",
        now=now,
    )
    assert weight_sandbox == pytest.approx(1.0)


def test_get_all_candidates():
    candidates = get_all_candidates()
    assert len(candidates) >= 2
    names = [c.name for c in candidates]
    assert "Akri" in names
    assert "Argo CD" in names

    # Check candidates for week A
    week_a_candidates = get_all_candidates(week_letter="A")
    assert len(week_a_candidates) >= 2
    assert all(c.week_letter == "A" for c in week_a_candidates)


def test_draw_task_roulette():
    task = draw_task(week_letter="A", seed=42, allow_adhoc=False)
    assert task is not None
    assert isinstance(task, DrawnTask)
    assert task.week_letter == "A"
    assert task.task_type == "roulette"
    assert "data/weeks/00-A/research/" in task.research_file
    assert "website/content/tools/" in task.tool_page_file
    assert "data/weeks/00-A/tracker.yaml" in task.tracker_file

    prompt = task.to_prompt()
    assert task.project_name in prompt
    assert task.research_file in prompt
    assert task.tool_page_file in prompt


def test_draw_task_adhoc(setup_test_data):
    cfg = setup_test_data
    adhoc_file = cfg.data_dir / "adhoc_tasks.yaml"
    adhoc_file.parent.mkdir(parents=True, exist_ok=True)

    # Write a test adhoc task
    test_adhoc = {
        "tasks": [
            {
                "project_name": "Argo CD",
                "reason": "Test Urgent Priority Task",
                "status": "pending",
                "priority": "high",
            }
        ]
    }
    with adhoc_file.open("w", encoding="utf-8") as f:
        yaml.safe_dump(test_adhoc, f)

    # Draw task - should pick adhoc Argo CD
    task = draw_task(allow_adhoc=True)
    assert task is not None
    assert task.task_type == "adhoc"
    assert task.project_name == "Argo CD"
    assert "Test Urgent Priority Task" in task.reason
    assert "Ad-hoc Priority" in task.to_prompt()


def test_generate_single_tool_page(setup_test_data):
    cfg = setup_test_data
    research_file = cfg.weeks_dir / "00-A" / "research" / "akri.yaml"
    assert research_file.exists()

    output = generate_single_tool_page(research_file)
    assert output is not None
    assert output.exists()
    assert output.name == "akri.md"
    content = output.read_text(encoding="utf-8")
    assert "Akri" in content

