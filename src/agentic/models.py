from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict

class ProjectMetadata(BaseModel):
    name: str
    repo_url: Optional[str] = None
    homepage: Optional[str] = None
    week_letter: str = Field(..., description="The week letter this project belongs to")

class LatestRelease(BaseModel):
    version: Optional[str] = Field(None, description="Release version tag (e.g. v1.2.0)")
    date: Optional[str] = Field(None, description="Release date YYYY-MM-DD")
    url: Optional[str] = Field(None, description="Direct URL to release notes")

class SourceLink(BaseModel):
    label: str
    url: str

class GetStartedDetails(BaseModel):
    command: Optional[str] = Field(None, description="Quickstart CLI command or installation manifest")
    docs_url: Optional[str] = Field(None, description="Direct URL to official getting started documentation")

class ResearchOutput(BaseModel):
    project_name: str
    official_website: Optional[str] = Field(None, description="Official project website URL")
    repo_url: Optional[str] = Field(None, description="GitHub or primary source repository URL")
    cncf_status: Optional[str] = Field(None, description="CNCF status: graduated, incubating, sandbox, or non-cncf")
    summary: str = Field(..., description="A concise summary of the project")
    key_features: List[str] = Field(default_factory=list, description="List of key features")
    latest_release: Optional[Union[LatestRelease, str]] = Field(None, description="Latest release metadata or version string")
    recent_updates: str = Field(..., description="Recent updates or news about the project")
    use_cases: str = Field(..., description="Common use cases")
    interesting_facts: Optional[str] = Field(None, description="Any interesting facts found")
    get_started: Optional[Union[GetStartedDetails, Dict[str, str], str]] = Field(None, description="Getting started guide, dict, or command")
    related_tools: Optional[List[str]] = Field(default_factory=list, description="List of related tools or projects")
    sources: Optional[List[SourceLink]] = Field(default_factory=list, description="Ground truth primary source links")

class BlogPostDraft(BaseModel):
    title: str
    content_markdown: str

class WriterDeps(BaseModel):
    research_results: List[ResearchOutput]
    week_letter: str

class NextWeekDecision(BaseModel):
    week_letter: str = Field(..., description="The letter of the week to process (A-Z)")
    action: str = Field(..., description="Action to take: 'research_and_write' or 'done'")
    reason: str = Field(..., description="Reason for the decision")
