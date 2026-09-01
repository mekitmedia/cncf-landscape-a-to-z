# CLAUDE

Use skills from `.claude/skills` (symlinked to `.agents/skills`).

Primary workflow skill in this repository:
- `cncf-weekly-content` → `.claude/skills/cncf-weekly-content/SKILL.md`

## Coding Standards

- **Strongly-Typed Pydantic Models**: Use `BaseModel` and `BaseSettings` for settings, data structures, and state (no untyped dicts).
- **Secret Management**: Protect all API keys and credentials with `pydantic.SecretStr`. Rely on native `SecretStr` string representation instead of custom masking functions.
