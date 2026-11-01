import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(".agents/skills/software-architecture/SKILL.md")
content = p.read_text(encoding="utf-8")
lines = content.splitlines()

for i in range(80, min(120, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")
