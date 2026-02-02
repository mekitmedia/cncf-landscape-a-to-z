from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.config import AppConfig
    from src.agentic.models import ProjectMetadata, ResearchOutput

@dataclass
class AgentDeps:
    config: AppConfig

@dataclass
class ResearcherDeps(AgentDeps):
    project: ProjectMetadata

@dataclass
class WriterDeps(AgentDeps):
    research_results: List[ResearchOutput]
    week_letter: str
