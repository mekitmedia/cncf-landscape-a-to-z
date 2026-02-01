from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def _repo_root() -> Path:
    """Return the repository root (one level above src/)."""
    return Path(__file__).resolve().parents[1]


def _load_yaml_config(path: Path) -> Dict[str, Any]:
    """Load config.yaml if present; return empty config otherwise."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _get_nested(config: Dict[str, Any], keys: list[str], default: Any) -> Any:
    """Safely read nested keys from a dict with a default fallback."""
    current: Any = config
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


@dataclass(frozen=True)
class AppConfig:
    """Resolved configuration for paths and URLs used across ETL/agentic/website."""
    repo_root: Path
    data_dir: Path
    index_dir: Path
    stats_dir: Path
    extras_dir: Path
    weeks_dir: Path
    website_dir: Path
    hugo_content_dir: Path
    hugo_posts_dir: Path
    hugo_letters_dir: Path
    hugo_tools_dir: Path
    templates_dir: Path
    todo_path: Path
    landscape_source: str


_CONFIG: Optional[AppConfig] = None


def load_config() -> AppConfig:
        """Load config.yaml overrides and memoize the resolved AppConfig.

        config.yaml (optional) structure:

        paths:
            data_dir: data
            weeks_dir: data/weeks
            index_dir: data/index
            stats_dir: data/stats
            extras_dir: data/extras
            website_dir: website
            hugo_content_dir: website/content
            hugo_posts_dir: website/content/posts
            hugo_letters_dir: website/content/letters
            hugo_tools_dir: website/content/tools
            templates_dir: src/templates
            todo_path: TODO.md

        urls:
            landscape_source: https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml
        """
    global _CONFIG
    if _CONFIG is not None:
        return _CONFIG

    # Resolve base paths and allow overrides via config.yaml.
    root = _repo_root()
    config_path = root / "config.yaml"
    config = _load_yaml_config(config_path)

    data_dir = Path(_get_nested(config, ["paths", "data_dir"], "data"))
    weeks_dir = Path(_get_nested(config, ["paths", "weeks_dir"], data_dir / "weeks"))
    index_dir = Path(_get_nested(config, ["paths", "index_dir"], data_dir / "index"))
    stats_dir = Path(_get_nested(config, ["paths", "stats_dir"], data_dir / "stats"))
    extras_dir = Path(_get_nested(config, ["paths", "extras_dir"], data_dir / "extras"))

    website_dir = Path(_get_nested(config, ["paths", "website_dir"], "website"))
    hugo_content_dir = Path(
        _get_nested(config, ["paths", "hugo_content_dir"], website_dir / "content")
    )
    hugo_posts_dir = Path(
        _get_nested(config, ["paths", "hugo_posts_dir"], hugo_content_dir / "posts")
    )
    hugo_letters_dir = Path(
        _get_nested(config, ["paths", "hugo_letters_dir"], hugo_content_dir / "letters")
    )
    hugo_tools_dir = Path(
        _get_nested(config, ["paths", "hugo_tools_dir"], hugo_content_dir / "tools")
    )

    templates_dir = Path(_get_nested(config, ["paths", "templates_dir"], "src/templates"))
    todo_path = Path(_get_nested(config, ["paths", "todo_path"], "TODO.md"))

    # Upstream CNCF landscape URL (overridable).
    landscape_source = _get_nested(
        config,
        ["urls", "landscape_source"],
        "https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml",
    )

    _CONFIG = AppConfig(
        repo_root=root,
        data_dir=data_dir,
        index_dir=index_dir,
        stats_dir=stats_dir,
        extras_dir=extras_dir,
        weeks_dir=weeks_dir,
        website_dir=website_dir,
        hugo_content_dir=hugo_content_dir,
        hugo_posts_dir=hugo_posts_dir,
        hugo_letters_dir=hugo_letters_dir,
        hugo_tools_dir=hugo_tools_dir,
        templates_dir=templates_dir,
        todo_path=todo_path,
        landscape_source=landscape_source,
    )
    return _CONFIG


def resolve_data_dirs(output_dir: Optional[str] = None) -> Dict[str, Path]:
    """Return consistent data output directories for ETL runs.

    If output_dir is provided, use it as the root for a full data tree.
    Otherwise, use the configured data directories.
    """
    if output_dir:
        base = Path(output_dir)
        return {
            "data": base,
            "index": base / "index",
            "stats": base / "stats",
            "extras": base / "extras",
            "weeks": base / "weeks",
        }

    cfg = load_config()
    return {
        "data": cfg.data_dir,
        "index": cfg.index_dir,
        "stats": cfg.stats_dir,
        "extras": cfg.extras_dir,
        "weeks": cfg.weeks_dir,
    }


def week_id(letter: str) -> str:
    """Convert a letter to the week folder name (e.g. A -> 00-A)."""
    idx = ord(letter.upper()) - ord("A")
    return f"{idx:02d}-{letter.upper()}"


def letter_from_week_id(week_id_value: str) -> str:
    """Extract the letter from a week folder name (e.g. 00-A -> A)."""
    return week_id_value.split("-")[-1]