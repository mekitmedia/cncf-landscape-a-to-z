import os
from pydantic_ai import Agent, RunContext
from src.agentic.models import BlogPostDraft
from src.agentic.tools.tracker import update_tracker_status, get_ready_tasks
from src.agentic.config import get_model
from src.agentic.deps import WriterDeps
from src.tracker import get_tracker

model = get_model('writer')

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

@writer_agent.instructions
def add_writer_context(ctx: RunContext[WriterDeps]) -> str:
    return (
        f"You are writing the blog post for Week: {ctx.deps.week_letter}.\n"
        f"You have research data for {len(ctx.deps.research_results)} projects."
    )

writer_agent.tool(update_tracker_status)
writer_agent.tool(get_ready_tasks)


