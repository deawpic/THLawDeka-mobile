import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# Check Section 3.6
m5_start = "### 3.6 โมดูลการส่งคืนไฟล์และดาวน์โหลดเอกสาร (Artifact & File Download Handshake Spec)"
m5_end = "### 3.7 ข้อกำหนดการเพิ่มประสิทธิภาพและความเร็วขั้นสูง (Performance & Latency Optimization Spec)"
assert m5_start in content and m5_end in content, "Section 3.6 marker not found"
print("Section 3.6 marker found!")

# Check Section 4.1
m6_start = "### 4.1 โค้ดฝั่ง Backend Gateway (`backend/main.py`)"
m6_end = "### 4.2 โค้ดฝั่ง Android Client (`LegalChatRepository.kt`)"
assert m6_start in content and m6_end in content, "Section 4.1 marker not found"
print("Section 4.1 marker found!")

# Check Section 4.2
m7_start = "### 4.2 โค้ดฝั่ง Android Client (`LegalChatRepository.kt`)"
m7_end = "### 4.3 โค้ดฝั่ง Android สำหรับการเรนเดอร์ Markdown & Tables (`MarkdownViewManager.kt`)"
assert m7_start in content and m7_end in content, "Section 4.2 marker not found"
print("Section 4.2 marker found!")

# Check Section 4.5
m8_start = "### 4.5 โค้ดฝั่ง Android สำหรับพิมพ์/ส่งออกเอกสาร PDF (`PdfExportManager.kt`)"
m8_end = "### 4.6 โค้ดฝั่ง Android สำหรับจัดเก็บการตั้งค่าแบบเข้ารหัส (`AppConfigManager.kt`)"
assert m8_start in content and m8_end in content, "Section 4.5 marker not found"
print("Section 4.5 marker found!")

# Check Section 5 & 6
m9_start = "## 5. แผนการดำเนินงานเป็นลำดับขั้น (Phase-by-Phase Implementation Plan)"
m9_end = "## 6. แนวทางการแก้ไขปัญหา (Troubleshooting & Runbook)"
assert m9_start in content and m9_end in content, "Section 5 marker not found"
print("Section 5 marker found!")
