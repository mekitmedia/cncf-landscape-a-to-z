import os
from pydantic_ai import Agent, RunContext
from src.agentic.models import BlogPostDraft
from src.agentic.tools.tracker import update_tracker_status, get_ready_tasks
from src.agentic.config import get_model
from src.agentic.deps import WriterDeps
from src.tracker import get_tracker

from src.agentic.prompts import WRITER_SYSTEM_PROMPT

model = get_model('writer')

writer_agent = Agent(
    model,
    output_type=BlogPostDraft,
    system_prompt=WRITER_SYSTEM_PROMPT,
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


