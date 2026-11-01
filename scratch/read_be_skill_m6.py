import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(".agents/skills/backend-development/SKILL.md")
content = p.read_text(encoding="utf-8")
lines = content.splitlines()

for i, line in enumerate(lines, 1):
    if "Module 6" in line:
        print(f"L{i:4d}: {line}")
        for j in range(max(0, i - 1), min(len(lines), i + 40)):
            print(f"  {j+1}: {lines[j]}")
        break
