import pytest
from pathlib import Path
from src.pipeline.transform import get_workflow_stats

def test_get_workflow_stats():
    sample_landscape = [
        {
            "name": "App Definition and Development",
            "subcategories": [
                {
                    "name": "Database",
                    "items": [
                        {"name": "ArangoDB", "project": "non-cncf", "repo_url": "https://github.com/arangodb/arangodb"},
                        {"name": "ArchivedDB", "project": "archived", "repo_url": "https://github.com/archived/db"}
                    ]
                }
            ]
        }
    ]

    stats = get_workflow_stats(sample_landscape, data_dir=Path("data"))

    assert "summary" in stats
    assert stats["summary"]["total_tools"] == 1
    assert "cncf_statuses" in stats
    assert stats["cncf_statuses"]["non-cncf"] >= 1
    assert "categories" in stats
    assert stats["categories"]["Database"] == 1
    assert "letter_progress" in stats
    assert "A" in stats["letter_progress"]
    assert stats["letter_progress"]["A"]["letter"] == "A"
