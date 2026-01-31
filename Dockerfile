FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster pip
RUN pip install uv

COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

# Default command runs the agent workflow with a limit of 50 items
CMD ["python", "src/cli.py", "run", "workflow", "--limit=50", "--local"]
