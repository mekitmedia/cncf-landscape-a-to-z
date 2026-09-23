import html
import re
import unicodedata

def canonical_normalize(text: str) -> str:
    """
    Normalizes text to prevent false-alarm quote rejections.
    """
    if not text:
        return ""

    # Decode HTML entities
    text = html.unescape(text)

    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)

    # Standardize typographic quotes
    # Replace double-like quotes with standard double quote
    text = text.translate(str.maketrans('“”„«»', '"""""'))
    # Replace single-like quotes with standard single quote (including backtick just in case, though prompt mentions specific ones)
    text = text.translate(str.maketrans('‘’', "''"))

    # Standardize dashes
    text = text.translate(str.maketrans('—–−', '---'))

    # Collapse multiple whitespace characters and newlines into a single space
    text = re.sub(r'\s+', ' ', text)

    # Convert to lowercase and strip leading/trailing whitespace
    return text.lower().strip()

def is_quote_in_source(quote: str, source_text: str) -> bool:
    """
    Returns True if canonical_normalize(quote) is a substring of canonical_normalize(source_text).
    """
    return canonical_normalize(quote) in canonical_normalize(source_text)
