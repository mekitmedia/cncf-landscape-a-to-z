#!/usr/bin/env python3
"""Smart Contract Validator CLI.

Validates research YAML files, tracker YAML files, and blog post Markdown files
against Pydantic models and contract requirements. Designed to be run via pre-commit,
CI workflows, or CLI.
"""

import sys
import os
import glob
import re
import argparse
import subprocess
import yaml
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Add repository root to path for module imports
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.agentic.models import ResearchOutput
from src.tracker.models import WeekTracker
from src.tracker.lifecycle import (
    LifecycleStage,
    determine_lifecycle_stage,
    validate_transition,
    find_touched_tools,
    get_tool_stage_at_git_ref,
    get_tool_stage_in_working_tree,
    sanitize_for_filename,
)


def validate_lifecycle_transitions(
    diff_files: List[str],
    ref: str,
    repo_root: Path = REPO_ROOT,
) -> List[Tuple[str, str, str, str, str]]:
    """Validate that lifecycle stage transitions for all touched tools in diff_files are valid.

    Returns:
        List of (item_name, week_id, from_stage, to_stage, error_message)
    """
    errors: List[Tuple[str, str, str, str, str]] = []

    # Check if git ref exists
    try:
        cmd = ["git", "rev-parse", "--verify", ref]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False, cwd=repo_root)
        if res.returncode != 0:
            print(f"Warning: Git ref '{ref}' could not be resolved. Skipping lifecycle transition check.", file=sys.stderr)
            return []
    except Exception as e:
        print(f"Warning: Error resolving git ref '{ref}': {e}", file=sys.stderr)
        return []

    touched_tools = find_touched_tools(diff_files, repo_root=repo_root, ref=ref)
    if not touched_tools:
        return []

    diff_file_set = set(diff_files)

    for tool in touched_tools:
        week_id = tool["week_id"]
        item_name = tool["item_name"]
        slug = tool["slug"]

        from_stage = get_tool_stage_at_git_ref(ref, week_id, item_name, slug, repo_root)
        to_stage = get_tool_stage_in_working_tree(week_id, item_name, slug, repo_root)

        is_valid, msg = validate_transition(from_stage, to_stage, allow_same=True)
        if not is_valid:
            errors.append((item_name, week_id, from_stage.value, to_stage.value, msg))
            continue

        # Invariant check: In first_pass (research stage), tool page markdown must NOT be created from initial
        if to_stage == LifecycleStage.FIRST_PASS and from_stage == LifecycleStage.INITIAL:
            tool_page_rel = f"website/content/tools/{slug}.md"
            if tool_page_rel in diff_file_set and (repo_root / tool_page_rel).is_file():
                errors.append((
                    item_name,
                    week_id,
                    from_stage.value,
                    to_stage.value,
                    f"Tool page markdown '{tool_page_rel}' cannot be created in 'first_pass' (research stage). "
                    f"Tool page creation belongs to the subsequent 'tech_writing' stage in a follow-up PR.",
                ))

    return errors


def get_git_diff_files(ref: str) -> List[str]:
    """Get list of changed files relative to a git ref."""
    try:
        cmd = ["git", "diff", "--name-only", "--diff-filter=ACMRT", ref]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=REPO_ROOT)
        return [f.strip() for f in res.stdout.splitlines() if f.strip()]
    except Exception as e:
        print(f"Warning: Could not get git diff against '{ref}': {e}", file=sys.stderr)
        return []


def validate_research_file(file_path: Path) -> Tuple[bool, str]:
    """Validate a research YAML file against ResearchOutput Pydantic model."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            return False, f"YAML content must be a dictionary, got {type(data).__name__}"

        # Validate using Pydantic model
        ResearchOutput.model_validate(data)
        return True, ""
    except Exception as e:
        return False, str(e)


def validate_tracker_file(file_path: Path) -> Tuple[bool, str]:
    """Validate a tracker YAML file against WeekTracker Pydantic model."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not isinstance(data, dict):
            return False, f"YAML content must be a dictionary, got {type(data).__name__}"

        WeekTracker.model_validate(data)
        return True, ""
    except Exception as e:
        return False, str(e)


