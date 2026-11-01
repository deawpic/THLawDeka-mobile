import sys
from pathlib import Path

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# Check if references are present
ref_url = "https://antigravity.google/docs/overview"

# In header metadata:
old_header = "**Official Documentation Reference:** [Google Antigravity Overview](https://antigravity.google/docs/overview)"
new_header = "**แหล่งอ้างอิงเอกสารหลัก (Official Documentation Reference):** [Google Antigravity Overview](https://antigravity.google/docs/overview)"

if old_header in content:
    content = content.replace(old_header, new_header)

# In Section 1:
old_sec1 = "เพื่อแยกบทบาทระหว่าง Mobile Client Gateway และ Core Agent อย่างชัดเจน ป้องกันความสับสนในการพัฒนาและบำรุงรักษาระบบ"
new_sec1 = "โดยพัฒนาตามมาตรฐานและสถาปัตยกรรมหลักของ Google Antigravity อย่างเป็นทางการ (แหล่งอ้างอิง: https://antigravity.google/docs/overview) เพื่อแยกบทบาทระหว่าง Mobile Client Gateway และ Core Agent อย่างชัดเจน ป้องกันความสับสนในการพัฒนาและบำรุงรักษาระบบ"

if old_sec1 in content and "แหล่งอ้างอิง: https://antigravity.google/docs/overview" not in content:
    content = content.replace(old_sec1, new_sec1)

spec_path.write_text(content, encoding="utf-8")
print("Successfully verified/updated reference in techdocs/system_spec_and_implementation_plan.md!")
