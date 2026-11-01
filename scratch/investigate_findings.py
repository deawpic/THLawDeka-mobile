import sys
import re
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

# 1. Investigate Section 4.8 header
print("=== Section 4.8 Inspection ===")
for i, line in enumerate(lines):
    if "4.8" in line:
        print(f"Line {i+1}: {repr(line)}")
        for j in range(i, min(i + 20, len(lines))):
            print(f"  {j+1}: {lines[j]}")
        break

# 2. Investigate the 2 TODOs
print("\n=== TODO / Placeholder Occurrences ===")
for i, line in enumerate(lines):
    m = re.search(r"(?i)\b(todo|fixme|xxx|tbd|placeholder)\b", line)
    if m:
        print(f"Line {i+1}: {repr(line)}")

# 3. Investigate Diagram 7
print("\n=== Mermaid Diagrams Inspection ===")
mermaid_blocks = re.finditer(r"```mermaid\s*(.*?)\s*```", content, re.DOTALL)
for idx, mb in enumerate(mermaid_blocks, 1):
    first_lines = mb.group(1).strip().splitlines()[:3]
    print(f"Diagram {idx} (starts around char {mb.start()}): {first_lines}")
