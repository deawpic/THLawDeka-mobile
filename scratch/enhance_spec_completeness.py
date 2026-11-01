import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# 1. Update Section 5: Phase-by-Phase Plan with comprehensive details & Gherkin criteria
old_sec5 = """## 5. แผนการดำเนินงานเป็นลำดับขั้น (Phase-by-Phase Implementation Plan)

```mermaid
flowchart TD
    Phase1["<b>Phase 1: Local Harness Pipe Test</b><br/>ทดสอบสั่ง agy ผ่าน stdin ด้วย Python script"]
    Phase2["<b>Phase 2: FastAPI Gateway & SSE</b><br/>สร้าง API Gateway ทดสอบสตรีมด้วย curl"]
    Phase3["<b>Phase 3: Tailscale HTTPS Setup</b><br/>เปิดใช้งาน tailscale serve รับรอง SSL"]
    Phase4["<b>Phase 4: Android App Integration</b><br/>เขียน OkHttp SSE + แสดงผล Markdown"]
    Phase5["<b>Phase 5: E2E Verification & Hardening</b><br/>ทดสอบสลับเน็ต 4G/5G และทดสอบโหลดคิว"]

    Phase1 --> Phase2
    Phase2 --> Phase3
    Phase3 --> Phase4
    Phase4 --> Phase5
```

### เฟสที่ 1: ตรวจสอบและทดสอบ `agy stdin` Pipe บน Local Host (Day 1)
- **เป้าหมาย:** พิสูจน์ว่า `agy` สามารถรับข้อเท็จจริงคดีผ่าน `stdin` และส่งผลวิเคราะห์ออกมาทาง `stdout` ได้ 100%
- **ขั้นตอนการทำ:**
  1. สร้างสคริปต์สั้น `test_pipe.py`
  2. รันคำสั่งทดสอบ: `python test_pipe.py`
  3. ตรวจสอบว่าไม่มีคำถามคดีความปรากฏในคำสั่ง Process ของระบบปฏิบัติการ

### เฟสที่ 2: พัฒนาและทดสอบ FastAPI Gateway + Admin UI + SSE (Day 1-2)
- **เป้าหมาย:** ให้ Gateway สามารถตรวจสอบสิทธิ์ด้วย `keys.db`, เปิดหน้าเว็บ `/admin` สำหรับออก/เพิกถอนกุญแจ และส่ง Event SSE ไปยัง Client ได้อย่างถูกต้อง
- **ขั้นตอนการทำ:**
  1. สร้างไฟล์ `backend/auth_db.py`, `backend/templates/admin.html` และ `backend/main.py`
  2. ติดตั้ง Dependencies ใน virtual environment (แนะนำ: `uv venv && uv pip install -r requirements.txt` หรือ `pip install -r requirements.txt`)
  3. สั่งรันเซิร์ฟเวอร์: `uv run uvicorn main:app --port 8000` (หรือ `uvicorn main:app --port 8000`)
  4. เข้าหน้าเบราว์เซอร์ `http://127.0.0.1:8000/admin` เพื่อทดสอบสร้างกุญแจสำหรับผู้ใช้งานคนแรก
  5. ทดสอบยิงคำขอด้วยคำสั่ง `curl` โดยใช้กุญแจที่เพิ่งสร้าง:
     ```bash
     curl -N -X POST http://127.0.0.1:8000/api/v1/chat/stream \\
       -H "Authorization: Bearer <กุญแจที่สร้างจากหน้า admin>" \\
       -H "Content-Type: application/json" \\
       -d "{\\"query\\": \\"ให้เพื่อนยืมเงิน 50,000 บาท มีแชตไลน์แต่ไม่ได้เซ็นสัญญา ฟ้องได้ไหม\\"}"
     ```

### เฟสที่ 3: กำหนดค่าเครือข่าย Tailscale HTTPS บน Home Server (Day 2)
- **เป้าหมาย:** เปลี่ยน Local Port 8000 ให้กลายเป็น Public HTTPS ภายในวง Tailnet
- **ขั้นตอนการทำ:**
  1. ตรวจสอบสถานะการเชื่อมต่อ: `tailscale status`
  2. เปิดใช้งาน Reverse Proxy HTTPS:
     ```bash
     tailscale serve --bg https / http://127.0.0.1:8000
     ```
  3. บันทึก URL ที่ได้รับ เช่น `https://my-server.tailnet-xyz.ts.net`

### เฟสที่ 4: พัฒนาแอปพลิเคชัน Android (Day 3-4)
- **เป้าหมาย:** สร้าง UI สำหรับแชตที่รองรับการรับข้อความแบบสตรีมมิ่ง, จัดการประวัติการสนทนา (แชตต่อของเดิม / สร้างแชตใหม่ / ลบแชต), เรนเดอร์ Markdown พร้อมตาราง, แสดงผัง Mermaid ในตัวเครื่อง, สั่งพิมพ์/ส่งออก PDF, และมีหน้าจอตั้งค่า Tailscale Gateway URL + authen_key แบบเข้ารหัส
- **ขั้นตอนการทำ:**
  1. เพิ่มไลบรารี `okhttp-sse`, `markwon`, `markwon-ext-tables`, `webkit` และ `security-crypto` ใน `build.gradle.kts`
  2. พัฒนาระบบจัดเก็บการตั้งค่าแบบเข้ารหัส `AppConfigManager.kt` และหน้าจอตั้งค่า `ConnectionSettingsManager.kt`
  3. พัฒนาระบบจัดการประวัติห้องแชตด้วย SQLite ภายในเครื่อง `ChatDatabaseHelper.kt` (รองรับการแชตต่อของเดิม, การสร้างแชตใหม่, และการลบแชตพร้อม Confirm Dialog)
  4. เขียนคลาสเชื่อมต่อเครือข่าย `LegalChatRepository.kt` ดึง URL และ Key จาก Config พร้อมส่ง `conversation_id` เมื่อแชตต่อของเดิม
  5. ติดตั้งคลาสแสดงผล `MarkdownViewManager.kt` และสร้างเทมเพลต `mermaid_template.html` ในโฟลเดอร์ assets พร้อมคลาส `MermaidRendererView.kt`
  6. เพิ่มฟังก์ชันส่งออกเอกสาร `PdfExportManager.kt`
  7. ทำกล่องแสดงสถานะ (Status Chip) เพื่อโชว์ข้อความจาก `event: status`
  8. ทดสอบเชื่อมต่อผ่าน URL ของ Tailscale HTTPS ด้วยปุ่ม Test Connection

### เฟสที่ 5: การทดสอบรอบด้านและรับมือข้อผิดพลาด (End-to-End Verification) (Day 5)
- **เป้าหมาย:** รับประกันเสถียรภาพในการใช้งานจริง
- **รายการตรวจสอบ (Test Checklist):**
  - [ ] **Network Switching Test:** ทดสอบถามคำถามขณะใช้ Wi-Fi แล้วเดินตัดสัญญาณเข้า 4G/5G
  - [ ] **Timeout Test:** ยิงคำถามที่ซับซ้อนมาก และตรวจสอบว่าระบบตัดจบตามเวลา 60 วินาทีอย่างถูกต้อง
  - [ ] **Injection Prevention Test:** ส่งอักขระพิเศษ (เช่น quotes, semicolons, shell pipe) เพื่อยืนยันว่าไม่กระทบต่อ OS
  - [ ] **Markdown Rendering Test:** ตรวจสอบว่าตารางเปรียบเทียบข้อกฎหมายและบล็อกโค้ดแสดงผลได้ถูกต้องบนหน้าจอมือถือ"""

