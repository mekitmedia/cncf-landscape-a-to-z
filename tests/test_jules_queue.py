import pytest
from pathlib import Path
from scripts.jules_queue import (
    list_pending_tasks,
    extract_task_title,
    resolve_prompt,
    validate_task_file,
    get_repo_root,
)


def test_list_pending_tasks_sorting(tmp_path):
    tasks_dir = tmp_path / ".github" / "prompts" / "tasks"
    tasks_dir.mkdir(parents=True)
    
    # Create tasks out of order
    (tasks_dir / "03_c.md").write_text("# Task 03: Task C\n## Objective\n...", encoding="utf-8")
    (tasks_dir / "01_a.md").write_text("# Task 01: Task A\n## Objective\n...", encoding="utf-8")
    (tasks_dir / "02_b.md").write_text("# Task 02: Task B\n## Objective\n...", encoding="utf-8")
    (tasks_dir / "ignored.txt").write_text("not a markdown file", encoding="utf-8")

    tasks = list_pending_tasks(tmp_path)
    names = [t.name for t in tasks]
    assert names == ["01_a.md", "02_b.md", "03_c.md"]


def test_extract_task_title(tmp_path):
    task_file = tmp_path / "01_sample.md"
    task_file.write_text("# Task 01: Implement Core Feature\n\nSome body text", encoding="utf-8")
    
    assert extract_task_title(task_file) == "Task 01: Implement Core Feature"


def test_resolve_prompt_custom_override(tmp_path):
    custom = "Perform specific prompt override directly."
    prompt, source_type, source_ref = resolve_prompt(custom_prompt=custom, repo_root=tmp_path)
    
    assert prompt == custom
    assert source_type == "custom"
    assert source_ref is None


def test_resolve_prompt_from_backlog(tmp_path):
    tasks_dir = tmp_path / ".github" / "prompts" / "tasks"
    tasks_dir.mkdir(parents=True)
    
    (tasks_dir / "02_second.md").write_text("Second prompt content", encoding="utf-8")
    (tasks_dir / "01_first.md").write_text("First prompt content", encoding="utf-8")

    prompt, source_type, source_ref = resolve_prompt(repo_root=tmp_path)
    assert prompt == "First prompt content"
    assert source_type == "backlog_task"
    assert source_ref == "01_first.md"


def test_resolve_prompt_fallback_to_default(tmp_path):
    prompts_dir = tmp_path / ".github" / "prompts"
    prompts_dir.mkdir(parents=True)
    default_file = prompts_dir / "jules_prompt.md"
    default_file.write_text("Default weekly research prompt", encoding="utf-8")

    prompt, source_type, source_ref = resolve_prompt(repo_root=tmp_path, allow_roulette=False)
    assert prompt == "Default weekly research prompt"
    assert source_type == "default_fallback"
    assert source_ref == "jules_prompt.md"


def test_resolve_prompt_roulette_draw(tmp_path):
    prompt, source_type, source_ref = resolve_prompt(repo_root=tmp_path, allow_roulette=True)
    assert prompt is not None
    assert source_type.startswith("roulette_")
    assert source_ref is not None



def test_validate_task_file_valid(tmp_path):
    task_file = tmp_path / "01_valid.md"
    task_file.write_text(
        """# Task 01: Test Valid Task
## Objective
Do something meaningful.

## Technical Specifications
### File: src/test.py
def foo(): pass

## Execution Steps
1. Run step.
2. Self-cleaning: Delete this task file before PR.
""",
        encoding="utf-8",
    )
    errors = validate_task_file(task_file)
    assert errors == []


def test_validate_task_file_invalid(tmp_path):
    task_file = tmp_path / "01_invalid.md"
    task_file.write_text("Just some random text without headers", encoding="utf-8")
    errors = validate_task_file(task_file)
    assert len(errors) > 0
    assert any("missing '## Objective'" in e for e in errors)
    assert any("missing self-cleaning" in e for e in errors)
