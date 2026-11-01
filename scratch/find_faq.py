import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("Quick_start_Windows.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "### Q" in line or "Troubleshooting" in line or "คำถาม" in line:
        print(f"{i+1}: {line.strip()}")
