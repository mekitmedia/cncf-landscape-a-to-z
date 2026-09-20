#!/usr/bin/env python3
"""
scripts/jules_queue.py

CLI tool for managing and inspecting the file-based task queue for Jules in .github/prompts/tasks/.
Enables local inspection, validation, and deterministic prompt resolution for CI/CD workflows.
"""

import argparse
import os
import re
import sys
import uuid
from pathlib import Path
from typing import List, Optional, Tuple


def get_repo_root() -> Path:
    """Find the root of the git repository."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists() or (current / ".github").exists():
            return current
        current = current.parent
    return Path.cwd()


def get_tasks_dir(repo_root: Optional[Path] = None) -> Path:
    root = repo_root or get_repo_root()
    return root / ".github" / "prompts" / "tasks"


def get_default_prompt_file(repo_root: Optional[Path] = None) -> Path:
    root = repo_root or get_repo_root()
    return root / ".github" / "prompts" / "jules_prompt.md"


def list_pending_tasks(repo_root: Optional[Path] = None) -> List[Path]:
    """Return sorted list of pending task files (.md) in .github/prompts/tasks/."""
    tasks_dir = get_tasks_dir(repo_root)
    if not tasks_dir.exists():
        return []
    tasks = [f for f in tasks_dir.glob("*.md") if f.is_file()]
    # Sort deterministically by filename
    return sorted(tasks, key=lambda p: p.name)


def extract_task_title(task_file: Path) -> str:
    """Extract first heading from task markdown file."""
    try:
        content = task_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return task_file.stem


def resolve_prompt(
    custom_prompt: Optional[str] = None,
    repo_root: Optional[Path] = None,
) -> Tuple[str, str, Optional[str]]:
    """
    Deterministically resolves the prompt string.

    Returns:
        Tuple of (prompt_content, source_type, task_name_or_file)
        source_type: 'custom', 'backlog_task', or 'default_fallback'
    """
    root = repo_root or get_repo_root()

    if custom_prompt and custom_prompt.strip():
        return custom_prompt.strip(), "custom", None

    tasks = list_pending_tasks(root)
    if tasks:
        selected_task = tasks[0]
        content = selected_task.read_text(encoding="utf-8").strip()
        return content, "backlog_task", selected_task.name

    default_file = get_default_prompt_file(root)
    if default_file.exists():
        content = default_file.read_text(encoding="utf-8").strip()
        return content, "default_fallback", default_file.name

    raise FileNotFoundError(f"No task files found in {get_tasks_dir(root)} and default prompt {default_file} is missing.")


def validate_task_file(task_file: Path) -> List[str]:
    """Validate that a task file adheres to the required contract."""
    errors = []
    content = task_file.read_text(encoding="utf-8")

    if not content.strip():
        return [f"{task_file.name}: file is empty"]

    # Check for title
    if not re.search(r"^#\s+Task\s+", content, re.MULTILINE) and not content.startswith("# "):
        errors.append(f"{task_file.name}: missing '# Task <...>' heading")

    # Check for Objective
    if not re.search(r"##\s+Objective", content, re.IGNORECASE):
        errors.append(f"{task_file.name}: missing '## Objective' section")

    # Check for Technical Specifications
    if not re.search(r"##\s+Technical Specifications", content, re.IGNORECASE):
        errors.append(f"{task_file.name}: missing '## Technical Specifications' section")

    # Check for Execution Steps
    if not re.search(r"##\s+Execution Steps", content, re.IGNORECASE):
        errors.append(f"{task_file.name}: missing '## Execution Steps' section")

    # Check for Self-Cleaning deletion instruction
    if "Delete this task file" not in content and "self-cleaning" not in content.lower():
        errors.append(f"{task_file.name}: missing self-cleaning deletion instruction")

    return errors


def write_to_github_output(key: str, value: str):
    """Write multiline-safe output to GITHUB_OUTPUT environment file."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return

    delimiter = f"EOF_{uuid.uuid4().hex}"
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"{key}<<{delimiter}\n{value}\n{delimiter}\n")


def cmd_list(args):
    tasks = list_pending_tasks()
    if not tasks:
        print("No pending tasks in .github/prompts/tasks/ (Queue is empty).")
        return 0

    print(f"Pending Jules Tasks ({len(tasks)} in backlog):")
    print(f"{'Idx':<4} {'File':<45} {'Title'}")
    print("-" * 80)
    for idx, task in enumerate(tasks, 1):
        title = extract_task_title(task)
        print(f"{idx:<4} {task.name:<45} {title}")
    return 0


def cmd_get_prompt(args):
    try:
        prompt, source_type, source_ref = resolve_prompt(custom_prompt=args.custom_prompt)
    except Exception as e:
        print(f"Error resolving prompt: {e}", file=sys.stderr)
        return 1

    if args.info:
        print(f"Source: {source_type} ({source_ref or 'custom input'})", file=sys.stderr)

    if args.output_file:
        Path(args.output_file).write_text(prompt, encoding="utf-8")

    if args.github_output:
        write_to_github_output("prompt", prompt)
        write_to_github_output("source_type", source_type)
        write_to_github_output("source_ref", source_ref or "")
        write_to_github_output("should_run", "true")

    if not args.output_file and not args.github_output:
        print(prompt)

    return 0


def cmd_validate(args):
    tasks = list_pending_tasks()
    if not tasks:
        print("No task files to validate.")
        return 0

    all_errors = []
    for task in tasks:
        errors = validate_task_file(task)
        all_errors.extend(errors)

    if all_errors:
        print("Task validation errors found:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"All {len(tasks)} task prompt files are valid!")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Jules Task Backlog & Prompt Resolution CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list command
    subparsers.add_parser("list", help="List all pending tasks in the backlog queue")

    # get-prompt command
    prompt_parser = subparsers.add_parser("get-prompt", help="Resolve the prompt for Jules")
    prompt_parser.add_argument("--custom-prompt", type=str, default=None, help="Optional custom prompt override")
    prompt_parser.add_argument("--output-file", type=str, default=None, help="File path to write prompt to")
    prompt_parser.add_argument("--github-output", action="store_true", help="Write outputs to GITHUB_OUTPUT")
    prompt_parser.add_argument("--info", action="store_true", help="Print resolution source info to stderr")

    # validate command
    subparsers.add_parser("validate", help="Validate task prompt files against schema")

    args = parser.parse_args()

    if args.command == "list":
        sys.exit(cmd_list(args))
    elif args.command == "get-prompt":
        sys.exit(cmd_get_prompt(args))
    elif args.command == "validate":
        sys.exit(cmd_validate(args))


if __name__ == "__main__":
    main()
