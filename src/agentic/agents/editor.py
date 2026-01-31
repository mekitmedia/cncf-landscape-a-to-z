import os
import glob
import logfire
from pathlib import Path
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from src.agentic.models import NextWeekDecision

def get_model():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable is not set. "
            "Cannot initialize the editor agent without a configured Gemini model."
        )
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    return GoogleModel(model_name)

model = get_model()

@logfire.instrument
def check_week_status(ctx: RunContext, week_letter: str) -> str:
    """Checks if the blog post for the given week letter exists."""
    # Validate input to prevent path traversal
    if not (len(week_letter) == 1 and 'A' <= week_letter <= 'Z'):
        return "Invalid week letter provided"
    
    posts_dir = "website/content/posts"
    if not os.path.exists(posts_dir):
        return "Posts directory not found"

    # Check for YYYY-{week_letter}.md
    pattern = os.path.join(posts_dir, f"*-{week_letter}.md")
    files = glob.glob(pattern)

    if files:
        return f"Exists: {files[0]}"
    return "Not Found"

@logfire.instrument
def check_todo(ctx: RunContext) -> str:
    """Reads the TODO.md file to track progress and memory across sessions."""
    todo_path = "TODO.md"
    if not os.path.exists(todo_path):
        return "TODO.md not found. You should create it to track progress."
    try:
        with open(todo_path, "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading TODO.md: {e}"

@logfire.instrument
def update_todo(ctx: RunContext, content: str) -> str:
    """Updates the TODO.md file with new notes or progress."""
    todo_path = "TODO.md"
    try:
        with open(todo_path, "w", encoding='utf-8') as f:
            f.write(content)
        return "TODO.md updated successfully"
    except Exception as e:
        return f"Error writing TODO.md: {e}"

@logfire.instrument
def read_week_summary(ctx: RunContext, week_letter: str) -> str:
    """Reads the README.md summary for a specific week's data to understand workload."""
    # Validate input to prevent path traversal
    if not (len(week_letter) == 1 and 'A' <= week_letter <= 'Z'):
        return "Invalid week letter provided"
    
    # Pattern: data/week_*_{week_letter}/README.md
    pattern = f"data/week_*_{week_letter}/README.md"
    files = glob.glob(pattern)
    if not files:
        return f"Summary for week {week_letter} not found in data/. ETL may not have run yet."

    try:
        with open(files[0], "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {files[0]}: {e}"

editor_agent = Agent(
    model,
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
