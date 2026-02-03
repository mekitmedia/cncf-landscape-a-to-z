import asyncio
from typing import List, Optional
from prefect import flow, task, get_run_logger
from src.agentic.models import ResearchOutput, BlogPostDraft, NextWeekDecision, ProjectMetadata
from src.tracker import get_tracker, ReadyTask
from src.agentic.actions import decisions, weekly, research, writing
from src.agentic.tools.tracker import get_ready_tasks, GetReadyTasksInput
from src.agentic.deps import AgentDeps

@task
async def determine_next_week() -> NextWeekDecision:
    logger = get_run_logger()
    logger.info("Asking Editor Agent for next week...")
    result = await decisions.determine_next_week()
    logger.info(f"Editor decision: {result}")
    return result

@task
async def get_ready_tasks_batch(agent_type: str, limit: int = 5) -> List[ReadyTask]:
    """Get tasks ready for execution by a specific agent.
    
    Args:
        agent_type: 'researcher' or 'writer'
        limit: Maximum tasks to return
        
    Returns:
        List of ReadyTask objects
    """
    logger = get_run_logger()
    logger.info(f"Getting {limit} ready tasks for {agent_type}")
    
    tracker = get_tracker()
    ready_tasks = tracker.get_ready_tasks(limit=limit)
    
    # Filter by agent type
    filtered = [t for t in ready_tasks if t.agent.lower() == agent_type.lower()]
    
    if not filtered:
        logger.info(f"No ready tasks for {agent_type}")
        return []
    
    logger.info(f"Found {len(filtered)} ready tasks for {agent_type}")
    return filtered

@task
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
async def write_weekly_post(week_letter: str, research_results: List[ResearchOutput]) -> BlogPostDraft:
    logger = get_run_logger()
    logger.info(f"Writing blog post for week {week_letter}")
    draft = await writing.write_weekly_post(week_letter, research_results)
    logger.info(f"Blog post written for week {week_letter}")
    return draft

@task
async def save_post(week_letter: str, draft: BlogPostDraft):
    """Save blog post and update tracker."""
    logger = get_run_logger()
    logger.info(f"Saving blog post for week {week_letter}")
    await writing.save_post(week_letter, draft)
    logger.info(f"Blog post saved for week {week_letter}")

@task
async def save_research(week_letter: str, research: ResearchOutput):
    """Save individual research file to data/weeks/XX-Letter/research/{sanitized_name}.yaml
    and update tracker."""
    logger = get_run_logger()
    logger.info(f"Saving research for {research.project_name}")
    await research.save_research(week_letter, research)
    logger.info(f"Research saved for {research.project_name}")

@flow(name="Weekly Content Flow")
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
        research_tasks = [research_item(item, week_letter) for item in items_to_process]
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

@flow(name="Parallel Task Orchestration")
async def parallel_orchestration_flow(max_rounds: int = 10, batch_size: int = 5):
    """
    Graph-driven parallel orchestration that enables researchers and writers to work independently.
    
    This flow respects the task dependency graph:
    - research tasks can be picked by researchers at any time
    - blog_post tasks can only be picked once all research for that week is complete
    
    Token Cost Estimation:
    - Per agent invocation: ~10-20K tokens
    - Per round: batch_size × 2 agent types × 15K avg tokens
    - Full run: max_rounds × 2 × batch_size × 15K tokens (varies by early exit)
    
    Example token budgets:
    - max_rounds=10, batch_size=3: ~900K tokens (8 rounds avg completion)
    - max_rounds=10, batch_size=5: ~1.5M tokens
    - max_rounds=26, batch_size=1: ~780K tokens (conservative, sequential-like)
    
    Args:
        max_rounds: Maximum orchestration rounds (prevents infinite loops).
                   Early exit occurs if no ready tasks found.
                   Default 10 is ~8 rounds average for 26 weeks.
        batch_size: Number of tasks per agent per round (1-20).
                   Default 5 provides good parallelism.
                   Reduce to 1-2 for lower token usage.
    """
    logger = get_run_logger()
    
    # Log token estimates
    estimated_tokens_per_round = batch_size * 2 * 15_000  # 2 agent types, 15K avg per call
    estimated_total_tokens = estimated_tokens_per_round * max_rounds
    logger.info(f"Starting parallel orchestration:")
    logger.info(f"  max_rounds={max_rounds}, batch_size={batch_size}")
    logger.info(f"  Estimated ~{estimated_tokens_per_round:,.0f} tokens/round")
    logger.info(f"  Estimated total: ~{estimated_total_tokens:,.0f} tokens (actual varies by early exit)")
    
    round_num = 0
    total_tasks_processed = 0
    
    while round_num < max_rounds:
        round_num += 1
        logger.info(f"\n=== Round {round_num}/{max_rounds} ===")
        
        # Get ready tasks for researchers and writers
        researcher_tasks = await get_ready_tasks_batch("researcher", batch_size)
        writer_tasks = await get_ready_tasks_batch("writer", batch_size)
        
        if not researcher_tasks and not writer_tasks:
            logger.info(f"✓ No more ready tasks. Early exit after {round_num} rounds.")
            actual_tokens = estimated_tokens_per_round * round_num
            logger.info(f"  Actual estimated tokens: ~{actual_tokens:,.0f}")
            break
        
        round_tokens = (len(researcher_tasks) + len(writer_tasks)) * 15_000
        total_tasks_processed += len(researcher_tasks) + len(writer_tasks)
        logger.info(f"Round tokens estimate: ~{round_tokens:,.0f}")
        logger.info(f"Total tasks so far: {total_tasks_processed}")
        
        # Execute researcher tasks in parallel
        if researcher_tasks:
            logger.info(f"Dispatching {len(researcher_tasks)} research tasks")
            research_coros = []
            for task in researcher_tasks:
                # Create project metadata from task
                project = ProjectMetadata(
                    name=task.item_name,
                    week_letter=task.week_letter
                )
                research_coros.append(research_item(project, task.week_letter))
            
            research_results = await asyncio.gather(*research_coros, return_exceptions=True)
            
            # Save research results
            save_tasks = []
            for result in research_results:
                if isinstance(result, ResearchOutput):
                    save_tasks.append(save_research(result.project_name, result))
            
            if save_tasks:
                await asyncio.gather(*save_tasks)
        
        # Execute writer tasks in parallel
        if writer_tasks:
            logger.info(f"Dispatching {len(writer_tasks)} blog_post tasks")
            writer_coros = []
            for task in writer_tasks:
                # For blog_post tasks, gather all research for that week first
                tracker = get_tracker()
                week_research = []  # TODO: gather research results for week
                writer_coros.append(write_weekly_post(task.week_letter, week_research))
            
            blog_results = await asyncio.gather(*writer_coros, return_exceptions=True)
            
            # Save blog posts
            save_tasks = []
            for i, result in enumerate(blog_results):
                if isinstance(result, BlogPostDraft):
                    if i < len(writer_tasks):
                        save_tasks.append(save_post(writer_tasks[i].week_letter, result))
            
            if save_tasks:
                await asyncio.gather(*save_tasks)
        
        logger.info(f"Round {round_num} complete\n")
    
    actual_total_tokens = estimated_tokens_per_round * round_num
    logger.info(f"✓ Orchestration complete")
    logger.info(f"  Rounds executed: {round_num}")
    logger.info(f"  Total tasks processed: {total_tasks_processed}")
    logger.info(f"  Actual estimated tokens: ~{actual_total_tokens:,.0f}")

if __name__ == "__main__":
    asyncio.run(weekly_content_flow(limit=1))


