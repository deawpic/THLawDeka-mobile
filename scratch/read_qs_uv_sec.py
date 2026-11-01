import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

qs = Path("QUICK_START.md")
lines = qs.read_text(encoding="utf-8").splitlines()

for i, l in enumerate(lines, 1):
    if "### 📌 คำสั่งติดตั้ง `uv`" in l:
        for j in range(i, min(i+45, len(lines))):
            print(f"Line {j}: {lines[j-1]}")
        break
