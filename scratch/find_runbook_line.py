import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")
lines = content.splitlines()

for i, line in enumerate(lines, 1):
    if "ดาวน์โหลดไฟล์ไม่ผ่าน" in line or "output/" in line:
        print(f"L{i:4d}: {line}")
