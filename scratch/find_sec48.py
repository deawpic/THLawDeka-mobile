from pathlib import Path

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

for i, line in enumerate(lines):
    if "### 4.8" in line:
        print(f"Line {i+1}: {repr(line)}")
        for j in range(i, min(i + 30, len(lines))):
            print(f"  {j+1}: {lines[j]}")
        break
