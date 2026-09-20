# Jules Content & Research Memory Log

This file records insights, learnings, and canonical actions discovered during CNCF landscape research, weekly post writing, and content management workflows.

## 2026-09-20 - Source Quote Grounding & Text Normalization
**Learning:** Raw quote strings extracted from GitHub release notes or markdown documentation often contain Unicode smart quotes (\u201c, \u201d), em-dashes (\u2014), non-breaking spaces (\u00a0), or trailing punctuation that cause exact string matching to fail.
**Action:** Always normalize quotes and source text through `src/utils/text_normalizer.py:normalize_text()` before performing deterministic substring grounding checks.

## 2026-09-20 - Direct Citation Requirement
**Learning:** LLMs tend to generate paraphrased summaries rather than direct quotes, which fails strict source grounding verification.
**Action:** Every assertion in `ResearchOutput` must have an exact `direct_quote` verified against the raw fetched repository/website content with an explicit source URL.
