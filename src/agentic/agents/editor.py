import os
from pydantic_ai import Agent
from src.agentic.models import NextWeekDecision
from src.agentic.tools.editor import check_week_status, check_todo, update_todo, read_week_summary
from src.agentic.tools.tracker import check_tracker_progress
from src.agentic.config import get_model
from src.agentic.deps import AgentDeps

model = get_model('editor')

editor_agent = Agent(
    model,
    deps_type=AgentDeps,
    output_type=NextWeekDecision,
    system_prompt=(
        "You are the Managing Editor for the CNCF Landscape A to Z blog series. "
        "Your job is to decide which week (Letter A-Z) to tackle next. "
        "\n\n"
        "Process:\n"
        "1. Check TODO.md to see your notes and current progress. If it doesn't exist, you're starting fresh.\n"
        "2. Check the status of letters sequentially (A, B, C, etc.).\n"
        "3. For each incomplete letter, read its data summary (README.md) to understand the workload.\n"
        "4. Consider that each week can have up to 50 items.\n"
        "5. Update TODO.md with your notes about which weeks are done and which are in progress.\n"
        "6. Return the first letter that needs work.\n"
        "7. If all letters A-Z are done, return action='done'.\n"
        "\n"
        "Use TODO.md as your memory between runs to track progress efficiently."
    ),
)

editor_agent.tool(check_week_status)
editor_agent.tool(check_todo)
editor_agent.tool(update_todo)
editor_agent.tool(read_week_summary)
editor_agent.tool(check_tracker_progress)

