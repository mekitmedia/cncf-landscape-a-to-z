from src.logger import get_logger
from src.transformer import Transformer
from src.extract import get_landscape_data
from src.load import to_yaml, save_partial_data

logger = get_logger(__name__)

class Processor:
    def __init__(self, landscape_url):
        self.landscape_url = landscape_url
        self.landscape_data = None
        self.transformed_data = {}

    def run(self):
        logger.info("Starting landscape processing pipeline...")
        self._extract()
        self._transform()
        logger.info("Landscape processing pipeline finished.")

    def save_results(self, output_dir='data'):
        if not self.landscape_data:
            self._extract()
        if not self.transformed_data:
            self._transform()
        self._load(output_dir)

    def _extract(self):
        logger.info("Extracting data...")
        self.landscape_data = get_landscape_data(self.landscape_url)

    def _transform(self):
        logger.info("Transforming data...")
        transformer = Transformer(self.landscape_data)
        self.transformed_data = transformer.transform()

    def _load(self, output_dir):
        logger.info("Loading data...")
        to_yaml(self.transformed_data.get("categories"), f"{output_dir}/category_index.yaml")
        to_yaml(self.transformed_data.get("items"), f"{output_dir}/category_item_index.yaml")
        to_yaml(self.transformed_data.get("all_categories"), f"{output_dir}/categories.yaml")
        to_yaml(self.transformed_data.get("stats_per_category"), f"{output_dir}/stats_per_category.yaml")
        to_yaml(self.transformed_data.get("stats_by_status"), f"{output_dir}/stats_by_status.yaml")
        self._save_weekly_stats(output_dir)
        self._save_letter_based_data(output_dir)

    def _save_weekly_stats(self, output_dir):
        stats_per_category_per_week = {
            f"week_{str(index).zfill(2)}_{chr(letter)}": self.transformed_data.get("stats_per_category")
            for index, letter in enumerate(range(ord('A'), ord('Z') + 1))
        }
        to_yaml(stats_per_category_per_week, f"{output_dir}/stats_per_category_per_week.yaml")

    def _save_letter_based_data(self, output_dir):
        from src.transform import get_only_letter
        for letter_code in range(ord('A'), ord('Z') + 1):
            letter = chr(letter_code)
            index = letter_code - ord('A')
            partial = get_only_letter(letter, self.landscape_data)

            for key in partial:
                save_partial_data(key, partial, letter, index, output_dir)
