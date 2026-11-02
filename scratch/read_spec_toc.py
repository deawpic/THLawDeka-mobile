import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines[:60]):
    print(f"{i+1}: {line.strip()}")
