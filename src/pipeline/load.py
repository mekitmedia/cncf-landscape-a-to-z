import yaml
from pathlib import Path
from src.config import load_config, resolve_data_dirs, week_id
from src.logger import get_logger
import jinja2

def get_old_items(output_dir: str = "data") -> dict:
    """Reads existing items from data/weeks/*/categories/*.yaml to capture state before the update"""
    old_items = {}
    dirs = resolve_data_dirs(output_dir)
    for yaml_file in dirs["weeks"].glob("*/categories/*.yaml"):
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    for item in data:
                        if 'name' in item:
                            old_items[item['name']] = item
        except Exception as e:
            logger.warning(f"Failed to load old item data from {yaml_file}: {e}")
    return old_items

def build_changelog(old_items: dict, new_items: dict, output_dir: str = "data"):
    """Compares old and new items to generate a changelog.md file"""
    logger.info("Building changelog...")

    added_tools = []
    removed_tools = []
    updated_tools = []

    # Check for added and updated tools
    for name, item in new_items.items():
        if name not in old_items:
            added_tools.append(item)
        else:
            old_item = old_items[name]
            changes = []

            # Check for project status changes
            if item.get('project') != old_item.get('project'):
                old_status = old_item.get('project') or 'None'
                new_status = item.get('project') or 'None'
                changes.append(f"Status changed from **{old_status}** to **{new_status}**")

            if changes:
                updated_tools.append({'item': item, 'changes': changes})

    # Check for removed tools
    for name, item in old_items.items():
        if name not in new_items:
            removed_tools.append(item)

    # Generate Markdown
    changelog = ["# Data Update Changelog\n"]

    if added_tools:
        changelog.append("## 🚀 Added Tools\n")
        for tool in sorted(added_tools, key=lambda x: x.get('name', '')):
            repo_link = f"([Repo]({tool['repo_url']}))" if tool.get('repo_url') else ""
            changelog.append(f"- **{tool.get('name')}** {repo_link}")
        changelog.append("\n")

    if removed_tools:
        changelog.append("## 🗑️ Removed Tools\n")
        for tool in sorted(removed_tools, key=lambda x: x.get('name', '')):
            changelog.append(f"- **{tool.get('name')}**")
        changelog.append("\n")

    if updated_tools:
        changelog.append("## 🔄 Updated Tools\n")
        for update in sorted(updated_tools, key=lambda x: x['item'].get('name', '')):
            tool = update['item']
            changes_str = ", ".join(update['changes'])
            changelog.append(f"- **{tool.get('name')}**: {changes_str}")
        changelog.append("\n")

    if not (added_tools or removed_tools or updated_tools):
        changelog.append("_No tool changes detected in this update._\n")

    # Write to file
    changelog_path = Path(output_dir) / "changelog.md"

    with open(changelog_path, 'w') as f:
        f.write("\n".join(changelog))
    logger.info(f"Changelog saved to {changelog_path}")

logger = get_logger(__name__)

def to_yaml(data: dict, path: str):
    """
    This function saves a dictionary to a yaml file
    """
    logger.info(f"Saving data to {path}")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w+') as file:
        yaml.dump(data, file)

def save_partial_data(key: str, partial_data: dict, letter: str, index: int, output_dir: str = "data"):
    """
    This function saves the partial data to a yaml file
    """
    dirs = resolve_data_dirs(output_dir)
    week_folder = dirs["weeks"] / week_id(letter)
    categories_dir = week_folder / "categories"
    categories_dir.mkdir(parents=True, exist_ok=True)
    path = categories_dir / f"{key}.yaml"
    logger.info(f"Saving partial data to {path}")
    with open(path, 'w+') as file:
        yaml.dump(partial_data[key], file)

