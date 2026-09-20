import pytest
from src.agentic.models import ResearchOutput, SourceEvidence
from src.agentic.actions.research import save_research
from pydantic import ValidationError
from unittest.mock import patch, MagicMock
import yaml
import tempfile
import os
from pathlib import Path
import asyncio

def test_source_evidence_parsing():
    """Test ResearchOutput can parse and dump SourceEvidence with verbatim quotes."""
    data = {
        "project_name": "TestProject",
        "summary": "Summary",
        "key_features": ["Feature"],
        "recent_updates": "Updates",
        "use_cases": "Use Cases",
        "sources": [
            {
                "id": "doc1",
                "title": "Official Docs",
                "url": "https://example.com/docs",
                "source_type": "official_docs",
                "quotes": ["This is a quote.", "Another quote."]
            }
        ]
    }

    output = ResearchOutput(**data)
    assert len(output.sources) == 1
    assert output.sources[0].id == "doc1"
    assert len(output.sources[0].quotes) == 2

    dumped = output.model_dump()
    assert dumped["sources"][0]["quotes"] == ["This is a quote.", "Another quote."]

def test_research_output_preserves_editorial_lock():
    """Test ResearchOutput preserves editorial_lock: true and lock metadata."""
    data = {
        "project_name": "TestProject",
        "summary": "Summary",
        "key_features": ["Feature"],
        "recent_updates": "Updates",
        "use_cases": "Use Cases",
        "editorial_lock": True,
        "locked_by": "human_editor",
        "locked_at": "2023-10-01T12:00:00Z"
    }

    output = ResearchOutput(**data)
    assert output.editorial_lock is True
    assert output.locked_by == "human_editor"
    assert output.locked_at == "2023-10-01T12:00:00Z"

@pytest.mark.asyncio
async def test_execution_guard_skips_locked_items():
    """Test execution guard correctly skips locked items."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch('src.agentic.actions.research.load_config') as mock_load_config, \
             patch('src.agentic.actions.research.get_tracker') as mock_get_tracker, \
             patch('src.agentic.actions.research.week_id', return_value="00-A"), \
             patch('src.agentic.actions.research.logger.info') as mock_logger_info:

            mock_cfg = MagicMock()
            mock_cfg.weeks_dir = Path(temp_dir)
            mock_load_config.return_value = mock_cfg

            research_dir = Path(temp_dir) / "00-A" / "research"
            os.makedirs(research_dir, exist_ok=True)

            # Create a locked item file
            locked_file = research_dir / "testproject.yaml"
            with open(locked_file, "w") as f:
                yaml.dump({
                    "project_name": "TestProject",
                    "editorial_lock": True,
                    "locked_by": "human_editor",
                    "summary": "Original Summary"
                }, f)

            # Create new research output
            new_output = ResearchOutput(
                project_name="TestProject",
                summary="New Summary",
                key_features=[],
                recent_updates="New Updates",
                use_cases="New Cases"
            )

            # Attempt to save without force_override
            await save_research("A", new_output)

            # Check logger was called with skip message
            mock_logger_info.assert_called_with("Skipping TestProject: Protected by editorial lock")

            # Check file was not overwritten
            with open(locked_file, "r") as f:
                saved_data = yaml.safe_load(f)
            assert saved_data["summary"] == "Original Summary"
            assert saved_data["editorial_lock"] is True

            # Attempt to save with force_override
            await save_research("A", new_output, force_override=True)

            # Check file was overwritten
            with open(locked_file, "r") as f:
                saved_data = yaml.safe_load(f)
            assert saved_data["summary"] == "New Summary"
            # It will have default editorial_lock=False since new_output doesn't set it to True
            assert saved_data["editorial_lock"] is False
