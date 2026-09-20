from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any


class ProjectMetadata(BaseModel):
    name: str
    repo_url: Optional[str] = None
    homepage: Optional[str] = None
    week_letter: str = Field(..., description="The week letter this project belongs to")


class SourceLink(BaseModel):
    title: str = Field(..., description="Description or title of the source")
    url: str = Field(..., description="Direct URL to documentation, release, talk, etc.")


class LatestReleaseInfo(BaseModel):
    version: Optional[str] = Field(None, description="Latest verified release tag or version")
    date: Optional[str] = Field(None, description="Release date in ISO format or string")
    release_notes_url: Optional[str] = Field(None, description="Direct URL to official release notes")


class EcosystemPerspectives(BaseModel):
    strengths: Optional[str] = Field(None, description="Key technical strengths in the cloud-native ecosystem")
    considerations: Optional[str] = Field(None, description="Architectural tradeoffs, prerequisites, or considerations")
    community_discussions: Optional[List[str]] = Field(default_factory=list, description="Notable community references, talks, or evaluations")


class ResearchOutput(BaseModel):
    project_name: str
    homepage_url: Optional[str] = Field(None, description="Official project homepage URL")
    repo_url: Optional[str] = Field(None, description="Official source code repository URL")
    docs_url: Optional[str] = Field(None, description="Official documentation URL")
    cncf_status: Optional[str] = Field(None, description="CNCF project status (e.g. sandbox, incubating, graduated, member)")
    latest_release: Optional[Union[LatestReleaseInfo, Dict[str, Any], str]] = Field(None, description="Latest verified release details")
    summary: str = Field(description="A concise summary of the project")
    key_features: List[str] = Field(description="List of key features")
    recent_updates: str = Field(description="Recent updates or news about the project")
    use_cases: str = Field(description="Common use cases")
    ecosystem_perspectives: Optional[Union[EcosystemPerspectives, Dict[str, Any], str]] = Field(None, description="Neutral ecosystem fit, strengths, and tradeoffs")
    interesting_facts: Optional[str] = Field(None, description="Any interesting facts found")
    get_started: Optional[str] = Field(None, description="Getting started guide or quick start command")
    related_tools: Optional[List[str]] = Field(None, description="List of related tools or projects")
    sources: Optional[List[Union[SourceLink, Dict[str, str], str]]] = Field(default_factory=list, description="Primary source links for ground-truth citations")
    last_researched_at: Optional[str] = Field(None, description="ISO 8601 UTC timestamp of research execution")
    research_version: Optional[int] = Field(1, description="Schema/research iteration version")


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
