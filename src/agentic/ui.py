# This file is used to run the agent UI
import uvicorn
from pydantic_ai import Agent

def create_app(agent_name: str, **kwargs):
    if agent_name == "researcher":
        from src.agentic.agents.researcher import researcher_agent
        return researcher_agent.to_web()
    elif agent_name == "writer":
        from src.agentic.agents.writer import writer_agent
        return writer_agent.to_web()
    elif agent_name == "editor":
        from src.agentic.agents.editor import editor_agent
        return editor_agent.to_web()
    else:
        raise ValueError(f"Unknown agent: {agent_name}")

def run_ui(agent_name: str, port: int = 8000):
    print(f"Starting UI for {agent_name} agent on port {port}...")
    # We need to construct the app. Since uvicorn expects an app instance or import string,
    # and to_web returns an ASGI app (Starlette), we can run it directly.
    app = create_app(agent_name)
    uvicorn.run(app, host="0.0.0.0", port=port)
