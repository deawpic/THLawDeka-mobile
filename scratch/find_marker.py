# -*- coding: utf-8 -*-
spec_path = r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md"
with open(spec_path, "r", encoding="utf-8") as f:
    text = f.read()

marker = "## 4. แหล่งโค้ดต้นแบบสำหรับการนำไปสร้างจริง"
pos = text.find(marker)
print(f"Marker found at position {pos}")
if pos != -1:
    print("Surrounding text:")
    print(repr(text[pos-100:pos+100]))