new_sec5 = """## 5. แผนการดำเนินงานเป็นลำดับขั้น (Phase-by-Phase Implementation Plan)

```mermaid
flowchart TD
    Phase1["<b>Phase 1: Local Harness Pipe Test</b><br/>ทดสอบสั่ง agy ผ่าน stdin ด้วย Python script"]
    Phase2["<b>Phase 2: FastAPI Gateway & SSE</b><br/>สร้าง API Gateway, Admin UI, Fast-Path Cache & File Endpoint"]
    Phase3["<b>Phase 3: Tailscale HTTPS Setup</b><br/>เปิดใช้งาน tailscale serve รับรอง SSL + Direct STUN"]
    Phase4["<b>Phase 4: Android App Integration</b><br/>OkHttp SSE, Markwon GFM, 50ms Throttler & PDF Export<br/><i>(User builds/runs via Android Studio)</i>"]
    Phase5["<b>Phase 5: E2E Verification & Hardening</b><br/>ทดสอบสลับเน็ต, 60s Zombie Reaper, RCE Fuzzing & Cache Speed"]

    Phase1 --> Phase2
    Phase2 --> Phase3
    Phase3 --> Phase4
    Phase4 --> Phase5
```

### เฟสที่ 1: ตรวจสอบและทดสอบ `agy stdin` Pipe บน Local Host (Day 1)
- **เป้าหมาย:** พิสูจน์ว่า `agy` สามารถรับข้อเท็จจริงคดีผ่าน `stdin` และส่งผลวิเคราะห์ออกมาทาง `stdout` ได้ 100% โดยไม่มีข้อเท็จจริงคดีหลุดรอดใน Process Table
- **เกณฑ์การยอมรับ (Acceptance Criteria - Gherkin):**
  - **Given** เครื่องคอมพิวเตอร์ติดตั้ง `agy` CLI และอยู่ในโฟลเดอร์ `THLawDeka/`
  - **When** สคริปต์ส่งคำถามกฎหมายผ่าน `stdin` (`-p -`) ด้วย `asyncio.subprocess.PIPE`
  - **Then** ได้รับคำตอบสตรีม NDJSON ทาง `stdout` โดยที่คำสั่ง OS (`ps` หรือ `wmic process`) ปรากฏเพียงอาร์กิวเมนต์ `-p -` เท่านั้น
- **ขั้นตอนการทำ:**
  1. สร้างสคริปต์สั้น `test_pipe.py` ในเครื่อง
  2. รันคำสั่งทดสอบ: `python test_pipe.py`
  3. ตรวจสอบว่าไม่มีคำถามคดีความปรากฏในคำสั่ง Process ของระบบปฏิบัติการ

### เฟสที่ 2: พัฒนาและทดสอบ FastAPI Gateway + Admin UI + SSE + Fast-Path Cache (Day 1-2)
- **เป้าหมาย:** สร้าง ASGI Gateway ตรวจสอบสิทธิ์ด้วย `keys.db`, เปิดหน้าเว็บ `/admin`, ให้บริการสตรีม SSE, Fast-Path Legal Cache (<5ms), และ Endpoint ดาวน์โหลดเอกสาร `GET /api/v1/files/{filename}`
- **เกณฑ์การยอมรับ (Acceptance Criteria - Gherkin):**
  - **Given** เซิร์ฟเวอร์ Gateway ทำงานที่พอร์ต 8000 และมี SQLite `keys.db` (โหมด WAL)
  - **When** ผู้ดูแลระบบเข้าหน้า `GET /admin` และป้อน Master Secret
  - **Then** สามารถออกกุญแจใหม่ และสั่งเพิกถอนกุญแจ (Revoke) ได้ทันทีแบบ Real-time ($O(1)$ In-Memory Cache)
  - **When** ยิงคำถามทั่วไปซ้ำใน 24 ชม. โดยไม่มี `conversation_id`
  - **Then** ระบบตอบกลับจาก `legal_cache` ภายในเวลา < 5 มิลลิวินาที (X-Cache-Status: HIT)
  - **When** ยิงคำขอดาวน์โหลดไฟล์ `GET /api/v1/files/case.md` พร้อม Bearer Token
  - **Then** ได้รับไฟล์ `.md` กลับมาอย่างถูกต้อง โดยป้องกัน Directory Traversal และ ADS 100%
- **ขั้นตอนการทำ:**
  1. สร้างไฟล์ `backend/auth_db.py`, `backend/templates/admin.html` และ `backend/main.py`
  2. ติดตั้ง Dependencies: `uv venv && uv pip install -r requirements.txt` (หรือ `pip install -r requirements.txt`)
  3. สั่งรันเซิร์ฟเวอร์: `uv run uvicorn main:app --port 8000`
  4. เข้าหน้าเบราว์เซอร์ `http://127.0.0.1:8000/admin` เพื่อทดสอบสร้างกุญแจแรก
  5. ทดสอบยิงคำขอด้วย `curl` ตรวจสอบทั้ง Event SSE ปกติ และการดักจับแท็ก `<!-- ARTIFACT: output/<filename>.md -->` สู่ `event: file`

### เฟสที่ 3: กำหนดค่าเครือข่าย Tailscale HTTPS บน Home Server (Day 2)
- **เป้าหมาย:** ผูก Local Port 8000 ให้กลายเป็น HTTPS ที่ปลอดภัยภายในวง Tailnet พร้อมรับประกันการเชื่อมต่อแบบ Direct STUN (ไม่ผ่าน DERP Relay)
- **เกณฑ์การยอมรับ (Acceptance Criteria - Gherkin):**
  - **Given** เครื่องโฮสต์เชื่อมต่อใน Tailnet สำเร็จ
  - **When** รันคำสั่ง `tailscale serve --bg https / http://127.0.0.1:8000`
  - **Then** สามารถเข้าถึง `https://<node-name>.tailnet.ts.net/api/v1/health` ด้วยการเข้ารหัส TLS และค่า Latency เครือข่าย < 30ms (สถานะ `direct`)
- **ขั้นตอนการทำ:**
  1. ตรวจสอบสถานะการเชื่อมต่อ: `tailscale status`
  2. เปิดใช้งาน Reverse Proxy HTTPS: `tailscale serve --bg https / http://127.0.0.1:8000`
  3. ตรวจสอบการเปิดพอร์ต UDP Firewall ฝั่ง Server เพื่อให้มือถือเชื่อมต่อแบบ Direct STUN

### เฟสที่ 4: พัฒนาแอปพลิเคชัน Android (Day 3-4)
- **เป้าหมาย:** พัฒนา Mobile Client ใน Kotlin ตามมาตรฐาน **Target SDK 36**, Release build เซ็นด้วย Debug key, ขนาด APK เล็กที่สุด (R8/Shrink), ระบบหลายห้องแชต (แชตต่อของเดิม / สร้างใหม่ / ลบแชต via SQLite WAL), ปุ่ม Stop Generating, บัฟเฟอร์หน่วงเวลาโทเคน 50ms, รองรับ Markwon GFM, Mermaid WebView, FileProvider native share, และส่งออกเอกสาร A4 Sarabun PDF *(หมายเหตุ: ผู้ใช้เปิดและบิลด์ผ่าน Android Studio ด้วยตนเอง; ห้าม Agent รัน Gradle)*
- **เกณฑ์การยอมรับ (Acceptance Criteria - Gherkin):**
  - **Given** ผู้ใช้เปิดแอป THLawDeka-mobile บน Android
  - **When** ผู้ใช้กรอก Tailscale URL และ Bearer Key ในหน้าจอการตั้งค่า
  - **Then** ข้อมูลถูกบันทึกลง `EncryptedSharedPreferences` ผ่าน Jetpack Security อย่างปลอดภัย
  - **When** ผู้ใช้กดส่งคำถามกฎหมาย
  - **Then** ข้อความสตรีมเข้ามาอย่างนุ่มลื่นด้วย `StreamTokenThrottler` (50ms) หน้าจอไม่กระตุก และปุ่มส่งเปลี่ยนเป็นปุ่ม "หยุดสร้างคำตอบ (Stop)"
  - **When** ผู้ใช้กดปุ่ม Stop
  - **Then** การสตรีมตัดขาดทันที ข้อความถูกบันทึกเป็น `status = 'interrupted'` และส่งสัญญาณไปฆ่า Subprocess บน Gateway ภายใน 0.1 วินาที
  - **When** ได้รับ SSE `event: file` หรือแตะลิงก์ดาวน์โหลด
  - **Then** ไฟล์ `.md` ถูกดาวน์โหลดลง Private Storage พร้อมปุ่มพรีวิว, ปุ่มแชร์ผ่าน Android Share Sheet, และปุ่ม Export A4 PDF
- **ขั้นตอนการทำ:**
  1. เพิ่มไลบรารีใน `build.gradle.kts` ตามสเปก พร้อมกำหนด R8 Proguard และ Resource Shrinking
  2. พัฒนาระบบจัดเก็บค่าคอนฟิก `AppConfigManager.kt` และหน้าจอทดสอบการเชื่อมต่อ `ConnectionSettingsManager.kt`
  3. พัฒนาระบบห้องแชต `ChatDatabaseHelper.kt` (เปิด WAL mode) และ `ChatSessionRepository.kt`
  4. พัฒนา `LegalChatRepository.kt` รองรับ OkHttp SSE, `cancelStream()`, และ `downloadArtifactFile()`
  5. พัฒนา `MarkdownViewManager.kt`, `MermaidRendererView.kt`, และ `PdfExportManager.kt`
  6. ทดสอบการทำงานร่วมกันบนเครื่องจริงผ่าน Android Studio

### เฟสที่ 5: การทดสอบรอบด้านและรับมือข้อผิดพลาด (End-to-End Verification) (Day 5)
- **เป้าหมาย:** รับประกันเสถียรภาพ ความมั่นคงปลอดภัยระดับ RCE Immunity และความทนทานต่อสภาพแวดล้อมเครือข่ายจริง
- **รายการตรวจสอบ (Test Checklist):**
  - [ ] **Network Switching Test:** ทดสอบถามคำถามขณะใช้ Wi-Fi แล้วตัดสัญญาณเข้า 4G/5G ยืนยันว่าบันทึก `status = 'interrupted'` และมีปุ่ม Retry ที่สืบทอด `conversation_id` ได้ต่อเนื่อง
  - [ ] **Timeout & Zombie Reaper Test:** ยิงคำถามแล้วตัดเน็ต/ยกเลิกทันที ยืนยันว่า Subprocess `agy` ถูกทำลายภายใน 0.1 วินาที ไม่ตกค้างเป็น Process ผี
  - [ ] **RCE & CLI Flag Injection Fuzz Test:** ส่ง `conversation_id = "--dangerously-allow-all"` และ `-v` ยืนยันว่า Gateway ตอบกลับด้วย `HTTP 400 Bad Request`
  - [ ] **Path Traversal & Windows ADS Test:** ยิง `GET /api/v1/files/..%2f..%2fwin.ini` และ `secret.md::$DATA` ยืนยันว่าถูกสกัดกั้น 100%
  - [ ] **Fast-Path Legal Cache Benchmark:** ส่งคำถามซ้ำเดิม ยืนยันว่าเวลาตอบกลับลดลงเหลือ < 5 มิลลิวินาที (X-Cache-Status: HIT)
  - [ ] **Markdown & Mermaid Test:** ตรวจสอบว่าตารางเปรียบเทียบข้อกฎหมายและผัง Mermaid เรนเดอร์ถูกต้องในตัวเครื่องโดยไม่ออกเน็ตภายนอก"""

