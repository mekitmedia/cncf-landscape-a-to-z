---
title: "Putting Jules to Work: Asynchronous AI Agents in a 52-Week Cloud Native Journey"
date: 2026-10-05T20:00:00Z
draft: true
letter: "Meta"
tags:
  - "ai-agents"
  - "jules"
  - "cncf"
  - "automation"
  - "devops"
---

With over 1,000 projects spanning service meshes, container runtimes, observability pipelines, and AI orchestrators, the [CNCF Landscape](https://landscape.cncf.io/) is as vast as it is fast-moving. When we set out on our **CNCF Landscape A-to-Z in 52 Weeks** project, our goal was simple: explore the entire ecosystem letter by letter, sharing concise overviews, architectural deep-dives, and getting-started guides for every tool in the landscape.

However, behind that simple goal lies a massive operational challenge. Curating, fact-checking, and structuring information for dozens of projects every single week quickly overwhelms a solo maintainer. To avoid burnout, we needed more than just a chat-based assistant that requires constant prompt babysitting; we needed **asynchronous AI background workers**.

Enter **Google Labs Jules**. Over the past few months, we integrated Jules into our GitHub workflow to handle small bug fixes, data pipeline optimizations, and automated project research tasks. 

In this post, we’ll break down what Jules is, what it does well (and where its limits lie), how we structured our repository to make it thrive, and what we learned about putting autonomous agents to work on real-world engineering and content workflows.

---

## What is Jules?

**Jules** is an experimental asynchronous coding agent developed by Google Labs. Unlike synchronous chat interfaces or inline code-completion extensions (like GitHub Copilot or Cursor) that require an engineer to stay in the loop during generation, Jules is designed to work autonomously in the background directly against your GitHub repositories.

When you dispatch a task to Jules—whether via a scheduled job, a prompt, or an issue—it:
1. Clones your repository and inspects the codebase.
2. Develops a multi-step plan to solve the prompt or task description.
3. Makes necessary file edits, runs scripts, or structures data.
4. Commits the changes under `google-labs-jules[bot]` on a dedicated branch.
5. Opens a clean Pull Request with a summary of its changes for human review.

This asynchronous model shifts the human role from **prompt writer** to **code reviewer**. Instead of waiting for tokens to stream into a terminal, you queue tasks and review ready-to-merge pull requests whenever you are ready.

---

## What Can Jules Do? Real Examples from Our Repo

We put Jules to work across a variety of tasks ranging from quick UI chores to multi-step research and code refactoring. Here are a few concrete examples straight from our git commit history:

### 1. Small Frontend & Configuration Chores
Small housekeeping tasks often take longer to context-switch into than to actually write. Jules handled these effortlessly:
* **Custom 404 Pages**: When we needed a fallback page for un-generated tool routes ([PR #111](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/111)), Jules created the Hugo template, styled it to match our theme, and verified the routing structure.
* **UI Label Migrations**: When updating our project schedule from 26 weeks to 52 weeks ([PR #97](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/97)), Jules scanned templates and replaced all user-facing references cleanly without breaking internal variable names.
* **Navigation & Config Tweaks**: Jules injected Google Analytics partials into Hugo headers ([PR #103](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/103)) and added repository links to the main navigation header ([PR #98](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/98)).

### 2. Code Optimization & Performance Refactoring
We noticed our static page generator `tool_pages.py` was slowing down as the number of researched projects grew. We assigned Jules the task of optimizing the script:
* **Optimizing N+1 File Reads**: In [PR #73](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/73), Jules diagnosed an N+1 filesystem bottleneck, introduced in-memory caching for category files, and cut pipeline execution time significantly—all while preserving the script's original interface and unit test compatibility.

### 3. Autonomous Project Research & Schema Population
Our primary content workflow requires researching CNCF projects and outputting standardized YAML files for our static site generator. 

Jules took on individual research tasks for projects such as **Akri** ([PR #116](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/116)), **Atlantis** ([PR #114](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/114)), **Athenz** ([PR #113](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/113)), and **Aeraki Mesh** ([PR #110](https://github.com/mekitmedia/cncf-landscape-a-to-z/pull/110)).

For each task, Jules produced structured output adhering strictly to our research contract:

```yaml
project_name: "Akri"
summary: "Akri (A Kubernetes Resource Interface for the Edge) is a Cloud Native Computing Foundation (CNCF) Sandbox project that easily exposes heterogeneous leaf devices—such as IP cameras, USB sensors, and OPC UA equipment—as resources in a Kubernetes cluster."
key_features:
  - "Automated discovery of IoT edge devices (ONVIF, udev, OPC UA, etc.)"
  - "Exposes devices as Kubernetes Custom Resources (CRDs)"
  - "Extends the Kubernetes device plugin framework for the edge"
  - "Schedules workloads automatically on nodes where devices are detected"
  - "Supports high availability and device failover"
recent_updates: "Akri continues to grow its ecosystem of discovery handlers, enabling support for a wider array of industrial and edge protocols..."
use_cases: "Simplifying edge computing deployments by automating the connection of cameras in retail, sensors in warehouses, and OPC UA equipment..."
get_started: "Install Akri using its Helm charts (`helm install akri akri-helm-charts/akri`), apply an Akri Configuration..."
```

---

## Performance Report Card: Strengths & Boundaries

After processing dozens of PRs with Jules, clear patterns emerged regarding its strengths and operational boundaries:

### Small Tasks: ⭐⭐⭐⭐⭐ (Outstanding)
For single-file edits, localized bug fixes, template adjustments, and configuration updates, Jules is exceptional. It rarely hallucinates file paths, respects existing code conventions, and generates clean, minimal diffs.

### Medium Tasks: ⭐⭐⭐⭐ (Very Good)
For medium-complexity tasks—such as implementing a caching layer across a pipeline module or generating structured project research—Jules performs reliably **if and only if** the task is bounded by clear constraints. When provided with an explicit schema and a defined target output, it completes the task with high fidelity.

### Web Search & Information Retrieval: ⭐⭐⭐½ (Good for First-Pass Discovery)
One of the most interesting aspects of Jules is its search capability:
* **The "First Search Layer"**: Jules excels at acting as an initial retrieval layer. It inspects repository metadata, READMEs, release notes, and documentation linked within the project's repository to extract core features and installation commands.
* **GitHub-Centric Scope**: In our experience, Jules's search behavior stays tightly scoped to GitHub repositories, official documentation links, and directly discoverable repository assets. It does not perform open-ended, deep-web exploratory scraping across arbitrary tech blogs or forum threads.
* **The Verdict on Knowledge Bases**: Jules is not meant to autonomously build an entire external multi-source knowledge base from scratch. However, it is **more than enough for first-pass data extraction**—gathering accurate baseline facts, commands, and summaries that can then be validated by a human editor or synthesized into a final weekly post.

---

## How We Architected the Workflow

To make asynchronous agents effective at scale, you cannot simply throw unstructured prompts at them. We built an architecture based on four core principles:

```
┌─────────────────────────────────────────────────────────────┐
│                   JULES ASYNC WORKFLOW                      │
│                                                             │
│  ┌────────────────┐         ┌────────────────────────────┐  │
│  │  tracker.yaml  │───────► │ Dispatch Task to Jules     │  │
│  │ (Pending Task) │         │ (Project + Schema Contract)│  │
│  └────────────────┘         └─────────────┬──────────────┘  │
│                                           │                 │
│                                           ▼                 │
│                             ┌────────────────────────────┐  │
│                             │ Google Labs Jules          │  │
│                             │ • First-pass repo search   │  │
│                             │ • Writes research/*.yaml   │  │
│                             │ • Updates tracker.yaml     │  │
│                             └─────────────┬──────────────┘  │
│                                           │                 │
│                                           ▼                 │
│  ┌────────────────┐         ┌────────────────────────────┐  │
│  │ Merged to Main │◄─────── │ GitHub Pull Request        │  │
│  │ (Published)    │         │ (Human Review & QA)        │  │
│  └────────────────┘         └────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1. Rigid Schema Contracts
Agents hallucinate when instructions are vague. We created strict YAML schemas for both input tasks and output research. By pointing Jules to an exact format (`summary`, `key_features`, `use_cases`, `get_started`), the model knows precisely what fields to populate and what types are expected.

### 2. Granular Task Decomposition
Instead of asking Jules to "research all 50 projects starting with the letter A," we decomposed the workload into atomic units: **1 Project = 1 Task = 1 Pull Request**.
This granular approach has major advantages:
* If one project fails or requires manual correction, it doesn't block the other 49.
* Pull requests remain small (10–30 lines), making code review fast and frictionless.
* Token budgets and execution timeouts are kept well within safe limits.

### 3. State Synchronization via `tracker.yaml`
We keep state in git. Each week directory contains a `tracker.yaml` file tracking the status of every project (`pending`, `in_progress`, `completed`, `failed`). When Jules completes a research file, its task instructions require it to update the corresponding tracker entry in the same PR. Merging the PR atomically commits both the data and its completion status.

### 4. Human-in-the-Loop Review
Jules does not push directly to `main`. Every contribution arrives as a PR. Reviewing a 20-line YAML file takes less than 30 seconds: verify that the project name is accurate, the links are functional, and the features make sense, then click **Merge**.

---

## Key Takeaways for Engineering Teams

If you're considering integrating asynchronous agents like Jules into your software lifecycle or content engine, keep these lessons in mind:

1. **Treat Agents as Junior Engineers with PR Privileges**: Never allow autonomous agents to commit directly to production branches. The pull request review model provides the ideal safety boundary.
2. **Invest in Task Definitions & Schemas**: The quality of an asynchronous agent's output is directly proportional to how well-defined your inputs and outputs are. Rigid templates eliminate 90% of hallucination risks.
3. **Use the Right Tool for the Right Job**: 
   * Use **Jules** for async repository chores, bug fixes, script optimizations, and first-layer GitHub research.
   * Use **orchestrated multi-agent pipelines** (such as Prefect + Pydantic AI) when you need complex multi-turn editorial loops, custom search harnesses, or real-time consensus between multiple specialized personas.
4. **Embrace Asynchronous Batching**: The true productivity multiplier isn't how fast an LLM streams tokens—it's having tasks run in the background while you focus on higher-level architectural decisions.

---

## What's Next?

With Jules handling first-layer research and repo housekeeping, we're accelerating our journey through the CNCF landscape. In our upcoming posts, we'll look at the projects starting with **D**, **E**, and beyond, while continuously refining our agentic pipelines.

Have you tried using asynchronous agents like Jules in your repositories? Let us know your thoughts and favorite workflows!
