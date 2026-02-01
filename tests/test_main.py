import tempfile
import shutil
import os
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.legacy_main import Cli
from src.config import clear_config_cache

def test_run_pipeline():
    # Clear config cache to ensure test-specific paths are used
    clear_config_cache()
    
    test_dir = tempfile.mkdtemp()
    try:
        # Set test data directory to match the test output directory
        os.environ['TEST_DATA_DIR'] = test_dir
        # Use path relative to test file
        test_data_path = Path(__file__).parent / 'test_data' / 'landscape_with_excluded.yml'
        expected_outputs = {
            'index/category_index.yaml': {'Category 1': {'Subcategory 1': 'category_1_subcategory_1'}, 'Category 2': {'Subcategory 2': 'category_2_subcategory_2'}},
            'index/category_item_index.yaml': {'Category 1': {'Subcategory 1': ['Item 1', 'Another Item', 'An item starting with A']}, 'Category 2': {'Subcategory 2': ['Item 3']}},
            'stats/stats_by_status.yaml': {'graduated': 1},
            'extras/excluded_items.yaml': ['Item 2 (no repo)', 'Item 4 (no repo)'],
            'weeks/00-A/categories/category_1_subcategory_1.yaml': [
                {
                    'name': 'Another Item',
                    'repo_url': 'https://github.com/another/item',
                    'homepage_url': None,
                    'project': 'graduated',
                    'featured': True,
                },
                {
                    'name': 'An item starting with A',
                    'repo_url': 'https://github.com/a/item',
                    'homepage_url': None,
                    'project': None,
                    'featured': True,
                }
            ],
            'weeks/08-I/categories/category_1_subcategory_1.yaml': [
                {
                    'name': 'Item 1',
                    'repo_url': 'https://github.com/item1/item1',
                    'homepage_url': None,
                    'project': None,
                    'featured': True,
                }
            ],
            'weeks/08-I/categories/category_2_subcategory_2.yaml': [
                {
                    'name': 'Item 3',
                    'repo_url': 'https://github.com/item3/item3',
                    'homepage_url': None,
                    'project': None,
                    'featured': True,
                }
            ],
        }

        expected_tasks = {
            'weeks/00-A/tasks.yaml': [
                'An item starting with A',
                'Another Item'
            ],
            'weeks/08-I/tasks.yaml': [
                'Item 1',
                'Item 3'
            ]
        }

        with patch('src.pipeline.runner.generate_letter_pages') as mock_generate_letter_pages:
            mock_generate_letter_pages.return_value = None

            cli = Cli()
            cli.run(input_path=str(test_data_path), output_dir=test_dir)

            # Check that the output files were created
            assert os.path.exists(f'{test_dir}/index/category_index.yaml')
            assert os.path.exists(f'{test_dir}/index/category_item_index.yaml')
            assert os.path.exists(f'{test_dir}/index/categories.yaml')
            assert os.path.exists(f'{test_dir}/stats/stats_per_category.yaml')
            assert os.path.exists(f'{test_dir}/stats/stats_per_category_per_week.yaml')
            assert os.path.exists(f'{test_dir}/stats/stats_by_status.yaml')
            assert os.path.exists(f'{test_dir}/extras/excluded_items.yaml')
            assert os.path.exists(f'{test_dir}/weeks/00-A/categories/category_1_subcategory_1.yaml')
            assert os.path.exists(f'{test_dir}/weeks/00-A/README.md')

            # Check the content of the output files
            for file_path, expected_content in expected_outputs.items():
                with open(f'{test_dir}/{file_path}', 'r') as f:
                    if file_path.endswith('.yaml'):
                        content = yaml.safe_load(f)
                        assert content == expected_content

            # Check the content of the task files
            for file_path, expected_content in expected_tasks.items():
                assert os.path.exists(f'{test_dir}/{file_path}')
                with open(f'{test_dir}/{file_path}', 'r') as f:
                    content = yaml.safe_load(f)
                    # content is now a list of strings
                    content.sort()
                    expected_content.sort()
                    assert content == expected_content

            # Check the content of the README.md file
            with open(f'{test_dir}/weeks/00-A/README.md', 'r') as f:
                content = f.read()
                assert '# Summary for 00-A' in content
                # The summary now counts all yaml files, including tasks.yaml
                # 2 items in subcategory file + 2 items in tasks.yaml = 4 total items reported by current summary logic
                # We might want to adjust the summary logic later, but for now let's adjust the test expectation
                # or we can filter out tasks.yaml from the summary generation.
                # Given the user didn't ask to change summary logic, I will filter tasks.yaml in load.py
                # so that the summary remains about the content parts.
                assert 'This week has a total of 2 items.' in content
                assert '- **Category 1 Subcategory 1**: 2 items' in content
    finally:
        shutil.rmtree(test_dir)
