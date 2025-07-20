# CNCF Landscape CLI

This CLI provides a set of tools for analyzing the CNCF landscape. It fetches the latest landscape data from the official CNCF repository and processes it into a series of YAML files, making it easier to analyze the different categories and projects within the CNCF ecosystem.

## Features

- Fetches the latest CNCF landscape data.
- Generates a consolidated index of all categories, subcategories, and their items in `data/categories.yaml`.
- Splits the landscape into individual YAML files, organized by the first letter of the project name.

## Usage

To run the CLI, simply execute the following command:

```bash
python src/cli.py run
```

This will generate the following files:

- `data/categories.yaml`: A consolidated index of all categories, subcategories, and their items.
- `data/category_index.yaml`: An index of all categories and their sanitized names.
- `data/category_item_index.yaml`: An index of all categories and their items.
- `data/week_*/`: A series of directories containing individual YAML files for each subcategory, organized by the first letter of the project name.
