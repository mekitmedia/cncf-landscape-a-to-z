import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from src.agentic.models import NextWeekDecision, ResearchOutput, BlogPostDraft, ProjectMetadata
import os

# Set dummy key for tests to avoid instantiation errors
os.environ['GOOGLE_API_KEY'] = 'dummy_key'

# Mock AgentRunResult class to match pydantic-ai structure
class MockAgentRunResult:
    def __init__(self, output):
        self._output = output

    @property
    def data(self):
        return self._output

@pytest.mark.asyncio
async def test_determine_next_week_mock():
    # Use .fn to bypass Prefect task wrapper
    from src.agentic.flow import determine_next_week

    with patch('src.agentic.actions.decisions.editor_agent.run', new_callable=AsyncMock) as mock_run:
        # Create expected decision using correct kwargs
        expected_decision = NextWeekDecision(
            action="next",
            week_letter="A",
            reason="Test reason"
        )

        # Create a mock result that behaves like AgentRunResult
        mock_result = MagicMock()
        mock_result.data = expected_decision

        mock_run.return_value = mock_result

        # We must mock get_run_logger because we are running without a Prefect run context
        with patch('src.agentic.flow.get_run_logger') as mock_logger:
            if hasattr(determine_next_week, 'fn'):
                 result = await determine_next_week.fn()
            else:
                 result = await determine_next_week()

        assert result == expected_decision

@pytest.mark.asyncio
async def test_research_item_mock():
    from src.agentic.flow import research_item

    with patch('src.agentic.actions.research.researcher_agent.run', new_callable=AsyncMock) as mock_run, \
         patch('src.agentic.actions.research.get_tracker') as mock_get_tracker:
        
        # Mock tracker
        mock_tracker = MagicMock()
        mock_get_tracker.return_value = mock_tracker
        
        expected_output = ResearchOutput(
            project_name="Test Project",
            summary="A test project",
            key_features=["Feature A"],
            recent_updates="Update 1",
            use_cases="Use case 1"
        )
        mock_result = MagicMock()
        mock_result.data = expected_output
        mock_run.return_value = mock_result

        item = ProjectMetadata(name="Test Project", repo_url="http://test", homepage="http://test", week_letter="A")

        with patch('src.agentic.flow.get_run_logger'):
             if hasattr(research_item, 'fn'):
                 result = await research_item.fn(item, item.week_letter)
             else:
                 result = await research_item(item, item.week_letter)

        assert result == expected_output
        # Verify tracker was called
        mock_tracker.update_task.assert_called()

@pytest.mark.asyncio
async def test_write_weekly_post_mock():
    from src.agentic.flow import write_weekly_post

    with patch('src.agentic.actions.writing.writer_agent.run', new_callable=AsyncMock) as mock_run:
        expected_draft = BlogPostDraft(title="Test Post", content_markdown="Content")
        mock_result = MagicMock()
        mock_result.data = expected_draft
        mock_run.return_value = mock_result

        with patch('src.agentic.flow.get_run_logger'):
             if hasattr(write_weekly_post, 'fn'):
                 result = await write_weekly_post.fn("A", [])
             else:
                 result = await write_weekly_post("A", [])

        assert result == expected_draft
