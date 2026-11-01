# -*- coding: utf-8 -*-
report_path = r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md"

sec16 = """

---

## 16. การบูรณาการ 4 เสาหลักความมั่นคงและประสบการณ์ผู้ใช้ขั้นสูง (Zero-PII, Rate Limiting, Offline FTS5 & Context Budgeting)

ตามคำสั่งอนุมัติของ User (1-A, 2, 3, 4) ได้ทำการผสาน 4 มาตรการวิศวกรรมขั้นสูงเข้าสู่ [system_spec_and_implementation_plan.md](techdocs/system_spec_and_implementation_plan.md), [AGENTS.md](AGENTS.md), Skills และสคริปต์ทดสอบอัตโนมัติ [verify_all.py](scratch/verify_all.py) ดังนี้:

### 16.1 สรุปสาระสำคัญของ 4 เสาหลักที่ได้รับการนำไปปรับใช้จริง:

| เสาหลัก | รายละเอียดทางเทคนิคที่เพิ่มเข้าไป | ไฟล์ที่ได้รับการปรับปรุง |
| :--- | :--- | :--- |
| **1-A: Zero-PII Audit Logging** | บันทึกเฉพาะ Telemetry เชิงตัวเลข `{timestamp, endpoint, key_prefix, query_bytes, duration_ms, status}` โดย **ห้ามบันทึกเนื้อหาคำถามหรือคำตอบคดีความลง Disk Log เด็ดขาด** สอดคล้องกับ PDPA และมรรยาททนายความ | Section 3.8 & `backend/main.py` (`log_zero_pii_audit`) |
| **2-A: Per-Key Rate Limiting** | จำกัดความถี่ไม่เกิน 10 คำขอ/นาทีต่อกุญแจ API Key คำนวณแบบ $O(1)$ ใน RAM หากเกินจะตัดจบด้วย `HTTP 429 Too Many Requests` ทันที ป้องกันการยิงสแปมผูกขาด `Semaphore(3)` | Section 3.9 & `backend/main.py` (`check_rate_limit`) |
| **2-B: Automated SQLite Backup** | เพิ่มฟังก์ชัน `backup_db()` ผ่าน SQLite Online Backup API (`sqlite3_backup`) สำรองข้อมูล `keys.db` อัตโนมัติแบบ Zero-Downtime เก็บย้อนหลัง 7 ชุด | Section 3.10 & `backend/auth_db.py` (`backup_db`) |
| **3-A: Offline FTS5 Search** | เพิ่มตารางเสมือน `chat_messages_fts USING fts5` พร้อมทริกเกอร์อัตโนมัติใน SQLite และฟังก์ชัน `searchMessages(keyword)` ให้ทนายความค้นหาคำสำคัญในฎีกาเก่าได้แม้อยู่ในห้องพิจารณาคดีที่ไม่มีเน็ต | Section 3.4 & `data/local/ChatDatabaseHelper.kt` |
| **3-B: Partial Stream Recovery** | เมื่อสัญญาณเน็ต 4G/5G หลุดกลางคัน บันทึกข้อความส่วนที่สตรีมมาได้ลง SQLite ด้วยสถานะ `interrupted` และมีฟังก์ชัน `continueInterruptedStream` ส่งข้อความต่อจากเดิมทันทีในคลิกเดียว | Section 3.4 & `data/LegalChatRepository.kt` |
| **4-A: Long-Context Budgeting** | ตรวจวัดขนาดบริบทคดีความ หากเกินเกณฑ์ 64 KB (~16,000 Thai Tokens) Gateway จะส่ง SSE `event: advisory` แนะนำให้ผู้ใช้พิมพ์ `/compact` เพื่อย่อสรุปประเด็น หรือเริ่มห้องแชตใหม่ | Section 3.11 & `backend/main.py` |

### 16.2 ผลการตรวจสอบเชิงประจักษ์ (Step 8 Verification Sign-Off):
- เพิ่มการทดสอบ Step 8 ใน `scratch/verify_all.py` ครอบคลุมการยืนยัน JSON ปลอด PII, การทดสอบ Rate Limit บล็อกคำขอที่ 11 ด้วย HTTP 429, การรัน Snapshot สำรองข้อมูลจริง, การค้นหาคำสำคัญภาษาไทยใน FTS5, และการยิงสัญญาณเตือนเมื่อเกิน 64 KB
- ผลการทดสอบผ่านฉลุย **8/8 ขั้นตอน 0 Errors (Exit Code: 0)**
"""

with open(report_path, "a", encoding="utf-8") as f:
    f.write(sec16)

print("Section 16 appended to agent_enhancement_report.md successfully.")
