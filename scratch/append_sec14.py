import sys
from pathlib import Path

report_path = Path(r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md")
content = report_path.read_text(encoding="utf-8")

sec14_text = """

---

## 14. การจัดทำคู่มือ Quick Start Guide สำหรับส่งต่องานพัฒนา (Developer Handover)

เพื่ออำนวยความสะดวกให้นักพัฒนาท่านอื่นสามารถโคลนหรือคัดลอกโปรเจกต์นี้ไปทำต่อบนเครื่องใหม่ได้อย่างรวดเร็วและถูกต้อง ได้ทำการจัดทำเอกสาร **`QUICK_START.md`** ไว้ที่ Root Directory ของ Monorepo:

### 14.1 สาระสำคัญในเอกสาร `QUICK_START.md`
1. **ภาพรวมระบบและโครงสร้าง Monorepo:** สรุปหน้าที่ของโฟลเดอร์ `THLawDeka/`, `backend/`, `android/`, `techdocs/`
2. **สิ่งที่ต้องติดตั้งก่อนเริ่มงาน (Prerequisites):** Python 3.10+, `uv`, `agy` CLI, Tailscale, Android Studio (Ladybug/Koala, SDK 36, JDK 17)
3. **ขั้นตอนการเริ่มงาน 5 สเต็ป (5-Step Walkthrough):**
   - Step 1: ทดสอบ Local Harness Pipe (`THLawDeka/`)
   - Step 2: ติดตั้งและรัน FastAPI Backend Gateway (`backend/`) พร้อมออก API Key ผ่าน `/admin`
   - Step 3: เปิดใช้งาน Tailscale HTTPS (เลือกได้ระหว่าง Serve หรือ Funnel)
   - Step 4: เปิดและบิลด์แอป Android ผ่าน Android Studio
   - Step 5: ตรวจสอบความสมบูรณ์ทั้งระบบด้วย `python scratch/verify_all.py`
4. **กฎเหล็กการพัฒนาสำหรับทีมงาน (Engineering Iron Laws):**
   - Zero-Test by Default (ห้ามเขียน/รัน unit tests เอง)
   - No Gradle CLI for Agents (ผู้ใช้บิลด์ผ่าน Android Studio)
   - Server-Side Zero-Disk-Write Policy (เซิร์ฟเวอร์ Read-Only 100% ส่งออกเอกสารบนมือถือ)
   - 100% Portability (Relative Paths เสมอ)
5. **คู่มือคำสั่งลัดและการแก้ไขปัญหาเบื้องต้น (Cheat Sheet & Troubleshooting):**
   - คำสั่ง CLI จัดการกุญแจ `manage_keys.py`
   - สคริปต์ Background Service (Windows Task Scheduler / Linux systemd)
   - การแก้ปัญหาพอร์ตชน, Tailscale Funnel ACL, และ Android Cleartext
"""

if "## 14. การจัดทำคู่มือ Quick Start Guide สำหรับส่งต่องานพัฒนา" not in content:
    content += sec14_text
    report_path.write_text(content, encoding="utf-8")
    print("Successfully added Section 14 to agent_enhancement_report.md!")
