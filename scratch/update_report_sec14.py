import sys
from pathlib import Path

report_path = Path(r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md")
content = report_path.read_text(encoding="utf-8")

old_sec14 = """## 14. การจัดทำคู่มือ Quick Start Guide สำหรับส่งต่องานพัฒนา (Developer Handover)

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
   - การแก้ปัญหาพอร์ตชน, Tailscale Funnel ACL, และ Android Cleartext"""

new_sec14 = """## 14. การจัดทำคู่มือ Quick Start Guide และชุดคำสั่ง Prompt ส่งต่องานพัฒนา (Developer Handover & Antigravity Workflow)

เพื่ออำนวยความสะดวกให้นักพัฒนาท่านอื่นสามารถรับไฟล์ Zip โปรเจกต์นี้ไปแตกไฟล์ เปิดใน **Antigravity Desktop** และสั่งการ AI Agent ให้เริ่มพัฒนาตั้งแต่ Phase 1 จนเสร็จสมบูรณ์ ได้ทำการปรับปรุงเอกสาร **`QUICK_START.md`** ไว้ที่ Root Directory ของ Monorepo โดยเพิ่มหัวข้อสำคัญดังนี้:

### 14.1 สาระสำคัญที่เพิ่มเข้าไปใน `QUICK_START.md`
1. **การเตรียมไฟล์ Zip และการนำเข้าสู่ Antigravity Desktop (Section 1):**
   - คำแนะนำสิ่งที่ควรลบก่อนบีบอัดไฟล์ (`.venv/`, `__pycache__/`, `build/`) เพื่อความสะอาดและเบา
   - ขั้นตอนการ Import โปรเจกต์ผ่านเมนู `File -> Open Workspace...` ใน Antigravity Desktop
2. **คลังคำสั่ง Prompt สำหรับสั่งการ Agent ตั้งแต่ Phase 1 ถึง Phase 5 (Section 2):**
   - **ทางเลือกที่ 1 (Master Autonomous Prompt):** ชุดคำสั่งเดียวให้ Agent เริ่มทำงานอัตโนมัติต่อเนื่องตั้งแต่ Phase 1 ถึง Phase 5 พร้อมตีกรอบกฎเหล็ก
   - **ทางเลือกที่ 2 (Phase-by-Phase Prompts):** ชุดคำสั่งแยกรายเฟส สำหรับผู้พัฒนาที่ต้องการสั่งการและตรวจรับงานทีละสเต็ป (Phase 1 ถึง Phase 5)
3. **ภาพรวมระบบและโครงสร้าง Monorepo (Section 3):** สรุปหน้าที่ของโฟลเดอร์ `THLawDeka/`, `backend/`, `android/`, `techdocs/`
4. **สิ่งที่ต้องติดตั้งก่อนเริ่มงาน (Prerequisites - Section 4):** Python 3.10+, `uv`, `agy` CLI, Tailscale, Android Studio (Ladybug/Koala, SDK 36, JDK 17)
5. **คู่มือการเริ่มงานทางเทคนิคทีละสเต็ป (Manual Verification - Section 5):**
   - Step 1: ทดสอบ Local Safe Stdin Pipe (`THLawDeka/`)
   - Step 2: ติดตั้งและรัน FastAPI Backend Gateway (`backend/`) พร้อมออก API Key ผ่าน `/admin`
   - Step 3: เปิดใช้งาน Tailscale HTTPS (Serve & Funnel)
   - Step 4: เปิดและบิลด์แอป Android ผ่าน Android Studio
   - Step 5: ตรวจสอบความสมบูรณ์ทั้งระบบด้วย `python scratch/verify_all.py`
6. **กฎเหล็กการพัฒนาสำหรับทีมงาน (Engineering Iron Laws - Section 6):**
   - Zero-Test by Default (ห้ามเขียน/รัน unit tests เอง)
   - No Gradle CLI for Agents (ผู้ใช้บิลด์ผ่าน Android Studio)
   - Server-Side Zero-Disk-Write Policy (เซิร์ฟเวอร์ Read-Only 100% ส่งออกเอกสารบนมือถือ)
   - 100% Portability (Relative Paths เสมอ)
7. **คู่มือคำสั่งลัดและการแก้ไขปัญหาเบื้องต้น (Cheat Sheet & Troubleshooting - Section 7-8):**
   - คำสั่ง CLI จัดการกุญแจ `manage_keys.py`
   - สคริปต์ Background Service (Windows Task Scheduler / Linux systemd)
   - การแก้ปัญหาพอร์ตชน, Tailscale Funnel ACL, และ Android Cleartext"""

assert old_sec14 in content, "old_sec14 not found"
content = content.replace(old_sec14, new_sec14)

report_path.write_text(content, encoding="utf-8")
print("Successfully updated Section 14 in agent_enhancement_report.md!")
