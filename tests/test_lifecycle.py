"""Tests for lifecycle state machine and transition validation."""

import pytest
from pathlib import Path

from src.tracker.lifecycle import (
    LifecycleStage,
    determine_lifecycle_stage,
    validate_transition,
    sanitize_for_filename,
    find_touched_tools,
    ALLOWED_TRANSITIONS,
)


def test_lifecycle_stage_enum():
    assert LifecycleStage.INITIAL == "initial"
    assert LifecycleStage.FIRST_PASS == "first_pass"
    assert LifecycleStage.TECH_WRITING == "tech_writing"
    assert LifecycleStage.APPROVED == "approved"
    assert isinstance(LifecycleStage.INITIAL, str)


def test_determine_lifecycle_stage():
    # 1. Approved via editorial_lock
    assert determine_lifecycle_stage(
        item_tracker={"tasks": {"content": {"status": "completed"}, "research": {"status": "completed"}}},
        research_data={"editorial_lock": True, "summary": "Locked project"},
    ) == LifecycleStage.APPROVED

    # Approved via tool frontmatter
    assert determine_lifecycle_stage(
        tool_frontmatter={"lifecycle_stage": "approved"}
    ) == LifecycleStage.APPROVED

    # 2. Tech Writing via tracker content completed
    assert determine_lifecycle_stage(
        item_tracker={"tasks": {"content": {"status": "completed"}, "research": {"status": "completed"}}},
        research_data={"editorial_lock": False, "summary": "Project summary"},
    ) == LifecycleStage.TECH_WRITING

    # Tech Writing via frontmatter
    assert determine_lifecycle_stage(
        tool_frontmatter={"lifecycle_stage": "tech_writing"}
    ) == LifecycleStage.TECH_WRITING

    # 3. First Pass via tracker research completed
    assert determine_lifecycle_stage(
        item_tracker={"tasks": {"content": {"status": "pending"}, "research": {"status": "completed"}}},
        research_data={"summary": "Gathered research"},
    ) == LifecycleStage.FIRST_PASS

    # First Pass via research YAML data with pending tracker
    assert determine_lifecycle_stage(
        item_tracker={"tasks": {"content": {"status": "pending"}, "research": {"status": "pending"}}},
        research_data={"project_name": "Test", "summary": "Some research summary"},
    ) == LifecycleStage.FIRST_PASS

    # 4. Initial state
    assert determine_lifecycle_stage(
        item_tracker={"tasks": {"content": {"status": "pending"}, "research": {"status": "pending"}}},
        research_data={},
    ) == LifecycleStage.INITIAL

    assert determine_lifecycle_stage(None, None, None) == LifecycleStage.INITIAL


def test_validate_transition_legal_forward():
    # Step 1: initial -> first_pass
    valid, msg = validate_transition(LifecycleStage.INITIAL, LifecycleStage.FIRST_PASS)
    assert valid is True
    assert msg == ""

    # Step 2: first_pass -> tech_writing
    valid, msg = validate_transition(LifecycleStage.FIRST_PASS, LifecycleStage.TECH_WRITING)
    assert valid is True
    assert msg == ""

    # Step 3: tech_writing -> approved
    valid, msg = validate_transition(LifecycleStage.TECH_WRITING, LifecycleStage.APPROVED)
    assert valid is True
    assert msg == ""


def test_validate_transition_idempotent_self():
    for stage in LifecycleStage:
        valid, msg = validate_transition(stage, stage, allow_same=True)
        assert valid is True
        assert msg == ""

        valid_no_same, err_no_same = validate_transition(stage, stage, allow_same=False)
        assert valid_no_same is False
        assert "did not change" in err_no_same


def test_validate_transition_rollbacks():
    # Unlocking approved tool to tech_writing
    valid, msg = validate_transition(LifecycleStage.APPROVED, LifecycleStage.TECH_WRITING)
    assert valid is True

    # Re-researching tech_writing tool to first_pass
    valid, msg = validate_transition(LifecycleStage.TECH_WRITING, LifecycleStage.FIRST_PASS)
    assert valid is True


def test_validate_transition_illegal_skips():
    # initial -> tech_writing (Skipped first_pass research review!)
    valid, msg = validate_transition(LifecycleStage.INITIAL, LifecycleStage.TECH_WRITING)
    assert valid is False
    assert "Illegal lifecycle skip" in msg
    assert "initial" in msg
    assert "tech_writing" in msg
    assert "first_pass" in msg

    # initial -> approved (Skipped both!)
    valid, msg = validate_transition(LifecycleStage.INITIAL, LifecycleStage.APPROVED)
    assert valid is False
    assert "Illegal lifecycle skip" in msg

    # first_pass -> approved (Skipped tech_writing!)
    valid, msg = validate_transition(LifecycleStage.FIRST_PASS, LifecycleStage.APPROVED)
    assert valid is False
    assert "Illegal lifecycle skip" in msg
    assert "tech_writing" in msg


def test_validate_transition_string_inputs():
    valid, msg = validate_transition("initial", "first_pass")
    assert valid is True

    valid, msg = validate_transition("initial", "tech_writing")
    assert valid is False
    assert "Illegal lifecycle skip" in msg

    invalid, err = validate_transition("unknown_stage", "first_pass")
    assert invalid is False
    assert "Invalid source stage" in err


def test_find_touched_tools(tmp_path: Path):
    # Setup mock structure
    weeks_dir = tmp_path / "data" / "weeks"
    week_dir = weeks_dir / "00-A"
    week_cat = week_dir / "categories"
    week_cat.mkdir(parents=True, exist_ok=True)
    
    (week_cat / "cloud.yaml").write_text(
        "- name: Foo Tool\n  project: sandbox\n",
        encoding="utf-8"
    )

    diff_files = [
        "data/weeks/00-A/research/foo_tool.yaml",
        "website/content/tools/foo_tool.md",
    ]

    tools = find_touched_tools(diff_files, repo_root=tmp_path)
    assert len(tools) == 1
    assert tools[0]["week_id"] == "00-A"
    assert tools[0]["slug"] == "foo_tool"
    assert tools[0]["item_name"] == "Foo Tool"
