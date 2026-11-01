import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

for fname in [".agents/skills/software-architecture/SKILL.md", ".agents/skills/product-management/SKILL.md"]:
    p = Path(fname)
    if p.exists():
        content = p.read_text(encoding="utf-8")
        for i, line in enumerate(content.splitlines(), 1):
            if any(k in line for k in ["ARTIFACT", "output/", "/api/v1/files", "files"]):
                print(f"{fname} L{i:3d}: {line}")
