# Justfile for common tasks

set dotenv-load := false

# Show available recipes
help:
    @just --list

# Create virtual environment (uv)
venv:
    uv venv .venv

# Install Python dependencies using uv
install:
    uv pip install --system -r requirements.txt
    uv pip install --system -r requirements-dev.txt

# Run ETL pipeline
etl:
    uv run python -m src.cli run etl

# Run agentic workflow (optional limit, local)
workflow limit="" local="":
    if [ -n "{{limit}}" ]; then \
        limit_arg="--limit={{limit}}"; \
    else \
        limit_arg=""; \
    fi; \
    if [ -n "{{local}}" ]; then \
        export PREFECT_API_URL=""; \
    fi; \
    uv run python -m src.cli run workflow $limit_arg

# Generate tool pages from research
tools:
    uv run python -m src.pipeline.tool_pages

# Run unit tests
test:
    uv run python -m unittest tests/test_main.py
