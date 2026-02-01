from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectMetadata(BaseModel):
    name: str
    repo_url: Optional[str] = None
    homepage: Optional[str] = None

class ResearchOutput(BaseModel):
    project_name: str
    summary: str = Field(description="A concise summary of the project")
    key_features: List[str] = Field(description="List of key features")
    recent_updates: str = Field(description="Recent updates or news about the project")
    use_cases: str = Field(description="Common use cases")
    interesting_facts: Optional[str] = Field(None, description="Any interesting facts found")
    get_started: Optional[str] = Field(None, description="Getting started guide or quick start command")
    related_tools: Optional[List[str]] = Field(None, description="List of related tools or projects")

class BlogPostDraft(BaseModel):
    title: str
    content_markdown: str

class NextWeekDecision(BaseModel):
    week_letter: str = Field(..., description="The letter of the week to process (A-Z)")
    action: str = Field(..., description="Action to take: 'research_and_write' or 'done'")
    reason: str = Field(..., description="Reason for the decision")
