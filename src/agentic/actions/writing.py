import os
from datetime import datetime
from typing import List
from src.agentic.agents.writer import writer_agent
from src.agentic.models import ResearchOutput, BlogPostDraft
from src.tracker import get_tracker, TaskStatus
from src.config import load_config
from src.agentic.deps import WriterDeps

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
    full_content = f"""---
title: "{draft.title}"
date: {date_str}
draft: false
---

{draft.content_markdown}
"""

    os.makedirs(os.path.dirname(str(filename)), exist_ok=True)
    with open(filename, "w") as f:
        f.write(full_content)

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