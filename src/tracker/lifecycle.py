"""Lifecycle State Machine and Transition Validator for CNCF Content Pipeline.

Defines the 4 lifecycle stages:
  1. initial: Seeded from category YAML, research: pending, content: pending.
  2. first_pass: Raw research notes gathered, research: completed, content: pending.
  3. tech_writing: Hugo tool page generated/written, content: completed.
  4. approved: Editorial review passed, source quotes verified, editorial_lock: true.

Enforces transition validity across git diffs to prevent skipping stages (e.g. initial -> tech_writing).
"""

from __future__ import annotations

import re
import subprocess
import yaml
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Re-use sanitize_for_filename logic
_FILENAME_SANITIZE_PATTERN = re.compile(r"[^a-z0-9_-]+")


def sanitize_for_filename(name: str) -> str:
    """Normalize a project name to snake_case filename slug."""
    s = name.strip().lower()
    s = s.replace(" ", "_")
    s = s.replace(".", "_")
    s = _FILENAME_SANITIZE_PATTERN.sub("", s)
    return s


class LifecycleStage(str, Enum):
    """The 4 formal stages of a tool's content lifecycle."""
    INITIAL = "initial"
    FIRST_PASS = "first_pass"
    TECH_WRITING = "tech_writing"
    APPROVED = "approved"


# Allowed state transitions: from_stage -> set of allowed to_stages
ALLOWED_TRANSITIONS: Dict[LifecycleStage, Set[LifecycleStage]] = {
    LifecycleStage.INITIAL: {
        LifecycleStage.INITIAL,
        LifecycleStage.FIRST_PASS,
    },
    LifecycleStage.FIRST_PASS: {
        LifecycleStage.FIRST_PASS,
        LifecycleStage.TECH_WRITING,
    },
    LifecycleStage.TECH_WRITING: {
        LifecycleStage.TECH_WRITING,
        LifecycleStage.APPROVED,
        LifecycleStage.FIRST_PASS,  # Re-researching if content rejected
    },
    LifecycleStage.APPROVED: {
        LifecycleStage.APPROVED,
        LifecycleStage.TECH_WRITING,  # Unlocked for curation update
        LifecycleStage.FIRST_PASS,   # Unlocked for full re-research
    },
}


def determine_lifecycle_stage(
    item_tracker: Optional[Dict[str, Any]] = None,
    research_data: Optional[Dict[str, Any]] = None,
    tool_frontmatter: Optional[Dict[str, Any]] = None,
) -> LifecycleStage:
    """Determine the lifecycle stage for a tool from its research, tracker, and frontmatter.

    Precedence:
    1. 'approved': editorial_lock is True in research YAML or frontmatter.
    2. 'tech_writing': content task is completed in tracker, or frontmatter stage is tech_writing.
    3. 'first_pass': research task is completed in tracker, or research YAML has substantive content.
    4. 'initial': default initial seed state.
    """
    # 1. Check for editorial lock / approved status
    if research_data and research_data.get("editorial_lock", False):
        return LifecycleStage.APPROVED
    if tool_frontmatter and tool_frontmatter.get("lifecycle_stage") == LifecycleStage.APPROVED.value:
        return LifecycleStage.APPROVED

    # 2. Check tracker tasks
    if item_tracker:
        tasks = item_tracker.get("tasks", {})
        content_task = tasks.get("content", {})
        research_task = tasks.get("research", {})

        if content_task.get("status") == "completed":
            return LifecycleStage.TECH_WRITING
        if research_task.get("status") == "completed":
            return LifecycleStage.FIRST_PASS

    # 3. Check tool page frontmatter
    if tool_frontmatter:
        stage_str = tool_frontmatter.get("lifecycle_stage")
        if stage_str == LifecycleStage.TECH_WRITING.value:
            return LifecycleStage.TECH_WRITING
        if stage_str == LifecycleStage.FIRST_PASS.value:
            return LifecycleStage.FIRST_PASS

    # 4. Check research YAML substantive content
    if research_data:
        has_summary = bool(research_data.get("summary"))
        has_features = bool(research_data.get("key_features"))
        if has_summary or has_features:
            return LifecycleStage.FIRST_PASS

    return LifecycleStage.INITIAL


