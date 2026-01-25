import fire
import asyncio
from src.legacy_main import Cli as LegacyCli

class RunCommands:
    def etl(self, input_path="https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml", output_dir="data"):
        """Runs the legacy ETL pipeline."""
        LegacyCli().run(input_path, output_dir)

    def agent(self, name, port: int = 8000, **kwargs):
        """
        Starts the web UI for a specific agent.
        Usage: python src/cli.py run agent <name> [--port=8000]
        """
        from src.agentic.ui import run_ui
        try:
            run_ui(name, port)
        except Exception as e:
            print(f"Error starting UI: {e}")

    def workflow(self, limit: int = None):
        """
        Runs the agentic workflow.
        Usage: python src/cli.py run workflow --limit=5
        """
        from src.agentic.flow import weekly_content_flow
        asyncio.run(weekly_content_flow(limit=limit))

class Cli:
    def __init__(self):
        self.run = RunCommands()

if __name__ == '__main__':
    fire.Fire(Cli)
