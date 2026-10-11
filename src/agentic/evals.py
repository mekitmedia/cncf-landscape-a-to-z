import asyncio
import glob
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from src.agentic.config import get_model
from src.agentic.models import BlogPostDraft, ResearchOutput
from src.config import load_config

logger = logging.getLogger(__name__)


class ResearchEvaluation(BaseModel):
    score: int = Field(..., description="Overall score from 1 to 10")
    grounding_quality: int = Field(..., description="Score 1-10 on primary source citations and verifiable facts")
    technical_depth: int = Field(..., description="Score 1-10 on feature accuracy and ecosystem perspectives")
    specific_feedback: str = Field(..., description="Detailed feedback on strengths and gaps")
    improvement_actions: List[str] = Field(default_factory=list, description="Actionable recommendations")


class ContentEvaluation(BaseModel):
    score: int = Field(..., description="Overall score from 1 to 10")
    tone_consistency: int = Field(..., description="Score 1-10 matching the curated non-advocacy benchmark (e.g. Letter C)")
    structure_quality: int = Field(..., description="Score 1-10 on curation, featured sections, and concise overview")
    no_shadowing_compliance: int = Field(..., description="Score 1-10 on avoiding duplication of persistent tool pages")
    specific_feedback: str = Field(..., description="Detailed critique of the post")
    improvement_actions: List[str] = Field(default_factory=list, description="List of specific actions to improve the post")


def get_reference_post_content() -> Optional[str]:
    """Retrieves the benchmark post (Letter C: cruising-through-the-cs.md) as the gold standard."""
    benchmark_path = Path("website/content/posts/cruising-through-the-cs.md")
    if benchmark_path.exists():
        try:
            return benchmark_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Error reading benchmark post: {e}")
    return None


async def evaluate_research_file(file_path: Path) -> Optional[ResearchEvaluation]:
    """Ad-hoc evaluation of a saved research YAML artifact on disk."""
    if not file_path.exists():
        logger.error(f"Research file not found: {file_path}")
        return None

    try:
        model = get_model("evaluator")
    except RuntimeError as e:
        logger.error(f"Cannot initialize evaluator model: {e}")
        return None

    content_yaml = file_path.read_text(encoding="utf-8")

    judge_agent = Agent(
        model,
        output_type=ResearchEvaluation,
        system_prompt=(
            "You are a principal cloud-native software researcher and evaluator. "
            "Evaluate this saved research YAML file for a CNCF landscape project.\n\n"
            "Evaluation Rubric:\n"
            "1. Grounding & Citations: Presence of credible primary source URLs in `sources`, valid `latest_release` tags, and docs links.\n"
            "2. Technical Depth: Concrete features (`key_features`), real use cases (`use_cases`), and balanced `ecosystem_perspectives`.\n"
            "3. Factuality: Strictly factual, zero hallucinated release numbers or vague marketing claims.\n"
            "4. Provenance: Clear `last_researched_at` timestamp and schema completeness."
        ),
    )

    logger.info(f"Evaluating research artifact: {file_path}...")
    result = await judge_agent.run(f"Evaluate this saved research YAML artifact:\n\n```yaml\n{content_yaml}\n```")
    return result.data


async def evaluate_post_file(file_path: Path) -> Optional[ContentEvaluation]:
    """Ad-hoc evaluation of a saved weekly blog post markdown artifact against the Letter C benchmark."""
    if not file_path.exists():
        logger.error(f"Post file not found: {file_path}")
        return None

    try:
        model = get_model("evaluator")
    except RuntimeError as e:
        logger.error(f"Cannot initialize evaluator model: {e}")
        return None

    post_content = file_path.read_text(encoding="utf-8")
    benchmark_content = get_reference_post_content()
    ref_section = f"Benchmark Reference (Letter C):\n```markdown\n{benchmark_content}\n```\n\n" if benchmark_content else ""

    judge_agent = Agent(
        model,
        output_type=ContentEvaluation,
        system_prompt=(
            "You are a Managing Editor for the CNCF Landscape A-to-Z series. "
            "Evaluate this weekly blog post draft against our curated editorial standards.\n\n"
            "Evaluation Rubric:\n"
            "1. Tone & Non-Advocacy: Neutral, informative, inviting users to discover tools without marketing hyperbole.\n"
            "2. Curation vs Shadowing: Introduces key pillars and spotlights featured tools; avoids exhaustive dissertations that shadow persistent /tools/ pages.\n"
            "3. Frontmatter & Draft: Contains `draft: true` and `letter: \"<LETTER>\"`.\n"
            "4. Navigation & Links: Markdown links to persistent pages (`/letters/<LETTER>/` or `/tools/...`) and official project repos."
        ),
    )

    logger.info(f"Evaluating blog post artifact: {file_path}...")
    result = await judge_agent.run(
        f"{ref_section}Draft Post to Evaluate ({file_path.name}):\n```markdown\n{post_content}\n```"
    )
    return result.data


async def run_adhoc_eval(week: Optional[str] = None, agent: Optional[str] = None, limit: int = 5):
    """Run an ad-hoc evaluation sweep across saved research and post artifacts with optional provenance filters."""
    cfg = load_config()
    weeks_to_scan = [cfg.weeks_dir / week] if week else sorted(cfg.weeks_dir.glob("*-*"))

    evaluated_research = 0
    print(f"\n================ AD-HOC EVALUATION REPORT ================")
    print(f"Filter - Week: {week or 'All'} | Agent Provenance: {agent or 'All'} | Limit: {limit}\n")

    for week_dir in weeks_to_scan:
        if not week_dir.is_dir() or evaluated_research >= limit:
            continue

        # Check tracker for provenance filtering
        tracker_file = week_dir / "tracker.yaml"
        agent_item_map: Dict[str, str] = {}
        if tracker_file.exists():
            try:
                tracker_data = yaml.safe_load(tracker_file.read_text(encoding="utf-8")) or {}
                for item_name, item_info in tracker_data.get("items", {}).items():
                    assigned_agent = item_info.get("tasks", {}).get("research", {}).get("agent", "unknown")
                    agent_item_map[item_name] = assigned_agent
            except Exception:
                pass

        research_dir = week_dir / "research"
        if research_dir.exists():
            for r_file in sorted(research_dir.glob("*.yaml")):
                if evaluated_research >= limit:
                    break

                try:
                    r_data = yaml.safe_load(r_file.read_text(encoding="utf-8")) or {}
                    p_name = r_data.get("project_name", r_file.stem)
                    item_agent = r_data.get("provenance", {}).get("agent") or agent_item_map.get(p_name, "unknown")

                    if agent and agent.lower() not in item_agent.lower():
                        continue

                    eval_res = await evaluate_research_file(r_file)
                    if eval_res:
                        evaluated_research += 1
                        print(f"\n--- Research: {p_name} ({week_dir.name}) [Agent: {item_agent}] ---")
                        print(f"Overall Score: {eval_res.score}/10 | Grounding: {eval_res.grounding_quality}/10 | Depth: {eval_res.technical_depth}/10")
                        print(f"Feedback: {eval_res.specific_feedback}")
                        if eval_res.improvement_actions:
                            print(f"Action Items: {', '.join(eval_res.improvement_actions)}")
                except Exception as e:
                    logger.error(f"Error evaluating {r_file}: {e}")

    print(f"\nCompleted evaluation of {evaluated_research} artifacts.")
