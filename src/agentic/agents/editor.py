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

def check_todo(ctx: RunContext) -> str:
    """Reads the TODO.md file to track progress."""
    todo_path = "TODO.md"
    if not os.path.exists(todo_path):
        return "TODO.md not found. You should create it."
    with open(todo_path, "r") as f:
        return f.read()

def read_week_summary(ctx: RunContext, week_letter: str) -> str:
    """Reads the README.md summary for a specific week's data."""
    # Pattern: data/week_*_{week_letter}/README.md
    pattern = f"data/week_*_{week_letter}/README.md"
    files = glob.glob(pattern)
    if not files:
        return f"Summary for week {week_letter} not found in data/."

    with open(files[0], "r") as f:
        return f.read()

editor_agent = Agent(
    model,
    output_type=NextWeekDecision,
    system_prompt=(
        "You are the Managing Editor. Your job is to decide which week (Letter A-Z) to tackle next. "
        "1. Check the 'TODO.md' file to see current progress. "
        "2. If 'TODO.md' does not exist or is empty, assume you need to start from A. "
        "3. Check the status of letters sequentially. "
        "4. If a letter's blog post exists, check the next one. "
        "5. If you select a week, read its data summary (README.md in data folder) to understand the workload. "
        "Return the first letter that needs work. If all are done (A-Z), return action='done'."
    ),
)

editor_agent.tool(check_week_status)
editor_agent.tool(check_todo)
editor_agent.tool(read_week_summary)
