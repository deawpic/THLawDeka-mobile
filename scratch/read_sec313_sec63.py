import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

print("=== Section 3.1.3 lines 205-245 ===")
for i in range(204, min(245, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")

print("\n=== Section 6.3 lines 2385-2415 ===")
for i in range(2384, min(2415, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")
