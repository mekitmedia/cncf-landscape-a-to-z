import os
import logfire
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from duckduckgo_search import DDGS
from src.agentic.models import ResearchOutput, ProjectMetadata
from src.tracker import get_tracker, TaskStatus
import logging

# Setup logger
logger = logging.getLogger(__name__)

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

@logfire.instrument
def search_tool(ctx: RunContext, query: str) -> str:
    """Perform a web search using DuckDuckGo."""
    logger.info(f"Searching for: {query}")
    try:
        with DDGS() as ddgs:
            # limiting to 3 results to save tokens/time
            results = list(ddgs.text(query, max_results=3))
            return str(results)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"Search failed: {e}"

@logfire.instrument
def update_tracker_status(ctx: RunContext, item_name: str, task_type: str, status: str, week_letter: str) -> str:
    """Update the tracker status for a task."""
    try:
        tracker = get_tracker()
        task_status = TaskStatus(status.lower())
        tracker.update_task(week_letter, item_name, task_type, task_status)
        return f"Updated {item_name} {task_type} to {status}"
    except Exception as e:
        logger.error(f"Failed to update tracker: {e}")
        return f"Failed to update tracker: {e}"

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
