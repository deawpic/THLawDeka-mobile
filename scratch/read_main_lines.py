import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

# Let's inspect Section 4.1 lines 850-960 and 1050-1170
print("=== Section 4.1 around lines 860-910 ===")
for i in range(860, min(910, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")

print("\n=== Section 4.1 around lines 1060-1160 ===")
for i in range(1060, min(1160, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")
