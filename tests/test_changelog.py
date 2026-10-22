import os
from pathlib import Path
from src.pipeline.load import build_changelog

def test_build_changelog_new(tmp_path):
    output_dir = tmp_path
    old_items = {}
    new_items = {
        "Tool A": {"name": "Tool A", "repo_url": "https://github.com/example/tool-a"},
        "Tool B": {"name": "Tool B"}
    }

    build_changelog(old_items, new_items, str(output_dir))

    changelog_path = output_dir / "changelog.md"
    assert changelog_path.exists()

    content = changelog_path.read_text()
    assert content.startswith("# Data Update Changelog")
    assert "### 🚀 Added Tools" in content
    assert "- **Tool A** ([Repo](https://github.com/example/tool-a))" in content
    assert "- **Tool B**" in content


def test_build_changelog_prepend(tmp_path):
    output_dir = tmp_path
    changelog_path = output_dir / "changelog.md"

    initial_content = """# Data Update Changelog

## [2026-01-01] Data Update

### 🚀 Added Tools

- **Old Tool** ([Repo](https://github.com/example/old-tool))
"""
    changelog_path.write_text(initial_content)

    old_items = {
        "Tool X": {"name": "Tool X", "project": "sandbox"}
    }
    new_items = {
        "Tool X": {"name": "Tool X", "project": "incubating"},
        "Tool Y": {"name": "Tool Y"}
    }

    build_changelog(old_items, new_items, str(output_dir))

    content = changelog_path.read_text()
    assert content.startswith("# Data Update Changelog")
    assert "## [" in content
    assert "### 🚀 Added Tools" in content
    assert "- **Tool Y**" in content
    assert "### 🔄 Updated Tools" in content
    assert "- **Tool X**: Status changed from **sandbox** to **incubating**" in content
    assert "## [2026-01-01] Data Update" in content
    assert "- **Old Tool**" in content

    # Check order: new update comes before old update
    new_pos = content.find("Tool Y")
    old_pos = content.find("Old Tool")
    assert new_pos < old_pos


def test_build_changelog_no_changes(tmp_path):
    output_dir = tmp_path
    old_items = {"Tool A": {"name": "Tool A", "project": "sandbox"}}
    new_items = {"Tool A": {"name": "Tool A", "project": "sandbox"}}

    build_changelog(old_items, new_items, str(output_dir))

    changelog_path = output_dir / "changelog.md"
    content = changelog_path.read_text()
    assert "_No tool changes detected in this update._" in content