def validate_blog_post_file(file_path: Path) -> Tuple[bool, str]:
    """Validate a Hugo blog post Markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            return False, "Post must start with Hugo frontmatter delimiter '---'"

        frontmatter_match = re.search(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
        if not frontmatter_match:
            return False, "Invalid or unclosed Hugo frontmatter block ('---')"

        fm_text = frontmatter_match.group(1)
        fm_data = yaml.safe_load(fm_text)

        if not isinstance(fm_data, dict):
            return False, "Frontmatter YAML is not a valid key-value mapping"

        if "title" not in fm_data:
            return False, "Missing 'title' in frontmatter"
        if "date" not in fm_data:
            return False, "Missing 'date' in frontmatter"
        if "draft" not in fm_data:
            return False, "Missing 'draft' status in frontmatter"

        return True, ""
    except Exception as e:
        return False, str(e)


def filter_target_files(file_paths: List[str], must_exist: bool = False) -> Tuple[List[Path], List[Path], List[Path]]:
    """Classify input files into research, tracker, and blog post lists."""
    research_files = []
    tracker_files = []
    post_files = []

    for path_str in file_paths:
        p = Path(path_str)
        if must_exist and not p.is_file():
            continue
        try:
            rel_str = str(p.relative_to(REPO_ROOT) if p.is_absolute() else p)
        except ValueError:
            rel_str = str(p)

        if re.match(r"^data/weeks/[^/]+/research/.*\.yaml$", rel_str):
            research_files.append(p)
        elif re.match(r"^data/weeks/[^/]+/tracker\.yaml$", rel_str):
            tracker_files.append(p)
        elif re.match(r"^website/content/posts/.*\.md$", rel_str) and not rel_str.endswith("_index.md"):
            post_files.append(p)

    return research_files, tracker_files, post_files


def main():
    parser = argparse.ArgumentParser(description="Validate CNCF Content workflow files against Pydantic contract.")
    parser.add_argument("files", nargs="*", help="File paths passed by pre-commit or CLI")
    parser.add_argument("--git-diff", nargs="?", const="origin/main", help="Validate files modified in git diff against ref (default: origin/main)")
    parser.add_argument("--week", help="Validate all files for a specific week ID (e.g. 00-A)")
    parser.add_argument("--all-files", action="store_true", help="Validate all contract files in the repository")

    args = parser.parse_args()

    files_to_check: List[str] = list(args.files)
    raw_diff_files: List[str] = []

    if args.git_diff:
        raw_diff_files = get_git_diff_files(args.git_diff)
        files_to_check.extend(raw_diff_files)

    if args.week:
        week_pattern = f"data/weeks/{args.week}"
        files_to_check.extend(glob.glob(f"{week_pattern}/research/*.yaml"))
        files_to_check.extend(glob.glob(f"{week_pattern}/tracker.yaml"))
        # Check matching post(s)
        letter = args.week.split("-")[-1]
        files_to_check.extend(glob.glob(f"website/content/posts/*-{letter}*.md"))

    if args.all_files:
        files_to_check.extend(glob.glob("data/weeks/*/research/*.yaml"))
        files_to_check.extend(glob.glob("data/weeks/*/tracker.yaml"))
        files_to_check.extend(glob.glob("website/content/posts/*.md"))

    # Remove duplicates
    files_to_check = sorted(list(set(files_to_check)))

    research_files, tracker_files, post_files = filter_target_files(files_to_check, must_exist=True)

    lifecycle_errors: List[Tuple[str, str, str, str, str]] = []
    if args.git_diff and raw_diff_files:
        print(f"Contract Validator: Validating lifecycle state transitions against '{args.git_diff}'...")
        lifecycle_errors = validate_lifecycle_transitions(raw_diff_files, ref=args.git_diff, repo_root=REPO_ROOT)

    total_files = len(research_files) + len(tracker_files) + len(post_files)
    if total_files == 0 and not lifecycle_errors:
        print("Contract Validator: No research, tracker, or post files to check.")
        sys.exit(0)

    errors: List[Tuple[str, str]] = []

    if total_files > 0:
        print(f"Contract Validator: Validating {total_files} file(s) ({len(research_files)} research, {len(tracker_files)} tracker, {len(post_files)} posts)...")

        # Validate research files
        for rf in research_files:
            ok, err = validate_research_file(rf)
            if not ok:
                errors.append((str(rf), err))

        # Validate tracker files
        for tf in tracker_files:
            ok, err = validate_tracker_file(tf)
            if not ok:
                errors.append((str(tf), err))

        # Validate blog post files
        for pf in post_files:
            ok, err = validate_blog_post_file(pf)
            if not ok:
                errors.append((str(pf), err))

    has_failures = bool(errors or lifecycle_errors)

    if lifecycle_errors:
        print("\n❌ LIFECYCLE TRANSITION FAILURES:")
        for item_name, week_id, from_st, to_st, msg in lifecycle_errors:
            print(f"\n- Tool: {item_name} (Week {week_id})")
            print(f"  Transition: {from_st} ➔ {to_st}")
            print(f"  Error Details: {msg}")
            print("  Fix Guidance: Ensure lifecycle steps are not skipped. Complete 'first_pass' research in an initial PR, then generate content in 'tech_writing' in a subsequent PR.")

    if errors:
        print("\n❌ CONTRACT VALIDATION FAILURES:")
        for path_str, err_msg in errors:
            print(f"\n- File: {path_str}")
            print(f"  Error Details: {err_msg}")
            print("  Fix Guidance: Ensure the file fields match the Pydantic schema defined in src/agentic/models.py and .agents/skills/cncf-weekly-content/SKILL.md.")

    if has_failures:
        total_errs = len(errors) + len(lifecycle_errors)
        print(f"\nTotal Errors: {total_errs} (Schema: {len(errors)}, Lifecycle: {len(lifecycle_errors)}).")
        sys.exit(1)

    print(f"✅ Contract Validator: Passed all Pydantic schema and lifecycle transition checks successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()
