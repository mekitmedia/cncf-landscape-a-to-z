from prefect import flow, task
from src.agentic.agents import ResearcherAgent, WriterAgent
from typing import List

@task
async def research_project(project_name: str):
    agent = ResearcherAgent()
    return await agent.research(project_name)

@task
async def write_content(research_data: dict):
    agent = WriterAgent()
    return await agent.draft(research_data)

@flow(name="content-generation-flow")
async def generate_content(projects: List[str]):
    for project in projects:
        research_data = await research_project(project)
        content = await write_content(research_data)
        print(f"Generated content for {project}:\n{content}")

if __name__ == "__main__":
    import asyncio
    # Example run
    asyncio.run(generate_content(["Example Project"]))
