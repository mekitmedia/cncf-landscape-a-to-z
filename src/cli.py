import sys
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
        import sys
        try:
            if local or not os.getenv('PREFECT_API_URL'):
                from src.agentic.runner import run_agentic_workflow
                asyncio.run(run_agentic_workflow(limit=limit))
            else:
                from src.agentic.flow import weekly_content_flow
                asyncio.run(weekly_content_flow(limit=limit))
        except RuntimeError as e:
            logger.error(f"\n❌ Configuration / Authentication Error:\n{e}\n")
            sys.exit(1)
        except Exception as e:
            err_str = str(e)
            if "API key" in err_str or "INVALID_ARGUMENT" in err_str or "400" in err_str:
                logger.error(
                    "\n❌ API Key Authentication Error: Invalid or missing API key.\n"
                    "If using 1Password CLI, run:\n"
                    "  op run -- just workflow\n"
                    "Or set GOOGLE_API_KEY / PYDANTIC_AI_GATEWAY_API_KEY in your environment.\n"
                )
                sys.exit(1)
            raise



class Cli:
    def __init__(self):
        self.run = RunCommands()

if __name__ == '__main__':
    setup_observability()
    try:
        fire.Fire(Cli)
    except RuntimeError as e:
        logger.error(f"\n❌ Configuration / Authentication Error:\n{e}\n")
        sys.exit(1)
    except Exception as e:
        err_str = str(e)
        if "API key" in err_str or "INVALID_ARGUMENT" in err_str or "400" in err_str:
            logger.error(
                "\n❌ API Key Authentication Error: Invalid or missing API key.\n"
                "If using 1Password CLI, run:\n"
                "  op run -- just workflow\n"
                "Or set GOOGLE_API_KEY / PYDANTIC_AI_GATEWAY_API_KEY in your environment.\n"
            )
            sys.exit(1)
        raise