def validate_transition(
    from_stage: LifecycleStage | str,
    to_stage: LifecycleStage | str,
    allow_same: bool = True,
) -> Tuple[bool, str]:
    """Validate a lifecycle transition from from_stage to to_stage.

    Returns:
        (is_valid, error_message)
    """
    if isinstance(from_stage, str):
        try:
            from_stage = LifecycleStage(from_stage)
        except ValueError:
            return False, f"Invalid source stage '{from_stage}'"

    if isinstance(to_stage, str):
        try:
            to_stage = LifecycleStage(to_stage)
        except ValueError:
            return False, f"Invalid target stage '{to_stage}'"

    if from_stage == to_stage:
        if not allow_same:
            return False, f"Stage did not change from '{from_stage.value}'."
        return True, ""

    allowed = ALLOWED_TRANSITIONS.get(from_stage, set())
    if to_stage in allowed:
        return True, ""

    # Specific informative error messages for illegal skips
    if from_stage == LifecycleStage.INITIAL and to_stage in (LifecycleStage.TECH_WRITING, LifecycleStage.APPROVED):
        return False, (
            f"Illegal lifecycle skip: Cannot transition directly from '{from_stage.value}' to '{to_stage.value}'. "
            f"Tools must first pass through '{LifecycleStage.FIRST_PASS.value}' (research gathering and validation) "
            f"in a dedicated PR before creating content or tool pages."
        )

    if from_stage == LifecycleStage.FIRST_PASS and to_stage == LifecycleStage.APPROVED:
        return False, (
            f"Illegal lifecycle skip: Cannot transition directly from '{from_stage.value}' to '{to_stage.value}'. "
            f"Content must first be written and reviewed in '{LifecycleStage.TECH_WRITING.value}' "
            f"before receiving editorial approval."
        )

    return False, f"Illegal lifecycle transition: '{from_stage.value}' -> '{to_stage.value}' is not permitted."


def parse_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Parse YAML frontmatter from a Markdown file string."""
    if not content.startswith("---"):
        return None
    match = re.search(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def read_file_from_git_ref(ref: str, rel_path: str, repo_root: Path) -> Optional[str]:
    """Read a file's content at a git ref using git show."""
    try:
        cmd = ["git", "show", f"{ref}:{rel_path}"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False, cwd=repo_root)
        if res.returncode == 0:
            return res.stdout
        return None
    except Exception:
        return None


def get_tool_stage_at_git_ref(
    ref: str,
    week_id: str,
    item_name: str,
    slug: str,
    repo_root: Path,
) -> LifecycleStage:
    """Determine the lifecycle stage of a tool as it existed at a git ref."""
    # Read research file
    research_rel = f"data/weeks/{week_id}/research/{slug}.yaml"
    research_content = read_file_from_git_ref(ref, research_rel, repo_root)
    research_data = None
    if research_content:
        try:
            research_data = yaml.safe_load(research_content)
        except Exception:
            pass

    # Read tracker file
    tracker_rel = f"data/weeks/{week_id}/tracker.yaml"
    tracker_content = read_file_from_git_ref(ref, tracker_rel, repo_root)
    item_tracker = None
    if tracker_content:
        try:
            tracker_data = yaml.safe_load(tracker_content)
            if isinstance(tracker_data, dict):
                items = tracker_data.get("items", {})
                if item_name in items:
                    item_tracker = items[item_name]
                else:
                    # Match by slug
                    for k, v in items.items():
                        if sanitize_for_filename(k) == slug:
                            item_tracker = v
                            break
        except Exception:
            pass

    # Read tool page markdown
    tool_page_rel = f"website/content/tools/{slug}.md"
    tool_content = read_file_from_git_ref(ref, tool_page_rel, repo_root)
    tool_frontmatter = parse_frontmatter(tool_content) if tool_content else None

    return determine_lifecycle_stage(
        item_tracker=item_tracker,
        research_data=research_data,
        tool_frontmatter=tool_frontmatter,
    )


