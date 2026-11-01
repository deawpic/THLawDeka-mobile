import re
from pathlib import Path

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# 1. Update line 688 in Section 3.6.2 (Path Traversal Shield description)
old_traversal = "- **Path Traversal Shield:** ใช้ `os.path.basename(filename)` สกัดอักขระทางเดินไดเรกทอรี (เช่น `../`, `..\\`) ป้องกันการเจาะอ่านไฟล์ระบบนอกไดเรกทอรี `output/`"
new_traversal = "- **Path Traversal & ADS Shield:** ตรวจสอบชื่อไฟล์ด้วย Regex Whitelist `^[a-zA-Z0-9_\\-\\u0E00-\\u0E7F]+\\.md$` และตรวจสอบการกักขังไดเรกทอรีด้วย `file_path.is_relative_to(OUTPUT_DIR.resolve())` ป้องกันการเจาะอ่านไฟล์ระบบนอกไดเรกทอรี `output/` และ Alternate Data Streams"

if old_traversal in content:
    content = content.replace(old_traversal, new_traversal)
    print("Updated Section 3.6.2 Path Traversal description.")
else:
    print("Warning: old_traversal not found in spec!")

# 2. Add Section 3.7 before Section 4
sec37_text = """### 3.7 ข้อกำหนดการเพิ่มประสิทธิภาพและความเร็วขั้นสูง (Performance & Latency Optimization Spec)

เพื่อให้ระบบตอบสนองได้รวดเร็วระดับเสี้ยววินาที ขจัดปัญหาความล่าช้าจาก Cold Start ของกระบวนการ Subprocess และป้องกันอาการหน้าจอกระตุก (UI Jank) บนโทรศัพท์มือถือ ระบบจึงกำหนดมาตรการเพิ่มประสิทธิภาพ 5 ประการ:

#### 3.7.1 ระบบแคชคำถามกฎหมายที่พบบ่อย (FastAPI Legal Response Cache)
- **วัตถุประสงค์:** ลดระยะเวลาตอบสนองจาก 8–15 วินาที เหลือต่ำกว่า 5 มิลลิวินาที (เร็วขึ้นกว่า 1,600 เท่า) สำหรับข้อหารือกฎหมายพื้นฐานที่ผู้ใช้สอบถามบ่อยครั้ง
- **โครงสร้างตาราง `legal_cache` ใน `keys.db`:**
  - `query_hash TEXT PRIMARY KEY`: ผลการแฮช SHA-256 ของคำถามที่ผ่านการ Normalize (ตัดช่องว่าง, แปลงเป็นตัวพิมพ์เล็ก)
  - `query_text TEXT NOT NULL`: ข้อความคำถามต้นฉบับ
  - `cached_events TEXT NOT NULL`: ข้อมูล JSON Array ของ SSE Events ทั้งหมด (`status`, `token`, `file`, `done`)
  - `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`: เวลาที่เริ่มบันทึก
  - `expires_at TIMESTAMP NOT NULL`: เวลาหมดอายุ (TTL กำหนดไว้ 24–48 ชั่วโมง)
- **เงื่อนไขการทำงานและการ Bypass:**
  - หากคำขอมี `conversation_id` ส่งมาด้วย (หมายถึงกำลังสนทนาต่อเนื่องในคดีเฉพาะเรื่อง) -> **ข้ามแคช (Bypass Cache)** เพื่อให้ Core Agent ตอบตามข้อเท็จจริงของคดีนั้นเสมอ
  - หากเป็นคำถามเดี่ยว (ไม่มี `conversation_id`) และพบ Cache Hit ที่ยังไม่หมดอายุ -> Gateway จะจำลองการสตรีมชุดข้อความ SSE ออกไปทันทีด้วยอัตราหน่วงสั้น ๆ (5ms ต่อ Chunk) ทำให้ผู้ใช้ได้รับคำตอบทันทีโดยที่ UI บนมือถือยังคงแอนิเมชันการสตรีมที่นุ่มนวล

#### 3.7.2 การเปิดโหมด SQLite WAL & In-Memory Bearer Token Validation
- **SQLite Write-Ahead Logging (WAL Mode):**
  - ฝั่ง Backend: เรียกใช้ `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;` ใน `AuthDB`
  - ฝั่ง Android: เรียกใช้ `db.enableWriteAheadLogging()` ใน `ChatDatabaseHelper.kt`
  - **ผลลัพธ์:** ปลดล็อกให้การอ่านข้อมูล (Reads) สามารถทำพร้อมกับการเขียน (Writes) ได้ทันทีโดยไม่ติดล็อกไฟล์ (Non-blocking Concurrency) ขจัดปัญหาคอขวด Disk I/O เมื่อมีการส่งข้อความถี่
- **In-Memory Bearer Token Validation ($O(1)$ Lookup):**
  - ใน `backend/main.py` จัดเตรียมตัวแปร `ACTIVE_KEYS_CACHE: set[str]` ในหน่วยความจำ RAM
  - โหลด Active Keys ขึ้น RAM ตอนสตาร์ตเซิร์ฟเวอร์ และอัปเดตเมื่อมีการเพิ่ม/ระงับคีย์ผ่าน Admin UI
  - เมื่อมี HTTP Request เข้ามา สามารถตรวจสอบความถูกต้องของ Token ได้ทันทีในระดับนาโนวินาที ($O(1)$) โดยไม่ต้องเปิดอ่าน Disk ทุกคำขอ

#### 3.7.3 ระบบหน่วงเวลาและรวมกลุ่มโทเคนฝั่ง Android (Stream Token Batching Buffer - 50ms)
- **ปัญหาเดิม:** การเรียกใช้งาน Markwon เพื่อแปลงและวาด Spannable Layout บน `TextView` ทุกครั้งที่ได้รับ SSE `event: token` (10-20 ครั้งต่อวินาที) ทำให้ Main Thread ทำงานหนักเกินไป เกิดอาการกระตุก (Jank) และเปลืองแบตเตอรี่
- **กลไก Batching Buffer:**
  - สร้างตัวสะสมข้อความ (Throttler Buffer) ใน Coroutines Scope ฝั่ง Android
  - รวบรวมข้อความตัวอักษรที่สตรีมเข้ามา แล้วยิงสั่ง Render บน UI Thread ทุก ๆ **50 – 80 ms** หรือเมื่อพบอักขระขึ้นบรรทัดใหม่ (`\n`)
  - **ผลลัพธ์:** ลดภาระการคำนวณ Layout ของ UI Thread ลงกว่า 75% ทำให้หน้าจอแสดงผลได้ลื่นไหลเต็มที่ 60–120 fps

#### 3.7.4 ระบบบันทึกข้อความแบบ Batch Write ฝั่ง Android (Mobile Disk I/O Optimization)
- **ปัญหาเดิม:** การบันทึกข้อความลง SQLite ในเครื่องมือถือทุกคำหรือทุก Chunk ทำให้เกิด Disk Write I/O ถี่เกินไป (I/O Thrashing)
- **กลไก Batch Write:**
  - ระหว่างที่ข้อความกำลังสตรีม ให้เก็บเนื้อหาข้อความทั้งหมดไว้ใน StateFlow / LiveData ใน RAM ของ `LegalChatViewModel`
  - บันทึกลงตาราง `chat_messages` เฉพาะเมื่อ:
    1. ได้รับ SSE `event: done` (สตรีมคำตอบเสร็จสิ้นสมบูรณ์)
    2. ได้รับ SSE `event: error` หรือผู้ใช้กดปุ่ม Stop / เน็ตหลุด (`interrupted`)
    3. หรือบันทึกเป็นระยะ (Periodic Flush) ทุก 2-3 วินาทีหากเป็นคำตอบที่ยาวมาก
  - **ผลลัพธ์:** ลดภาระการเขียนหน่วยความจำแฟลชของโทรศัพท์มือถือลงกว่า 90%

#### 3.7.5 การปรับแต่ง Tailscale Direct Connection & WebView Lazy Loading
- **Tailscale Direct Peer-to-Peer (STUN / UDP Hole Punching):**
  - ตรวจสอบผ่านคำสั่ง `tailscale status` ว่าสถานะการเชื่อมต่อระหว่างมือถือกับ Server เป็นแบบ `direct` (ไม่วิ่งผ่าน `relay (DERP)`)
  - เปิดพอร์ต UDP 41641 (หรือค่าตามที่ Tailscale สุ่ม) ที่ Firewall ฝั่ง Server
  - **ผลลัพธ์:** ลด Latency เครือข่ายจาก ~120-150ms เหลือเพียง 10-30ms
- **Lazy Loading Mermaid WebView:**
  - `MermaidRendererView` จะไม่ถูก Initialize หรือผูกเข้ากับ View Hierarchy จนกว่าระบบจะตรวจพบแท็ก ````mermaid ในข้อความ Markdown
  - **ผลลัพธ์:** ประหยัดหน่วยความจำ RAM บนอุปกรณ์มือถือไป 50–80 MB ในห้องสนทนาทั่วไปที่ไม่มีแผนผังกระบวนการศาล

---

"""

target_sec4 = "## 4. แหล่งโค้ดต้นแบบสำหรับการนำไปสร้างจริง (Reference Implementation Code)"

if "### 3.7 ข้อกำหนดการเพิ่มประสิทธิภาพและความเร็วขั้นสูง" not in content:
    if target_sec4 in content:
        content = content.replace(target_sec4, sec37_text + target_sec4)
        print("Inserted Section 3.7 successfully!")
    else:
        print("Warning: target_sec4 not found in spec!")
else:
    print("Section 3.7 already present in spec.")

spec_path.write_text(content, encoding="utf-8")
print("Saved spec updates!")
