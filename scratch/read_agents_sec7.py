import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

agents_path = Path("THLawDeka/AGENTS.md")
content = agents_path.read_text(encoding="utf-8")
lines = content.splitlines()

for i in range(100, min(160, len(lines))):
    print(f"{i+1:3d}: {lines[i]}")
