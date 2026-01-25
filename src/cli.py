import fire
import asyncio
from src.legacy_main import Cli as LegacyCli

class RunCommands:
    def etl(self, input_path="https://raw.githubusercontent.com/cncf/landscape/master/landscape.yml", output_dir="data"):
        """Runs the legacy ETL pipeline."""
        LegacyCli().run(input_path, output_dir)

    def agent(self, name, **kwargs):
        """
        Runs a specific agent.
        Usage: python src/cli.py run agent <name> --arg1=val1
        Example: python src/cli.py run agent researcher --project_name="Kubernetes"
        """
        import asyncio
        from src.agentic.agents.researcher import researcher_agent
        from src.agentic.models import ProjectMetadata

        async def run_agent():
            if name == "researcher":
                project_name = kwargs.get("project_name")
                if not project_name:
                    print("Error: --project_name is required for researcher agent.")
                    return

                # Create metadata
                item = ProjectMetadata(name=project_name)

                print(f"Running ResearcherAgent for {project_name}...")
                try:
                    result = await researcher_agent.run(
                        f"Research the project: {project_name}",
                        deps=item
                    )
                    print("Result:")
                    print(result.data)
                except Exception as e:
                    print(f"Error running agent: {e}")

            elif name == "writer":
                print("Writer agent CLI support is limited due to complex input requirements.")
            elif name == "editor":
                from src.agentic.agents.editor import editor_agent
                print("Running EditorAgent...")
                try:
                    result = await editor_agent.run("Please decide the next week to tackle.")
                    print("Result:")
                    print(result.data)
                except Exception as e:
                    print(f"Error running agent: {e}")
            else:
                print(f"Unknown agent: {name}")

        asyncio.run(run_agent())

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
