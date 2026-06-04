with open('src/pipeline/transform.py', 'r') as f:
    content = f.read()

old_get_items = """def get_items(landscape: list) -> dict:
    \"\"\"
    This function gets the items from the landscape data
    \"\"\"
    logger.info("Getting items from landscape data")
    return {
        c['name']: {
            sub['name']: [
                item['name'] for item in sub['items'] if _is_valid_item(item)
            ]
            for sub in c['subcategories']
        }
        for c in landscape
    }"""

new_get_items = """def get_items(landscape: list) -> dict:
    \"\"\"
    This function gets the items from the landscape data
    \"\"\"
    logger.info("Getting items from landscape data")
    return {
        c['name']: {
            sub['name']: [
                item['name'] for item in sub.get('items', []) if _is_valid_item(item)
            ]
            for sub in c.get('subcategories', [])
        }
        for c in landscape
    }"""

content = content.replace(old_get_items, new_get_items)

old_get_all_categories = """def get_all_categories(landscape: list) -> list:
    \"\"\"
    This function gets all the categories from the landscape data
    \"\"\"
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
    } for c in landscape]"""

new_get_all_categories = """def get_all_categories(landscape: list) -> list:
    \"\"\"
    This function gets all the categories from the landscape data
    \"\"\"
    logger.info("Getting all categories from landscape data")
    return [{
        'category': c['name'],
        'subcategories': [{
            'subcategory': sub['name'],
            'path': make_path(c['name'], sub['name']),
            'items': [
                item['name'] for item in sub.get('items', []) if _is_valid_item(item)
            ]
        } for sub in c.get('subcategories', [])]
    } for c in landscape]"""

content = content.replace(old_get_all_categories, new_get_all_categories)

old_get_categories = """def get_categories(landscape: list) -> dict:
    \"\"\"
    This function gets the categories from the landscape data
    \"\"\"
    logger.info("Getting categories from landscape data")
    return {
        c['name']: {
            sub['name']: make_path(c['name'], sub['name'])
            for sub in c['subcategories']
        }
        for c in landscape
    }"""

new_get_categories = """def get_categories(landscape: list) -> dict:
    \"\"\"
    This function gets the categories from the landscape data
    \"\"\"
    logger.info("Getting categories from landscape data")
    return {
        c['name']: {
            sub['name']: make_path(c['name'], sub['name'])
            for sub in c.get('subcategories', [])
        }
        for c in landscape
    }"""

content = content.replace(old_get_categories, new_get_categories)


old_get_only_letter = """def get_only_letter(x: str, landscape: list) -> dict:
    \"\"\"
    This function gets the letter we want, not best performance but does the job
    \"\"\"
    logger.info(f"Filtering landscape data for letter {x}")
    return {
        make_path(c['name'], sub['name']): [
            item for item in sub['items'] if item['name'].startswith(x) and _is_valid_item(item)
        ]
        for c in landscape for sub in c['subcategories']
    }"""

new_get_only_letter = """def get_only_letter(x: str, landscape: list) -> dict:
    \"\"\"
    This function gets the letter we want, not best performance but does the job
    \"\"\"
    logger.info(f"Filtering landscape data for letter {x}")
    return {
        make_path(c['name'], sub['name']): [
            item for item in sub.get('items', []) if item['name'].startswith(x) and _is_valid_item(item)
        ]
        for c in landscape for sub in c.get('subcategories', [])
    }"""
content = content.replace(old_get_only_letter, new_get_only_letter)

old_get_tasks_for_letter = """def get_tasks_for_letter(x: str, landscape: list) -> list:
    \"\"\"
    This function returns a list of tasks (items) for a specific letter
    \"\"\"
    logger.info(f"Getting tasks for letter {x}")
    tasks = []
    for c in landscape:
        for sub in c['subcategories']:
            for item in sub['items']:
                if item['name'].startswith(x) and _is_valid_item(item):
                    tasks.append(item['name'])
    return sorted(tasks)"""

new_get_tasks_for_letter = """def get_tasks_for_letter(x: str, landscape: list) -> list:
    \"\"\"
    This function returns a list of tasks (items) for a specific letter
    \"\"\"
    logger.info(f"Getting tasks for letter {x}")
    tasks = []
    for c in landscape:
        for sub in c.get('subcategories', []):
            for item in sub.get('items', []):
                if item['name'].startswith(x) and _is_valid_item(item):
                    tasks.append(item['name'])
    return sorted(tasks)"""

