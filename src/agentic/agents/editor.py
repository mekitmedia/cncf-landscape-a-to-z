import os
from datetime import date
from pydantic_ai import Agent, RunContext
from src.agentic.models import NextWeekDecision
from src.agentic.tools.editor import check_week_status, read_week_summary
from src.agentic.tools.tracker import check_tracker_progress, update_tracker_status, get_all_weeks_status, get_ready_tasks, GetAllWeeksStatusInput
from src.agentic.config import get_model
from src.agentic.deps import AgentDeps

model = get_model('editor')

editor_agent = Agent(
    model,
    deps_type=AgentDeps,
    output_type=NextWeekDecision,
    system_prompt=(
        "You are the Managing Editor for the CNCF Landscape A to Z blog series. "
        "Your job is to decide which week (Letter A-Z) to tackle next based on the tracker status. "
        "\n\n"
        "Process:\n"
        "1. Use `get_all_weeks_status` to get all incomplete weeks (context-optimized).\n"
        "2. Return the first incomplete week letter from the list.\n"
        "3. If no incomplete weeks are returned, return action='done'.\n"
        "\n"
        "Keep decisions simple and efficient. Do NOT use check_tracker_progress or read_week_summary; "
        "the status from get_all_weeks_status is sufficient."
    ),
)

@editor_agent.instructions
def add_editor_context(ctx: RunContext[AgentDeps]) -> str:
    return f"Today's date is {date.today()}. You are managing the editorial calendar."

editor_agent.tool(check_week_status)
editor_agent.tool(read_week_summary)
editor_agent.tool(check_tracker_progress)
editor_agent.tool(update_tracker_status)
editor_agent.tool(get_all_weeks_status)
editor_agent.tool(get_ready_tasks)


