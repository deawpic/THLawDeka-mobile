import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

p = Path("AGENTS.md")
content = p.read_text(encoding="utf-8")
lines = content.splitlines()

for i, line in enumerate(lines, 1):
    if "Backend Developer" in line or "Mobile / Frontend Developer" in line:
        print(f"L{i:4d}: {line}")
        for j in range(i, min(len(lines), i + 20)):
            print(f"  {j+1}: {lines[j]}")
