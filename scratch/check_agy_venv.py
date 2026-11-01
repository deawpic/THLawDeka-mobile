import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

qs = Path("QUICK_START.md")
content = qs.read_text(encoding="utf-8")
print("Has agy test:", "agy -p" in content)
print("Has uv venv:", "uv venv" in content)
