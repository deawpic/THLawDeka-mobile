import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(".agents/skills/backend-development/SKILL.md")
content = p.read_text(encoding="utf-8")
lines = content.splitlines()

for i in range(130, len(lines)):
    print(f"{i+1:3d}: {lines[i]}")
