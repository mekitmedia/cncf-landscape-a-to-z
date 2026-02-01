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
    uv pip install -r requirements.txt
    uv pip install -r requirements-dev.txt

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
    PYTHONPATH=. uv run pytest tests/
