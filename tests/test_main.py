import unittest
import tempfile
import shutil
import os
import yaml
from main import Cli

class TestMain(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.maxDiff = None

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_run_pipeline(self):
        expected_outputs = {
            'category_index.yaml': {'Category 1': {'Subcategory 1': 'category_1_subcategory_1'}},
            'category_item_index.yaml': {'Category 1': {'Subcategory 1': ['Item 1', 'Another Item', 'An item starting with A']}},
            'stats_by_status.yaml': {'graduated': 1},
            'week_00_A/category_1_subcategory_1.yaml': [{'name': 'Another Item'}, {'name': 'An item starting with A'}]
        }

        cli = Cli()
        cli.run(input_path='tests/test_data/landscape.yml', output_dir=self.test_dir)

        # Check that the output files were created
        self.assertTrue(os.path.exists(f'{self.test_dir}/category_index.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/category_item_index.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/categories.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_per_category.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_per_category_per_week.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_by_status.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/week_00_A/category_1_subcategory_1.yaml'))

        # Check the content of the output files
        for file_path, expected_content in expected_outputs.items():
            with open(f'{self.test_dir}/{file_path}', 'r') as f:
                content = yaml.safe_load(f)
                self.assertEqual(content, expected_content)


if __name__ == '__main__':
    unittest.main()
