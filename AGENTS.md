# AGENTS

Universal entrypoint for agent tooling and autonomous contributors in this repository.

## Skills Root
- Canonical skill location: `.agents/skills`
- Claude native path: `.claude/skills` (symlink)
- Codex/OpenAI native path: `.codex/skills` (symlink)
- OpenCode native path: `.opencode/skills` (symlink)

## Available Skills
- `cncf-weekly-content`: `.agents/skills/cncf-weekly-content/SKILL.md`

## Supported Agent Harnesses
- **Claude Code**: Reads `.claude/skills` / `CLAUDE.md`.
- **GitHub Copilot**: Reads `.github/copilot-instructions.md` -> `.agents/skills/`.
- **Google Jules**: Invoked via `.github/workflows/jules_schedule.yml` using `.github/prompts/jules_prompt.md` (compiled from `.agents/skills/cncf-weekly-content/prompts/`).
- **Pydantic AI Agents**: Python runtime in `src/agentic/` loading canonical system prompts from `.agents/skills/cncf-weekly-content/prompts/`.
- **Codex / OpenCode**: Native skill symlinks in `.codex/skills` and `.opencode/skills`.