def save_tasks(tasks: list, letter: str, index: int, output_dir: str = "data"):
    """
    This function saves the tasks for a specific week to a yaml file
    """
    dirs = resolve_data_dirs(output_dir)
    week_folder = dirs["weeks"] / week_id(letter)
    week_folder.mkdir(parents=True, exist_ok=True)
    path = week_folder / "tasks.yaml"
    logger.info(f"Saving tasks to {path}")
    with open(path, 'w+') as file:
        yaml.dump(tasks, file)

def generate_summary(output_dir: str = "data", landscape_by_letter: dict = None) -> dict:
    """
    This function generates a summary of the week's data and returns it as a dictionary.
    """
    template_loader = jinja2.FileSystemLoader(searchpath=str(load_config().templates_dir))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("weekly_summary.md.j2")

    summaries = {}

    if landscape_by_letter:
        for letter, data in landscape_by_letter.items():
            index = ord(letter) - ord('A')
            week_dir_name = f"{str(index).zfill(2)}-{letter}"
            week_dir = Path(output_dir) / "weeks" / week_dir_name

            if not week_dir.is_dir():
                continue

            items_per_category = {}
            total_items = 0

            partial = data.get('partial', {})
            for key, items in partial.items():
                if items:
                    category = key.replace('_', ' ').title()
                    item_count = len(items)
                    total_items += item_count
                    items_per_category[category] = item_count

            summary_content = template.render(
                week_name=week_dir_name,
                total_items=total_items,
                items_per_category=items_per_category
            )
            summaries[week_dir_name] = summary_content
        return summaries

    for week_dir in (Path(output_dir) / "weeks").glob("*-*"):
        if not week_dir.is_dir():
            continue

        items_per_category = {}
        total_items = 0

        categories_dir = week_dir / "categories"
        for yaml_file in categories_dir.glob("*.yaml"):
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    category = yaml_file.stem.replace('_', ' ').title()
                    item_count = len(data)
                    total_items += item_count
                    items_per_category[category] = item_count

        summary_content = template.render(
            week_name=week_dir.name,
            total_items=total_items,
            items_per_category=items_per_category
        )
        summaries[week_dir.name] = summary_content

    return summaries

def generate_letter_pages(output_dir: str = "website/content", summaries: dict = None):
    """
    Generates Hugo-style content pages for each letter A–Z under ``{output_dir}/letters/``.
    For each letter, this function creates a directory ``{output_dir}/letters/<LETTER>/`` containing an ``_index.md`` file.
    That file consists of YAML front matter with the fields:
    - ``title``: Human-readable title (e.g. "Week 1: Letter A").
    - ``letter``: The uppercase letter (A–Z).
    - ``week``: Zero-based week index (0–25).
    - ``data_key``: Key of the corresponding week's data directory, formatted as ``{week_num}-{letter}`` (e.g. ``00-A``).
    - ``layout``: The Hugo layout to use (set to ``"list"``).
    In addition, a root ``_index.md`` is created in ``{output_dir}/letters/`` that defines the "All Letters" section.
    """
    logger.info("Generating letter pages")
    letters_dir = Path(output_dir) / "letters"
    letters_dir.mkdir(parents=True, exist_ok=True)

    for letter_code in range(ord('A'), ord('Z') + 1):
        letter = chr(letter_code)
        index = letter_code - ord('A')
        week_num = str(index).zfill(2)
        week_key = f"{week_num}-{letter}"

        letter_dir = letters_dir / letter
        letter_dir.mkdir(exist_ok=True)

        summary = ""
        if summaries:
            summary = summaries.get(week_key, "")

        content = f"""---
title: "Letter {letter}: CNCF Projects Starting with {letter}"
letter: "{letter}"
week: {index}
data_key: "{week_key}"
layout: "list"
---

{summary}
"""
        with open(letter_dir / "_index.md", "w") as f:
            f.write(content)

    # Generate the root section index for letters
    content_root = """---
title: "All Letters"
layout: "list"
---
"""
    with open(letters_dir / "_index.md", "w") as f:
        f.write(content_root)
