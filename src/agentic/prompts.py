"""Centralized system prompts loaded directly from canonical skill definitions (.agents/skills)."""

from pathlib import Path
from typing import Optional

PROMPTS_DIR = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "cncf-weekly-content" / "prompts"


def load_prompt(filename: str, fallback: Optional[str] = None) -> str:
    """Load prompt from canonical markdown file with fallback."""
    prompt_path = PROMPTS_DIR / filename
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8").strip()
    if fallback is not None:
        return fallback.strip()
    raise FileNotFoundError(f"Prompt file not found: {prompt_path}")


CONTENT_MANAGER_SYSTEM_PROMPT = load_prompt("content_manager.md")
EDITOR_SYSTEM_PROMPT = load_prompt("editor.md")
RESEARCHER_SYSTEM_PROMPT = load_prompt("researcher.md")
WRITER_SYSTEM_PROMPT = load_prompt("writer.md")
JULES_SYSTEM_PROMPT = load_prompt("jules.md")
