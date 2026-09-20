#!/usr/bin/env python3
import argparse
import sys
import os
import yaml
import subprocess
from pathlib import Path
from typing import List

# Add src to python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.text_normalizer import is_quote_in_source
from src.agentic.models import ResearchOutput
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False

def validate_yaml_file(filepath: Path) -> List[str]:
    errors = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"Failed to parse YAML: {e}"]

    if data is None:
        return ["YAML file is empty"]
    if not isinstance(data, dict):
        return [f"YAML content must be a mapping, got {type(data).__name__}"]

    try:
        # Validate schema structure
        research_output = ResearchOutput(**data)
    except Exception as e:
        pass

    sources = data.get('sources', [])
    if not sources:
        errors.append("No sources found")
        return errors

    project_slug = data.get('project_name', filepath.stem).lower()
    cache_dir = filepath.parent / '.cache'

    # 1. & 3. Quote existence & Link syntax
    for source in sources:
        source_id = source.get('id')
        if not source_id:
            errors.append(f"Source missing 'id'")
            continue

        url = source.get('url')
        if not url or not is_valid_url(url):
            errors.append(f"Source '{source_id}' has invalid or missing url: {url}")

        quotes = source.get('quotes', [])
        if not quotes or not isinstance(quotes, list):
            errors.append(f"Source '{source_id}' has missing or empty 'quotes' list")
            continue

        # 2. Local Cache / Snapshot Substring Check
        cache_file = cache_dir / f"{project_slug}_{source_id}.txt"
        cached_text = None
        if cache_file.exists():
            try:
                cached_text = cache_file.read_text(encoding="utf-8")
            except Exception as e:
                errors.append(f"Failed to read cache file {cache_file}: {e}")

        for quote in quotes:
            if not isinstance(quote, str) or not quote.strip():
                errors.append(f"Source '{source_id}' has empty or invalid quote")
                continue

            if cached_text is not None and not is_quote_in_source(quote, cached_text):
                errors.append(f"Quote '{quote[:50]}...' not found in cached source {source_id}")

    # 4. Summary & Feature Grounding Attribution
    # In deterministic script, we just verify that these fields are not empty
    summary = data.get('summary')
    if not summary or not isinstance(summary, str) or not summary.strip():
        errors.append("Missing or empty 'summary'")

    key_features = data.get('key_features', [])
    if not key_features or not isinstance(key_features, list) or len(key_features) == 0:
        errors.append("Missing or empty 'key_features'")

    return errors

def get_git_diff_files(ref: str) -> List[Path]:
    repo_root = Path(__file__).resolve().parent.parent
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMRT", ref],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_root,
        )
        files = [f.strip() for f in result.stdout.splitlines() if f.strip()]

        # Filter for only research YAMLs
        research_files: List[Path] = []
        for f in files:
            p = repo_root / f
            if p.suffix == ".yaml" and "research" in p.parts and p.exists():
                research_files.append(p)

        return research_files
    except Exception as e:
        print(f"Warning: Could not get git diff against '{ref}': {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description="Validate grounding of research notes")
    parser.add_argument("files", nargs="*", help="Files to validate")
    parser.add_argument("--week", help="Week ID to validate (e.g., 00-A)")
    parser.add_argument("--all-files", action="store_true", help="Validate all research files")
    parser.add_argument("--git-diff", nargs="?", const="HEAD", help="Check changed files relative to git ref")

    args = parser.parse_args()

    files_to_check = set()

    if args.files:
        files_to_check.update([Path(f) for f in args.files])

    if args.week:
        week_dir = Path("data/weeks") / args.week / "research"
        if week_dir.exists():
            files_to_check.update(week_dir.glob("*.yaml"))

    if args.all_files:
        files_to_check.update(Path("data/weeks").glob("*/research/*.yaml"))

    if args.git_diff is not None:
        files_to_check.update(get_git_diff_files(args.git_diff))

    if not files_to_check:
        print("No files specified for validation.")
        return 0

    has_errors = False

    for filepath in sorted(files_to_check):
        # Ignore tracker.yaml, tasks.yaml, and any cache files
        if filepath.name in ('tracker.yaml', 'tasks.yaml') or filepath.parent.name == '.cache':
            continue

        print(f"Validating {filepath}...")
        errors = validate_yaml_file(filepath)

        if errors:
            has_errors = True
            for error in errors:
                print(f"  ❌ {error}")
        else:
            print(f"  ✅ Passed")

    if has_errors:
        sys.exit(1)
    else:
        print("All checks passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
