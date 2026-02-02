# This file is used to run the agent UI
import logging
import os
from src.agentic.observability import setup_observability

# Setup logger
logger = logging.getLogger(__name__)

def create_app(agent_name: str, **kwargs):
    from src.config import load_config
    from src.agentic.deps import AgentDeps, ResearcherDeps, WriterDeps
    from src.agentic.config import get_available_models
    
    cfg = load_config()
    models = get_available_models()

    if agent_name == "researcher":
        from src.agentic.agents.researcher import researcher_agent
        from src.agentic.models import ProjectMetadata
        # Provide default deps for the UI
        default_deps = ResearcherDeps(
            project=ProjectMetadata(name="CNCF", week_letter="A"), 
            config=cfg
        )
        return researcher_agent.to_web(deps=default_deps, models=models)
    elif agent_name == "writer":
        from src.agentic.agents.writer import writer_agent
        # Provide default deps for the UI
        default_deps = WriterDeps(research_results=[], week_letter="A", config=cfg)
        return writer_agent.to_web(deps=default_deps, models=models)
    elif agent_name == "editor":
        from src.agentic.agents.editor import editor_agent
        return editor_agent.to_web(deps=AgentDeps(config=cfg), models=models)
    else:
        raise ValueError(f"Unknown agent: {agent_name}")

def run_ui(agent_name: str, port: int = 8000):
    logger.info(f"Starting UI for {agent_name} agent on port {port}...")
    setup_observability()
    # pydantic-ai-slim[web] provides built-in web UI support
    # The to_web() method returns an ASGI app that can be run directly
    import uvicorn
    app = create_app(agent_name)
    uvicorn.run(app, host="0.0.0.0", port=port)
