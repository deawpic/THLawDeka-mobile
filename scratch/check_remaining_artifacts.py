import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

print("Remaining occurrences of ARTIFACT or /api/v1/files in spec:")
for idx, line in enumerate(lines, 1):
    if any(k in line for k in ["ARTIFACT", "/api/v1/files", "OUTPUT_DIR"]):
        print(f"L{idx:4d}: {line}")
