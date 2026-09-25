from src.logger import get_logger

import yaml
from pathlib import Path
from src.config import load_config

def _get_overlay_data() -> dict:
    config = load_config()
    overlay_path = config.data_dir / "overlay" / "overlay.yaml"
    if overlay_path.exists():
        with open(overlay_path, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}


logger = get_logger(__name__)

def make_path(c: str, s: str) -> str:
    """
    This function sanitize a category and subcategory name to make it a viable folder name
    """
    return (c + "_" + s).lower() \
        .replace(" & ", "_") \
        .replace(" ", "_") \
        .replace("_-", "") \
        .replace(",", "") \
        .replace("/", "_")

def _is_valid_item(item: dict) -> bool:
    """
    This function checks if an item is valid (not archived and has a repo_url)
    """
    return item.get('project') != 'archived' and item.get('repo_url') is not None

def _get_featured_priority(item: dict) -> tuple:
    """
    This function returns a priority tuple for featured selection.
    Priority: graduated > incubating > sandbox (alphabetically within same status)
    """
    project_status = item.get('project')
    if project_status is None:
        project_status = 'sandbox'
    project_status = project_status.lower()
    
    status_priority = {
        'graduated': 0,
        'incubating': 1,
        'sandbox': 2
    }
    
    priority = status_priority.get(project_status, 3)
    name = item.get('name', '')
    
    return (priority, name)

def _prepare_item_for_output(item: dict, is_featured: bool = False, overlay_data: dict = None) -> dict:
    """
    This function prepares an item for YAML output, adding featured flag and description.
    """
    output_item = {
        'name': item.get('name'),
        'repo_url': item.get('repo_url'),
        'homepage_url': item.get('homepage_url'),
        'project': item.get('project'),
        'featured': is_featured
    }
    
    # Add optional fields if they exist
    if item.get('logo'):
        output_item['logo'] = item.get('logo')
    if item.get('description'):
        output_item['description'] = item.get('description')
    if item.get('twitter'):
        output_item['twitter'] = item.get('twitter')
    if item.get('crunchbase'):
        output_item['crunchbase'] = item.get('crunchbase')

    if overlay_data and item.get('name') in overlay_data:
        for k, v in overlay_data[item.get('name')].items():
            output_item[k] = v
    
    return output_item

def get_items_without_repo_url(landscape: list) -> list:
    """
    This function returns a list of all items in the landscape that do not have a repo_url
    """
    return sorted([
        item['name']
        for c in landscape
        for sub in (c.get('subcategories') or [])
        for item in (sub.get('items') or [])
        if item.get('repo_url') is None
    ])

def get_only_letter(x: str, landscape: list) -> dict:
    """
    This function gets the letter we want, not best performance but does the job
    """
    logger.info(f"Filtering landscape data for letter {x}")
    return {
        make_path(c['name'], sub['name']): [
            item for item in (sub.get('items') or []) if item['name'].startswith(x) and _is_valid_item(item)
        ]
        for c in landscape for sub in (c.get('subcategories') or [])
    }

def get_tasks_for_letter(x: str, landscape: list) -> list:
    """
    This function returns a list of tasks (items) for a specific letter
    """
    logger.info(f"Getting tasks for letter {x}")
    tasks = []
    for c in landscape:
        for sub in (c.get('subcategories') or []):
            for item in (sub.get('items') or []):
                if item['name'].startswith(x) and _is_valid_item(item):
                    tasks.append(item['name'])
    return sorted(tasks)

def get_categories(landscape: list) -> dict:
    """
    This function gets the categories from the landscape data
    """
    logger.info("Getting categories from landscape data")
    return {
        c['name']: {
            sub['name']: make_path(c['name'], sub['name'])
            for sub in (c.get('subcategories') or [])
        }
        for c in landscape
    }

def get_items(landscape: list) -> dict:
    """
    This function gets the items from the landscape data
    """
    logger.info("Getting items from landscape data")
    return {
        c['name']: {
            sub['name']: [
                item['name'] for item in (sub.get('items') or []) if _is_valid_item(item)
            ]
            for sub in (c.get('subcategories') or [])
        }
        for c in landscape
    }

def get_all_categories(landscape: list) -> list:
    """
    This function gets all the categories from the landscape data
    """
    logger.info("Getting all categories from landscape data")
    return [{
        'category': c['name'],
        'subcategories': [{
            'subcategory': sub['name'],
            'path': make_path(c['name'], sub['name']),
            'items': [
                item['name'] for item in (sub.get('items') or []) if _is_valid_item(item)
            ]
        } for sub in (c.get('subcategories') or [])]
    } for c in landscape]

def get_stats_per_category(landscape: list) -> dict:
    """
    This function gets the stats per category from the landscape data
    """
    logger.info("Getting stats per category from landscape data")
    return {c['name']: len((c.get('subcategories') or [])) for c in landscape}

def get_stats_per_category_per_week(landscape: list) -> dict:
    """
    This function gets the stats per category per week from the landscape data
    """
    logger.info("Getting stats per category per week from landscape data")
    stats_per_category = {c['name']: len((c.get('subcategories') or [])) for c in landscape}
    return {
        f"week_{str(index).zfill(2)}_{chr(letter)}": stats_per_category.copy()
        for index, letter in enumerate(range(ord('A'), ord('Z') + 1))
    }

