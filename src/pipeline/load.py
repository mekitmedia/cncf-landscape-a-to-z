import yaml
from pathlib import Path
from src.logger import get_logger
import jinja2

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
    path = Path(f'{output_dir}/week_{str(index).zfill(2)}_{letter}')
    path.mkdir(parents=True, exist_ok=True)
    path = path.joinpath(f"{key}.yaml")
    logger.info(f"Saving partial data to {path}")
    with open(path, 'w+') as file:
        yaml.dump(partial_data[key], file)

def save_tasks(tasks: list, letter: str, index: int, output_dir: str = "data"):
    """
    This function saves the tasks for a specific week to a yaml file
    """
    path = Path(f'{output_dir}/week_{str(index).zfill(2)}_{letter}')
    path.mkdir(parents=True, exist_ok=True)
    path = path.joinpath("tasks.yaml")
    logger.info(f"Saving tasks to {path}")
    with open(path, 'w+') as file:
        yaml.dump(tasks, file)

def generate_summary(output_dir: str = "data", landscape_by_letter: dict = None):
    """
    This function generates a summary.md file with a summary of the week's data.
    Note: Changed from README.md to summary.md to avoid conflicts with Hugo's
    data directory parsing, which tries to load all files including README.md.
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./src/templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("weekly_summary.md.j2")

    if landscape_by_letter:
        for letter, data in landscape_by_letter.items():
            index = ord(letter) - ord('A')
            week_dir_name = f"week_{str(index).zfill(2)}_{letter}"
            week_dir = Path(output_dir) / week_dir_name

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

            summary_path = week_dir / "summary.md"
            logger.info(f"Generating weekly summary at {summary_path}")
            with open(summary_path, 'w+') as f:
                f.write(summary_content)
        return

    for week_dir in Path(output_dir).glob("week_*"):
        if not week_dir.is_dir():
            continue

        items_per_category = {}
        total_items = 0

        for yaml_file in week_dir.glob("*.yaml"):
            # Skip tasks.yaml from the summary count as it duplicates items
            if yaml_file.name == "tasks.yaml":
                continue

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

        summary_path = week_dir / "summary.md"
        logger.info(f"Generating weekly summary at {summary_path}")
        with open(summary_path, 'w+') as f:
            f.write(summary_content)

def generate_letter_pages(output_dir: str = "website/content"):
    """
    Generates Hugo-style content pages for each letter A–Z under
    ``{output_dir}/letters/``.

    For each letter, this function creates a directory
    ``{output_dir}/letters/<LETTER>/`` containing an ``_index.md`` file.
    That file consists of YAML front matter with the fields:

    - ``title``: Human-readable title (e.g. "Week 1: Letter A").
    - ``letter``: The uppercase letter (A–Z).
    - ``week``: Zero-based week index (0–25).
    - ``data_key``: Key of the corresponding week's data directory,
      formatted as ``week_{week_num}_{letter}`` (e.g. ``week_00_A``),
      matching the directory names produced by the data pipeline
      (such as via ``save_partial_data`` / ``save_tasks``).
    - ``layout``: The Hugo layout to use (set to ``"list"``).

    In addition, a root ``_index.md`` is created in
    ``{output_dir}/letters/`` that defines the "All Letters" section.
    
    Args:
        output_dir: Base output directory path (default: "website/content")
    """
    logger.info("Generating letter pages")
    letters_dir = Path(output_dir) / "letters"
    letters_dir.mkdir(parents=True, exist_ok=True)

    for letter_code in range(ord('A'), ord('Z') + 1):
        letter = chr(letter_code)
        index = letter_code - ord('A')
        week_num = str(index).zfill(2)

        letter_dir = letters_dir / letter
        letter_dir.mkdir(exist_ok=True)

        content = f"""---
title: "Week {index + 1}: Letter {letter}"
letter: "{letter}"
week: {index}
data_key: "week_{week_num}_{letter}"
layout: "list"
---
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
