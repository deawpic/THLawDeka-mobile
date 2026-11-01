import sys
from pathlib import Path

qs = Path("QUICK_START.md")
content = qs.read_text(encoding="utf-8")

old_text = 'powershell -c "irm https://astral.sh/uv/install.ps1 \\| iex"'
new_text = 'powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \\| iex" หรือ `winget install --id astral-sh.uv`'

if old_text in content:
    content = content.replace(old_text, new_text)
    qs.write_text(content, encoding="utf-8")
    print("Updated QUICK_START.md with uv install command!")
