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

def generate_summary(output_dir: str = "data"):
    """
    This function generates a README.md file with a summary of the week's data.
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./src/templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("weekly_summary.md.j2")

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

        readme_path = week_dir / "README.md"
        logger.info(f"Generating weekly summary at {readme_path}")
        with open(readme_path, 'w+') as f:
            f.write(summary_content)
