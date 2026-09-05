# Justfile for common tasks

set dotenv-load := false
set export


# Global env vars
GEMINI_MODEL := env_var_or_default("GEMINI_MODEL", "gemini-2.5-flash")

# Show available recipes
help:
    @just --list

# Create virtual environment (uv)
venv:
    uv venv .venv

# Install Python dependencies using uv
install:
    uv sync

# Internal helper to auto-wrap execution with 1Password CLI if .env contains op:// references
_run +cmd:
    #!/usr/bin/env bash
    env_file=""
    if [ -f ".env" ]; then
        env_file=".env"
    elif [ -f "../.env" ]; then
        env_file="../.env"
    elif [ -f "../../.env" ]; then
        env_file="../../.env"
    fi

    if [ -n "$env_file" ] && command -v op >/dev/null 2>&1 && grep -q "op://" "$env_file" 2>/dev/null; then
        if [ -z "$GOOGLE_API_KEY" ] || [[ "$GOOGLE_API_KEY" == op://* ]] || [ -z "$PYDANTIC_AI_GATEWAY_API_KEY" ] || [[ "$PYDANTIC_AI_GATEWAY_API_KEY" == op://* ]]; then
            op run --env-file="$env_file" -- {{cmd}}
            exit $?
        fi
    fi

    {{cmd}}

# Run ETL pipeline
etl:
    just _run uv run python -m src.cli run etl

# Run agentic workflow (optional limit, local)
workflow limit="" local="":
    #!/usr/bin/env bash
    raw_limit="{{limit}}"
    raw_local="{{local}}"
    clean_limit=$(echo "$raw_limit" | sed -E 's/^(limit=)?//')
    clean_local=$(echo "$raw_local" | sed -E 's/^(local=)?//')
    limit_arg=""
    if [ -n "$clean_limit" ]; then
        limit_arg="--limit=$clean_limit"
    fi
    if [ -n "$clean_local" ] && [ "$clean_local" != "false" ]; then
        export PREFECT_API_URL=""
    fi
    just _run uv run python -m src.cli run workflow $limit_arg

# Start Web UI for agent
ui agent="editor" port="8000":
    just _run uv run python -m src.cli run ui --agent={{agent}} --port={{port}}

# List available AI models
list-models:
    just _run uv run python scripts/list_models.py

# Alias for list-models
models:
    @just list-models

# Generate tool pages from research
tools:
    just _run uv run python -m src.pipeline.tool_pages


# Run unit tests
test:
    PYTHONPATH=. uv run pytest tests/

# Validate content contract against Pydantic models (e.g. just validate week=00-A)
validate week="" ref="":
    @uv run python scripts/validate_contract.py {{ if week != "" { "--week " + week } else if ref != "" { "--git-diff " + ref } else { "--git-diff origin/main" } }}

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

