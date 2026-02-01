import fire
import asyncio
import logging
import os
import logfire
from src.pipeline.runner import run_etl

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

    def agent(self, name: str, port: int = 8000):
        """
        Starts the web UI for a specific agent using pydantic-ai-slim[web].
        Users can chat with the agents through the web interface.
        
        Usage: python src/cli.py run agent <name> [--port=8000]
        Available agents: editor, researcher, writer
        """
        from src.agentic.ui import run_ui
        try:
            run_ui(name, port)
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

class Cli:
    def __init__(self):
        self.run = RunCommands()

if __name__ == '__main__':
    # Configure Logfire if token is present
    if os.getenv('LOGFIRE_TOKEN'):
        try:
            logfire.configure()
            # Auto-instrument Pydantic and Pydantic AI
            logfire.instrument_pydantic()
            # Use 'if available' check or try/except block if concerned about version,
            # but dir() showed it exists.
            if hasattr(logfire, 'instrument_pydantic_ai'):
                logfire.instrument_pydantic_ai()
            logger.info("Logfire configured successfully.")
        except Exception as e:
            logger.error(f"Failed to configure Logfire: {e}")

    fire.Fire(Cli)
