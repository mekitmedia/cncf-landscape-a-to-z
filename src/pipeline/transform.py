from src.logger import get_logger

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

def get_items_without_repo_url(landscape: list) -> list:
    """
    This function returns a list of all items in the landscape that do not have a repo_url
    """
    return sorted([
        item['name']
        for c in landscape
        for sub in c['subcategories']
        for item in sub['items']
        if item.get('repo_url') is None
    ])

def get_only_letter(x: str, landscape: list) -> dict:
    """
    This function gets the letter we want, not best performance but does the job
    """
    logger.info(f"Filtering landscape data for letter {x}")
    return {
        make_path(c['name'], sub['name']): [
            item for item in sub['items'] if item['name'].startswith(x) and _is_valid_item(item)
        ]
        for c in landscape for sub in c['subcategories']
    }

def get_categories(landscape: list) -> dict:
    """
    This function gets the categories from the landscape data
    """
    logger.info("Getting categories from landscape data")
    return {
        c['name']: {
            sub['name']: make_path(c['name'], sub['name'])
            for sub in c['subcategories']
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
                item['name'] for item in sub['items'] if _is_valid_item(item)
            ]
            for sub in c['subcategories']
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
                item['name'] for item in sub['items'] if _is_valid_item(item)
            ]
        } for sub in c['subcategories']]
    } for c in landscape]

def get_stats_per_category(landscape: list) -> dict:
    """
    This function gets the stats per category from the landscape data
    """
    logger.info("Getting stats per category from landscape data")
    return {c['name']: len(c['subcategories']) for c in landscape}

def get_stats_per_category_per_week(landscape: list) -> dict:
    """
    This function gets the stats per category per week from the landscape data
    """
    logger.info("Getting stats per category per week from landscape data")
    return {
        f"week_{str(index).zfill(2)}_{chr(letter)}": {
            c['name']: len(c['subcategories']) for c in landscape
        }
        for index, letter in enumerate(range(ord('A'), ord('Z') + 1))
    }

def get_stats_by_status(landscape: list) -> dict:
    """
    This function gets the stats by status from the landscape data
    """
    logger.info("Getting stats by status from landscape data")
    stats = {}
    for c in landscape:
        for sub in c['subcategories']:
            for item in sub['items']:
                if not _is_valid_item(item):
                    continue
                status = item.get('project')
                if status:
                    stats[status] = stats.get(status, 0) + 1
    return stats
