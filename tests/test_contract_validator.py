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
        "sources": [{"label": "GitHub", "url": "https://github.com/test/test"}],
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
