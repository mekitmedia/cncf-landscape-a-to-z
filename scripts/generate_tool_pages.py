#!/usr/bin/env python3
"""
Generate individual tool pages from research YAML files.

This script reads research YAML files from data/week_XX_Y/research/ directories
and generates corresponding Hugo content pages in website/content/tools/.

Each tool page is a single.html template with research data in front matter.
"""

import os
import glob
import yaml
from pathlib import Path
from datetime import datetime


def sanitize_for_filename(name: str) -> str:
    """Convert project name to sanitized filename format."""
    return name.lower() \
        .replace(" ", "_") \
        .replace("&", "and") \
        .replace("/", "_") \
        .replace(".", "_") \
        .replace(",", "")


def get_cncf_status_from_etl(project_name: str) -> str:
    """Try to find CNCF status from ETL output files."""
    # Search all week directories for this project
    for week_dir in glob.glob("data/week_*/"):
        for yaml_file in glob.glob(f"{week_dir}/*.yaml"):
            if yaml_file.endswith("tasks.yaml") or yaml_file.endswith("README.yaml"):
                continue
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    items = yaml.safe_load(f)
                    if items and isinstance(items, list):
                        for item in items:
                            if item.get('name') == project_name:
                                return item.get('project', 'sandbox')
            except Exception:
                pass
    
    return 'sandbox'


def get_letter_from_week_dir(week_dir: str) -> str:
    """Extract letter from week directory name (e.g., 'week_00_A' -> 'A')."""
    return week_dir.split('_')[-1]


def generate_tool_page(research_file: str, week_dir: str) -> str:
    """
    Generate a tool page from a research YAML file.
    
    Args:
        research_file: Path to the research YAML file
        week_dir: The week directory name (e.g., 'week_00_A')
    
    Returns:
        The generated page content as a string
    """
    try:
        with open(research_file, 'r', encoding='utf-8') as f:
            research = yaml.safe_load(f)
        
        if not research:
            return None
        
        # Extract project name (should be in research file)
        project_name = research.get('project_name', Path(research_file).stem)
        letter = get_letter_from_week_dir(week_dir)
        
        # Get CNCF status from ETL data
        cncf_status = get_cncf_status_from_etl(project_name)
        
        # Build front matter
        front_matter = {
            'title': project_name,
            'project_name': project_name,
            'letter': letter,
            'cncf_status': cncf_status,
            'layout': 'single',
            'date': datetime.now().isoformat()
        }
        
        # Add research fields to front matter
        for key in ['summary', 'key_features', 'recent_updates', 'use_cases', 
                    'interesting_facts', 'get_started', 'related_tools']:
            if key in research:
                front_matter[key] = research[key]
        
        # Try to get project URLs from ETL
        for week_dir_path in glob.glob("data/week_*/"):
            for yaml_file in glob.glob(f"{week_dir_path}/*.yaml"):
                if yaml_file.endswith("tasks.yaml"):
                    continue
                
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        items = yaml.safe_load(f)
                        if items and isinstance(items, list):
                            for item in items:
                                if item.get('name') == project_name:
                                    if 'repo_url' in item:
                                        front_matter['repo_url'] = item['repo_url']
                                    if 'homepage_url' in item:
                                        front_matter['homepage_url'] = item['homepage_url']
                                    break
                except Exception:
                    pass
        
        # Create YAML front matter
        front_matter_yaml = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
        
        # Create page content
        content = f"""---
{front_matter_yaml}---

This is an auto-generated tool page. For more details, see the [letter page](/letters/{letter}/).
"""
        
        return content
    
    except Exception as e:
        print(f"Error processing {research_file}: {e}")
        return None


def main():
    """Main function to generate all tool pages."""
    tools_content_dir = Path("website/content/tools")
    tools_content_dir.mkdir(parents=True, exist_ok=True)
    
    generated_count = 0
    skipped_count = 0
    
    # Find all research files
    for research_file in glob.glob("data/week_*/research/*.yaml"):
        try:
            week_dir = Path(research_file).parent.parent.name  # Get 'week_XX_Y'
            filename = Path(research_file).stem  # Get sanitized name
            
            page_content = generate_tool_page(research_file, week_dir)
            if page_content:
                output_file = tools_content_dir / f"{filename}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(page_content)
                print(f"✓ Generated {output_file}")
                generated_count += 1
            else:
                print(f"⊘ Skipped {research_file}")
                skipped_count += 1
        
        except Exception as e:
            print(f"✗ Error processing {research_file}: {e}")
            skipped_count += 1
    
    print(f"\nGenerated: {generated_count} tool pages")
    print(f"Skipped: {skipped_count} tool pages")


if __name__ == "__main__":
    main()
