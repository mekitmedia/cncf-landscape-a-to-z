import os
import yaml
import glob
import logging

def create_tool_card(research_data: dict) -> str:
    """
    Extracts project name, 1-line summary, CNCF status, top 2 key features, and repo URL.
    Returns a compact markdown bullet (~80 words).
    """
    project_name = research_data.get("project_name", "Unknown Project")
    summary = research_data.get("summary", "")
    cncf_status = research_data.get("cncf_status") or "unknown"
    repo_url = research_data.get("repo_url", "No Repo URL")

    key_features = research_data.get("key_features", [])
    if isinstance(key_features, list):
        top_features = key_features[:2]
    else:
        top_features = []

    features_text = " ".join([f"- {feat}" for feat in top_features])

    card = f"- **{project_name}** ({cncf_status}): {summary} [Repo]({repo_url})\n  Features: {features_text}"
    return card

def project_week_deck(week_id: str) -> str:
    """
    Reads all completed research files in data/weeks/<WEEK_ID>/research/*.yaml
    and compiles them into a compact deck.
    """
    search_path = f"data/weeks/{week_id}/research/*.yaml"
    files = sorted(glob.glob(search_path))

    cards = []
    for filepath in files:
        with open(filepath, 'r') as f:
            try:
                data = yaml.safe_load(f)
                if data:
                    cards.append(create_tool_card(data))
            except yaml.YAMLError as e:
                logging.error(f"Failed to parse {filepath}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error while processing {filepath}: {e}")

    return "\n\n".join(cards)
