import asyncio
import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from src.agentic.agents import researcher_agent
from src.agentic.models import ProjectMetadata, ResearchOutput

# Judge Model
class EvaluationResult(BaseModel):
    score: int = Field(..., description="Score from 1 to 10")
    feedback: str = Field(..., description="Explanation of the score")

async def evaluate_researcher():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("GOOGLE_API_KEY not set, skipping eval.")
        return

    model = GeminiModel('gemini-1.5-flash', api_key=api_key)

    judge_agent = Agent(
        model,
        output_type=EvaluationResult,
        system_prompt="You are an impartial judge. Evaluate the research output based on accuracy, completeness, and clarity."
    )

    # Test Input
    test_item = ProjectMetadata(
        name="Kubernetes",
        repo_url="https://github.com/kubernetes/kubernetes",
        homepage="https://kubernetes.io"
    )

    print(f"Running ResearcherAgent for {test_item.name}...")
    try:
        # We assume the agent can use the search tool in this environment.
        result = await researcher_agent.run(
            f"Research the project: {test_item.name}",
            deps=test_item
        )
        research_output = result.data
        print("Research Output:", research_output)

        # Evaluate
        print("Evaluating output...")
        eval_result = await judge_agent.run(
            f"Evaluate this research output for project 'Kubernetes':\n{research_output.model_dump_json()}",
        )

        print(f"Score: {eval_result.data.score}")
        print(f"Feedback: {eval_result.data.feedback}")

    except Exception as e:
        print(f"Eval failed: {e}")

if __name__ == "__main__":
    asyncio.run(evaluate_researcher())
