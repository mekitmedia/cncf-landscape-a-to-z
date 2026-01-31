# This file is used to run the agent UI
from src.logger import logger

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
    logger.info(f"Starting UI for {agent_name} agent on port {port}...")
    # pydantic-ai-slim[web] provides built-in web UI support
    # The to_web() method returns an ASGI app that can be run directly
    import uvicorn
    app = create_app(agent_name)
    uvicorn.run(app, host="0.0.0.0", port=port)
