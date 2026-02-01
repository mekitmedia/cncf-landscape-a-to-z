import glob
import yaml
from typing import List
from pathlib import Path
from src.config import load_config, week_id
from src.agentic.models import ProjectMetadata
from src.tracker import get_tracker

async def get_items_for_week(letter: str, task_type: str = "research") -> List[ProjectMetadata]:
    """Get items with pending tasks for a specific week.

    Args:
        letter: Week letter (A-Z)
        task_type: Type of task to check (default: research)

    Returns:
        List of ProjectMetadata for items with pending tasks
    """
    # Get tracker instance
    tracker = get_tracker()

    # Check if tracker exists for this week
    if not tracker.tracker_exists(letter):
        return []

    # Get pending items from tracker
    pending_item_names = tracker.get_pending_items(letter, task_type)

    if not pending_item_names:
        return []

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
            # Log error but continue
            pass

    items.sort(key=lambda x: x.name)

    return items