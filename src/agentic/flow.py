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
from src.agentic.models import ResearchOutput, BlogPostDraft, NextWeekDecision, ProjectMetadata

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
async def get_items_for_week(letter: str) -> List[ProjectMetadata]:
    logger = get_run_logger()
    logger.info(f"Getting items for letter {letter}")

    # Read from generated tasks (output of ETL pipeline)
    # The ETL pipeline generates data/weeks/XX-Letter/tasks.yaml
    cfg = load_config()
    week_folders = glob.glob(str(cfg.weeks_dir / f"*-{letter.upper()}"))

    items = []

    if week_folders:
        week_folder = week_folders[0]
        logger.info(f"Using ETL output from {week_folder}")

        # Read all category yaml files for that week
        yaml_files = glob.glob(f"{week_folder}/categories/*.yaml")
        for yf in yaml_files:
            try:
                with open(yf, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, list):
                        for item in data:
                            items.append(ProjectMetadata(
                                name=item.get('name'),
                                repo_url=item.get('repo_url'),
                                homepage=item.get('homepage_url')
                            ))
            except FileNotFoundError:
                logger.error(f"File not found: {yf}")
            except yaml.YAMLError as e:
                logger.error(f"YAML parsing error in {yf}: {e}")
            except UnicodeDecodeError as e:
                logger.error(f"Encoding error while reading {yf}: {e}")
            except Exception as e:
                logger.exception(f"Unexpected error while reading {yf}: {e}")

    else:
        # Fallback to fetching raw data if ETL hasn't run
        logger.warning("ETL output not found. Falling back to fetching raw landscape data.")
        input_path = load_config().landscape_source

        def _fetch_and_transform():
            from src.pipeline.extract import get_landscape_data
            from src.pipeline.transform import get_landscape_by_letter
            landscape = get_landscape_data(input_path)
            return get_landscape_by_letter(landscape)

        landscape_by_letter = await asyncio.to_thread(_fetch_and_transform)

        data = landscape_by_letter.get(letter, {})
        if 'partial' in data:
            for path, item_list in data['partial'].items():
                for item in item_list:
                    items.append(ProjectMetadata(
                        name=item.get('name'),
                        repo_url=item.get('repo_url'),
                        homepage=item.get('homepage_url')
                    ))

    items.sort(key=lambda x: x.name)
    logger.info(f"Found {len(items)} items for letter {letter}")
    return items

@task
@logfire.instrument
async def research_item(item: ProjectMetadata) -> ResearchOutput:
    logger = get_run_logger()
    logger.info(f"Researching item: {item.name}")
    try:
        # Pydantic AI agents are async
        result = await researcher_agent.run(
            f"Research the project: {item.name}",
            deps=item
        )
        return result.data
    except Exception as e:
        logger.error(f"Failed to research {item.name}: {e}")
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
    result = await writer_agent.run(
        f"Write a blog post for CNCF projects starting with letter {week_letter}.",
        deps=research_results
    )
    return result.data

@task
@logfire.instrument
async def save_post(week_letter: str, draft: BlogPostDraft):
    logger = get_run_logger()
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

@task
@logfire.instrument
async def save_research(week_letter: str, research: ResearchOutput):
    """Save individual research file to data/weeks/XX-Letter/research/{sanitized_name}.yaml"""
    logger = get_run_logger()
    
    cfg = load_config()
    research_dir = cfg.weeks_dir / week_id(week_letter) / "research"
    
    # Sanitize project name for filename: spaces to underscores, lowercase, remove special chars
    sanitized_name = research.project_name.lower() \
        .replace(" ", "_") \
        .replace("&", "and") \
        .replace("/", "_") \
        .replace(".", "_") \
        .replace(",", "")
    
    filename = Path(research_dir) / f"{sanitized_name}.yaml"
    
    logger.info(f"Saving research for {research.project_name} to {filename}")
    
    # Create directory if it doesn't exist
    os.makedirs(research_dir, exist_ok=True)
    
    # Convert research to dict and save as YAML
    research_dict = research.model_dump(exclude_none=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(research_dict, f, default_flow_style=False, allow_unicode=True)
    
    logger.info(f"Research saved to {filename}")

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
