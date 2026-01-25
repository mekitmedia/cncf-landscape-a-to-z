from invoke import task
import sys

@task
def setup(c):
    """Install dependencies."""
    c.run(f"{sys.executable} -m pip install -r requirements.txt")
    if sys.platform != "win32":
        # Optional: install dev requirements if they exist
        c.run(f"{sys.executable} -m pip install -r requirements-dev.txt", warn=True)

@task
def test(c):
    """Run tests."""
    c.run(f"{sys.executable} -m unittest discover tests")

@task
def run_pipeline(c):
    """Run the main pipeline."""
    c.run(f"{sys.executable} src/cli.py run etl")

@task
def lint(c):
    """Run linting (placeholder)."""
    print("Linting setup pending decision on linter")

@task
def clean(c):
    """Clean up generated data."""
    import shutil
    import os
    if os.path.exists("data"):
        shutil.rmtree("data")
        print("Removed data/ directory")