# 2. Update Section 6: Add 6.1 header and enrich troubleshooting table
old_sec6 = """## 6. แนวทางการแก้ไขปัญหา (Troubleshooting & Runbook)

| อาการที่พบ | สาเหตุที่เป็นไปได้ | แนวทางแก้ไข |
| :--- | :--- | :--- |
| **Android แจ้งข้อผิดพลาด `CLEARTEXT_NOT_PERMITTED`** | แอปยิงเข้า `http://` ธรรมดา | ให้สลับไปใช้ `https://` ผ่าน **Tailscale Serve** หรืออนุญาตใน `network_security_config.xml` |
| **เซิร์ฟเวอร์นิ่งค้าง (Hang) ไม่ตอบกลับ** | ลืมใส่แฟล็ก `--dangerously-skip-permissions` ทำให้ `agy` รอคอนเฟิร์มในคอนโซล | เพิ่มแฟล็ก `--dangerously-skip-permissions` ในคำสั่ง Subprocess เสมอ |
| **Tailscale บนมือถือหลุดบ่อยเมื่อจอดับ** | ระบบประหยัดพลังงานของ Android ปิด Background Process | ตั้งค่าแอป Tailscale เป็น `Unrestricted` และเปิด `Always-on VPN` |
| **คำตอบไม่ออกมาทีละคำ แต่พรวดมาทั้งก้อน** | มี Reverse Proxy กักบัฟเฟอร์ไว้ | ตรวจสอบว่าได้ตั้งค่า Header `X-Accel-Buffering: no` และ `Cache-Control: no-cache` ใน FastAPI แล้ว |"""