def get_tool_stage_in_working_tree(
    week_id: str,
    item_name: str,
    slug: str,
    repo_root: Path,
) -> LifecycleStage:
    """Determine the lifecycle stage of a tool currently in the working tree."""
    research_path = repo_root / "data" / "weeks" / week_id / "research" / f"{slug}.yaml"
    research_data = None
    if research_path.is_file():
        try:
            with open(research_path, "r", encoding="utf-8") as f:
                research_data = yaml.safe_load(f)
        except Exception:
            pass

    tracker_path = repo_root / "data" / "weeks" / week_id / "tracker.yaml"
    item_tracker = None
    if tracker_path.is_file():
        try:
            with open(tracker_path, "r", encoding="utf-8") as f:
                tracker_data = yaml.safe_load(f)
            if isinstance(tracker_data, dict):
                items = tracker_data.get("items", {})
                if item_name in items:
                    item_tracker = items[item_name]
                else:
                    for k, v in items.items():
                        if sanitize_for_filename(k) == slug:
                            item_tracker = v
                            break
        except Exception:
            pass

    tool_page_path = repo_root / "website" / "content" / "tools" / f"{slug}.md"
    tool_frontmatter = None
    if tool_page_path.is_file():
        try:
            with open(tool_page_path, "r", encoding="utf-8") as f:
                tool_frontmatter = parse_frontmatter(f.read())
        except Exception:
            pass

    return determine_lifecycle_stage(
        item_tracker=item_tracker,
        research_data=research_data,
        tool_frontmatter=tool_frontmatter,
    )


def find_touched_tools(
    diff_files: List[str],
    repo_root: Path,
    ref: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Inspect changed files relative to ref and identify all touched tools.

    Returns list of dicts: [{"week_id": ..., "item_name": ..., "slug": ...}]
    """
    touched: Dict[Tuple[str, str], Dict[str, str]] = {}

    def _register(week_id: str, item_name: str, slug: str):
        key = (week_id, slug)
        if key not in touched:
            touched[key] = {
                "week_id": week_id,
                "item_name": item_name,
                "slug": slug,
            }

    # Preload all known items across weeks to resolve names/slugs
    slug_to_item: Dict[str, Tuple[str, str]] = {}  # slug -> (week_id, item_name)
    for cat_file in (repo_root / "data" / "weeks").glob("*/categories/*.yaml"):
        week_id = cat_file.parent.parent.name
        try:
            with open(cat_file, "r", encoding="utf-8") as f:
                items = yaml.safe_load(f)
            if isinstance(items, list):
                for it in items:
                    name = it.get("name")
                    if name:
                        sl = sanitize_for_filename(name)
                        slug_to_item[sl] = (week_id, name)
        except Exception:
            pass

    for path_str in diff_files:
        p = Path(path_str)
        try:
            rel = str(p.relative_to(repo_root) if p.is_absolute() else p)
        except ValueError:
            rel = str(p)

        # 1. Research file changed
        m_res = re.match(r"^data/weeks/([^/]+)/research/(.+)\.yaml$", rel)
        if m_res:
            week_id = m_res.group(1)
            slug = m_res.group(2)
            item_name = slug_to_item.get(slug, (week_id, slug))[1]
            _register(week_id, item_name, slug)
            continue

        # 2. Tool markdown page changed
        m_tool = re.match(r"^website/content/tools/(.+)\.md$", rel)
        if m_tool and not rel.endswith("_index.md"):
            slug = m_tool.group(1)
            if slug in slug_to_item:
                week_id, item_name = slug_to_item[slug]
                _register(week_id, item_name, slug)
            continue

        # 3. Tracker YAML changed
        m_track = re.match(r"^data/weeks/([^/]+)/tracker\.yaml$", rel)
        if m_track:
            week_id = m_track.group(1)
            # Compare current tracker with tracker at git ref to detect modified items
            curr_tracker_file = repo_root / rel
            curr_items = {}
            if curr_tracker_file.is_file():
                try:
                    with open(curr_tracker_file, "r", encoding="utf-8") as f:
                        curr_data = yaml.safe_load(f)
                    if isinstance(curr_data, dict):
                        curr_items = curr_data.get("items", {})
                except Exception:
                    pass

            ref_items = {}
            if ref:
                ref_content = read_file_from_git_ref(ref, rel, repo_root)
                if ref_content:
                    try:
                        ref_data = yaml.safe_load(ref_content)
                        if isinstance(ref_data, dict):
                            ref_items = ref_data.get("items", {})
                    except Exception:
                        pass

            # Detect any item whose tasks changed between ref and current
            all_item_keys = set(curr_items.keys()) | set(ref_items.keys())
            for item_k in all_item_keys:
                c_item = curr_items.get(item_k)
                r_item = ref_items.get(item_k)
                if c_item != r_item:
                    slug = sanitize_for_filename(item_k)
                    _register(week_id, item_k, slug)

    return list(touched.values())
