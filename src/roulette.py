"""
Task Roulette and Dispatcher for CNCF Landscape Projects.

Provides weighted roulette selection across all landscape projects,
with support for ad-hoc priority tasks and single-task prompt generation.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
import jinja2

from src.config import load_config, letter_from_week_id
from src.pipeline.tool_pages import sanitize_for_filename


@dataclass
class ProjectCandidate:
    """A candidate project in the landscape with calculated selection weight."""
    name: str
    sanitized_name: str
    week_id: str
    week_letter: str
    category: str
    cncf_status: str
    repo_url: Optional[str] = None
    homepage_url: Optional[str] = None
    has_research: bool = False
    last_updated: Optional[datetime] = None
    weight: float = 1.0


@dataclass
class DrawnTask:
    """A task drawn by the dispatcher (via ad-hoc priority queue or roulette)."""
    task_type: str  # "adhoc" or "roulette"
    project_name: str
    sanitized_name: str
    week_id: str
    week_letter: str
    category: str
    cncf_status: str
    repo_url: Optional[str]
    homepage_url: Optional[str]
    is_refresh: bool
    weight: float
    reason: Optional[str] = None
    research_file: str = field(init=False)
    tool_page_file: str = field(init=False)
    tracker_file: str = field(init=False)

    def __post_init__(self):
        self.research_file = f"data/weeks/{self.week_id}/research/{self.sanitized_name}.yaml"
        self.tool_page_file = f"website/content/tools/{self.sanitized_name}.md"
        self.tracker_file = f"data/weeks/{self.week_id}/tracker.yaml"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_prompt(self) -> str:
        cfg = load_config()
        template_file = cfg.templates_dir / "task_prompt.md.j2"
        if template_file.exists():
            loader = jinja2.FileSystemLoader(searchpath=str(cfg.templates_dir))
            env = jinja2.Environment(loader=loader, autoescape=False)
            template = env.get_template("task_prompt.md.j2")
            return template.render(task=self)
        raise FileNotFoundError(f"Template not found at {template_file}")



def _get_project_last_updated(research_file: Path) -> Optional[datetime]:
    """Get the last updated timestamp of a research file."""
    if not research_file.exists():
        return None
    try:
        mtime = research_file.stat().st_mtime
        return datetime.fromtimestamp(mtime, tz=timezone.utc)
    except Exception:
        return None


def calculate_project_weight(
    has_research: bool,
    last_updated: Optional[datetime],
    cncf_status: str,
    now: Optional[datetime] = None,
) -> float:
    """Calculate selection weight for a project candidate."""
    if not has_research:
        return 100.0

    if now is None:
        now = datetime.now(timezone.utc)

    if last_updated is None:
        days_old = 30.0
    else:
        # Ensure last_updated is timezone-aware
        if last_updated.tzinfo is None:
            last_updated = last_updated.replace(tzinfo=timezone.utc)
        days_old = max(0.0, (now - last_updated).total_seconds() / 86400.0)

    # Base refresh weight: grows with age
    refresh_weight = max(1.0, days_old / 7.0)

    # CNCF maturity multipliers
    maturity_multipliers = {
        "graduated": 1.5,
        "incubating": 1.2,
        "sandbox": 1.0,
    }
    multiplier = maturity_multipliers.get(cncf_status.lower(), 0.9)
    return refresh_weight * multiplier


def get_all_candidates(week_letter: Optional[str] = None) -> List[ProjectCandidate]:
    """Scan the repository and return all project candidates with calculated weights."""
    cfg = load_config()
    candidates: List[ProjectCandidate] = []
    now = datetime.now(timezone.utc)

    target_letter = week_letter.upper() if week_letter else None

    # Iterate through week directories
    for week_dir in sorted(cfg.weeks_dir.glob("*-*")):
        week_id = week_dir.name
        letter = letter_from_week_id(week_id)

        if target_letter and letter != target_letter:
            continue

        categories_dir = week_dir / "categories"
        research_dir = week_dir / "research"

        if not categories_dir.exists():
            continue

        for cat_file in sorted(categories_dir.glob("*.yaml")):
            cat_name = cat_file.stem
            try:
                with cat_file.open("r", encoding="utf-8") as f:
                    items = yaml.safe_load(f)
                if not items or not isinstance(items, list):
                    continue

                for item in items:
                    name = item.get("name")
                    if not name:
                        continue

                    sanitized = sanitize_for_filename(name)
                    research_file = research_dir / f"{sanitized}.yaml"
                    has_research = research_file.exists()
                    last_updated = _get_project_last_updated(research_file) if has_research else None
                    cncf_status = item.get("project", "sandbox")

                    weight = calculate_project_weight(
                        has_research=has_research,
                        last_updated=last_updated,
                        cncf_status=cncf_status,
                        now=now,
                    )

                    candidate = ProjectCandidate(
                        name=name,
                        sanitized_name=sanitized,
                        week_id=week_id,
                        week_letter=letter,
                        category=cat_name,
                        cncf_status=cncf_status,
                        repo_url=item.get("repo_url"),
                        homepage_url=item.get("homepage_url"),
                        has_research=has_research,
                        last_updated=last_updated,
                        weight=weight,
                    )
                    candidates.append(candidate)
            except Exception:
                continue

    return candidates


def check_adhoc_tasks(week_letter: Optional[str] = None) -> Optional[DrawnTask]:
    """Check data/adhoc_tasks.yaml for pending priority tasks."""
    cfg = load_config()
    adhoc_file = cfg.data_dir / "adhoc_tasks.yaml"
    if not adhoc_file.exists():
        return None

    try:
        with adhoc_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if not data or not isinstance(data, dict):
            return None

        tasks = data.get("tasks", [])
        if not tasks or not isinstance(tasks, list):
            return None

        target_letter = week_letter.upper() if week_letter else None

        for task_entry in tasks:
            if not isinstance(task_entry, dict):
                continue
            status = task_entry.get("status", "pending")
            if status != "pending":
                continue

            project_name = task_entry.get("project_name")
            if not project_name:
                continue

            # Find this project in candidates
            all_candidates = get_all_candidates()
            for cand in all_candidates:
                if cand.name.lower() == project_name.lower():
                    if target_letter and cand.week_letter != target_letter:
                        continue
                    return DrawnTask(
                        task_type="adhoc",
                        project_name=cand.name,
                        sanitized_name=cand.sanitized_name,
                        week_id=cand.week_id,
                        week_letter=cand.week_letter,
                        category=cand.category,
                        cncf_status=cand.cncf_status,
                        repo_url=cand.repo_url,
                        homepage_url=cand.homepage_url,
                        is_refresh=cand.has_research,
                        weight=float("inf"),
                        reason=task_entry.get("reason", "Ad-hoc task queue"),
                    )
    except Exception:
        return None

    return None


def draw_task(
    week_letter: Optional[str] = None,
    seed: Optional[int] = None,
    allow_adhoc: bool = True,
) -> Optional[DrawnTask]:
    """
    Draw a task using 2-tier dispatch:
    1. Check ad-hoc priority queue
    2. Spin weighted roulette across landscape candidates
    """
    if seed is not None:
        random.seed(seed)

    # 1. Check ad-hoc queue
    if allow_adhoc:
        adhoc_task = check_adhoc_tasks(week_letter=week_letter)
        if adhoc_task:
            return adhoc_task

    # 2. Weighted roulette
    candidates = get_all_candidates(week_letter=week_letter)
    if not candidates:
        return None

    weights = [c.weight for c in candidates]
    selected: ProjectCandidate = random.choices(candidates, weights=weights, k=1)[0]

    return DrawnTask(
        task_type="roulette",
        project_name=selected.name,
        sanitized_name=selected.sanitized_name,
        week_id=selected.week_id,
        week_letter=selected.week_letter,
        category=selected.category,
        cncf_status=selected.cncf_status,
        repo_url=selected.repo_url,
        homepage_url=selected.homepage_url,
        is_refresh=selected.has_research,
        weight=selected.weight,
    )
