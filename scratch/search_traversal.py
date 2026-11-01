from pathlib import Path

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()
for idx, line in enumerate(lines):
    if "Path Traversal" in line or "basename" in line:
        print(f"Line {idx+1}: {repr(line)}")
