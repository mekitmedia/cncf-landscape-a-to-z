# Justfile for common tasks

set dotenv-load := false
set export

# Global env vars
GEMINI_MODEL := env_var_or_default("GEMINI_MODEL", "gemini-2.5-flash-lite")

# Show available recipes
help:
    @just --list

# Create virtual environment (uv)
venv:
    uv venv .venv

# Install Python dependencies using uv
install:
    uv sync

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

ui agent="editor" port="8000":
    uv run python -m src.cli run ui --agent={{agent}} --port={{port}}

# Generate tool pages from research
tools:
    uv run python -m src.pipeline.tool_pages

# Run unit tests
test:
    PYTHONPATH=. uv run pytest tests/

# Run e2e tests (headless)
e2e:
    npx playwright test

# Run e2e tests in headed mode
e2e-headed:
    npx playwright test --headed

# Run e2e tests with UI
e2e-ui:
    npx playwright test --ui

# Start Hugo site locally
hugo:
    hugo server -s website
