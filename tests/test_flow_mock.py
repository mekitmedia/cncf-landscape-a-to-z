import pytest
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

# Set dummy key for tests to avoid instantiation errors
os.environ['GOOGLE_API_KEY'] = 'dummy_key'


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic_ai.models.function import FunctionModel
from pydantic_ai.messages import ModelResponse, TextPart
from src.agentic.models import NextWeekDecision, ResearchOutput, BlogPostDraft, ProjectMetadata
from src.agentic.agents.editor import editor_agent
from src.agentic.agents.researcher import researcher_agent
from src.agentic.agents.writer import writer_agent


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


@pytest.mark.asyncio
async def test_runner_stops_at_limit():
    """Verify run_agentic_workflow halts immediately when limit is reached without drafting incomplete posts."""
    from src.agentic.runner import run_agentic_workflow
    from src.tracker import TaskProgress

    def editor_fn(messages, info):
        return ModelResponse(parts=[TextPart(NextWeekDecision(action="next", week_letter="A", reason="test").model_dump_json())])

    def researcher_fn(messages, info):
        return ModelResponse(parts=[TextPart(ResearchOutput(
            project_name="P1",
            summary="P1 summary",
            key_features=[],
            recent_updates="v1",
            use_cases="test"
        ).model_dump_json())])

    with editor_agent.override(model=FunctionModel(editor_fn)), \
         researcher_agent.override(model=FunctionModel(researcher_fn)), \
         patch('src.agentic.runner.weekly.get_items_for_week', new_callable=AsyncMock) as mock_get_items, \
         patch('src.agentic.runner.research.save_research', new_callable=AsyncMock) as mock_save_research, \
         patch('src.agentic.runner.writing.write_weekly_post', new_callable=AsyncMock) as mock_write_post, \
         patch('src.agentic.runner.get_tracker') as mock_get_tracker:

        mock_tracker = MagicMock()
        # Research is only partially complete (1 of 10)
        mock_tracker.get_progress.return_value = TaskProgress(
            total=10, pending=9, in_progress=0, completed=1, failed=0, skipped=0
        )
        mock_get_tracker.return_value = mock_tracker

        mock_get_items.return_value = [
            ProjectMetadata(name="P1", week_letter="A"),
            ProjectMetadata(name="P2", week_letter="A"),
            ProjectMetadata(name="P3", week_letter="A"),
        ]

        summary = await run_agentic_workflow(limit=1)

        assert summary["items_processed"] == 1
        assert summary["weeks_completed"] == 0
        mock_save_research.assert_called_once()
        # Blog post should NOT be written when research is only partially complete
        mock_write_post.assert_not_called()


@pytest.mark.asyncio
async def test_runner_drafts_post_when_research_complete():
    """Verify run_agentic_workflow drafts blog post when 100% of research is completed."""
    from src.agentic.runner import run_agentic_workflow
    from src.tracker import TaskProgress

    def editor_fn(messages, info):
        return ModelResponse(parts=[TextPart(NextWeekDecision(action="next", week_letter="A", reason="test").model_dump_json())])

    def researcher_fn(messages, info):
        return ModelResponse(parts=[TextPart(ResearchOutput(
            project_name="P1",
            summary="P1 summary",
            key_features=[],
            recent_updates="v1",
            use_cases="test"
        ).model_dump_json())])

    def writer_fn(messages, info):
        return ModelResponse(parts=[TextPart(BlogPostDraft(
            title="Week A Post",
            content_markdown="Content"
        ).model_dump_json())])

    with editor_agent.override(model=FunctionModel(editor_fn)), \
         researcher_agent.override(model=FunctionModel(researcher_fn)), \
         writer_agent.override(model=FunctionModel(writer_fn)), \
         patch('src.agentic.runner.weekly.get_items_for_week', new_callable=AsyncMock) as mock_get_items, \
         patch('src.agentic.runner.research.save_research', new_callable=AsyncMock), \
         patch('src.agentic.runner.load_week_research', new_callable=AsyncMock) as mock_load_research, \
         patch('src.agentic.runner.writing.save_post', new_callable=AsyncMock) as mock_save_post, \
         patch('src.agentic.runner.get_tracker') as mock_get_tracker:

        mock_tracker = MagicMock()
        # Research is 100% complete (1 of 1)
        mock_tracker.get_progress.return_value = TaskProgress(
            total=1, pending=0, in_progress=0, completed=1, failed=0, skipped=0
        )
        mock_get_tracker.return_value = mock_tracker


        mock_get_items.return_value = [
            ProjectMetadata(name="P1", week_letter="A")
        ]
        mock_load_research.return_value = [
            ResearchOutput(project_name="P1", summary="P1 summary", key_features=[], recent_updates="v1", use_cases="test")
        ]

        summary = await run_agentic_workflow(limit=1)

        assert summary["items_processed"] == 1
        assert summary["weeks_completed"] == 1
        mock_save_post.assert_called_once()




