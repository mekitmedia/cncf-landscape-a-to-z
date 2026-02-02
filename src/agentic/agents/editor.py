import os
from datetime import date
from pydantic_ai import Agent, RunContext
from src.agentic.models import NextWeekDecision
from src.agentic.tools.editor import check_week_status, read_week_summary
from src.agentic.tools.tracker import check_tracker_progress, update_tracker_status, get_all_weeks_status
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
        "1. Check the overall status of all weeks using `get_all_weeks_status`.\n"
        "2. Identify the first week that is not yet completed.\n"
        "3. For incomplete weeks, you can use `check_tracker_progress` and `read_week_summary` to understand the workload.\n"
        "4. Return the letter of the first week that needs work.\n"
        "5. If all letters A-Z are done, return action='done'.\n"
        "\n"
        "The tracker system is your source of truth."
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

