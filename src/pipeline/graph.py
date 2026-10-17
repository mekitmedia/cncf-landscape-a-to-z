from __future__ import annotations

import re
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


CNCFStatus = Literal["sandbox", "incubating", "graduated", "archived", "non-cncf"]


class ToolFrontmatter(BaseModel):
    name: str = Field(..., description="Tool name")
    cncf_status: CNCFStatus = Field(
        default="non-cncf", description="CNCF project status"
    )
    category: str = Field(default="", description="CNCF category")
    layer: str = Field(default="", description="CNCF layer")
    primary_use_case: str = Field(
        ..., description="1-sentence summary or primary use case"
    )
    integrations: List[str] = Field(
        default_factory=list, description="List of integrated tool names"
    )
    alternatives: List[str] = Field(
        default_factory=list, description="List of alternative tool names"
    )
    tags: List[str] = Field(default_factory=list, description="List of tags")
    eval_status: str = Field(default="pending_review", description="Evaluation status")
    confidence_score: int = Field(
        default=3, ge=1, le=5, description="Confidence score from 1 to 5"
    )
    last_researched: str = Field(
        ..., description="Date in YYYY-MM-DD format"
    )

    @field_validator("cncf_status", mode="before")
    @classmethod
    def normalize_cncf_status(cls, v: str) -> str:
        if not v or str(v).lower() in ("null", "none", ""):
            return "non-cncf"
        v_str = str(v).lower()
        if v_str in ("sandbox", "incubating", "graduated", "archived", "non-cncf"):
            return v_str
        return "non-cncf"

    @field_validator("last_researched")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        if not v:
            return "2026-01-01"
        if isinstance(v, str) and len(v) >= 10:
            date_part = v[:10]
            if re.match(r"^\d{4}-\d{2}-\d{2}$", date_part):
                return date_part
        raise ValueError(f"last_researched must be in YYYY-MM-DD format, got: {v}")


class GraphNode(BaseModel):
    id: str
    name: str
    cncf_status: str
    category: str
    layer: str
    primary_use_case: str
    tags: List[str]
    eval_status: str
    confidence_score: int
    last_researched: str


class GraphEdge(BaseModel):
    source: str
    target: str
    type: Literal["integration", "alternative"]


class GraphOutput(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
