import sys
from pathlib import Path
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_contract import (
    validate_research_file,
    validate_tracker_file,
    validate_blog_post_file,
    filter_target_files,
    validate_lifecycle_transitions,
)


def test_validate_research_file_valid(tmp_path: Path):
    res_file = tmp_path / "valid_research.yaml"
    data = {
        "project_name": "Test Project",
        "homepage_url": "https://test.io",
        "repo_url": "https://github.com/test/test",
        "cncf_status": "incubating",
        "summary": "A test project summary",
        "key_features": ["Feature 1", "Feature 2"],
        "latest_release": {
            "version": "v1.0.0",
            "date": "2026-01-01",
            "url": "https://github.com/test/test/releases/tag/v1.0.0",
        },
        "recent_updates": "Released v1.0.0",
        "use_cases": "Testing automation",
        "interesting_facts": "Fact here",
        "get_started": "kubectl apply -f test.yaml",
        "docs_url": "https://test.io/docs",
        "related_tools": ["Tool A"],
        "sources": [{"id": "github1", "title": "GitHub", "url": "https://github.com/test/test", "source_type": "github_readme", "quotes": ["Some quote"]}],
    }
    res_file.write_text(yaml.dump(data), encoding="utf-8")

    ok, err = validate_research_file(res_file)
    assert ok is True
    assert err == ""


def test_validate_research_file_invalid_schema(tmp_path: Path):
    res_file = tmp_path / "invalid_research.yaml"
    # Invalid data: key_features is a string instead of a list
    data = {
        "project_name": "Test Project",
        "summary": "Summary",
        "key_features": "Not a list",
        "recent_updates": "Updates",
        "use_cases": "Use cases",
    }
    res_file.write_text(yaml.dump(data), encoding="utf-8")

    ok, err = validate_research_file(res_file)
    assert ok is False
    assert "key_features" in err


def test_validate_blog_post_file_valid(tmp_path: Path):
    post_file = tmp_path / "2026-A.md"
    content = """---
title: "Letter A: CNCF Projects"
date: 2026-01-01T00:00:00Z
draft: false
---

# Introduction
Sample post content
"""
    post_file.write_text(content, encoding="utf-8")

    ok, err = validate_blog_post_file(post_file)
    assert ok is True
    assert err == ""


def test_validate_blog_post_file_missing_frontmatter(tmp_path: Path):
    post_file = tmp_path / "invalid_post.md"
    post_file.write_text("# Just Header\nNo frontmatter here", encoding="utf-8")

    ok, err = validate_blog_post_file(post_file)
    assert ok is False
    assert "frontmatter" in err


def test_filter_target_files():
    paths = [
        "data/weeks/00-A/research/akri.yaml",
        "data/weeks/00-A/tracker.yaml",
        "website/content/posts/2026-A.md",
        "website/content/posts/_index.md",
        "random/file.txt",
    ]
    research, tracker, posts = filter_target_files(paths)

    assert len(research) == 1
    assert str(research[0]).endswith("akri.yaml")
    assert len(tracker) == 1
    assert str(tracker[0]).endswith("tracker.yaml")
    assert len(posts) == 1
    assert str(posts[0]).endswith("2026-A.md")

def test_validate_blog_post_file_crlf_valid(tmp_path: Path):
    post_file = tmp_path / "crlf-test.md"
    content = "---\r\ntitle: \"Letter A\"\r\ndate: 2026-01-01T00:00:00Z\r\ndraft: false\r\n---\r\n\r\n# Body"
    with open(post_file, "wb") as f:
        f.write(content.encode("utf-8"))
    ok, err = validate_blog_post_file(post_file)
    assert ok is True, f"Failed: {err}"


def test_validate_lifecycle_transitions_skip_error(tmp_path: Path, monkeypatch):
    from unittest.mock import patch
    from src.tracker.lifecycle import LifecycleStage

    # Mock git ref verification
    with patch("scripts.validate_contract.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        # Mock git show helper to return INITIAL stage for "keep"
        with patch("scripts.validate_contract.get_tool_stage_at_git_ref", return_value=LifecycleStage.INITIAL):
            # Mock working tree to return TECH_WRITING
            with patch("scripts.validate_contract.get_tool_stage_in_working_tree", return_value=LifecycleStage.TECH_WRITING):
                diff_files = [
                    "data/weeks/10-K/research/keep.yaml",
                    "data/weeks/10-K/tracker.yaml",
                    "website/content/tools/keep.md",
                ]

                # Mock find_touched_tools
                with patch("scripts.validate_contract.find_touched_tools") as mock_find:
                    mock_find.return_value = [
                        {"week_id": "10-K", "item_name": "Keep", "slug": "keep"}
                    ]

                    errs = validate_lifecycle_transitions(diff_files, ref="origin/main", repo_root=tmp_path)
                    assert len(errs) == 1
                    item_name, week_id, from_st, to_st, msg = errs[0]
                    assert item_name == "Keep"
                    assert from_st == "initial"
                    assert to_st == "tech_writing"
                    assert "Illegal lifecycle skip" in msg


def test_validate_lifecycle_transitions_valid_first_pass(tmp_path: Path):
    from unittest.mock import patch
    from src.tracker.lifecycle import LifecycleStage

    with patch("scripts.validate_contract.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        with patch("scripts.validate_contract.get_tool_stage_at_git_ref", return_value=LifecycleStage.INITIAL):
            with patch("scripts.validate_contract.get_tool_stage_in_working_tree", return_value=LifecycleStage.FIRST_PASS):
                diff_files = [
                    "data/weeks/10-K/research/keep.yaml",
                    "data/weeks/10-K/tracker.yaml",
                ]

                with patch("scripts.validate_contract.find_touched_tools") as mock_find:
                    mock_find.return_value = [
                        {"week_id": "10-K", "item_name": "Keep", "slug": "keep"}
                    ]

                    errs = validate_lifecycle_transitions(diff_files, ref="origin/main", repo_root=tmp_path)
                    assert len(errs) == 0


def test_validate_lifecycle_transitions_first_pass_with_markdown_rejected(tmp_path: Path):
    from unittest.mock import patch
    from src.tracker.lifecycle import LifecycleStage

    # Create dummy markdown file in tmp_path
    tool_page = tmp_path / "website" / "content" / "tools" / "keep.md"
    tool_page.parent.mkdir(parents=True, exist_ok=True)
    tool_page.write_text("---\ntitle: Keep\n---\n", encoding="utf-8")

    with patch("scripts.validate_contract.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0

        with patch("scripts.validate_contract.get_tool_stage_at_git_ref", return_value=LifecycleStage.INITIAL):
            with patch("scripts.validate_contract.get_tool_stage_in_working_tree", return_value=LifecycleStage.FIRST_PASS):
                diff_files = [
                    "data/weeks/10-K/research/keep.yaml",
                    "website/content/tools/keep.md",
                ]

                with patch("scripts.validate_contract.find_touched_tools") as mock_find:
                    mock_find.return_value = [
                        {"week_id": "10-K", "item_name": "Keep", "slug": "keep"}
                    ]

                    errs = validate_lifecycle_transitions(diff_files, ref="origin/main", repo_root=tmp_path)
                    assert len(errs) == 1
                    assert "Tool page markdown 'website/content/tools/keep.md' cannot be created in 'first_pass'" in errs[0][4]
