#!/usr/bin/env python3
"""
Generate individual tool pages from research YAML files.
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
                                cache[name] = item
            except Exception:
                continue
    return cache


def get_cncf_status_from_etl(project_name: str) -> str:
    """Try to find CNCF status from ETL output files."""
    cache = _get_project_data_cache()
    if project_name in cache:
        return cache[project_name].get("project", "sandbox")
    return "sandbox"


def _get_project_urls(project_name: str) -> dict:
    cache = _get_project_data_cache()
    urls = {}
    if project_name in cache:
        item = cache[project_name]
        if item.get("repo_url"):
            urls["repo_url"] = item["repo_url"]
        if item.get("homepage_url"):
            urls["homepage_url"] = item["homepage_url"]
    return urls


def generate_tool_page(research_file: Path, week_id_value: str) -> Optional[str]:
    """
    Generate a tool page from a research YAML file.
    """
    try:
        with research_file.open("r", encoding="utf-8") as f:
            research = yaml.safe_load(f)

        if not research:
            return None

        project_name = research.get("project_name", research_file.stem)
        letter = letter_from_week_id(week_id_value)
        cncf_status = get_cncf_status_from_etl(project_name)

        front_matter = {
            "title": project_name,
            "project_name": project_name,
            "letter": letter,
            "cncf_status": cncf_status,
            "layout": "single",
            "date": datetime.now().isoformat(),
        }

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

        front_matter.update(_get_project_urls(project_name))

        front_matter_yaml = yaml.dump(
            front_matter, default_flow_style=False, allow_unicode=True
        )

        content = f"""---
{front_matter_yaml}---

This is an auto-generated tool page. For more details, see the [letter page](/letters/{letter}/).
"""

        return content

    except Exception as exc:
        print(f"Error processing {research_file}: {exc}")
        return None


def generate_tool_pages() -> int:
    """Generate all tool pages from research files."""
    cfg = load_config()
    tools_content_dir = cfg.hugo_tools_dir
    tools_content_dir.mkdir(parents=True, exist_ok=True)

    generated_count = 0
    skipped_count = 0

    for week_dir in _get_week_dirs(cfg):
        week_id_value = week_dir.name
        research_dir = week_dir / "research"
        if not research_dir.exists():
            continue
        for research_file in research_dir.glob("*.yaml"):
            page_content = generate_tool_page(research_file, week_id_value)
            if page_content:
                output_file = tools_content_dir / f"{research_file.stem}.md"
                with output_file.open("w", encoding="utf-8") as f:
                    f.write(page_content)
                print(f"✓ Generated {output_file}")
                generated_count += 1
            else:
                print(f"⊘ Skipped {research_file}")
                skipped_count += 1

    print(f"\nGenerated: {generated_count} tool pages")
    print(f"Skipped: {skipped_count} tool pages")
    return generated_count


if __name__ == "__main__":
    generate_tool_pages()
