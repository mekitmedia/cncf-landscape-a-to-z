import asyncio
import os
import glob
import yaml
import logfire
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from prefect import flow, task, get_run_logger
from src.config import load_config, week_id
from src.agentic.agents.researcher import researcher_agent
from src.agentic.agents.writer import writer_agent
from src.agentic.agents.editor import editor_agent
from src.agentic.models import ResearchOutput, BlogPostDraft, NextWeekDecision, ProjectMetadata, WriterDeps
from src.tracker import get_tracker, TaskStatus

@task
@logfire.instrument
async def determine_next_week() -> NextWeekDecision:
    logger = get_run_logger()
    logger.info("Asking Editor Agent for next week...")
    # Editor agent uses tool to check file system
    result = await editor_agent.run(
        "Please decide the next week to tackle.",
    )
    logger.info(f"Editor decision: {result.data}")
    return result.data

@task
@logfire.instrument
async def get_items_for_week(letter: str, task_type: str = "research") -> List[ProjectMetadata]:
    """Get items with pending tasks for a specific week.
    
    Args:
        letter: Week letter (A-Z)
        task_type: Type of task to check (default: research)
        
    Returns:
        List of ProjectMetadata for items with pending tasks
    """
    logger = get_run_logger()
    logger.info(f"Getting items for letter {letter} with pending '{task_type}' tasks")

    # Get tracker instance
    tracker = get_tracker()
    
    # Check if tracker exists for this week
    if not tracker.tracker_exists(letter):
        logger.warning(f"No tracker found for week {letter}. ETL may not have run yet.")
        return []
    
    # Get pending items from tracker
    pending_item_names = tracker.get_pending_items(letter, task_type)
    
    if not pending_item_names:
        logger.info(f"No pending '{task_type}' tasks for week {letter}")
        return []
    
    logger.info(f"Found {len(pending_item_names)} items with pending '{task_type}' tasks")
    
    # Load full metadata from category files
    cfg = load_config()
    week_folder = cfg.weeks_dir / week_id(letter)
    
    items = []
    yaml_files = glob.glob(str(week_folder / "categories" / "*.yaml"))
    
    for yf in yaml_files:
        try:
            with open(yf, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    for item in data:
                        item_name = item.get('name')
                        if item_name in pending_item_names:
                            items.append(ProjectMetadata(
                                name=item_name,
                                repo_url=item.get('repo_url'),
                                homepage=item.get('homepage_url'),
                                week_letter=letter
                            ))
        except Exception as e:
            logger.exception(f"Error reading {yf}: {e}")
    
    items.sort(key=lambda x: x.name)
    
    # Log progress
    progress = tracker.get_progress(letter, task_type)
    logger.info(
        f"Week {letter} progress for '{task_type}': "
        f"{progress.completed}/{progress.total} completed "
        f"({progress.completion_percentage:.1f}%)"
    )
    
    return items

@task
@logfire.instrument
async def research_item(item: ProjectMetadata, week_letter: str) -> ResearchOutput:
    """Research a single project and update tracker.
    
    Args:
        item: Project metadata
        week_letter: Week letter for tracking
        
    Returns:
        Research output
    """
    logger = get_run_logger()
    tracker = get_tracker()
    
    logger.info(f"Researching item: {item.name}")
    
    # Mark as in progress
    try:
        tracker.update_task(week_letter, item.name, "research", TaskStatus.IN_PROGRESS)
    except Exception as e:
        logger.warning(f"Failed to update tracker for {item.name}: {e}")
    
    try:
        # Pydantic AI agents are async
        result = await researcher_agent.run(
            f"Research the project: {item.name}",
            deps=item
        )
        return result.data
    except Exception as e:
        logger.error(f"Failed to research {item.name}: {e}")
        
        # Mark as failed in tracker
        try:
            tracker.update_task(
                week_letter,
                item.name,
                "research",
                TaskStatus.FAILED,
                error_message=str(e)
            )
        except Exception as track_error:
            logger.warning(f"Failed to update tracker failure for {item.name}: {track_error}")
        
        return ResearchOutput(
            project_name=item.name,
            summary="Research failed.",
            key_features=[],
            recent_updates=f"Error: {str(e)}",
            use_cases="Unknown"
        )

@task
@logfire.instrument
async def write_weekly_post(week_letter: str, research_results: List[ResearchOutput]) -> BlogPostDraft:
    logger = get_run_logger()
    logger.info(f"Writing blog post for week {week_letter}")
    deps = WriterDeps(research_results=research_results, week_letter=week_letter)
    result = await writer_agent.run(
        f"Write a blog post for CNCF projects starting with letter {week_letter}.",
        deps=deps
    )
    return result.data

@task
@logfire.instrument
async def save_post(week_letter: str, draft: BlogPostDraft):
    """Save blog post and update tracker."""
    logger = get_run_logger()
    tracker = get_tracker()
    
    cfg = load_config()
    year = datetime.now().year
    filename = cfg.hugo_posts_dir / f"{year}-{week_letter}.md"
    logger.info(f"Saving post to {filename}")

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
    logger.info("Post saved.")
    
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
        logger.info(f"Tracker updated: week {week_letter} blog post completed")
    except Exception as e:
        logger.warning(f"Failed to update tracker for blog post: {e}")

@task
@logfire.instrument
async def save_research(week_letter: str, research: ResearchOutput):
    """Save individual research file to data/weeks/XX-Letter/research/{sanitized_name}.yaml
    and update tracker."""
    logger = get_run_logger()
    tracker = get_tracker()
    
    cfg = load_config()
    research_dir = cfg.weeks_dir / week_id(week_letter) / "research"
    
    # Sanitize project name for filename: spaces to underscores, lowercase, remove special chars
    sanitized_name = research.project_name.lower() \
        .replace(" ", "_") \
        .replace("&", "and") \
        .replace("/", "_") \
        .replace(".", "_") \
        .replace(",", "") \
        .replace("'", "") \
        .replace('"', "")
    
    filename = Path(research_dir) / f"{sanitized_name}.yaml"
    
    logger.info(f"Saving research for {research.project_name} to {filename}")
    
    # Create directory if it doesn't exist
    os.makedirs(research_dir, exist_ok=True)
    
    # Convert research to dict and save as YAML
    research_dict = research.model_dump(exclude_none=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(research_dict, f, default_flow_style=False, allow_unicode=True)
    
    logger.info(f"Research saved to {filename}")
    
    # Update tracker to mark research as completed
    try:
        relative_path = f"research/{sanitized_name}.yaml"
        tracker.update_task(
            week_letter,
            research.project_name,
            "research",
            TaskStatus.COMPLETED,
            output_file=relative_path
        )
        logger.info(f"Tracker updated: {research.project_name} research completed")
    except Exception as e:
        logger.warning(f"Failed to update tracker for {research.project_name}: {e}")

@flow(name="Weekly Content Flow")
@logfire.instrument
async def weekly_content_flow(limit: Optional[int] = None):
    """
    Main workflow that processes CNCF projects week by week.
    
    Args:
        limit: Maximum number of items to process across all weeks (default: unlimited).
               Note: Each week can have up to 50 items, but limit applies to total items processed.
    """
    logger = get_run_logger()
    logger.info(f"Starting weekly content flow with item limit={limit}")

    items_processed = 0
    weeks_processed = 0

    while True:
        # Check if we've reached the item limit
        if limit and items_processed >= limit:
            logger.info(f"Item limit reached ({items_processed}/{limit}). Stopping.")
            break

        decision = await determine_next_week()

        if decision.action == 'done':
            logger.info("All weeks completed. Exiting.")
            break

        week_letter = decision.week_letter

        # Validate week letter
        if not (len(week_letter) == 1 and 'A' <= week_letter <= 'Z'):
            logger.error(f"Invalid week letter received from Editor: {week_letter}. Skipping.")
            continue

        logger.info(f"Processing Week: {week_letter}")

        items = await get_items_for_week(week_letter)

        if not items:
            logger.warning(f"No items found for week {week_letter}. Saving placeholder.")
            await save_post(
                week_letter,
                BlogPostDraft(title=f"CNCF Projects Starting with {week_letter} - Coming Soon", 
                             content_markdown="No items found for this week yet. Check back later!")
            )
            weeks_processed += 1
            continue

        # Calculate how many items to process this week based on remaining limit
        items_to_process = items
        if limit:
            remaining = limit - items_processed
            if remaining < len(items):
                items_to_process = items[:remaining]
                logger.info(f"Processing {len(items_to_process)} of {len(items)} items due to limit")

        # Research items in parallel using asyncio.gather
        research_tasks = [research_item(item) for item in items_to_process]
        research_results = await asyncio.gather(*research_tasks)

        # Save research files for each result
        save_research_tasks = [save_research(week_letter, result) for result in research_results]
        await asyncio.gather(*save_research_tasks)

        # Write the blog post
        draft = await write_weekly_post(week_letter, research_results)

        # Save the post
        await save_post(week_letter, draft)

        items_processed += len(items_to_process)
        weeks_processed += 1
        limit_display = limit if limit is not None else 'unlimited'
        logger.info(f"Completed week {week_letter}. Total items processed: {items_processed}/{limit_display}")

        # If we've processed partial items for this week, we're done
        if limit and items_processed >= limit:
            logger.info(f"Item limit reached after processing week {week_letter}.")
            break

if __name__ == "__main__":
    asyncio.run(weekly_content_flow(limit=1))
