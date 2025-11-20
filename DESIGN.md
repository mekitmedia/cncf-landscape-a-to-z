# Design Document: CNCF Landscape Content Generation

## Overview

This project aims to automate the generation of content for a website and newsletter focused on the Cloud Native Computing Foundation (CNCF) landscape. The goal is to provide weekly updates covering open source projects, prioritizing discovery.

## Architecture

The system is composed of two main layers:

1.  **Deterministic Layer (ETL)**: Parses the CNCF landscape and prepares structured data.
2.  **Agentic Layer (Content Generation)**: Uses AI agents to research and draft content for the selected projects.

### 1. Deterministic Layer (ETL)

This layer is responsible for fetching the source of truth (CNCF Landscape YAML) and organizing it into manageable chunks for the downstream agents.

*   **Input**: CNCF Landscape YAML (upstream).
*   **Process**:
    *   Filters projects by letter (Weekly approach).
    *   Splits data into categories and subcategories.
    *   Generates a `tasks.yaml` for each week/letter, containing metadata for all projects to be processed.
*   **Output**:
    *   Directory structure: `data/week_XX_L/`
    *   `tasks.yaml`: List of projects with `name`, `repo_url`, `homepage`, `description`, `twitter`, etc.
    *   Summary files (README.md).

### 2. Agentic Layer

This layer consumes the `tasks.yaml` (list of projects) and generates high-quality content using **Gemini models** via Pydantic AI and Prefect.

*   **Frameworks**: [Pydantic AI](https://github.com/pydantic/pydantic-ai), [Prefect](https://www.prefect.io/), Google Gemini.

#### Workflow Steps

The agentic workflow consists of the following sequential steps for each project:

1.  **Input**: The agent receives a project name (from `tasks.yaml`) and looks up its metadata (Repo URL, Homepage).

2.  **Research Phase (Researcher Agent)**:
    *   **Search**: Performs a search to find the latest information, independent reviews, and community discussions.
    *   **Scrape**: Visits the official repository (GitHub) and documentation.
    *   **Analyze**: identifying:
        *   **Problem Solved**: What pain point does this tool address?
        *   **Key Features**: What are the main capabilities?
        *   **Recent Updates**: What changed in the last release?
        *   **Use Cases**: Who should use this and when?

3.  **Drafting Phase (Writer Agent)**:
    *   **Context**: Takes the structured research output.
    *   **Generation**: Writes a blog post adhering to the site's style guide (engaging, informative, prioritizing discovery).
    *   **Structure**:
        *   Title & Hook.
        *   "What is it?" (Clear explanation).
        *   "Why it matters" (Value prop).
        *   "Deep Dive" (Features/Architecture).
        *   "Get Started" (Installation/Usage snippet).

4.  **Review Phase (Critic Agent - Optional)**:
    *   Review the draft for technical accuracy, tone, and formatting.
    *   Request revisions if necessary.

5.  **Output**:
    *   Saves the final content as a Markdown file in `website/content/posts/YYYY-[Letter].md`.

## Release Pipeline

The release pipeline ensures high-quality and engaging content is published regularly.

### Workflow Steps

1.  **Weekly Trigger (GitHub Actions)**:
    *   A scheduled workflow runs every week.
    *   It determines the current week's letter (A, B, C...).

2.  **Run Deterministic ETL**:
    *   Fetches the latest CNCF landscape.
    *   Generates the `tasks.yaml` for the current week.

3.  **Trigger Agentic Workflow**:
    *   The action triggers the Prefect Cloud flow (or runs a local Prefect worker).
    *   Agents process the projects in `tasks.yaml`.
    *   Content is generated in `website/content/posts/YYYY-[Letter].md`.

4.  **Pull Request Creation**:
    *   The workflow uses `peter-evans/create-pull-request` to open a PR with the new content.
    *   PR Title: "Weekly Content: Letter [X]".

5.  **Human Review**:
    *   Maintainers review the generated content.
    *   Agents can be re-triggered or content manually edited.
    *   Visual regression tests (Playwright) run to ensure the site looks good.

6.  **Publish**:
    *   Upon merge, the Hugo site is built and deployed (e.g., via GitHub Pages or Netlify).
    *   Newsletter is sent (integration TBD).

## Next Steps

1.  **Implement Agentic Layer**:
    *   Set up Pydantic AI agents for "Researcher" and "Writer".
    *   Create a Prefect flow to manage the parallel execution.
2.  **Content Templates**:
    *   Define clear prompts and templates for the Writer agent to ensure consistent style.
3.  **Frontend Integration**:
    *   Ensure generated Markdown files are correctly picked up by Hugo.
    *   Enhance the theme to display "Project of the Week" or similar highlights.
