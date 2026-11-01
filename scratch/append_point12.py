# -*- coding: utf-8 -*-
report_path = r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md"

addition = """12. **การตรวจสอบความถูกต้องและสมบูรณ์ขั้นสูงสุด (Deep Integrity Audit Sign-Off):**
    - พัฒนาสคริปต์ตรวจสอบความสมบูรณ์เชิงโครงสร้าง [audit_quickstarts_integrity.py](scratch/audit_quickstarts_integrity.py)
    - ยืนยันครบถ้วนทั้ง 18 หมวดหัวข้อสำคัญในทั้ง [Quick_start_Windows.md](Quick_start_Windows.md) และ [Quick_start_Linux.md](Quick_start_Linux.md)
    - ตรวจสอบลำดับคำถาม Troubleshooting ทั้ง 7 ข้อเรียงลำดับถูกต้องต่อเนื่อง (1 ถึง 7)
    - บาลานซ์บล็อกโค้ด Markdown (```) ปิดเปิดถูกต้อง 100% (Windows 15 บล็อก, Linux 31 บล็อก)
    - ลบเส้นแบ่งแนวนอน `---` ซ้ำซ้อน และยืนยัน Zero `file://` URIs และ Zero Hardcoded Absolute Paths
"""

with open(report_path, "a", encoding="utf-8") as f:
    f.write(addition)

print("Added point 12 to agent_enhancement_report.md.")
