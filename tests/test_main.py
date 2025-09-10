import unittest
import tempfile
import shutil
import os
import yaml
from main import Cli

class TestMain(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_run_pipeline(self):
        cli = Cli()
        cli.run(input_path='tests/test_data/landscape.yml', output_dir=self.test_dir)

        # Check that the output files were created
        self.assertTrue(os.path.exists(f'{self.test_dir}/category_index.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/category_item_index.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/categories.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_per_category.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_per_category_per_week.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_by_status.yaml'))

        # Check the content of the output files
        with open(f'{self.test_dir}/category_index.yaml', 'r') as f:
            category_index = yaml.safe_load(f)
            self.assertEqual(category_index, {'Category 1': {'Subcategory 1': 'category_1_subcategory_1'}})

        with open(f'{self.test_dir}/category_item_index.yaml', 'r') as f:
            category_item_index = yaml.safe_load(f)
            self.assertEqual(category_item_index, {'Category 1': {'Subcategory 1': ['Item 1', 'Another Item', 'An item starting with A']}})

        with open(f'{self.test_dir}/stats_by_status.yaml', 'r') as f:
            stats_by_status = yaml.safe_load(f)
            self.assertEqual(stats_by_status, {'graduated': 1})

        # Check that the partial data was created correctly
        self.assertTrue(os.path.exists(f'{self.test_dir}/week_00_A/category_1_subcategory_1.yaml'))
        with open(f'{self.test_dir}/week_00_A/category_1_subcategory_1.yaml', 'r') as f:
            partial_data = yaml.safe_load(f)
            self.assertEqual(partial_data, [{'name': 'Another Item'}, {'name': 'An item starting with A'}])


if __name__ == '__main__':
    unittest.main()
