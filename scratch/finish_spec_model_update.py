import sys
import re
import py_compile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

db_cols_target = """        const val TABLE_SESSIONS = "chat_sessions"
        const val COL_SESSION_ID = "id"
        const val COL_SESSION_TITLE = "title"
        const val COL_SESSION_CREATED = "created_at"
        const val COL_SESSION_UPDATED = "updated_at"
        const val COL_SESSION_LAST_MSG = "last_message"

        const val TABLE_MESSAGES = "chat_messages"
        const val COL_MSG_ID = "id"
        const val COL_MSG_SESSION_ID = "session_id"
        const val COL_MSG_ROLE = "role"
        const val COL_MSG_CONTENT = "content"
        const val COL_MSG_STATUS = "status"
        const val COL_MSG_TIMESTAMP = "timestamp" """

db_cols_target_clean = """        const val TABLE_SESSIONS = "chat_sessions"
        const val COL_SESSION_ID = "id"
        const val COL_SESSION_TITLE = "title"
        const val COL_SESSION_CREATED = "created_at"
        const val COL_SESSION_UPDATED = "updated_at"
        const val COL_SESSION_LAST_MSG = "last_message"

        const val TABLE_MESSAGES = "chat_messages"
        const val COL_MSG_ID = "id"
        const val COL_MSG_SESSION_ID = "session_id"
        const val COL_MSG_ROLE = "role"
        const val COL_MSG_CONTENT = "content"
        const val COL_MSG_STATUS = "status"
        const val COL_MSG_TIMESTAMP = "timestamp\""""

db_cols_replacement = """        const val TABLE_SESSIONS = "chat_sessions"
        const val COL_SESSION_ID = "id"
        const val COL_SESSION_TITLE = "title"
        const val COL_SESSION_MODEL = "selected_model"
        const val COL_SESSION_CREATED = "created_at"
        const val COL_SESSION_UPDATED = "updated_at"
        const val COL_SESSION_LAST_MSG = "last_message"

        const val TABLE_MESSAGES = "chat_messages"
        const val COL_MSG_ID = "id"
        const val COL_MSG_SESSION_ID = "session_id"
        const val COL_MSG_ROLE = "role"
        const val COL_MSG_CONTENT = "content"
        const val COL_MSG_STATUS = "status"
        const val COL_MSG_MODEL = "model_used"
        const val COL_MSG_TIMESTAMP = "timestamp\""""

assert db_cols_target_clean in content, "db_cols_target_clean not found"
content = content.replace(db_cols_target_clean, db_cols_replacement, 1)

db_sql_target = """        val createSessions = \"\"\"
            CREATE TABLE $TABLE_SESSIONS (
                $COL_SESSION_ID TEXT PRIMARY KEY,
                $COL_SESSION_TITLE TEXT NOT NULL,
                $COL_SESSION_CREATED INTEGER NOT NULL,
                $COL_SESSION_UPDATED INTEGER NOT NULL,
                $COL_SESSION_LAST_MSG TEXT
            )
        \"\"\".trimIndent()

        val createMessages = \"\"\"
            CREATE TABLE $TABLE_MESSAGES (
                $COL_MSG_ID TEXT PRIMARY KEY,
                $COL_MSG_SESSION_ID TEXT NOT NULL,
                $COL_MSG_ROLE TEXT NOT NULL,
                $COL_MSG_CONTENT TEXT NOT NULL,
                $COL_MSG_STATUS TEXT NOT NULL,
                $COL_MSG_TIMESTAMP INTEGER NOT NULL,
                FOREIGN KEY ($COL_MSG_SESSION_ID) REFERENCES $TABLE_SESSIONS($COL_SESSION_ID) ON DELETE CASCADE
            )
        \"\"\".trimIndent()"""

db_sql_replacement = """        val createSessions = \"\"\"
            CREATE TABLE $TABLE_SESSIONS (
                $COL_SESSION_ID TEXT PRIMARY KEY,
                $COL_SESSION_TITLE TEXT NOT NULL,
                $COL_SESSION_MODEL TEXT NOT NULL DEFAULT 'gemini-3.8-flash-high',
                $COL_SESSION_CREATED INTEGER NOT NULL,
                $COL_SESSION_UPDATED INTEGER NOT NULL,
                $COL_SESSION_LAST_MSG TEXT
            )
        \"\"\".trimIndent()

        val createMessages = \"\"\"
            CREATE TABLE $TABLE_MESSAGES (
                $COL_MSG_ID TEXT PRIMARY KEY,
                $COL_MSG_SESSION_ID TEXT NOT NULL,
                $COL_MSG_ROLE TEXT NOT NULL,
                $COL_MSG_CONTENT TEXT NOT NULL,
                $COL_MSG_STATUS TEXT NOT NULL,
                $COL_MSG_MODEL TEXT NOT NULL DEFAULT 'gemini-3.8-flash-high',
                $COL_MSG_TIMESTAMP INTEGER NOT NULL,
                FOREIGN KEY ($COL_MSG_SESSION_ID) REFERENCES $TABLE_SESSIONS($COL_SESSION_ID) ON DELETE CASCADE
            )
        \"\"\".trimIndent()"""

