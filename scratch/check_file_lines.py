from pathlib import Path

qs = Path("QUICK_START.md")
lines = qs.read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines, 1):
    if "file://" in l:
        print(f"QUICK_START.md line {i}: {l}")

spec = Path("techdocs/system_spec_and_implementation_plan.md")
lines_spec = spec.read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines_spec, 1):
    if "file://" in l:
        print(f"spec line {i}: {l}")
