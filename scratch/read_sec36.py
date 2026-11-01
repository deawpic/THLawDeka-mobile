import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

# Let's inspect Section 3.6 lines 690-760
print("=== Section 3.6 lines 690 to 765 ===")
for i in range(690, min(765, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")
