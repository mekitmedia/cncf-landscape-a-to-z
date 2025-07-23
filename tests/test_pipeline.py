import yaml
import unittest
import tempfile
import shutil
from pathlib import Path
from src.processor import Processor
from src.transform import get_only_letter, get_categories, get_items, get_all_categories, get_stats_per_category, get_stats_by_status

class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.landscape_data = self._get_test_data()
        self.test_dir = Path(tempfile.mkdtemp())
        self.output_dir = self.test_dir / 'output'
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _get_test_data(self):
        with open('tests/test_data/landscape.yml', 'r') as f:
            return yaml.safe_load(f)['landscape']

    def test_feature_parity(self):
        # Run the old pipeline
        old_categories = get_categories(self.landscape_data)
        old_items = get_items(self.landscape_data)
        old_all_categories = get_all_categories(self.landscape_data)
        old_stats_per_category = get_stats_per_category(self.landscape_data)
        old_stats_by_status = get_stats_by_status(self.landscape_data)

        # Run the new pipeline
        processor = Processor("tests/test_data/landscape.yml")
        processor.run()
        new_categories = processor.transformed_data.get("categories")
        new_items = processor.transformed_data.get("items")
        new_all_categories = processor.transformed_data.get("all_categories")
        new_stats_per_category = processor.transformed_data.get("stats_per_category")
        new_stats_by_status = processor.transformed_data.get("stats_by_status")

        # Compare the results
        self.assertEqual(old_categories, new_categories)
        self.assertEqual(old_items, new_items)
        self.assertEqual(old_all_categories, new_all_categories)
        self.assertEqual(old_stats_per_category, new_stats_per_category)
        self.assertEqual(old_stats_by_status, new_stats_by_status)

    def test_output_files(self):
        # Run the new pipeline and save the output to the temporary directory
        processor = Processor("tests/test_data/landscape.yml")
        processor.save_results(self.output_dir)

        # Check that the output files are created
        self.assertTrue((self.output_dir / 'category_index.yaml').exists())
        self.assertTrue((self.output_dir / 'category_item_index.yaml').exists())
        self.assertTrue((self.output_dir / 'categories.yaml').exists())
        self.assertTrue((self.output_dir / 'stats_per_category.yaml').exists())
        self.assertTrue((self.output_dir / 'stats_by_status.yaml').exists())
        self.assertTrue((self.output_dir / 'stats_per_category_per_week.yaml').exists())

if __name__ == '__main__':
    unittest.main()
