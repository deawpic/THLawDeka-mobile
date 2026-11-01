from pathlib import Path

spec = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec.read_text(encoding="utf-8")
lines = content.splitlines()

for i, l in enumerate(lines, 1):
    if "### เฟสที่ 1" in l:
        print(f"Spec line {i}: {l}")
        for j in range(i, min(i+25, len(lines))):
            print(f"  {j}: {lines[j-1]}")
