# AGENTS

Universal entrypoint for agent tooling and autonomous contributors in this repository.

## Skills Root
- Canonical skill location: `.agents/skills`
- Claude native path: `.claude/skills` (symlink)
- Codex/OpenAI native path: `.codex/skills` (symlink)
- OpenCode native path: `.opencode/skills` (symlink)

## Available Skills
- `cncf-weekly-content`: `.agents/skills/cncf-weekly-content/SKILL.md`
- `editorial-governance`: `.agents/skills/editorial-governance/SKILL.md`


## Supported Agent Harnesses
- **Claude Code**: Reads `.claude/skills` / `CLAUDE.md`.
- **GitHub Copilot**: Reads `.github/copilot-instructions.md` -> `.agents/skills/`.
- **KubeOpenCode**: Autonomous Kubernetes operator using `AgentTemplate`, `Agent`, and `CronTask` CRDs defined in `k8s/kubeopencode/` (see `docs/kubeopencode-agent-templates.md`). Supports Git auto-sync and reconciliation via Flux or `kubectl apply -k`.
- **Pydantic AI Agents**: Python runtime in `src/agentic/` loading canonical system prompts from `.agents/skills/cncf-weekly-content/prompts/`.
- **Codex / OpenCode**: Native skill symlinks in `.codex/skills` and `.opencode/skills`.
