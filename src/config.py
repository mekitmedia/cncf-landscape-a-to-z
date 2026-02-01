from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import os
import tempfile

import yaml


def _repo_root() -> Path:
    """Return the repository root (one level above src/)."""
    return Path(__file__).resolve().parents[1]


def _is_test_environment() -> bool:
    """Detect if we're running in a test environment."""
    return (
        os.getenv('PYTEST_CURRENT_TEST') is not None or
        'pytest' in os.environ.get('_', '') or
        os.getenv('TESTING') == '1'
    )


def _get_test_data_dir() -> Path:
    """Get a temporary directory for test data."""
    test_dir = os.getenv('TEST_DATA_DIR')
    if test_dir:
        return Path(test_dir)
    
    # Create a temp directory that persists for the test session
    temp_base = Path(tempfile.gettempdir()) / 'cncf-landscape-test-data'
    temp_base.mkdir(exist_ok=True)
    return temp_base


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
    agents: Dict[str, Any]


class Config:
    """Configuration class that builds paths from a root directory."""
    
    def __init__(self, root_path: Path, config_overrides: Optional[Dict[str, Any]] = None):
        self.root = root_path
        self.config_overrides = config_overrides or {}
        
        # Load config.yaml if present
        config_path = root_path / "config.yaml"
        self.yaml_config = _load_yaml_config(config_path)
        
        # Merge with overrides
        self._config = {**self.yaml_config, **self.config_overrides}
    
    @property
    def repo_root(self) -> Path:
        return self.root
    
    @property
    def data_dir(self) -> Path:
        path = _get_nested(self._config, ["paths", "data_dir"], "data")
        return self.root / path if not Path(path).is_absolute() else Path(path)
    
    @property
    def index_dir(self) -> Path:
        return self.data_dir / "index"
    
    @property
    def stats_dir(self) -> Path:
        return self.data_dir / "stats"
    
    @property
    def extras_dir(self) -> Path:
        return self.data_dir / "extras"
    
    @property
    def weeks_dir(self) -> Path:
        return self.data_dir / "weeks"
    
    @property
    def website_dir(self) -> Path:
        path = _get_nested(self._config, ["paths", "website_dir"], "website")
        return self.root / path if not Path(path).is_absolute() else Path(path)
    
    @property
    def hugo_content_dir(self) -> Path:
        return self.website_dir / "content"
    
    @property
    def hugo_posts_dir(self) -> Path:
        return self.hugo_content_dir / "posts"
    
    @property
    def hugo_letters_dir(self) -> Path:
        return self.hugo_content_dir / "letters"
    
    @property
    def hugo_tools_dir(self) -> Path:
        return self.hugo_content_dir / "tools"
    
    @property
    def templates_dir(self) -> Path:
        path = _get_nested(self._config, ["paths", "templates_dir"], "src/templates")
        return self.root / path if not Path(path).is_absolute() else Path(path)
    
    @property
    def todo_path(self) -> Path:
        path = _get_nested(self._config, ["paths", "todo_path"], "TODO.md")
        return self.root / path if not Path(path).is_absolute() else Path(path)
    
    @property
    def landscape_source(self) -> str:
        return _get_nested(
            self._config,
            ["urls", "landscape_source"],
            "https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml",
        )

    @property
    def agents(self) -> Dict[str, Any]:
        return _get_nested(self._config, ["agents"], {})
    
    def to_app_config(self) -> AppConfig:
        """Convert to the legacy AppConfig dataclass for backward compatibility."""
        return AppConfig(
            repo_root=self.repo_root,
            data_dir=self.data_dir,
            index_dir=self.index_dir,
            stats_dir=self.stats_dir,
            extras_dir=self.extras_dir,
            weeks_dir=self.weeks_dir,
            website_dir=self.website_dir,
            hugo_content_dir=self.hugo_content_dir,
            hugo_posts_dir=self.hugo_posts_dir,
            hugo_letters_dir=self.hugo_letters_dir,
            hugo_tools_dir=self.hugo_tools_dir,
            templates_dir=self.templates_dir,
            todo_path=self.todo_path,
            landscape_source=self.landscape_source,
            agents=self.agents,
        )


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
    
    # Use test data directory if in test environment
    if _is_test_environment():
        test_data_dir = _get_test_data_dir()
        config = Config(root, {
            "paths": {
                "data_dir": str(test_data_dir / "data"),
                "website_dir": str(test_data_dir / "website"),
                "templates_dir": "src/templates",  # Keep templates from source
                "todo_path": str(test_data_dir / "TODO.md")
            }
        })
    else:
        config = Config(root)

    _CONFIG = config.to_app_config()
    return _CONFIG


def clear_config_cache():
    """Clear the cached config (useful for tests)."""
    global _CONFIG
    _CONFIG = None


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