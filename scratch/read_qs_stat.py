from pathlib import Path

qs = Path("QUICK_START.md")
content = qs.read_text(encoding="utf-8")
print(f"Current QUICK_START.md length: {len(content)} characters, {len(content.splitlines())} lines")
