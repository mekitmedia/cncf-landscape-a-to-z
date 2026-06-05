import re

with open("src/pipeline/transform.py", "r") as f:
    content = f.read()

# Replace all occurrences of sub['items'] with (sub.get('items') or [])
# in list comprehensions and for loops.
content = content.replace("sub['items']", "(sub.get('items') or [])")

with open("src/pipeline/transform.py", "w") as f:
    f.write(content)
