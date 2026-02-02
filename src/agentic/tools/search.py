from pydantic_ai import RunContext
from duckduckgo_search import DDGS
from src.agentic.deps import AgentDeps
import logging

logger = logging.getLogger(__name__)

def search_tool(ctx: RunContext[AgentDeps], query: str) -> str:
    """Perform a web search using DuckDuckGo."""
    logger.info(f"Searching for: {query}")
    try:
        with DDGS() as ddgs:
            # limiting to 3 results to save tokens/time
            results = list(ddgs.text(query, max_results=3))
            return str(results)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"Search failed: {e}"
