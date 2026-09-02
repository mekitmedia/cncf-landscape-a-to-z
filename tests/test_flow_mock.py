import pytest
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelResponse, TextPart
from src.agentic.models import NextWeekDecision, ResearchOutput, BlogPostDraft, ProjectMetadata
from src.agentic.agents.editor import editor_agent
from src.agentic.agents.researcher import researcher_agent
from src.agentic.agents.writer import writer_agent

# Set dummy key for tests to avoid instantiation errors
os.environ['GOOGLE_API_KEY'] = 'dummy_key'


@pytest.mark.asyncio
async def test_determine_next_week_golden():
    """Test determine_next_week action using Pydantic AI FunctionModel golden response."""
    from src.agentic.flow import determine_next_week

    expected_decision = NextWeekDecision(
        action="next",
        week_letter="A",
        reason="Golden decision: sequence A-Z"
    )

    def editor_model_fn(messages, info):
        return ModelResponse(parts=[TextPart(expected_decision.model_dump_json())])

    with editor_agent.override(model=FunctionModel(editor_model_fn)):
        with patch('src.agentic.flow.get_run_logger'):
            if hasattr(determine_next_week, 'fn'):
                result = await determine_next_week.fn()
            else:
                result = await determine_next_week()

    assert result == expected_decision
    assert result.week_letter == "A"
    assert result.action == "next"


@pytest.mark.asyncio
async def test_research_item_golden():
    """Test research_item action using Pydantic AI FunctionModel golden response."""
    from src.agentic.flow import research_item

    expected_output = ResearchOutput(
        project_name="Test Project",
        summary="A verified test project",
        key_features=["Feature A", "Feature B"],
        recent_updates="Update v1.0 released",
        use_cases="Use case for cloud native workloads"
    )

    def researcher_model_fn(messages, info):
        return ModelResponse(parts=[TextPart(expected_output.model_dump_json())])

    with researcher_agent.override(model=FunctionModel(researcher_model_fn)):
        with patch('src.agentic.actions.research.get_tracker') as mock_get_tracker:
            mock_tracker = MagicMock()
            mock_get_tracker.return_value = mock_tracker

            item = ProjectMetadata(name="Test Project", repo_url="http://test", homepage="http://test", week_letter="A")

            with patch('src.agentic.flow.get_run_logger'):
                if hasattr(research_item, 'fn'):
                    result = await research_item.fn(item, item.week_letter)
                else:
                    result = await research_item(item, item.week_letter)

            assert result == expected_output
            assert result.project_name == "Test Project"
            mock_tracker.update_task.assert_called()


@pytest.mark.asyncio
async def test_write_weekly_post_golden():
    """Test write_weekly_post action using Pydantic AI FunctionModel golden response."""
    from src.agentic.flow import write_weekly_post

    expected_draft = BlogPostDraft(
        title="Letter A: 5 Projects Starting with A",
        content_markdown="# Letter A Projects\n\n## Test Project\nOverview of test project."
    )

    def writer_model_fn(messages, info):
        return ModelResponse(parts=[TextPart(expected_draft.model_dump_json())])

    with writer_agent.override(model=FunctionModel(writer_model_fn)):
        with patch('src.agentic.flow.get_run_logger'):
            if hasattr(write_weekly_post, 'fn'):
                result = await write_weekly_post.fn("A", [])
            else:
                result = await write_weekly_post("A", [])

    assert result == expected_draft
    assert result.title == "Letter A: 5 Projects Starting with A"


@pytest.mark.asyncio
async def test_weekly_content_flow_e2e_golden(tmp_path):
    """Test full weekly_content_flow end-to-end using golden FunctionModels for all 3 agents."""
    from src.agentic.flow import weekly_content_flow

    # Golden decision: process week A
    def editor_model_fn(messages, info):
        d = NextWeekDecision(action="next", week_letter="A", reason="Test e2e golden")
        return ModelResponse(parts=[TextPart(d.model_dump_json())])

    # Golden research output
    def researcher_model_fn(messages, info):
        r = ResearchOutput(
            project_name="TestProject",
            summary="A test project for e2e validation",
            key_features=["Feature 1"],
            recent_updates="v1.0.0",
            use_cases="Cloud native testing"
        )
        return ModelResponse(parts=[TextPart(r.model_dump_json())])

    # Golden blog post draft
    def writer_model_fn(messages, info):
        b = BlogPostDraft(
            title="Letter A: CNCF Projects",
            content_markdown="# Letter A Projects\n\n## TestProject\nTest summary."
        )
        return ModelResponse(parts=[TextPart(b.model_dump_json())])

    with editor_agent.override(model=FunctionModel(editor_model_fn)), \
         researcher_agent.override(model=FunctionModel(researcher_model_fn)), \
         writer_agent.override(model=FunctionModel(writer_model_fn)), \
         patch('src.agentic.flow.get_run_logger'), \
         patch('src.agentic.flow.get_items_for_week', new_callable=AsyncMock) as mock_get_items, \
         patch('src.agentic.flow.save_research', new_callable=AsyncMock), \
         patch('src.agentic.flow.save_post', new_callable=AsyncMock):

        mock_get_items.return_value = [
            ProjectMetadata(name="TestProject", week_letter="A")
        ]

        if hasattr(weekly_content_flow, 'fn'):
            await weekly_content_flow.fn(limit=1)
        else:
            await weekly_content_flow(limit=1)

        mock_get_items.assert_called_with("A")



