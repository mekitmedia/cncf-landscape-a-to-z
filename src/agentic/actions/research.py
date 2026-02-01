import os
import logfire
import yaml
from pathlib import Path
from datetime import datetime
from typing import List
from src.agentic.tools.agents.researcher import researcher_agent
from src.agentic.models import ResearchOutput, ProjectMetadata
from src.tracker import get_tracker, TaskStatus
from src.config import load_config

@logfire.instrument
async def research_item(item: ProjectMetadata, week_letter: str) -> ResearchOutput:
    """Research a single project and update tracker.

    Args:
        item: Project metadata
        week_letter: Week letter for tracking

    Returns:
        Research output
    """
    tracker = get_tracker()

    # Mark as in progress
    try:
        tracker.update_task(week_letter, item.name, "research", TaskStatus.IN_PROGRESS)
    except Exception as e:
        pass

    try:
        # Pydantic AI agents are async
        result = await researcher_agent.run(
            f"Research the project: {item.name}",
            deps=item
        )
        return result.data
    except Exception as e:
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
            pass

        return ResearchOutput(
            project_name=item.name,
            summary="Research failed.",
            key_features=[],
            recent_updates=f"Error: {str(e)}",
            use_cases="Unknown"
        )

@logfire.instrument
async def save_research(week_letter: str, research: ResearchOutput):
    """Save individual research file to data/weeks/XX-Letter/research/{sanitized_name}.yaml
    and update tracker."""
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

    # Create directory if it doesn't exist
    os.makedirs(research_dir, exist_ok=True)

    # Convert research to dict and save as YAML
    research_dict = research.model_dump(exclude_none=True)

    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(research_dict, f, default_flow_style=False, allow_unicode=True)

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
    except Exception as e:
        pass