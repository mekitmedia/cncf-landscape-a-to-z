import logfire
from src.agentic.tools.agents.editor import editor_agent
from src.agentic.models import NextWeekDecision

@logfire.instrument
async def determine_next_week() -> NextWeekDecision:
    """Determine the next week to process using the editor agent."""
    result = await editor_agent.run(
        "Please decide the next week to tackle.",
    )
    return result.data