import asyncio
import os
from datetime import datetime
from typing import List, Optional
from prefect import flow, task, get_run_logger
from src.agentic.agents import researcher_agent, writer_agent, editor_agent
from src.agentic.models import ResearchOutput, BlogPostDraft, NextWeekDecision, ProjectMetadata
from src.pipeline.extract import get_landscape_data
from src.pipeline.transform import get_landscape_by_letter

@task
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
async def get_items_for_week(letter: str) -> List[ProjectMetadata]:
    logger = get_run_logger()
    logger.info(f"Getting items for letter {letter}")

    input_path = "https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml"

    # Run blocking sync calls in a thread
    def _fetch_and_transform():
        landscape = get_landscape_data(input_path)
        return get_landscape_by_letter(landscape)

    landscape_by_letter = await asyncio.to_thread(_fetch_and_transform)

    data = landscape_by_letter.get(letter, {})
    items = []
    if 'partial' in data:
        for path, item_list in data['partial'].items():
            for item in item_list:
                items.append(ProjectMetadata(
                    name=item.get('name'),
                    repo_url=item.get('repo_url'),
                    homepage=item.get('homepage_url')
                ))

    # Sort by name
    items.sort(key=lambda x: x.name)
    logger.info(f"Found {len(items)} items for letter {letter}")
    return items

@task
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
async def write_weekly_post(week_letter: str, research_results: List[ResearchOutput]) -> BlogPostDraft:
    logger = get_run_logger()
    logger.info(f"Writing blog post for week {week_letter}")
    result = await writer_agent.run(
        f"Write a blog post for CNCF projects starting with letter {week_letter}.",
        deps=research_results
    )
    return result.data

@task
async def save_post(week_letter: str, draft: BlogPostDraft):
    logger = get_run_logger()
    year = datetime.now().year
    filename = f"website/content/posts/{year}-{week_letter}.md"
    logger.info(f"Saving post to {filename}")

    date_str = datetime.now().isoformat()
    full_content = f"""---
title: "{draft.title}"
date: {date_str}
draft: false
---

{draft.content_markdown}
"""

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(full_content)
    logger.info("Post saved.")

@flow(name="Weekly Content Flow")
async def weekly_content_flow(limit: Optional[int] = None):
    logger = get_run_logger()
    logger.info(f"Starting weekly content flow with limit={limit}")

    tasks_run = 0

    while True:
        if limit and tasks_run >= limit:
            logger.info("Limit reached. Stopping.")
            break

        decision = await determine_next_week()

        if decision.action == 'done':
            logger.info("All weeks completed. Exiting.")
            break

        week_letter = decision.week_letter

        if not (len(week_letter) == 1 and 'A' <= week_letter <= 'Z'):
            logger.error(f"Invalid week letter received from Editor: {week_letter}. Skipping.")
            tasks_run += 1
            continue

        logger.info(f"Processing Week: {week_letter}")

        items = await get_items_for_week(week_letter)

        if not items:
            logger.warning(f"No items found for week {week_letter}. Marking as done (saving empty placeholder?).")
            # If we don't save, the Editor will pick it again next time.
            # We should probably save a placeholder or handle this.
            # For now, let's skip research and write an "empty" post or just skip.
            # But if we skip, infinite loop!
            # Let's save a placeholder.
            await save_post(week_letter, BlogPostDraft(title=f"Week {week_letter}", content_markdown="No items found."))
            tasks_run += 1
            continue

        # Research in parallel
        # Note: Prefect tasks are better called with .submit() for parallelism in a flow,
        # but in async flow, direct await with asyncio.gather works too if tasks are async.
        # However, calling @task decorated functions directly in async flow behaves like normal async functions.
        # To get Prefect tracking for sub-tasks properly:
        # research_futures = [research_item.submit(item) for item in items]
        # research_results = [await f.result() for f in research_futures] # Wait for them?
        # Simpler is just direct call for now.

        research_tasks = [research_item(item) for item in items]
        research_results = await asyncio.gather(*research_tasks)

        # Write
        draft = await write_weekly_post(week_letter, research_results)

        # Save
        await save_post(week_letter, draft)

        tasks_run += 1

if __name__ == "__main__":
    asyncio.run(weekly_content_flow(limit=1))
