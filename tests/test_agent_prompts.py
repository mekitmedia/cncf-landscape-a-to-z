import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set dummy key for tests to avoid instantiation errors
os.environ['GOOGLE_API_KEY'] = 'dummy_key'

from src.agentic.prompts import (
    CONTENT_MANAGER_SYSTEM_PROMPT,
    EDITOR_SYSTEM_PROMPT,
    RESEARCHER_SYSTEM_PROMPT,
    WRITER_SYSTEM_PROMPT,
    JULES_SYSTEM_PROMPT,
    PROMPTS_DIR,
)
from src.agentic.agents.editor import editor_agent
from src.agentic.agents.researcher import researcher_agent
from src.agentic.agents.writer import writer_agent


def test_prompts_directory_exists():
    assert PROMPTS_DIR.exists()
    assert (PROMPTS_DIR / "content_manager.md").exists()
    assert (PROMPTS_DIR / "editor.md").exists()
    assert (PROMPTS_DIR / "researcher.md").exists()
    assert (PROMPTS_DIR / "writer.md").exists()
    assert (PROMPTS_DIR / "jules.md").exists()


def test_prompt_constants_non_empty():
    assert len(CONTENT_MANAGER_SYSTEM_PROMPT.strip()) > 0
    assert len(EDITOR_SYSTEM_PROMPT.strip()) > 0
    assert len(RESEARCHER_SYSTEM_PROMPT.strip()) > 0
    assert len(WRITER_SYSTEM_PROMPT.strip()) > 0
    assert len(JULES_SYSTEM_PROMPT.strip()) > 0


def test_pydantic_agents_use_canonical_prompts():
    assert EDITOR_SYSTEM_PROMPT in editor_agent._system_prompts
    assert RESEARCHER_SYSTEM_PROMPT in researcher_agent._system_prompts
    assert WRITER_SYSTEM_PROMPT in writer_agent._system_prompts


def test_github_prompts_synced():
    github_prompts = Path(__file__).parent.parent / ".github" / "prompts"
    assert github_prompts.exists()
    assert (github_prompts / "content_manager.md").read_text(encoding="utf-8").strip() == CONTENT_MANAGER_SYSTEM_PROMPT
    assert (github_prompts / "editor.md").read_text(encoding="utf-8").strip() == EDITOR_SYSTEM_PROMPT
    assert (github_prompts / "researcher.md").read_text(encoding="utf-8").strip() == RESEARCHER_SYSTEM_PROMPT
    assert (github_prompts / "writer.md").read_text(encoding="utf-8").strip() == WRITER_SYSTEM_PROMPT
    assert (github_prompts / "jules_prompt.md").read_text(encoding="utf-8").strip() == JULES_SYSTEM_PROMPT
