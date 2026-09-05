import asyncio
import logging
import os
import glob
import yaml
from typing import List, Optional

from src.config import load_config, week_id
from src.agentic.models import ResearchOutput
from src.tracker import get_tracker
from src.agentic.actions import decisions, weekly, research, writing

logger = logging.getLogger("agentic.runner")

async def load_week_research(week_letter: str) -> List[ResearchOutput]:
    """Load all saved research YAML files for a given week."""
    cfg = load_config()
    research_dir = cfg.weeks_dir / week_id(week_letter) / "research"
    results: List[ResearchOutput] = []

    if not os.path.exists(research_dir):
        return results

    yaml_files = glob.glob(str(research_dir / "*.yaml"))
    for yf in sorted(yaml_files):
        try:
            with open(yf, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    results.append(ResearchOutput.model_validate(data))
        except Exception as e:
            logger.warning(f"Could not load research file {yf}: {e}")

    return results

async def run_agentic_workflow(limit: Optional[int] = None) -> dict:
    """
    Native async runner for the CNCF Landscape A-to-Z weekly agentic workflow.
    
    Executes research tasks with strict limit control, and drafts weekly posts
    only when all research tasks for a week are completed.
    
    Args:
        limit: Maximum total items to research across all weeks (default: None/unlimited).
        
    Returns:
        Summary dictionary with execution statistics.
    """
    logger.info(f"Starting agentic workflow (limit={limit or 'unlimited'})")
    tracker = get_tracker()
    
    items_processed = 0
    weeks_completed = 0
    
    while True:
        if limit is not None and items_processed >= limit:
            logger.info(f"Reached item processing limit ({items_processed}/{limit}). Stopping.")
            break
            
        decision = await decisions.determine_next_week()
        if decision.action == "done":
            logger.info("All weeks are complete. Workflow finished.")
            break
            
        week_letter = decision.week_letter.upper()
        if not (len(week_letter) == 1 and "A" <= week_letter <= "Z"):
            logger.error(f"Invalid week letter received from Editor: '{week_letter}'. Stopping.")
            break
            
        logger.info(f"Active Week: {week_letter} (Reason: {decision.reason})")
        
        pending_items = await weekly.get_items_for_week(week_letter, task_type="research")
        
        if not pending_items:
            # Check if all research is done and blog post is pending
            progress = tracker.get_progress(week_letter, "research")
            if progress.total > 0 and progress.completed == progress.total:
                logger.info(f"All {progress.total} research items complete for Week {week_letter}. Drafting blog post...")
                week_research = await load_week_research(week_letter)
                draft = await writing.write_weekly_post(week_letter, week_research)
                await writing.save_post(week_letter, draft)
                weeks_completed += 1
                logger.info(f"Published blog post for Week {week_letter}")
            else:
                logger.info(f"No pending research items for Week {week_letter}.")
                
            break
            
        # Determine items to process in this batch
        items_to_process = pending_items
        if limit is not None:
            remaining = limit - items_processed
            items_to_process = pending_items[:remaining]
            
        logger.info(f"Researching {len(items_to_process)} project(s) for Week {week_letter}...")
        
        # Execute research tasks concurrently
        research_tasks = [
            research.research_item(item, week_letter)
            for item in items_to_process
        ]
        results = await asyncio.gather(*research_tasks, return_exceptions=True)
        
        # Save results
        for res in results:
            if isinstance(res, ResearchOutput):
                await research.save_research(week_letter, res)
                items_processed += 1
            elif isinstance(res, Exception):
                logger.error(f"Research task failed: {res}")
                
        # Check if week research is now 100% complete
        progress = tracker.get_progress(week_letter, "research")
        logger.info(
            f"Week {week_letter} Research Progress: "
            f"{progress.completed}/{progress.total} items ({progress.completion_percentage:.1f}%)"
        )
        
        if progress.total > 0 and progress.completed == progress.total:
            logger.info(f"Research 100% complete for Week {week_letter}. Drafting blog post...")
            week_research = await load_week_research(week_letter)
            draft = await writing.write_weekly_post(week_letter, week_research)
            await writing.save_post(week_letter, draft)
            weeks_completed += 1
            logger.info(f"Published blog post for Week {week_letter}")
            
        if limit is not None and items_processed >= limit:
            logger.info(f"Reached item processing limit ({items_processed}/{limit}). Stopping.")
            break

    summary = {
        "items_processed": items_processed,
        "weeks_completed": weeks_completed,
    }
    logger.info(f"Workflow run summary: {items_processed} items processed, {weeks_completed} weeks completed.")
    return summary
