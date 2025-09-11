import yaml
from pathlib import Path
from src.logger import get_logger

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

def generate_summary(output_dir: str = "data"):
    """
    This function generates a README.md file with a summary of the week's data.
    """
    for week_dir in Path(output_dir).glob("week_*"):
        if not week_dir.is_dir():
            continue

        summary = [f"# Summary for {week_dir.name}"]
        total_items = 0

        for yaml_file in week_dir.glob("*.yaml"):
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    category = yaml_file.stem.replace('_', ' ').title()
                    item_count = len(data)
                    total_items += item_count
                    summary.append(f"- **{category}**: {item_count} items")

        summary.insert(1, f"\nThis week has a total of {total_items} items.\n")

        readme_path = week_dir / "README.md"
        logger.info(f"Generating weekly summary at {readme_path}")
        with open(readme_path, 'w+') as f:
            f.write("\n".join(summary))
