import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# Find Section 4.8
start = content.find("### 4.8 โค้ดฝั่ง Backend สำหรับฐานข้อมูลกุญแจ")
end = content.find("### 4.9", start)
print(content[start:start+1500])
