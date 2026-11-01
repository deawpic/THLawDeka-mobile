from pathlib import Path

qs = Path("QUICK_START.md")
content = qs.read_text(encoding="utf-8")
lines = content.splitlines()

for i, l in enumerate(lines, 1):
    if "astral.sh" in l or "ติดตั้ง uv" in l or "Package Manager" in l:
        print(f"Line {i}: {l}")
