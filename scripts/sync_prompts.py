#!/usr/bin/env python3
"""Synchronize and compile prompt artifacts across .agents/skills and .github/prompts."""

import sys
from pathlib import Path

# Add repo root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agentic.prompts import (
    CONTENT_MANAGER_SYSTEM_PROMPT,
    EDITOR_SYSTEM_PROMPT,
    JULES_SYSTEM_PROMPT,
    RESEARCHER_SYSTEM_PROMPT,
    WRITER_SYSTEM_PROMPT,
)

GITHUB_PROMPTS_DIR = Path(".github/prompts")


def sync_prompts():
    GITHUB_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

    files_map = {
        GITHUB_PROMPTS_DIR / "content_manager.md": CONTENT_MANAGER_SYSTEM_PROMPT,
        GITHUB_PROMPTS_DIR / "researcher.md": RESEARCHER_SYSTEM_PROMPT,
        GITHUB_PROMPTS_DIR / "writer.md": WRITER_SYSTEM_PROMPT,
        GITHUB_PROMPTS_DIR / "editor.md": EDITOR_SYSTEM_PROMPT,
        GITHUB_PROMPTS_DIR / "jules_prompt.md": JULES_SYSTEM_PROMPT,
    }

    for path, content in files_map.items():
        path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"Synchronized {path}")


if __name__ == "__main__":
    sync_prompts()
