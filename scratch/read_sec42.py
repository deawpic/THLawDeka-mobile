import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

# Let's inspect Section 4.2 around lines 1220 to 1320
print("=== Section 4.2 around lines 1220-1310 ===")
for i in range(1220, min(1310, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")
