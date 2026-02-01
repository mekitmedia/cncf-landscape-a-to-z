import os
from typing import List
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from src.agentic.models import BlogPostDraft, ResearchOutput, WriterDeps
from src.tracker import get_tracker, TaskStatus
import logfire

def get_model():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable is not set; cannot initialize GoogleModel for writer_agent."
        )
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    return GoogleModel(model_name)

model = get_model()

@logfire.instrument
def update_tracker_status(ctx: RunContext, item_name: str, task_type: str, status: str, week_letter: str) -> str:
    """Update the tracker status for a task."""
    try:
        tracker = get_tracker()
        task_status = TaskStatus(status.lower())
        tracker.update_task(week_letter, item_name, task_type, task_status)
        return f"Updated {item_name} {task_type} to {status}"
    except Exception as e:
        return f"Failed to update tracker: {e}"

writer_agent = Agent(
    model,
    output_type=BlogPostDraft,
    system_prompt=(
        "You are a skilled technical writer. Your goal is to write a weekly blog post summarizing CNCF projects starting with a specific letter. "
        "You will receive research outputs and the week letter. "
        "Create an engaging, informative post in Markdown format. "
        "The post should have a catchy title and sections for each project. "
        "Do not invent information. Use the provided research. "
        "Use the update_tracker_status tool to mark blog_post as completed when done."
    ),
    deps_type=WriterDeps
)

writer_agent.tool(update_tracker_status)
