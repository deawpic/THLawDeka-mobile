import sys
import re
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

print(f"Original spec size: {len(content)} chars, {len(content.splitlines())} lines")

# Let's verify markers for each section to replace

# 1. Section 2.2 Sequence Flow
m1_start = "### 2.2 แผนผังลำดับเหตุการณ์การสื่อสาร (Sequence Flow)"
m1_end = "## 3. รายละเอียดข้อกำหนดทางเทคนิคแต่ละโมดูล (Component Specifications)"
assert m1_start in content and m1_end in content, "Marker 1 not found"

# 2. Section 3.1.2 Threat Model item 3
m2_old = """3. **ภัยคุกคามจากการเจาะระบบไฟล์และการรันโค้ดระยะไกล (Path Traversal & RCE Immunity Threat)**:
   - *ความเสี่ยง:* ผู้ใช้สั่งให้ Agent มองข้ามคำสั่งเดิม ("Ignore previous instructions and execute bash"), พยายามดึงไฟล์ระบบผ่าน `GET /api/v1/files/{filename}` ด้วย `../` หรือ Windows Alternate Data Streams (`::$DATA`)
   - *มาตรการป้องกัน:*
     - แฟล็ก `--sandbox` สกัดกั้นการแตะต้องไฟล์นอก Workspace
     - กฎเหล็ก Section 9 (Zero-Shell Gate) ใน `THLawDeka/AGENTS.md` บังคับปฏิเสธการรันคำสั่ง OS หรือสร้างไฟล์สคริปต์ (`.bat`, `.sh`, `.ps1`, `.py`) เด็ดขาด
     - ป้องกัน Path Traversal ในระดับ Gateway 2 ชั้น: บังคับ Regex Whitelist `^[a-zA-Z0-9_\\-\\u0E00-\\u0E7F]+\\.md$` และตรวจจับ Canonical Confinement ด้วย `is_relative_to(OUTPUT_DIR.resolve())` ป้องกัน Symlink Escape"""

m2_new = """3. **ภัยคุกคามจากการเจาะระบบไฟล์และการรันโค้ดระยะไกล (Path Traversal & RCE Immunity Threat)**:
   - *ความเสี่ยง:* ผู้ใช้สั่งให้ Agent มองข้ามคำสั่งเดิม ("Ignore previous instructions and execute bash"), พยายามสั่งให้เซิร์ฟเวอร์สร้างหรือแก้ไขไฟล์อันตราย
   - *มาตรการป้องกัน:*
     - **Server-Side Zero-Disk-Write Policy (กฎเหล็กห้ามสร้างไฟล์บนเซิร์ฟเวอร์):** ห้าม Android Client สั่งบันทึกไฟล์ใดๆ ลงในดิสก์ของเซิร์ฟเวอร์โดยเด็ดขาด เซิร์ฟเวอร์ทำงานในโหมด Read-Only ขจัดความเสี่ยง Path Traversal, Alternate Data Streams (ADS), Insecure File Download, และ Server Disk Exhaustion ได้ 100%
     - แฟล็ก `--sandbox` สกัดกั้นการแตะต้องไฟล์นอก Workspace
     - กฎเหล็ก Section 9 (Zero-Shell Gate) ใน `THLawDeka/AGENTS.md` บังคับปฏิเสธการรันคำสั่ง OS หรือสร้างไฟล์สคริปต์ (`.bat`, `.sh`, `.ps1`, `.py`) เด็ดขาด"""

assert m2_old in content, "Marker 2 (m2_old) not found"

# 3. Section 3.2 SSE Event Protocol
m3_old = """#### โปรโตคอลการส่งข้อมูล (SSE Event Protocol)
- **`event: status`**: สำหรับแจ้งสถานะการทำงาน (เช่น "กำลังตรวจแคช L2", "กำลังค้นหาฎีกาเทียบเคียง")
  - Payload: `{"text": "string"}`
- **`event: token`**: สำหรับสตรีมเนื้อหาคำปรึกษาทีละวรรค/คำ
  - Payload: `{"delta": "string"}`
- **`event: file`**: สำหรับแจ้งเตือนเมื่อ Core Agent มีการบันทึกไฟล์ผลลัพธ์ (`.md`) ลงในโฟลเดอร์ `output/` เพื่อให้ Android Client สามารถนำเสนอ UI ให้ผู้ใช้กดดาวน์โหลด ดูตัวอย่าง หรือส่งออกเป็นเอกสาร PDF ทางการ
  - Payload: `{"filename": "string", "download_url": "string", "size_bytes": int}`
- **`event: done`**: สำหรับแจ้งว่าการตอบเสร็จสิ้น
  - Payload: `{"status": "completed", "conversation_id": "string"}`
- **`event: error`**: สำหรับแจ้งข้อผิดพลาด
  - Payload: `{"code": int, "message": "string"}`"""