assert db_sql_target in content, "db_sql_target not found"
content = content.replace(db_sql_target, db_sql_replacement, 1)

insert_msg_target = """        val values = ContentValues().apply {
            put(COL_MSG_ID, msg.id)
            put(COL_MSG_SESSION_ID, msg.sessionId)
            put(COL_MSG_ROLE, msg.role)
            put(COL_MSG_CONTENT, msg.content)
            put(COL_MSG_STATUS, msg.status)
            put(COL_MSG_TIMESTAMP, msg.timestamp)
        }"""

insert_msg_replacement = """        val values = ContentValues().apply {
            put(COL_MSG_ID, msg.id)
            put(COL_MSG_SESSION_ID, msg.sessionId)
            put(COL_MSG_ROLE, msg.role)
            put(COL_MSG_CONTENT, msg.content)
            put(COL_MSG_STATUS, msg.status)
            put(COL_MSG_MODEL, msg.modelUsed)
            put(COL_MSG_TIMESTAMP, msg.timestamp)
        }"""

assert insert_msg_target in content, "insert_msg_target not found"
content = content.replace(insert_msg_target, insert_msg_replacement, 1)
print("✓ Updated ChatDatabaseHelper.kt with selected_model and model_used columns")

# Phase 2 & Phase 4 plan
phase2_target = """- **งานที่ต้องส่งมอบ:**
  - `backend/main.py`
  - `backend/auth_db.py`
  - `backend/templates/admin.html`
  - Unit tests: ทดสอบการออกกุญแจ, สั่ง Revoke, ทดสอบ Rate Limiting (10 req/min), ทดสอบ Zero-PII Logger, ทดสอบ Online Backup, ทดสอบ Pre-Filter สกัด Prompt Injection, และทดสอบการส่งสตรีมแบบบีบอัด Gzip"""

phase2_replacement = """- **งานที่ต้องส่งมอบ:**
  - `backend/main.py` (พร้อม Endpoint `/api/v1/models`, Whitelist Validation, และพารามิเตอร์ CLI `--model`)
  - `backend/auth_db.py`
  - `backend/templates/admin.html`
  - Unit tests: ทดสอบการออกกุญแจ, สั่ง Revoke, ทดสอบ Rate Limiting (10 req/min), ทดสอบ Zero-PII Logger, ทดสอบ Online Backup, ทดสอบ Pre-Filter สกัด Prompt Injection, ทดสอบ Whitelist และ Flag Injection ป้องกัน Model ID, และทดสอบการส่งสตรีมแบบบีบอัด Gzip"""

if phase2_target in content:
    content = content.replace(phase2_target, phase2_replacement, 1)
    print("✓ Updated Phase 2 plan")

phase4_target = """- **งานที่ต้องส่งมอบ:**
  - `android/` source code ทั้งหมด
  - ทดสอบการเชื่อมต่อ SSE, Decompress Gzip อัตโนมัติ, ทดสอบส่งออกเอกสาร `.pdf` ทางการศาล, `.md`, `.txt`, ทดสอบแชร์ผ่าน `FileProvider`, สลับห้องแชต, ปิด Main Thread Jank ด้วย Token Batching Buffer, และค้นหาคดีออฟไลน์ผ่าน SQLite FTS5"""

phase4_replacement = """- **งานที่ต้องส่งมอบ:**
  - `android/` source code ทั้งหมด
  - ทดสอบการเชื่อมต่อ SSE, Decompress Gzip อัตโนมัติ, ทดสอบระบบเลือกโมเดล (Top App Bar Switcher & ModelSelectionBottomSheet), ทดสอบส่งออกเอกสาร `.pdf` ทางการศาล, `.md`, `.txt`, ทดสอบแชร์ผ่าน `FileProvider`, สลับห้องแชต, ปิด Main Thread Jank ด้วย Token Batching Buffer, และค้นหาคดีออฟไลน์ผ่าน SQLite FTS5"""

if phase4_target in content:
    content = content.replace(phase4_target, phase4_replacement, 1)
    print("✓ Updated Phase 4 plan")

with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("\n✓ Successfully finished updating techdocs/system_spec_and_implementation_plan.md!")
