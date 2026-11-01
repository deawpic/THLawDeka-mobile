import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

# Let's inspect Section 4.5 lines 1450-1560
print("=== Section 4.5 lines 1450-1560 ===")
for i in range(1450, min(1560, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")
