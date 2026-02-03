import asyncio
import os
import glob
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from src.agentic.models import ProjectMetadata, BlogPostDraft
from src.agentic.config import get_model
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Judge Model
class EvaluationResult(BaseModel):
    score: int = Field(..., description="Score from 1 to 10")
    feedback: str = Field(..., description="Explanation of the score")

class ContentEvaluation(BaseModel):
    score: int = Field(..., description="Overall score from 1 to 10")
    tone_consistency: int = Field(..., description="Score 1-10 on how well the tone matches the reference")
    structure_quality: int = Field(..., description="Score 1-10 on structural organization")
    engagement: int = Field(..., description="Score 1-10 on how engaging the content is")
    specific_feedback: str = Field(..., description="Detailed feedback on what was good and what needs improvement")
    improvement_actions: List[str] = Field(..., description="List of specific actions to improve the post")

async def evaluate_researcher():
    # Import here to avoid crash if API key is missing during module load
    try:
        from src.agentic.agents.researcher import researcher_agent
    except Exception as e:
        logger.warning(f"Could not import researcher_agent: {e}")
        return

    try:
        model = get_model('evaluator')
    except RuntimeError as e:
        logger.warning(f"Skipping eval: {e}")
        return

    judge_agent = Agent(
        model,
        output_type=EvaluationResult,
        system_prompt="You are an impartial judge. Evaluate the research output based on accuracy, completeness, and clarity."
    )

    # Test Input
    test_item = ProjectMetadata(
        name="Kubernetes",
        repo_url="https://github.com/kubernetes/kubernetes",
        homepage="https://kubernetes.io",
        week_letter="K"
    )

    logger.info(f"Running ResearcherAgent for {test_item.name}...")
    try:
        from src.config import load_config
        from src.agentic.deps import ResearcherDeps
        cfg = load_config()
        deps = ResearcherDeps(project=test_item, config=cfg)
        result = await researcher_agent.run(
            f"Research the project: {test_item.name}",
            deps=deps
        )
        research_output = result.data
        logger.info(f"Research Output: {research_output}")

        # Evaluate
        logger.info("Evaluating output...")
        eval_result = await judge_agent.run(
            f"Evaluate this research output for project 'Kubernetes':\n{research_output.model_dump_json()}",
        )

        logger.info(f"Score: {eval_result.data.score}")
        logger.info(f"Feedback: {eval_result.data.feedback}")

    except Exception as e:
        logger.error(f"Eval failed: {e}")

def get_previous_post_content(current_letter: str) -> Optional[str]:
    """Retrieves the content of the blog post for the previous letter."""
    if not (len(current_letter) == 1 and 'A' <= current_letter <= 'Z'):
        logger.warning(f"Invalid letter: {current_letter}")
        return None

    if current_letter == 'A':
        return None # No previous letter

    prev_letter = chr(ord(current_letter) - 1)

    # Pattern: website/content/posts/YYYY-{prev_letter}.md
    pattern = f"website/content/posts/*-{prev_letter}.md"
    files = glob.glob(pattern)

    if not files:
        logger.warning(f"Previous post for letter {prev_letter} not found.")
        return None

    try:
        with open(files[0], "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading previous post: {e}")
        return None

async def evaluate_writer(draft: BlogPostDraft, current_letter: str):
    try:
        model = get_model('evaluator')
    except RuntimeError as e:
        logger.warning(f"Skipping writer eval: {e}")
        return

    reference_content = get_previous_post_content(current_letter)
    reference_text = f"Reference Content (Previous Week):\n{reference_content}" if reference_content else "Reference Content: None (First week or missing)"

    judge_agent = Agent(
        model,
        output_type=ContentEvaluation,
        system_prompt=(
            "You are a senior editor for a technical blog about Cloud Native technologies. "
            "Your task is to evaluate a blog post draft based on a provided reference (ground truth) or general quality standards if no reference is available.\n\n"
            "Rubric:\n"
            "1. Tone: Should be professional yet accessible. Consistent with reference if provided.\n"
            "2. Structure: Clear title, introduction, project sections.\n"
            "3. Engagement: Catchy title, interesting intro.\n"
            "4. Accuracy: No hallucinations (hard to check without context, but check for internal consistency)."
        )
    )

    logger.info(f"Evaluating draft for letter {current_letter}...")
    try:
        result = await judge_agent.run(
            f"Please evaluate the following draft.\n\n"
            f"{reference_text}\n\n"
            f"Draft Content:\nTitle: {draft.title}\n{draft.content_markdown}"
        )

        eval_data = result.data
        logger.info("Evaluation Result:")
        logger.info(f"Score: {eval_data.score}/10")
        logger.info(f"Tone: {eval_data.tone_consistency}/10")
        logger.info(f"Structure: {eval_data.structure_quality}/10")
        logger.info(f"Feedback: {eval_data.specific_feedback}")
        logger.info(f"Improvements: {eval_data.improvement_actions}")

        return eval_data

    except Exception as e:
        logger.error(f"Writer eval failed: {e}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Run researcher eval
    # asyncio.run(evaluate_researcher())

    # Run writer eval test
    mock_draft = BlogPostDraft(
        title="Week B: Better Backup",
        content_markdown="# Week B: Better Backup\n\nThis week we explore projects starting with B.\n\n## B-Project\nIt does cool stuff."
    )
    asyncio.run(evaluate_writer(mock_draft, "B"))
