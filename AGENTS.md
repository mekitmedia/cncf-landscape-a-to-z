# AGENTS

Universal entrypoint for agent tooling and coding standards in this repository.

## Coding Standards

### Strongly-Typed Pydantic Models & Secret Management
- **No Untyped Dicts for Settings/State**: Always use strongly-typed Pydantic models (`pydantic.BaseModel` and `pydantic_settings.BaseSettings`) instead of untyped `Dict[str, Any]` for settings, configuration, and status data structures.
- **Sensitive Data & API Keys**: Use `pydantic.SecretStr` for all API keys, tokens, and secrets. Do not write custom string masking/slicing functions (e.g. `mask_key`); rely on Pydantic native `SecretStr` string representation and `.get_secret_value()` getters.
- **Enum State & Provider Types**: Define explicit `str, Enum` classes (e.g. `ProviderType`) for states, categories, and provider options.

## Execution Personas & Operational Modes

When interacting with this repository, AI agents must distinguish between two operational personas based on the user's intent:

### 1. Content Contributor (Skill Mode)
- **Use Case**: When asked to directly research projects, update week tracker YAML files, or write weekly blog posts.
- **Tooling**: Use the skill located at `.agents/skills/cncf-weekly-content/SKILL.md`.
- **Action**: Execute content research, writing, and tracker updating directly within the workspace.

### 2. Workflow Developer & Tester (Codebase Mode)
- **Use Case**: When asked to develop, debug, test, or run the underlying Pydantic AI workflow codebase (`src/agentic/`).
- **Tooling**: Execute workflow and test commands via `just` / `uv`:
  - `just workflow`: Run the agentic workflow (e.g. `just workflow limit=1 local=true`).
  - `just test`: Run the unit test suite (`uv run pytest tests/`).
- **Action**: Always use `just` / `uv` for execution and run test suites to verify code logic after code changes.


## Skills Root
- Canonical skill location: `.agents/skills`
- Claude native path: `.claude/skills` (symlink)
- Codex/OpenAI native path: `.codex/skills` (symlink)
- OpenCode native path: `.opencode/skills` (symlink)

## Available Skills
- `cncf-weekly-content`: `.agents/skills/cncf-weekly-content/SKILL.md`

