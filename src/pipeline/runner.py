from src.config import load_config, resolve_data_dirs
from src.pipeline.extract import get_landscape_data
from src.pipeline.transform import (
    get_categories,
    get_items,
    get_all_categories,
    get_stats_per_category,
    get_stats_per_category_per_week,
    get_stats_by_status,
    get_items_without_repo_url,
    get_landscape_by_letter,
)
from src.pipeline.load import (
    to_yaml,
    save_partial_data,
    generate_summary,
    save_tasks,
    generate_letter_pages,
)
from src.logger import get_logger

logger = get_logger(__name__)


def run_etl(
    input_path: str = "https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml",
    output_dir: str = "data",
):
    """Run the ETL pipeline and write outputs to disk."""
    cfg = load_config()
    if input_path == "https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml":
        input_path = cfg.landscape_source
    dirs = resolve_data_dirs(output_dir)

    logger.info("Starting landscape processing")
    landscape = get_landscape_data(input_path)

    categories = get_categories(landscape)
    to_yaml(categories, str(dirs["index"] / "category_index.yaml"))

    items = get_items(landscape)
    to_yaml(items, str(dirs["index"] / "category_item_index.yaml"))

    all_categories = get_all_categories(landscape)
    to_yaml(all_categories, str(dirs["index"] / "categories.yaml"))

    landscape_by_letter = get_landscape_by_letter(landscape)

    for letter_code in range(ord('A'), ord('Z') + 1):
        letter = chr(letter_code)
        index = letter_code - ord('A')

        letter_data = landscape_by_letter.get(letter, {'partial': {}, 'tasks': []})
        partial = letter_data['partial']
        tasks = letter_data['tasks']

        save_tasks(tasks, letter, index, output_dir)

        for key in partial:
            save_partial_data(key, partial, letter, index, output_dir)

    stats_per_category = get_stats_per_category(landscape)
    to_yaml(stats_per_category, str(dirs["stats"] / "stats_per_category.yaml"))

    stats_per_category_per_week = get_stats_per_category_per_week(landscape)
    to_yaml(stats_per_category_per_week, str(dirs["stats"] / "stats_per_category_per_week.yaml"))

    stats_by_status = get_stats_by_status(landscape)
    to_yaml(stats_by_status, str(dirs["stats"] / "stats_by_status.yaml"))

    excluded_items = get_items_without_repo_url(landscape)
    to_yaml(excluded_items, str(dirs["extras"] / "excluded_items.yaml"))

    summaries = generate_summary(output_dir, landscape_by_letter)

    # Save summaries to README.md in each week's directory
    for week_dir_name, content in summaries.items():
        summary_path = dirs["weeks"] / week_dir_name / "README.md"
        with open(summary_path, "w") as f:
            f.write(content)

    generate_letter_pages(summaries=summaries)

    logger.info("Landscape processing finished")