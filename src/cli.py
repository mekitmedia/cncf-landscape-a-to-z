import fire
import asyncio
import logging
import os
from pathlib import Path
from src.pipeline.runner import run_etl
from src.agentic.observability import setup_observability

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class RunCommands:
    def etl(self, input_path="https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml", output_dir="data"):
        """Runs the ETL pipeline."""
        run_etl(input_path=input_path, output_dir=output_dir)

    def models(self):
        """Lists available AI models and current configuration."""
        from scripts.list_models import list_models
        list_models()

    def ui(self, agent: str = "editor", port: int = 8000):
        """
        Starts the web UI for a specific agent using pydantic-ai.
        Users can chat with the agents through the web interface.
        
        Usage: python -m src.cli run ui [--agent=editor] [--port=8000]
        Available agents: editor, researcher, writer
        """
        from src.agentic.ui import run_ui
        try:
            run_ui(agent, port)
        except Exception as e:
            logger.error(f"Error starting UI: {e}")
            raise

    def workflow(self, limit: int | None = None, local: bool = False):
        """
        Runs the agentic workflow.
        
        Args:
            limit: Maximum number of items to process (default: unlimited)
            local: Run with Prefect's local execution mode (default: False for cloud)
        
        Usage: 
            python src/cli.py run workflow --limit=50 --local
            python src/cli.py run workflow --local
        """
        from src.agentic.flow import weekly_content_flow
        
        # Set Prefect to run locally if requested
        if local:
            os.environ['PREFECT_API_URL'] = ''  # Empty URL forces local execution
            logger.info("Running workflow in local mode")
        
        asyncio.run(weekly_content_flow(limit=limit))


class EvalCommands:
    def research(self, path: str):
        """
        Evaluate a single research YAML artifact on disk.
        Usage: python src/cli.py eval research data/weeks/00-A/research/aibrix.yaml
        """
        from src.agentic.evals import evaluate_research_file
        res = asyncio.run(evaluate_research_file(Path(path)))
        if res:
            print(f"\nEvaluation for {path}:")
            print(f"Score: {res.score}/10 | Grounding: {res.grounding_quality}/10 | Depth: {res.technical_depth}/10")
            print(f"Feedback: {res.specific_feedback}")
            if res.improvement_actions:
                print(f"Action Items: {', '.join(res.improvement_actions)}")

    def post(self, path: str):
        """
        Evaluate a weekly blog post markdown artifact against the Letter C curated benchmark.
        Usage: python src/cli.py eval post website/content/posts/2026-A.md
        """
        from src.agentic.evals import evaluate_post_file
        res = asyncio.run(evaluate_post_file(Path(path)))
        if res:
            print(f"\nEvaluation for {path}:")
            print(f"Score: {res.score}/10 | Tone: {res.tone_consistency}/10 | Structure: {res.structure_quality}/10")
            print(f"Feedback: {res.specific_feedback}")
            if res.improvement_actions:
                print(f"Action Items: {', '.join(res.improvement_actions)}")

    def sweep(self, week: str | None = None, agent: str | None = None, limit: int = 5):
        """
        Run an ad-hoc evaluation sweep across saved research artifacts filtered by week or agent provenance.
        Usage: 
            python src/cli.py eval sweep --agent=jules --limit=5
            python src/cli.py eval sweep --week=00-A
        """
        from src.agentic.evals import run_adhoc_eval
        asyncio.run(run_adhoc_eval(week=week, agent=agent, limit=limit))


class Cli:
    def __init__(self):
        self.run = RunCommands()
        self.eval = EvalCommands()


if __name__ == '__main__':
    setup_observability()
    fire.Fire(Cli)
