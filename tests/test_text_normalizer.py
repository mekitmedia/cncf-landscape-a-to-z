import pytest
from src.utils.text_normalizer import canonical_normalize, is_quote_in_source

def test_canonical_normalize_html_entities():
    # Test HTML entity unescaping
    assert canonical_normalize("AT&amp;T") == "at&t"
    assert canonical_normalize("hello &quot;world&quot;") == 'hello "world"'
    assert canonical_normalize("5 &lt; 10") == "5 < 10"

def test_canonical_normalize_quotes():
    # Test curly/smart quote standardization
    assert canonical_normalize("“smart”") == '"smart"'
    assert canonical_normalize("„german“") == '"german"'
    assert canonical_normalize("«french»") == '"french"'
    assert canonical_normalize("‘single’") == "'single'"

def test_canonical_normalize_dashes():
    # Test em-dash, en-dash, and minus standardization
    assert canonical_normalize("em—dash") == "em-dash"
    assert canonical_normalize("en–dash") == "en-dash"
    assert canonical_normalize("math−minus") == "math-minus"

def test_canonical_normalize_whitespace():
    # Test multi-line text with whitespace and newline variations
    text = "hello \n  world\t\u00a0\r \n test"
    assert canonical_normalize(text) == "hello world test"

def test_canonical_normalize_strip_and_lower():
    # Test strip and lower
    assert canonical_normalize("  HELLO WORLD  ") == "hello world"

def test_is_quote_in_source():
    # Test positive cases
    source = "This is a “smart” text with an em—dash and \n some whitespace."
    assert is_quote_in_source('is a "smart" text', source) == True
    assert is_quote_in_source('em-dash and some', source) == True

    source_html = "Some &lt;html&gt; entities &amp; stuff."
    assert is_quote_in_source("<html> entities & stuff", source_html) == True

    # Test negative cases
    assert is_quote_in_source('not in source', source) == False
    assert is_quote_in_source('text with en-dash', source) == False # Different dash context

def test_canonical_normalize_empty():
    assert canonical_normalize("") == ""
    assert canonical_normalize(None) == ""
