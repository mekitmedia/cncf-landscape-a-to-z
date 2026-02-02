from src.agentic.agents.editor import editor_agent
from src.agentic.models import NextWeekDecision
from src.config import load_config

from src.agentic.deps import AgentDeps

async def determine_next_week() -> NextWeekDecision:
    """Determine the next week to process using the editor agent."""
    cfg = load_config()
    deps = AgentDeps(config=cfg)
    result = await editor_agent.run(
        "Please decide the next week to tackle.",
        deps=deps
    )
    return result.data
