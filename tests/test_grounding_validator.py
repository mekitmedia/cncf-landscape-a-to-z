import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_grounding import validate_yaml_file

@pytest.fixture
def test_data_dir(tmp_path):
    research_dir = tmp_path / "data" / "weeks" / "00-A" / "research"
    research_dir.mkdir(parents=True)
    cache_dir = research_dir / ".cache"
    cache_dir.mkdir()
    return research_dir

def test_valid_grounding(test_data_dir):
    yaml_content = """
project_name: ValidProject
summary: "This is a summary."
key_features:
  - "Feature 1"
sources:
  - id: src_1
    url: https://example.com/docs
    quotes:
      - "This is a valid quote."
"""
    yaml_file = test_data_dir / "validproject.yaml"
    yaml_file.write_text(yaml_content)

    cache_file = test_data_dir / ".cache" / "validproject_src_1.txt"
    cache_file.write_text("Some text here. This is a valid quote. More text.")

    errors = validate_yaml_file(yaml_file)
    assert not errors

def test_missing_sources(test_data_dir):
    yaml_content = """
project_name: NoSourcesProject
summary: "This is a summary."
key_features:
  - "Feature 1"
"""
    yaml_file = test_data_dir / "nosourcesproject.yaml"
    yaml_file.write_text(yaml_content)

    errors = validate_yaml_file(yaml_file)
    assert any("No sources found" in e for e in errors)

def test_empty_quotes(test_data_dir):
    yaml_content = """
project_name: EmptyQuotesProject
summary: "This is a summary."
key_features:
  - "Feature 1"
sources:
  - id: src_1
    url: https://example.com
    quotes: []
"""
    yaml_file = test_data_dir / "emptyquotes.yaml"
    yaml_file.write_text(yaml_content)

    errors = validate_yaml_file(yaml_file)
    assert any("empty 'quotes' list" in e for e in errors)

def test_invalid_url(test_data_dir):
    yaml_content = """
project_name: InvalidUrlProject
summary: "This is a summary."
key_features:
  - "Feature 1"
sources:
  - id: src_1
    url: not-a-url
    quotes:
      - "Quote"
"""
    yaml_file = test_data_dir / "invalidurl.yaml"
    yaml_file.write_text(yaml_content)

    errors = validate_yaml_file(yaml_file)
    assert any("invalid or missing url" in e for e in errors)

def test_quote_not_in_cache(test_data_dir):
    yaml_content = """
project_name: InvalidQuoteProject
summary: "This is a summary."
key_features:
  - "Feature 1"
sources:
  - id: src_1
    url: https://example.com
    quotes:
      - "This quote is made up."
"""
    yaml_file = test_data_dir / "invalidquoteproject.yaml"
    yaml_file.write_text(yaml_content)

    cache_file = test_data_dir / ".cache" / "invalidquoteproject_src_1.txt"
    cache_file.write_text("The source text does not contain that quote.")

    errors = validate_yaml_file(yaml_file)
    assert any("not found in cached source" in e for e in errors)

def test_missing_summary_and_features(test_data_dir):
    yaml_content = """
project_name: MissingAttributionProject
sources:
  - id: src_1
    url: https://example.com
    quotes:
      - "A real quote."
"""
    yaml_file = test_data_dir / "missingattributionproject.yaml"
    yaml_file.write_text(yaml_content)

    errors = validate_yaml_file(yaml_file)
    assert any("Missing or empty 'summary'" in e for e in errors)
    assert any("Missing or empty 'key_features'" in e for e in errors)

def test_empty_string_quotes(test_data_dir):
    yaml_content = """
project_name: EmptyStringQuotesProject
summary: "This is a summary."
key_features:
  - "Feature 1"
sources:
  - id: src_1
    url: https://example.com
    quotes:
      - ""
      - "   "
"""
    yaml_file = test_data_dir / "emptystringquotesproject.yaml"
    yaml_file.write_text(yaml_content)

    cache_file = test_data_dir / ".cache" / "emptystringquotesproject_src_1.txt"
    cache_file.write_text("Some text here.")

    errors = validate_yaml_file(yaml_file)
    assert any("empty or invalid quote" in e for e in errors)
