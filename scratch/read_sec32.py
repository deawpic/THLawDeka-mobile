import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

# Let's inspect Section 3.2 SSE protocol around lines 310-345
print("=== Section 3.2 lines 310 to 345 ===")
for i in range(310, min(345, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")
