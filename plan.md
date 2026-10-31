1. Update `scripts/validate_contract.py` to replace `re.search(r'^---\n(.*?)\n---', content, re.DOTALL)` with `re.search(r'^---\r?\n(.*?)\r?\n---', content, re.DOTALL)`.
2. Append the following test case code to `tests/test_contract_validator.py` to ensure it correctly parses frontmatter with CRLF line endings:
```python
def test_validate_blog_post_file_crlf_valid(tmp_path: Path):
    post_file = tmp_path / "crlf-test.md"
    content = "---\r\ntitle: \"Letter A\"\r\ndate: 2026-01-01T00:00:00Z\r\ndraft: false\r\n---\r\n\r\n# Body"
    with open(post_file, "wb") as f:
        f.write(content.encode("utf-8"))
    ok, err = validate_blog_post_file(post_file)
    assert ok is True, f"Failed: {err}"
```
3. Append the following entry to `.Jules/engineering.md`:
```markdown
## 2026-10-31 - Resilient Multiline Regex Matching for Cross-Platform Line Endings
**Learning:** Hardcoding `\n` in multiline regex operations (like frontmatter extraction using `re.search`) causes scripts to fail on Windows or when handling CRLF (`\r\n`) formatted files, resulting in flaky schema validation.
**Action:** Always use `\r?\n` in Python regex patterns dealing with text boundaries instead of `\n` alone to ensure correct parsing regardless of file line endings.
```
4. Use `cat` or `read_file` on `scripts/validate_contract.py`, `tests/test_contract_validator.py`, and `.Jules/engineering.md` to confirm the changes were written correctly.
5. Run tests locally by running `pnpm install`, `pnpm test`, `PYTHONPATH=. uv run pytest` and `uv run python scripts/validate_contract.py --week 00-A`.
6. Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
7. Submit the PR to the current branch with a descriptive commit message.
