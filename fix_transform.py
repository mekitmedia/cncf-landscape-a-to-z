with open('src/pipeline/transform.py', 'r') as f:
    content = f.read()

old_get_featured_priority = """def _get_featured_priority(item: dict) -> tuple:
    \"\"\"
    This function returns a priority tuple for featured selection.
    Priority: graduated > incubating > sandbox (alphabetically within same status)
    \"\"\"
    project_status = item.get('project', 'sandbox').lower()

    status_priority = {
        'graduated': 0,
        'incubating': 1,
        'sandbox': 2
    }

    priority = status_priority.get(project_status, 3)
    name = item.get('name', '')

    return (priority, name)"""

new_get_featured_priority = """def _get_featured_priority(item: dict) -> tuple:
    \"\"\"
    This function returns a priority tuple for featured selection.
    Priority: graduated > incubating > sandbox (alphabetically within same status)
    \"\"\"
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

    return (priority, name)"""

content = content.replace(old_get_featured_priority, new_get_featured_priority)

with open('src/pipeline/transform.py', 'w') as f:
    f.write(content)
