# AGENTS

Universal entrypoint for agent tooling and coding standards in this repository.

## Coding Standards

### Strongly-Typed Pydantic Models & Secret Management
- **No Untyped Dicts for Settings/State**: Always use strongly-typed Pydantic models (`pydantic.BaseModel` and `pydantic_settings.BaseSettings`) instead of untyped `Dict[str, Any]` for settings, configuration, and status data structures.
- **Sensitive Data & API Keys**: Use `pydantic.SecretStr` for all API keys, tokens, and secrets. Do not write custom string masking/slicing functions (e.g. `mask_key`); rely on Pydantic native `SecretStr` string representation and `.get_secret_value()` getters.
- **Enum State & Provider Types**: Define explicit `str, Enum` classes (e.g. `ProviderType`) for states, categories, and provider options.

## Skills Root
- Canonical skill location: `.agents/skills`
- Claude native path: `.claude/skills` (symlink)
- Codex/OpenAI native path: `.codex/skills` (symlink)
- OpenCode native path: `.opencode/skills` (symlink)

## Available Skills
- `cncf-weekly-content`: `.agents/skills/cncf-weekly-content/SKILL.md`
