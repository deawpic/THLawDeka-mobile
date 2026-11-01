import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("Quick_start_Linux.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Troubleshooting" in line or (line.strip().startswith(("1.", "2.", "7.", "8.")) and "ถาม" in line):
        print(f"{i+1}: {line.strip()}")
