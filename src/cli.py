import fire
import asyncio
import logging
import os
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
            import os
            os.environ['PREFECT_API_URL'] = ''  # Empty URL forces local execution
            logger.info("Running workflow in local mode")
        
        asyncio.run(weekly_content_flow(limit=limit))

    def draw(self, week: str | None = None, format: str = "prompt", allow_adhoc: bool = True):
        """
        Draw a project task via ad-hoc queue or weighted roulette.
        
        Args:
            week: Optional week letter (A-Z) to restrict task selection.
            format: Output format ('prompt', 'json', 'yaml', 'dict').
            allow_adhoc: Whether to check ad-hoc priority queue first (default: True).
            
        Usage:
            python -m src.cli run draw
            python -m src.cli run draw --week=A --format=prompt
            python -m src.cli run draw --format=json
        """
        from src.roulette import draw_task
        task = draw_task(week_letter=week, allow_adhoc=allow_adhoc)
        if not task:
            print("No candidate tasks found.")
            return

        if format.lower() == "json":
            print(task.to_json())
        elif format.lower() == "dict":
            print(task.to_dict())
        elif format.lower() == "yaml":
            import yaml
            print(yaml.dump(task.to_dict(), default_flow_style=False))
        else:
            print(task.to_prompt())

    def roulette(self, week: str | None = None, format: str = "prompt", allow_adhoc: bool = True):
        """Alias for draw."""
        return self.draw(week=week, format=format, allow_adhoc=allow_adhoc)

class Cli:
    def __init__(self):
        self.run = RunCommands()


if __name__ == '__main__':
    setup_observability()
    fire.Fire(Cli)
