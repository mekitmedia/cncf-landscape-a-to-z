# Data Processing Pipeline

This document describes the data processing pipeline for the CNCF landscape data.

## Overview

The pipeline extracts data from the CNCF landscape YAML file, transforms it, and saves it in a structured format in the `data` directory.

## Inputs

The main input for the pipeline is the CNCF landscape YAML file. By default, it uses the official landscape file from the CNCF GitHub repository: `https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml`.

The input can be configured by passing the `input_path` parameter to the `run` command. This can be a URL or a local file path.

## Outputs

The pipeline generates several YAML files in the `data` directory (or a configured output directory). These files contain the transformed data.

- `category_index.yaml`: An index of all categories and their subcategories.
- `category_item_index.yaml`: An index of all items in each category and subcategory.
- `categories.yaml`: A list of all categories with their subcategories and items.
- `stats_per_category.yaml`: Statistics about the number of subcategories per category.
- `stats_per_category_per_week.yaml`: Statistics about the number of subcategories per category, per week.
- `stats_by_status.yaml`: Statistics about the number of items per project status (e.g., graduated, incubating, sandbox).
- `week_*/`: A directory for each week, containing the items for each category and subcategory for that week.

## Assumptions

- The input data is a YAML file with a `landscape` key.
- The `landscape` key contains a list of categories.
- Each category has a `name` and a list of `subcategories`.
- Each subcategory has a `name` and a list of `items`.
- Each item has a `name` and an optional `project` status.
- Items with `project` status `archived` are ignored.

## Configurable Elements

- `input_path`: The path to the input landscape YAML file. Can be a URL or a local file path.
- `output_dir`: The directory where the output files will be saved. Defaults to `data`.

## How to Run

To run the pipeline with the default configuration, simply run the following command:

```bash
python main.py run
```

To run the pipeline with a custom input file and output directory, use the following command:

```bash
python main.py run --input_path /path/to/landscape.yml --output_dir /path/to/output
```
