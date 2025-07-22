import fire
from src.pipeline.extract import get_landscape_data
from src.pipeline.transform import (
    get_categories,
    get_items,
    get_all_categories,
    get_only_letter,
    get_stats_per_category,
    get_stats_per_category_per_week,
    get_stats_by_status
)
from src.pipeline.load import to_yaml, save_partial_data
from src.logger import get_logger

logger = get_logger(__name__)

class Cli:
  def run(self):
    logger.info("Starting landscape processing")
    landscape = get_landscape_data("https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml")

    categories = get_categories(landscape)
    to_yaml(categories, "data/category_index.yaml")

    items = get_items(landscape)
    to_yaml(items, "data/category_item_index.yaml")

    all_categories = get_all_categories(landscape)
    to_yaml(all_categories, "data/categories.yaml")

    for letter_code in range(ord('A'), ord('Z') + 1):
        letter = chr(letter_code)
        index = letter_code - ord('A')
        partial = get_only_letter(letter, landscape)

        for key in partial:
            save_partial_data(key, partial, letter, index)

    stats_per_category = get_stats_per_category(landscape)
    to_yaml(stats_per_category, "data/stats_per_category.yaml")

    stats_per_category_per_week = get_stats_per_category_per_week(landscape)
    to_yaml(stats_per_category_per_week, "data/stats_per_category_per_week.yaml")

    stats_by_status = get_stats_by_status(landscape)
    to_yaml(stats_by_status, "data/stats_by_status.yaml")

    logger.info("Landscape processing finished")

if __name__ == '__main__':
  fire.Fire(Cli)
