from pathlib import Path
import re

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

print(f"Total lines in spec: {len(lines)}")

# Find all headers
headers = []
for idx, line in enumerate(lines):
    if line.startswith("#"):
        headers.append((idx + 1, line))

for lnum, h in headers:
    if h.startswith("# ") or h.startswith("## ") or h.startswith("### "):
        print(f"{lnum:4d}: {h}")
