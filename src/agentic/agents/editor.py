import os
import glob
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from src.agentic.models import NextWeekDecision

def get_model():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return None
    return GeminiModel('gemini-1.5-flash', api_key=api_key)

model = get_model()

def check_week_status(ctx: RunContext, week_letter: str) -> str:
    """Checks if the blog post for the given week letter exists."""
    posts_dir = "website/content/posts"
    if not os.path.exists(posts_dir):
        return "Posts directory not found"

    # Check for YYYY-{week_letter}.md
    pattern = os.path.join(posts_dir, f"*-{week_letter}.md")
    files = glob.glob(pattern)

    if files:
        return f"Exists: {files[0]}"
    return "Not Found"

editor_agent = Agent(
    model,
    output_type=NextWeekDecision,
    system_prompt=(
        "You are the Managing Editor. Your job is to decide which week (Letter A-Z) to tackle next. "
        "Check the status of letters sequentially starting from A to Z. "
        "If a letter's blog post exists, check the next one. "
        "Return the first letter that needs work (i.e., does not exist). "
        "If all are done (A-Z), return action='done'."
    ),
)

editor_agent.tool(check_week_status)
