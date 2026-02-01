import os
from pydantic_ai import Agent
from src.agentic.models import BlogPostDraft, WriterDeps
from src.agentic.tools.tracker import update_tracker_status
from src.agentic.config import get_model

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

writer_agent.tool(update_tracker_status)

