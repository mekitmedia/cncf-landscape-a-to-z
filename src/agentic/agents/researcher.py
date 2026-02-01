import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from src.agentic.models import ResearchOutput, ProjectMetadata
from src.agentic.tools.search import search_tool
from src.agentic.tools.tracker import update_tracker_status

def get_model():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable is not set. "
            "Cannot initialize GoogleModel for researcher_agent."
        )
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    return GoogleModel(model_name)

model = get_model()

researcher_agent = Agent(
    model,
    output_type=ResearchOutput,
    system_prompt=(
        "You are an expert software researcher. Your goal is to research a specific Cloud Native Computing Foundation (CNCF) project. "
        "Use the search tool to find the latest information, documentation, and news. "
        "Focus on technical details, recent updates, and why it matters. "
        "Use the update_tracker_status tool to mark your progress (in_progress at start, completed at end)."
    ),
    deps_type=ProjectMetadata
)

researcher_agent.tool(search_tool)
researcher_agent.tool(update_tracker_status)

