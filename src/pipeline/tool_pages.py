#!/usr/bin/env python3
"""
Generate individual tool pages from research YAML files and category project items.
"""

from __future__ import annotations

import glob
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml

from src.config import load_config, letter_from_week_id


def sanitize_for_filename(name: str) -> str:
    """Convert project name to sanitized filename format."""
    return (
        name.lower()
        .replace(" ", "_")
        .replace("&", "and")
        .replace("/", "_")
        .replace(".", "_")
        .replace(",", "")
    )


def _get_week_dirs(cfg) -> list[Path]:
    return [Path(p) for p in glob.glob(str(cfg.weeks_dir / "*-*"))]


@lru_cache(maxsize=1)
def _get_project_data_cache() -> dict:
    cfg = load_config()
    cache = {}
    for week_dir in _get_week_dirs(cfg):
        categories_dir = week_dir / "categories"
        if not categories_dir.exists():
            continue
        for yaml_file in categories_dir.glob("*.yaml"):
            try:
                with yaml_file.open("r", encoding="utf-8") as f:
                    items = yaml.safe_load(f)
                    if items and isinstance(items, list):
                        for item in items:
                            name = item.get("name")
                            if name:
                                cache[name] = {
                                    "item": item,
                                    "week_id": week_dir.name,
                                }
            except Exception:
                continue
    return cache


def get_cncf_status_from_etl(project_name: str) -> str:
    """Try to find CNCF status from ETL output files."""
    cache = _get_project_data_cache()
    if project_name in cache:
        item = cache[project_name]["item"]
        status = item.get("project")
        if status and status not in ("null", "None", ""):
            return status
    return "non-cncf"


def _get_project_urls(project_name: str) -> dict:
    cache = _get_project_data_cache()
    urls = {}
    if project_name in cache:
        item = cache[project_name]["item"]
        if item.get("repo_url"):
            urls["repo_url"] = item["repo_url"]
        if item.get("homepage_url"):
            urls["homepage_url"] = item["homepage_url"]
    return urls


def generate_tool_pages() -> int:
    """Generate all tool pages from research files and category project items."""
    cfg = load_config()
    tools_content_dir = cfg.hugo_tools_dir
    tools_content_dir.mkdir(parents=True, exist_ok=True)

    project_cache = _get_project_data_cache()

    generated_count = 0
    skipped_count = 0

    for project_name, info in project_cache.items():
        item = info.get("item", {})
        week_id_value = info.get("week_id", "00-A")
        letter = letter_from_week_id(week_id_value)
        sanitized_name = sanitize_for_filename(project_name)

        research_file = cfg.weeks_dir / week_id_value / "research" / f"{sanitized_name}.yaml"

        cncf_status = item.get("project")
        if not cncf_status or str(cncf_status).lower() in ("null", "none", ""):
            cncf_status = "non-cncf"

        front_matter = {
            "title": project_name,
            "project_name": project_name,
            "letter": letter,
            "cncf_status": cncf_status,
            "layout": "single",
            "date": datetime.now().isoformat(),
        }

        if item.get("repo_url"):
            front_matter["repo_url"] = item["repo_url"]
        if item.get("homepage_url"):
            front_matter["homepage_url"] = item["homepage_url"]
        if item.get("description"):
            front_matter["description"] = item["description"]

        if research_file.exists():
            try:
                with research_file.open("r", encoding="utf-8") as f:
                    research = yaml.safe_load(f)
                if research:
                    front_matter["status"] = "completed"
                    for key in [
                        "summary",
                        "key_features",
                        "recent_updates",
                        "use_cases",
                        "interesting_facts",
                        "get_started",
                        "related_tools",
                    ]:
                        if key in research:
                            front_matter[key] = research[key]
                else:
                    front_matter["status"] = "in_progress"
                    front_matter["summary"] = item.get(
                        "description", "Research for this project is currently in progress."
                    )
            except Exception as exc:
                print(f"Error loading research file {research_file}: {exc}")
                front_matter["status"] = "in_progress"
                front_matter["summary"] = item.get(
                    "description", "Research for this project is currently in progress."
                )
        else:
            front_matter["status"] = "in_progress"
            front_matter["summary"] = item.get(
                "description", "Research for this project is currently in progress."
            )

        front_matter_yaml = yaml.dump(
            front_matter, default_flow_style=False, allow_unicode=True
        )

        content = f"""---
{front_matter_yaml}---

This is an auto-generated tool page. For more details, see the [letter page](/letters/{letter.lower()}/).
"""

        output_file = tools_content_dir / f"{sanitized_name}.md"
        try:
            with output_file.open("w", encoding="utf-8") as f:
                f.write(content)
            generated_count += 1
        except Exception as exc:
            print(f"Error writing {output_file}: {exc}")
            skipped_count += 1

    print(f"\nGenerated: {generated_count} tool pages")
    print(f"Skipped: {skipped_count} tool pages")
    return generated_count


if __name__ == "__main__":
    generate_tool_pages()
