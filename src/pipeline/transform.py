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


_TASKS_CACHE = {}


def _get_cached_tasks_index(landscape: list) -> dict:
    """
    Build and return a cached index of task names for the given landscape.

    The index maps the first character of each valid item name to a sorted list
    of item names starting with that character. The cache is stored in the
    module-level ``_TASKS_CACHE`` dictionary, keyed by the ``id`` of the
    ``landscape`` object, so repeated calls with the same in-memory landscape
    reuse the previously computed index.

    Cache management policy:
    the cache is bounded to a small number of landscapes. When the number of
    cached landscapes exceeds 5, the entire cache is cleared, effectively
    discarding older entries and keeping only indices for the most recently
    processed landscape thereafter.
    """
    lid = id(landscape)
    if lid in _TASKS_CACHE:
        return _TASKS_CACHE[lid]

    # Simple cache management: keep only recent landscapes.
    if len(_TASKS_CACHE) > 5:
        _TASKS_CACHE.clear()

    index = {}
    for c in landscape:
        for sub in c['subcategories']:
            for item in sub['items']:
                if _is_valid_item(item):
                    name = item['name']
                    if not name:
                        continue
                    first_char = name[0]
                    if first_char not in index:
                        index[first_char] = []
                    index[first_char].append(name)

    for k in index:
        index[k].sort()

    _TASKS_CACHE[lid] = index
    return index


def get_tasks_for_letter(x: str, landscape: list) -> list:
    """
    Return task names that match a given prefix, using a cached index for performance.

    The function builds (and reuses) an internal cache of task names indexed by their
    first character for the provided ``landscape``. Subsequent calls with the same
    ``landscape`` reuse this cache to avoid repeatedly traversing all items.

    Behavior by input ``x``:
    - If ``x`` is an empty string or otherwise falsy, all task names for the given
      ``landscape`` are returned as a single sorted list.
    - If ``x`` is a single character, all task names whose first character matches
      that character are returned. These names are drawn from the cached index and
      are already sorted.
    - If ``x`` has multiple characters, only task names that start with the full
      prefix ``x`` are returned (filtered from the single-character bucket).

    Note:
    - Only valid items (as determined by ``_is_valid_item``) are considered.
    - The function returns a list of task names (strings), not the full item objects.
    """
    logger.info(f"Getting tasks for letter {x}")
    index = _get_cached_tasks_index(landscape)

    if not x:
        # Return all tasks if x is empty string
        all_tasks = []
        for tasks in index.values():
            all_tasks.extend(tasks)
        return sorted(all_tasks)

    first_char = x[0]
    potential_tasks = index.get(first_char, [])

    if len(x) == 1:
        return list(potential_tasks)

    # For multi-character prefixes, we filter the pre-sorted bucket for the first
    # character. This preserves sorted order because `_get_cached_tasks_index`
    # sorts each list of names for a given first character (see line 73).
    return [t for t in potential_tasks if t.startswith(x)]

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

    # Initialize partial dicts with empty lists for all paths
    for letter in index:
        for path in all_paths:
            index[letter]['partial'][path] = []

    # Iterate landscape once
    for c in landscape:
        for sub in c['subcategories']:
            path = make_path(c['name'], sub['name'])
            for item in sub['items']:
                if _is_valid_item(item):
                    name = item['name']
                    if not name:
                        continue
                    first_char = name[0]
                    if 'A' <= first_char <= 'Z':
                         index[first_char]['partial'][path].append(item)
                         index[first_char]['tasks'].append(name)

    # Sort tasks
    for letter in index:
        index[letter]['tasks'].sort()

    return index