def get_stats_by_status(landscape: list) -> dict:
    """
    This function gets the stats by status from the landscape data
    """
    logger.info("Getting stats by status from landscape data")
    stats = {}
    for c in landscape:
        for sub in (c.get('subcategories') or []):
            for item in (sub.get('items') or []):
                if not _is_valid_item(item):
                    continue
                status = item.get('project')
                if status:
                    stats[status] = stats.get(status, 0) + 1
    return stats

def get_landscape_by_letter(landscape: list) -> dict:
    """
    This function processes the landscape once and returns data for all letters.
    Returns a dict { 'A': {'partial': {...}, 'tasks': [...]}, ... }
    Includes featured flag (top 6 items per category based on CNCF status).
    """
    logger.info("Indexing landscape data by letter")
    index = {}
    overlay_data = _get_overlay_data()

    # Initialize index for all letters A-Z
    for letter_code in range(ord('A'), ord('Z') + 1):
        letter = chr(letter_code)
        index[letter] = {
            'partial': {},
            'tasks': []
        }

    # Pre-calculate all paths
    all_paths = [
        make_path(c['name'], sub['name'])
        for c in landscape for sub in (c.get('subcategories') or [])
    ]

    # Iterate landscape once, collecting by letter and path
    for c in landscape:
        for sub in (c.get('subcategories') or []):
            path = make_path(c['name'], sub['name'])
            # Group items by first letter
            items_by_letter = {}
            for item in (sub.get('items') or []):
                if _is_valid_item(item):
                    name = item['name']
                    if not name:
                        continue
                    first_char = name[0]
                    if 'A' <= first_char <= 'Z':
                        if first_char not in items_by_letter:
                            items_by_letter[first_char] = []
                        items_by_letter[first_char].append(item)
            
            # For each letter, sort items and mark top 6 as featured
            for letter, letter_items in items_by_letter.items():
                # Sort by featured priority (status then alphabetically)
                sorted_items = sorted(letter_items, key=_get_featured_priority)
                
                # Mark top 6 as featured
                for idx, item in enumerate(sorted_items):
                    is_featured = idx < 6
                    prepared_item = _prepare_item_for_output(item, is_featured, overlay_data)

                    if path not in index[letter]['partial']:
                        index[letter]['partial'][path] = []

                    index[letter]['partial'][path].append(prepared_item)
                    index[letter]['tasks'].append(item['name'])

    # Sort tasks
    for letter in index:
        index[letter]['tasks'].sort()

    return index


def get_workflow_stats(landscape: list, data_dir: Path = None) -> dict:
    """
    Computes aggregated workflow statistics including landscape tool totals,
    CNCF status distribution, subcategory breakdowns, and letter-by-letter
    research/editorial workflow progress from data/weeks tracking files.
    """
    logger.info("Calculating workflow statistics")

    total_tools = 0
    cncf_statuses = {"graduated": 0, "incubating": 0, "sandbox": 0, "non-cncf": 0}
    category_counts = {}

    for c in landscape:
        for sub in (c.get('subcategories') or []):
            sub_name = sub['name']
            sub_items = [item for item in (sub.get('items') or []) if _is_valid_item(item)]
            if sub_items:
                category_counts[sub_name] = category_counts.get(sub_name, 0) + len(sub_items)
            for item in sub_items:
                total_tools += 1
                status = item.get('project')
                if status in cncf_statuses:
                    cncf_statuses[status] += 1
                else:
                    cncf_statuses["non-cncf"] += 1

    letter_progress = {}
    total_researched = 0
    total_editorial = 0

    if data_dir is None:
        from src.config import load_config
        data_dir = load_config().data_dir

    from src.config import week_id as get_week_id

    for index, letter_code in enumerate(range(ord('A'), ord('Z') + 1)):
        letter = chr(letter_code)
        w_id = get_week_id(letter)
        tracker_path = data_dir / "weeks" / w_id / "tracker.yaml"

        researched_count = 0
        editorial_count = 0
        letter_total = 0

        if tracker_path.exists():
            try:
                with open(tracker_path, "r", encoding="utf-8") as tf:
                    tdata = yaml.safe_load(tf) or {}
                items = tdata.get("items", {})
                for item_name, item_info in items.items():
                    if isinstance(item_info, dict) and not item_info.get("removed", False):
                        letter_total += 1
                        tasks = item_info.get("tasks", {})
                        res_task = tasks.get("research", {})
                        if isinstance(res_task, dict) and res_task.get("status") == "completed":
                            researched_count += 1
                        cnt_task = tasks.get("content", {})
                        if isinstance(cnt_task, dict) and cnt_task.get("status") == "completed":
                            editorial_count += 1
            except Exception as e:
                logger.warning(f"Error reading tracker for {w_id}: {e}")

        total_researched += researched_count
        total_editorial += editorial_count

        letter_progress[letter] = {
            "letter": letter,
            "week_id": w_id,
            "total_tools": letter_total,
            "researched": researched_count,
            "editorial": editorial_count,
            "is_complete": letter_total > 0 and researched_count == letter_total
        }

    return {
        "summary": {
            "total_tools": total_tools,
            "cncf_hosted": cncf_statuses["graduated"] + cncf_statuses["incubating"] + cncf_statuses["sandbox"],
            "researched_tools": total_researched,
            "published_posts": total_editorial
        },
        "cncf_statuses": cncf_statuses,
        "categories": dict(sorted(category_counts.items(), key=lambda x: x[0])),
        "letter_progress": letter_progress
    }
