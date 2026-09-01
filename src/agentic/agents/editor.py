import os
from datetime import date
from pydantic_ai import Agent, RunContext
from src.agentic.models import NextWeekDecision
from src.agentic.tools.editor import check_week_status, read_week_summary
from src.agentic.tools.tracker import check_tracker_progress, update_tracker_status, get_all_weeks_status, get_ready_tasks, GetAllWeeksStatusInput
from src.agentic.config import get_model
from src.agentic.deps import AgentDeps

from src.agentic.prompts import EDITOR_SYSTEM_PROMPT

model = get_model('editor')

editor_agent = Agent(
    model,
    deps_type=AgentDeps,
    output_type=NextWeekDecision,
    system_prompt=EDITOR_SYSTEM_PROMPT,
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


