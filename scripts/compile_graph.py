#!/usr/bin/env python3
"""
Build-step script that iterates through all tool markdown files in website/content/tools/,
extracts and validates frontmatter with Pydantic (ToolFrontmatter),
and compiles static/data/graph.json (and website/static/data/graph.json) containing nodes and directed edges.
"""

from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

import yaml
from pydantic import ValidationError

# Ensure repo root is in python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.graph import GraphEdge, GraphNode, GraphOutput, ToolFrontmatter


def extract_frontmatter(file_path: Path) -> dict:
    content = file_path.read_text(encoding="utf-8")
    match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError(f"No YAML frontmatter found in {file_path}")
    raw_yaml = match.group(1)
    data = yaml.safe_load(raw_yaml)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML frontmatter in {file_path}")
    return data


def parse_and_validate_tool(file_path: Path) -> Tuple[ToolFrontmatter, str]:
    raw_data = extract_frontmatter(file_path)
    if "name" not in raw_data:
        raw_data["name"] = raw_data.get("project_name") or raw_data.get("title") or file_path.stem
    if "primary_use_case" not in raw_data:
        desc = raw_data.get("description") or raw_data.get("title") or file_path.stem
        raw_data["primary_use_case"] = desc
    if "last_researched" not in raw_data:
        date_val = raw_data.get("date", "2026-01-01")
        raw_data["last_researched"] = str(date_val)[:10] if str(date_val) else "2026-01-01"

    tool = ToolFrontmatter.model_validate(raw_data)
    node_id = file_path.stem
    return tool, node_id


def compile_graph(tools_dir: Path) -> GraphOutput:
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []

    name_to_id = {}
    validated_tools: List[Tuple[ToolFrontmatter, str]] = []

    for file_path in sorted(tools_dir.glob("*.md")):
        try:
            tool, node_id = parse_and_validate_tool(file_path)
            validated_tools.append((tool, node_id))
            name_to_id[tool.name.lower()] = node_id
            name_to_id[node_id] = node_id
        except (ValueError, ValidationError) as exc:
            print(f"Error validating {file_path}: {exc}", file=sys.stderr)
            raise exc

    for tool, node_id in validated_tools:
        node = GraphNode(
            id=node_id,
            name=tool.name,
            cncf_status=tool.cncf_status,
            category=tool.category,
            layer=tool.layer,
            primary_use_case=tool.primary_use_case,
            tags=tool.tags,
            eval_status=tool.eval_status,
            confidence_score=tool.confidence_score,
            last_researched=tool.last_researched,
        )
        nodes.append(node)

        for target_name in tool.integrations:
            target_id = name_to_id.get(target_name.lower()) or target_name.lower().replace(" ", "_")
            edges.append(
                GraphEdge(
                    source=node_id,
                    target=target_id,
                    type="integration",
                )
            )

        for target_name in tool.alternatives:
            target_id = name_to_id.get(target_name.lower()) or target_name.lower().replace(" ", "_")
            edges.append(
                GraphEdge(
                    source=node_id,
                    target=target_id,
                    type="alternative",
                )
            )

    return GraphOutput(nodes=nodes, edges=edges)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    tools_dir = repo_root / "website" / "content" / "tools"

    if not tools_dir.exists():
        print(f"Tools directory not found at {tools_dir}", file=sys.stderr)
        sys.exit(1)

    graph_data = compile_graph(tools_dir)

    output_paths = [
        repo_root / "static" / "data" / "graph.json",
        repo_root / "website" / "static" / "data" / "graph.json",
    ]

    json_payload = graph_data.model_dump_json(indent=2)

    for path in output_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json_payload, encoding="utf-8")
        print(f"✓ Compiled graph data ({len(graph_data.nodes)} nodes, {len(graph_data.edges)} edges) -> {path}")


if __name__ == "__main__":
    main()
