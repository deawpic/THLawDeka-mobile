import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(".agents/skills/frontend-development/SKILL.md")
content = p.read_text(encoding="utf-8")
lines = content.splitlines()

for i, line in enumerate(lines, 1):
    if any(k in line for k in ["Artifact", "file", "export", "PdfExportManager", "download"]):
        print(f"L{i:4d}: {line}")
