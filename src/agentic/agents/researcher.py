import os
from pydantic_ai import Agent, RunContext, WebSearchTool, WebFetchTool
from src.agentic.models import ResearchOutput
from src.agentic.tools.tracker import update_tracker_status, get_ready_tasks, GetReadyTasksInput
from src.agentic.config import get_model
from src.agentic.deps import ResearcherDeps
from src.tracker import get_tracker

model = get_model('researcher')

researcher_agent = Agent(
    model,
    output_type=ResearchOutput,
    system_prompt=(
        "You are an expert software researcher. Your goal is to research a specific Cloud Native Computing Foundation (CNCF) project. "
        "Use web search to find the latest information, documentation, and news. "
        "Use web fetch to retrieve content from relevant pages. "
        "Focus on technical details, recent updates, and why it matters. "
        "Use the update_tracker_status tool to mark your progress (in_progress at start, completed at end)."
    ),
    deps_type=ResearcherDeps,
    builtin_tools=[WebSearchTool(), WebFetchTool()]
)

@researcher_agent.instructions
def add_research_context(ctx: RunContext[ResearcherDeps]) -> str:
    tracker = get_tracker(config=ctx.deps.config)
    progress = tracker.get_progress(ctx.deps.project.week_letter, "research")
    return (
        f"Current Project: {ctx.deps.project.name}\n"
        f"Week: {ctx.deps.project.week_letter}\n"
        f"Week Research Progress: {progress.completed}/{progress.total} projects completed."
    )

researcher_agent.tool(update_tracker_status)
researcher_agent.tool(get_ready_tasks)


