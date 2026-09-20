import glob
import logging
import yaml


logger = logging.getLogger(__name__)
MAX_TOOL_CARD_WORDS = 80


def _trim_words(words: list[str], limit: int) -> list[str]:
    """Trim a list of words to a maximum size, adding an ellipsis if needed."""
    if limit <= 0 or not words:
        return []
    if len(words) <= limit:
        return words
    if limit == 1:
        return ["…"]
    return words[: limit - 1] + ["…"]

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

    features_text = " ".join(f"- {feat}" for feat in top_features)

    header = f"- **{project_name}** ({cncf_status}):"
    repo_link = f"[Repo]({repo_url})"
    feature_label = "Features:"

    header_words = len(header.split())
    repo_words = len(repo_link.split())
    feature_label_words = len(feature_label.split()) if features_text else 0

    available_content_words = MAX_TOOL_CARD_WORDS - header_words - repo_words - feature_label_words
    feature_words = _trim_words(features_text.split(), max(available_content_words, 0))
    available_summary_words = available_content_words - len(feature_words)
    summary_words = _trim_words(summary.split(), max(available_summary_words, 0))

    card = f"{header} {' '.join(summary_words)} {repo_link}".strip()
    if feature_words:
        card = f"{card}\n  {feature_label} {' '.join(feature_words)}"
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
                logger.error(f"Failed to parse {filepath}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error while processing {filepath}: {e}")

    return "\n\n".join(cards)
