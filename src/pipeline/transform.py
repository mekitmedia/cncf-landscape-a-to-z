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

def _get_featured_priority(item: dict) -> tuple:
    """
    This function returns a priority tuple for featured selection.
    Priority: graduated > incubating > sandbox (alphabetically within same status)
    """
    project_status = item.get('project', 'sandbox').lower()
    
    status_priority = {
        'graduated': 0,
        'incubating': 1,
        'sandbox': 2
    }
    
    priority = status_priority.get(project_status, 3)
    name = item.get('name', '')
    
    return (priority, name)

def _prepare_item_for_output(item: dict, is_featured: bool = False) -> dict:
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
    
    return output_item

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

def get_tasks_for_letter(x: str, landscape: list) -> list:
    """
    This function returns a list of tasks (items) for a specific letter
    """
    logger.info(f"Getting tasks for letter {x}")
    tasks = []
    for c in landscape:
        for sub in c['subcategories']:
            for item in sub['items']:
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
    stats_per_category = {c['name']: len(c['subcategories']) for c in landscape}
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
        for sub in c['subcategories']:
            for item in sub['items']:
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
        for c in landscape for sub in c['subcategories']
    ]

    # Iterate landscape once, collecting by letter and path
    for c in landscape:
        for sub in c['subcategories']:
            path = make_path(c['name'], sub['name'])
            # Group items by first letter
            items_by_letter = {}
            for item in sub['items']:
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
                    prepared_item = _prepare_item_for_output(item, is_featured)

                    if path not in index[letter]['partial']:
                        index[letter]['partial'][path] = []

                    index[letter]['partial'][path].append(prepared_item)
                    index[letter]['tasks'].append(item['name'])

    # Sort tasks
    for letter in index:
        index[letter]['tasks'].sort()

    return index