new_sec6 = """## 6. แนวทางการแก้ไขปัญหา (Troubleshooting & Runbook)

### 6.1 ตารางวิเคราะห์ปัญหาที่พบบ่อย (Common Failure Modes & Runbook)

| อาการที่พบ | สาเหตุที่เป็นไปได้ | แนวทางแก้ไข |
| :--- | :--- | :--- |
| **Android แจ้งข้อผิดพลาด `CLEARTEXT_NOT_PERMITTED`** | แอปยิงเข้า `http://` ธรรมดา | ให้สลับไปใช้ `https://` ผ่าน **Tailscale Serve** หรืออนุญาตใน `network_security_config.xml` |
| **เซิร์ฟเวอร์นิ่งค้าง (Hang) ไม่ตอบกลับ** | ลืมใส่แฟล็ก `--dangerously-skip-permissions` ทำให้ `agy` รอคอนเฟิร์มในคอนโซล | เพิ่มแฟล็ก `--dangerously-skip-permissions` ในคำสั่ง Subprocess เสมอ |
| **Tailscale บนมือถือหลุดบ่อยเมื่อจอดับ** | ระบบประหยัดพลังงานของ Android ปิด Background Process | ตั้งค่าแอป Tailscale เป็น `Unrestricted` และเปิด `Always-on VPN` |
| **คำตอบไม่ออกมาทีละคำ แต่พรวดมาทั้งก้อน** | มี Reverse Proxy กักบัฟเฟอร์ไว้ | ตรวจสอบว่าได้ตั้งค่า Header `X-Accel-Buffering: no` และ `Cache-Control: no-cache` ใน FastAPI แล้ว |
| **หน้าจอมือถือกระตุก (UI Jank) ขณะสตรีม** | Markwon สั่งคำนวณ Spannable Layout ทุกก้อน Token | ตรวจสอบว่าได้เปิดใช้งาน `StreamTokenThrottler` (บัฟเฟอร์ 50ms) เพื่อลดภาระ Main Thread |
| **เกิดข้อผิดพลาด `database is locked` ใน SQLite** | มีการอ่านและเขียนพร้อมกันโดยใช้ Rollback Journal | ยืนยันว่าได้เปิดโหมด WAL: `PRAGMA journal_mode=WAL;` ฝั่ง Backend และ `db.enableWriteAheadLogging()` ฝั่ง Android |
| **CPU เครื่องโฮสต์สูงค้างจาก Process ผี (Zombie)** | ไคลเอนต์ตัดการเชื่อมต่อแต่ subprocess ไม่ถูกทำลาย | ยืนยันว่าบล็อก `finally` ใน `main.py` มีคำสั่ง `process.kill()` เพื่อทำลาย subprocess ทันที |
| **ดาวน์โหลดไฟล์ไม่ผ่าน (HTTP 400 Bad Request)** | ชื่อไฟล์มีอักขระพิเศษหรือนามสกุลไม่ใช่ `.md` | ตรวจสอบว่าไฟล์ผ่าน Regex `^[a-zA-Z0-9_\-\u0E00-\u0E7F]+\.md$` และอยู่ในโฟลเดอร์ `output/` จริง |"""

if old_sec5 in content:
    content = content.replace(old_sec5, new_sec5)
    print("Updated Section 5 with comprehensive Gherkin criteria & phase specs.")
else:
    print("Warning: old_sec5 not found!")

if old_sec6 in content:
    content = content.replace(old_sec6, new_sec6)
    print("Updated Section 6 with 6.1 header & extended runbook entries.")
else:
    print("Warning: old_sec6 not found!")

spec_path.write_text(content, encoding="utf-8")
print("Saved spec updates successfully!")
