from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectMetadata(BaseModel):
    name: str
    repo_url: Optional[str] = None
    homepage: Optional[str] = None

class ResearchOutput(BaseModel):
    project_name: str
    summary: str
    key_features: List[str]
    recent_updates: str
    use_cases: str

class BlogPostDraft(BaseModel):
    title: str
    content_markdown: str
