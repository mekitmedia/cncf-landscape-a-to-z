import pytest
from pathlib import Path
from pydantic import ValidationError

from src.pipeline.graph import GraphEdge, GraphNode, GraphOutput, ToolFrontmatter
from scripts.compile_graph import parse_and_validate_tool, compile_graph


def test_tool_frontmatter_valid():
    raw_data = {
        "name": "Test Tool",
        "cncf_status": "sandbox",
        "category": "orchestration",
        "layer": "runtime",
        "primary_use_case": "A test tool for cloud native workflows.",
        "integrations": ["kubernetes", "prometheus"],
        "alternatives": ["tool-a"],
        "tags": ["testing", "cncf"],
        "eval_status": "approved",
        "confidence_score": 5,
        "last_researched": "2026-10-05",
    }
    tool = ToolFrontmatter.model_validate(raw_data)
    assert tool.name == "Test Tool"
    assert tool.cncf_status == "sandbox"
    assert tool.confidence_score == 5
    assert tool.last_researched == "2026-10-05"


def test_tool_frontmatter_invalid_confidence_score():
    raw_data = {
        "name": "Invalid Tool",
        "primary_use_case": "Test",
        "confidence_score": 10,
        "last_researched": "2026-10-05",
    }
    with pytest.raises(ValidationError):
        ToolFrontmatter.model_validate(raw_data)


def test_tool_frontmatter_invalid_date():
    raw_data = {
        "name": "Invalid Date Tool",
        "primary_use_case": "Test",
        "last_researched": "invalid-date",
    }
    with pytest.raises(ValidationError):
        ToolFrontmatter.model_validate(raw_data)


def test_compile_graph_nodes_and_edges(tmp_path):
    tool_file = tmp_path / "test_tool.md"
    tool_file.write_text(
        """---
name: "Test Tool"
cncf_status: "graduated"
category: "observability"
primary_use_case: "Observability for testing."
integrations: ["Prometheus"]
alternatives: ["Thanos"]
tags: ["metrics"]
eval_status: "approved"
confidence_score: 4
last_researched: "2026-10-05"
---
# Test Tool
Content here.
""",
        encoding="utf-8",
    )

    graph = compile_graph(tmp_path)
    assert len(graph.nodes) == 1
    assert graph.nodes[0].id == "test_tool"
    assert graph.nodes[0].name == "Test Tool"
    assert len(graph.edges) == 2
    types = {e.type for e in graph.edges}
    assert "integration" in types
    assert "alternative" in types
