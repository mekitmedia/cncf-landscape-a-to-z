import asyncio
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

async def process_project(project: str):
    research_data = await research_project(project)
    content = await write_content(research_data)
    print(f"Generated content for {project}:\n{content}")
    return content

@flow(name="content-generation-flow")
async def generate_content(projects: List[str]):
    await asyncio.gather(*(process_project(project) for project in projects))

if __name__ == "__main__":
    # Example run
    asyncio.run(generate_content(["Example Project"]))
