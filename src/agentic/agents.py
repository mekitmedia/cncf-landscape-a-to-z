import os
from typing import List, Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
from duckduckgo_search import DDGS
from src.agentic.models import ResearchOutput, BlogPostDraft, NextWeekDecision, ProjectMetadata

def get_model():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        # Return None or a dummy if needed, but Agent expects a model.
        # We'll allow it to be None and let Agent init fail if it tries to use it,
        # or better, check if we are in a test env.
        # For now, let's try to return a valid object if possible or just None.
        return None
    return GeminiModel('gemini-1.5-flash', api_key=api_key)

model = get_model()

# --- Researcher Agent ---

def search_tool(ctx: RunContext, query: str) -> str:
    """Perform a web search using DuckDuckGo."""
    print(f"Searching for: {query}")
    try:
        with DDGS() as ddgs:
            # limiting to 3 results to save tokens/time
            results = list(ddgs.text(query, max_results=3))
            return str(results)
    except Exception as e:
        return f"Search failed: {e}"

researcher_agent = Agent(
    model,
    output_type=ResearchOutput,
    system_prompt=(
        "You are an expert software researcher. Your goal is to research a specific Cloud Native Computing Foundation (CNCF) project. "
        "Use the search tool to find the latest information, documentation, and news. "
        "Focus on technical details, recent updates, and why it matters."
    ),
    deps_type=ProjectMetadata
)

researcher_agent.tool(search_tool)

# --- Writer Agent ---

writer_agent = Agent(
    model,
    output_type=BlogPostDraft,
    system_prompt=(
        "You are a skilled technical writer. Your goal is to write a weekly blog post summarizing CNCF projects starting with a specific letter. "
        "You will receive a list of research outputs. "
        "Create an engaging, informative post in Markdown format. "
        "The post should have a catchy title and sections for each project. "
        "Do not invent information. Use the provided research."
    ),
    deps_type=List[ResearchOutput]
)

# --- Editor Agent ---

def check_week_status(ctx: RunContext, week_letter: str) -> str:
    """Checks if the blog post for the given week letter exists."""
    import glob
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
