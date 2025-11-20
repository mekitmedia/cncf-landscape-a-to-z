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
            'category_index.yaml': {'Category 1': {'Subcategory 1': 'category_1_subcategory_1'}, 'Category 2': {'Subcategory 2': 'category_2_subcategory_2'}},
            'category_item_index.yaml': {'Category 1': {'Subcategory 1': ['Item 1', 'Another Item', 'An item starting with A']}, 'Category 2': {'Subcategory 2': ['Item 3']}},
            'stats_by_status.yaml': {'graduated': 1},
            'excluded_items.yaml': ['Item 2 (no repo)', 'Item 4 (no repo)'],
            'week_00_A/category_1_subcategory_1.yaml': [{'name': 'Another Item', 'repo_url': 'https://github.com/another/item', 'project': 'graduated'}, {'name': 'An item starting with A', 'repo_url': 'https://github.com/a/item'}],
            'week_08_I/category_1_subcategory_1.yaml': [{'name': 'Item 1', 'repo_url': 'https://github.com/item1/item1'}],
            'week_08_I/category_2_subcategory_2.yaml': [{'name': 'Item 3', 'repo_url': 'https://github.com/item3/item3'}],
        }

        expected_tasks = {
            'week_00_A/tasks.yaml': [
                {'name': 'Another Item', 'repo_url': 'https://github.com/another/item', 'project': 'graduated', 'category': 'Category 1', 'subcategory': 'Subcategory 1'},
                {'name': 'An item starting with A', 'repo_url': 'https://github.com/a/item', 'category': 'Category 1', 'subcategory': 'Subcategory 1'}
            ],
            'week_08_I/tasks.yaml': [
                {'name': 'Item 1', 'repo_url': 'https://github.com/item1/item1', 'category': 'Category 1', 'subcategory': 'Subcategory 1'},
                {'name': 'Item 3', 'repo_url': 'https://github.com/item3/item3', 'category': 'Category 2', 'subcategory': 'Subcategory 2'}
            ]
        }

        cli = Cli()
        cli.run(input_path='tests/test_data/landscape_with_excluded.yml', output_dir=self.test_dir)

        # Check that the output files were created
        self.assertTrue(os.path.exists(f'{self.test_dir}/category_index.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/category_item_index.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/categories.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_per_category.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_per_category_per_week.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/stats_by_status.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/excluded_items.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/week_00_A/category_1_subcategory_1.yaml'))
        self.assertTrue(os.path.exists(f'{self.test_dir}/week_00_A/README.md'))

        # Check the content of the output files
        for file_path, expected_content in expected_outputs.items():
            with open(f'{self.test_dir}/{file_path}', 'r') as f:
                if file_path.endswith('.yaml'):
                    content = yaml.safe_load(f)
                    self.assertEqual(content, expected_content)

        # Check the content of the task files
        for file_path, expected_content in expected_tasks.items():
            self.assertTrue(os.path.exists(f'{self.test_dir}/{file_path}'))
            with open(f'{self.test_dir}/{file_path}', 'r') as f:
                content = yaml.safe_load(f)
                # Sort list of dicts by name to ensure order consistency for comparison
                content.sort(key=lambda x: x['name'])
                expected_content.sort(key=lambda x: x['name'])
                self.assertEqual(content, expected_content)

        # Check the content of the README.md file
        with open(f'{self.test_dir}/week_00_A/README.md', 'r') as f:
            content = f.read()
            self.assertIn('# Summary for week_00_A', content)
            # The summary now counts all yaml files, including tasks.yaml
            # 2 items in subcategory file + 2 items in tasks.yaml = 4 total items reported by current summary logic
            # We might want to adjust the summary logic later, but for now let's adjust the test expectation
            # or we can filter out tasks.yaml from the summary generation.
            # Given the user didn't ask to change summary logic, I will filter tasks.yaml in load.py
            # so that the summary remains about the content parts.
            self.assertIn('This week has a total of 2 items.', content)
            self.assertIn('- **Category 1 Subcategory 1**: 2 items', content)


if __name__ == '__main__':
    unittest.main()