content = content.replace(old_get_tasks_for_letter, new_get_tasks_for_letter)

old_get_stats_by_status = """def get_stats_by_status(landscape: list) -> dict:
    \"\"\"
    This function gets the stats by status from the landscape data
    \"\"\"
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
    return stats"""

new_get_stats_by_status = """def get_stats_by_status(landscape: list) -> dict:
    \"\"\"
    This function gets the stats by status from the landscape data
    \"\"\"
    logger.info("Getting stats by status from landscape data")
    stats = {}
    for c in landscape:
        for sub in c.get('subcategories', []):
            for item in sub.get('items', []):
                if not _is_valid_item(item):
                    continue
                status = item.get('project')
                if status:
                    stats[status] = stats.get(status, 0) + 1
    return stats"""

content = content.replace(old_get_stats_by_status, new_get_stats_by_status)

old_get_landscape_by_letter = """    # Iterate landscape once, collecting by letter and path
    for c in landscape:
        for sub in c['subcategories']:
            path = make_path(c['name'], sub['name'])
            # Group items by first letter
            items_by_letter = {}
            for item in sub['items']:
                if _is_valid_item(item):
                    name = item['name']
                    if not name:
                        continue"""

new_get_landscape_by_letter = """    # Iterate landscape once, collecting by letter and path
    for c in landscape:
        for sub in c.get('subcategories', []):
            path = make_path(c['name'], sub['name'])
            # Group items by first letter
            items_by_letter = {}
            for item in sub.get('items', []):
                if _is_valid_item(item):
                    name = item['name']
                    if not name:
                        continue"""

content = content.replace(old_get_landscape_by_letter, new_get_landscape_by_letter)


old_get_items_without_repo_url = """def get_items_without_repo_url(landscape: list) -> list:
    \"\"\"
    This function returns a list of all items in the landscape that do not have a repo_url
    \"\"\"
    return sorted([
        item['name']
        for c in landscape
        for sub in c['subcategories']
        for item in sub['items']
        if item.get('repo_url') is None
    ])"""

new_get_items_without_repo_url = """def get_items_without_repo_url(landscape: list) -> list:
    \"\"\"
    This function returns a list of all items in the landscape that do not have a repo_url
    \"\"\"
    return sorted([
        item['name']
        for c in landscape
        for sub in c.get('subcategories', [])
        for item in sub.get('items', [])
        if item.get('repo_url') is None
    ])"""
content = content.replace(old_get_items_without_repo_url, new_get_items_without_repo_url)


old_get_stats_per_category = """def get_stats_per_category(landscape: list) -> dict:
    \"\"\"
    This function gets the stats per category from the landscape data
    \"\"\"
    logger.info("Getting stats per category from landscape data")
    return {c['name']: len(c['subcategories']) for c in landscape}"""
new_get_stats_per_category = """def get_stats_per_category(landscape: list) -> dict:
    \"\"\"
    This function gets the stats per category from the landscape data
    \"\"\"
    logger.info("Getting stats per category from landscape data")
    return {c['name']: len(c.get('subcategories', [])) for c in landscape}"""
content = content.replace(old_get_stats_per_category, new_get_stats_per_category)

old_get_stats_per_category_per_week = """def get_stats_per_category_per_week(landscape: list) -> dict:
    \"\"\"
    This function gets the stats per category per week from the landscape data
    \"\"\"
    logger.info("Getting stats per category per week from landscape data")
    stats_per_category = {c['name']: len(c['subcategories']) for c in landscape}"""
new_get_stats_per_category_per_week = """def get_stats_per_category_per_week(landscape: list) -> dict:
    \"\"\"
    This function gets the stats per category per week from the landscape data
    \"\"\"
    logger.info("Getting stats per category per week from landscape data")
    stats_per_category = {c['name']: len(c.get('subcategories', [])) for c in landscape}"""
content = content.replace(old_get_stats_per_category_per_week, new_get_stats_per_category_per_week)

old_all_paths = """    # Pre-calculate all paths
    all_paths = [
        make_path(c['name'], sub['name'])
        for c in landscape for sub in c['subcategories']
    ]"""

new_all_paths = """    # Pre-calculate all paths
    all_paths = [
        make_path(c['name'], sub['name'])
        for c in landscape for sub in c.get('subcategories', [])
    ]"""

content = content.replace(old_all_paths, new_all_paths)

with open('src/pipeline/transform.py', 'w') as f:
    f.write(content)
