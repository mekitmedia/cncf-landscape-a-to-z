import os
from typing import List
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from src.agentic.models import BlogPostDraft, ResearchOutput

def get_model():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY environment variable is not set; cannot initialize GoogleModel for writer_agent."
        )
    return GoogleModel('gemini-1.5-flash')

model = get_model()

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
