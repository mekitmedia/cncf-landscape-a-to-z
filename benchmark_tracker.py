
import time
import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path.cwd()))

from src.tracker.yaml_backend import YAMLTrackerBackend

def benchmark():
    backend = YAMLTrackerBackend()

    # Warm up
    backend.get_ready_tasks()

    start_time = time.perf_counter()
    iterations = 10
    for _ in range(iterations):
        tasks = backend.get_ready_tasks()
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for get_ready_tasks: {avg_time:.4f} seconds")
    print(f"Number of ready tasks found: {len(tasks)}")

if __name__ == "__main__":
    benchmark()
