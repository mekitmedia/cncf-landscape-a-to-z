import os
import glob
from pydantic_ai import RunContext
from src.config import week_id
from src.agentic.deps import AgentDeps

def check_week_status(ctx: RunContext[AgentDeps], week_letter: str) -> str:
    """Checks if the blog post for the given week letter exists."""
    # Validate input to prevent path traversal
    if not (len(week_letter) == 1 and 'A' <= week_letter <= 'Z'):
        return "Invalid week letter provided"
    
    cfg = ctx.deps.config
    posts_dir = str(cfg.hugo_posts_dir)
    if not os.path.exists(posts_dir):
        return "Posts directory not found"

    # Check for YYYY-{week_letter}.md
    pattern = os.path.join(posts_dir, f"*-{week_letter}.md")
    files = glob.glob(pattern)

    if files:
        return f"Exists: {files[0]}"
    return "Not Found"

def check_todo(ctx: RunContext[AgentDeps]) -> str:
    """Reads the TODO.md file to track progress and memory across sessions."""
    cfg = ctx.deps.config
    todo_path = str(cfg.todo_path)
    if not os.path.exists(todo_path):
        return "TODO.md not found. You should create it to track progress."
    try:
        with open(todo_path, "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading TODO.md: {e}"

def update_todo(ctx: RunContext[AgentDeps], content: str) -> str:
    """Updates the TODO.md file with new notes or progress."""
    cfg = ctx.deps.config
    todo_path = str(cfg.todo_path)
    try:
        with open(todo_path, "w", encoding='utf-8') as f:
            f.write(content)
        return "TODO.md updated successfully"
    except Exception as e:
        return f"Error writing TODO.md: {e}"

def read_week_summary(ctx: RunContext[AgentDeps], week_letter: str) -> str:
    """Reads the README.md summary for a specific week's data to understand workload."""
    # Validate input to prevent path traversal
    if not (len(week_letter) == 1 and 'A' <= week_letter <= 'Z'):
        return "Invalid week letter provided"
    
    # Pattern: data/weeks/XX-Letter/README.md
    cfg = ctx.deps.config
    week_folder = cfg.weeks_dir / week_id(week_letter)
    pattern = str(week_folder / "README.md")
    files = glob.glob(pattern)
    if not files:
        return f"Summary for week {week_letter} not found in data/. ETL may not have run yet."

    try:
        with open(files[0], "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {files[0]}: {e}"