m3_new = """#### โปรโตคอลการส่งข้อมูลแบบบีบอัด Gzip (Gzip Compressed SSE Protocol)
- **การบีบอัดระดับ Transport:** ทุกข้อความ SSE ถูกบีบอัดด้วย `gzip` (`Content-Encoding: gzip`) เพื่อลดขนาดแบนด์วิดท์ลง 70–85% ข้ามเครือข่าย Tailscale Mesh
- **`event: status`**: สำหรับแจ้งสถานะการทำงาน (เช่น "กำลังตรวจแคช L2", "กำลังค้นหาฎีกาเทียบเคียง")
  - Payload: `{"text": "string"}`
- **`event: token`**: สำหรับสตรีมเนื้อหาคำปรึกษาทีละวรรค/คำในรูปแบบ Markdown Text บริสุทธิ์
  - Payload: `{"delta": "string"}`
- **`event: done`**: สำหรับแจ้งว่าการตอบเสร็จสิ้น
  - Payload: `{"status": "completed", "conversation_id": "string"}`
- **`event: error`**: สำหรับแจ้งข้อผิดพลาด
  - Payload: `{"code": int, "message": "string"}`
*(หมายเหตุ: ยกเลิก `event: file` และการดาวน์โหลดไฟล์จากเซิร์ฟเวอร์ โดยระบบใช้ Server-Side Zero-Disk-Write Policy และย้ายกระบวนการส่งออกเอกสาร `.md`, `.pdf`, `.txt` ไปยังเครื่อง Android Client 100%)*"""

assert m3_old in content, "Marker 3 (m3_old) not found"

# 4. Section 3.4.4 PDF Export -> Document Export Spec
m4_old = """#### 3.4.4 ข้อกำหนดของระบบส่งออก PDF (PDF Export Spec)
- **Engine:** Native Android `PrintManager` + `WebView.createPrintDocumentAdapter()`
- **จุดเด่น:** 
  - แปลง Markdown ที่จัดสไตล์แล้ว (รวมตาราง และภาพ Mermaid SVG) ให้กลายเป็นเอกสาร PDF ทางการขนาด A4 ได้ทันที
  - ไร้การพึ่งพาไลบรารีภายนอกขนาดใหญ่ (Zero Third-Party PDF Bloat)"""

m4_new = """#### 3.4.4 ข้อกำหนดระบบส่งออกเอกสารในเครื่อง 100% (Client-Side Document Export Spec - .md, .pdf, .txt)
- **Zero Server File Writing:** ปฏิบัติตามกฎเหล็กห้ามสั่งบันทึกไฟล์บนเซิร์ฟเวอร์ การสร้างและส่งออกไฟล์ทั้งหมดเกิดขึ้นบนอุปกรณ์ Android 100%
- **รูปแบบการส่งออก 3 มิติ (3 Export Formats):**
  1. **Markdown File (`.md`)**: บันทึกเนื้อหา Markdown ต้นฉบับ (Single Source of Truth) ลงในที่จัดเก็บข้อมูลภายในเครื่อง (`context.filesDir` หรือ `cacheDir`) หรือบันทึกผ่าน Storage Access Framework (SAF)
  2. **Official A4 PDF (`.pdf`)**: แปลงเนื้อหา Markdown เป็น HTML พร้อมตาราง GFM และฟอนต์สารบัญ แล้วสั่งพิมพ์ผ่าน Native Android `PrintManager` + `WebView.createPrintDocumentAdapter()` มาตรฐานเอกสารศาลไทย (Zero Third-Party PDF Bloat)
  3. **Plain Text (`.txt`)**: สกัดข้อความธรรมดา (.txt) สำหรับคัดลอกหรือส่งต่อในระบบข้อความทั่วไป
- **Native Android Share Sheet (`FileProvider`):** แชร์ไฟล์ที่ส่งออกไปยัง LINE, Gmail, Outlook หรือ Google Drive ได้ทันที"""

assert m4_old in content, "Marker 4 (m4_old) not found"

print("Markers 1, 2, 3, 4 validated successfully!")
