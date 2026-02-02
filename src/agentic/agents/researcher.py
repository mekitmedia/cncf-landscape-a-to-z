import os
from pydantic_ai import Agent
from src.agentic.models import ResearchOutput
from src.agentic.tools.search import search_tool
from src.agentic.tools.tracker import update_tracker_status
from src.agentic.config import get_model
from src.agentic.deps import ResearcherDeps

model = get_model('researcher')

researcher_agent = Agent(
    model,
    output_type=ResearchOutput,
    system_prompt=(
        "You are an expert software researcher. Your goal is to research a specific Cloud Native Computing Foundation (CNCF) project. "
        "Use the search tool to find the latest information, documentation, and news. "
        "Focus on technical details, recent updates, and why it matters. "
        "Use the update_tracker_status tool to mark your progress (in_progress at start, completed at end)."
    ),
    deps_type=ResearcherDeps
)

researcher_agent.tool(search_tool)
researcher_agent.tool(update_tracker_status)

