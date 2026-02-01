import asyncio
import logfire
from typing import List, Optional
from prefect import flow, task, get_run_logger
from src.agentic.models import ResearchOutput, BlogPostDraft, NextWeekDecision, ProjectMetadata
from src.tracker import get_tracker
from src.agentic.actions import decisions, weekly, research, writing

@task
@logfire.instrument
async def determine_next_week() -> NextWeekDecision:
    logger = get_run_logger()
    logger.info("Asking Editor Agent for next week...")
    result = await decisions.determine_next_week()
    logger.info(f"Editor decision: {result}")
    return result

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

    items = await weekly.get_items_for_week(letter, task_type)

    if not items:
        logger.info(f"No pending '{task_type}' tasks for week {letter}")
        return []

    logger.info(f"Found {len(items)} items with pending '{task_type}' tasks")

    # Log progress
    tracker = get_tracker()
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
    logger.info(f"Researching item: {item.name}")
    
    result = await research.research_item(item, week_letter)
    
    logger.info(f"Research completed for {item.name}")
    return result

@task
@logfire.instrument
async def write_weekly_post(week_letter: str, research_results: List[ResearchOutput]) -> BlogPostDraft:
    logger = get_run_logger()
    logger.info(f"Writing blog post for week {week_letter}")
    draft = await writing.write_weekly_post(week_letter, research_results)
    logger.info(f"Blog post written for week {week_letter}")
    return draft

@task
@logfire.instrument
async def save_post(week_letter: str, draft: BlogPostDraft):
    """Save blog post and update tracker."""
    logger = get_run_logger()
    logger.info(f"Saving blog post for week {week_letter}")
    await writing.save_post(week_letter, draft)
    logger.info(f"Blog post saved for week {week_letter}")

@task
@logfire.instrument
async def save_research(week_letter: str, research: ResearchOutput):
    """Save individual research file to data/weeks/XX-Letter/research/{sanitized_name}.yaml
    and update tracker."""
    logger = get_run_logger()
    logger.info(f"Saving research for {research.project_name}")
    await research.save_research(week_letter, research)
    logger.info(f"Research saved for {research.project_name}")

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
