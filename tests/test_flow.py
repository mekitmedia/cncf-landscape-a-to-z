import pytest
from unittest.mock import patch, AsyncMock
from src.agentic.flow import generate_content

@pytest.mark.asyncio
async def test_generate_content_concurrently():
    projects = ["Project A", "Project B", "Project C"]

    mock_research_return = {"project_name": "test", "summary": "test"}
    mock_draft_return = "Draft content"

    # Patching the methods on the classes
    with patch("src.agentic.agents.ResearcherAgent.research", new_callable=AsyncMock) as mock_research, \
         patch("src.agentic.agents.WriterAgent.draft", new_callable=AsyncMock) as mock_draft:

        mock_research.return_value = mock_research_return
        mock_draft.return_value = mock_draft_return

        await generate_content(projects)

        # Verify research was called for each project
        assert mock_research.call_count == 3
        # Ensure arguments are correct
        mock_research.assert_any_call("Project A")
        mock_research.assert_any_call("Project B")
        mock_research.assert_any_call("Project C")

        # Verify draft was called for each project
        assert mock_draft.call_count == 3
