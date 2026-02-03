import os
import asyncio
from datetime import datetime
from typing import List
from src.agentic.agents.writer import writer_agent
from src.agentic.models import ResearchOutput, BlogPostDraft
from src.tracker import get_tracker, TaskStatus
from src.config import load_config
from src.agentic.deps import WriterDeps

def _save_to_disk(filename, draft: BlogPostDraft, date_str: str):
    """Helper to save file to disk in a separate thread."""
    os.makedirs(os.path.dirname(str(filename)), exist_ok=True)
    with open(filename, "w") as f:
        f.write("---\n")
        f.write(f'title: "{draft.title}"\n')
        f.write(f"date: {date_str}\n")
        f.write("draft: false\n")
        f.write("---\n\n")
        f.write(draft.content_markdown)

async def write_weekly_post(week_letter: str, research_results: List[ResearchOutput]) -> BlogPostDraft:
    """Write a blog post for the given week based on research results."""
    cfg = load_config()
    deps = WriterDeps(research_results=research_results, week_letter=week_letter, config=cfg)
    result = await writer_agent.run(
        f"Write a blog post for CNCF projects starting with letter {week_letter}.",
        deps=deps
    )
    return result.data

async def save_post(week_letter: str, draft: BlogPostDraft):
    """Save blog post and update tracker."""
    tracker = get_tracker()

    cfg = load_config()
    year = datetime.now().year
    filename = cfg.hugo_posts_dir / f"{year}-{week_letter}.md"

    date_str = datetime.now().isoformat()

    await asyncio.to_thread(_save_to_disk, filename, draft, date_str)

    # Update tracker to mark blog post as completed
    try:
        relative_path = f"website/content/letters/{year}-{week_letter}.md"
        tracker.update_task(
            week_letter,
            None,
            "blog_post",
            TaskStatus.COMPLETED,
            output_file=relative_path
        )
    except Exception as e:
        pass
