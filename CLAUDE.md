# CLAUDE

See [`AGENTS.md`](file:///home/xnok/.gemini/antigravity/worktrees/cncf-landscape-a-to-z/test_agentic_merge_workflow/AGENTS.md) for full agent execution personas and instructions.

## Operational Modes
- **Content Contributor (Skill Mode)**: Use `.claude/skills/cncf-weekly-content/SKILL.md` (symlinked to `.agents/skills`) when directly creating content or updating trackers.
- **Workflow Developer (Codebase Mode)**: Run `just workflow` to execute the Pydantic AI workflow (`src/agentic/`), and `just test` to run pytest suite.

## Coding & Testing Standards
- **Strongly-Typed Pydantic Models**: Use `BaseModel` and `BaseSettings` for settings, data structures, and state (no untyped dicts).
- **Secret Management**: Protect all API keys and credentials with `pydantic.SecretStr`. Rely on native `SecretStr` string representation instead of custom masking functions.
- **Agent Testing with Golden Stubs**: Always use `FunctionModel` / `TestModel` via `agent.override()` with golden responses instead of artificial mock objects.


