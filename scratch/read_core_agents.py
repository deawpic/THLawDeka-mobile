import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

agents_path = Path("THLawDeka/AGENTS.md")
content = agents_path.read_text(encoding="utf-8")
lines = content.splitlines()

for i, line in enumerate(lines, 1):
    if "Section 7" in line or "ARTIFACT" in line or "output/" in line:
        print(f"L{i:4d}: {line}")
        for j in range(max(0, i - 1), min(len(lines), i + 25)):
            print(f"  {j+1}: {lines[j]}")
        break
