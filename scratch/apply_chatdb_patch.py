import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update companion object in ChatDatabaseHelper
comp_target = """        const val TABLE_SESSIONS = "chat_sessions"
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

comp_target_clean = """        const val TABLE_SESSIONS = "chat_sessions"
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

comp_replacement = """        const val TABLE_SESSIONS = "chat_sessions"
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

assert comp_target_clean in content, "comp_target_clean not found"
content = content.replace(comp_target_clean, comp_replacement, 1)

# 2. Update onCreate in ChatDatabaseHelper
oncreate_target = """    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(\"\"\"
            CREATE TABLE $TABLE_SESSIONS (
                $COL_SESSION_ID TEXT PRIMARY KEY,
                $COL_SESSION_TITLE TEXT NOT NULL,
                $COL_SESSION_CREATED INTEGER NOT NULL,
                $COL_SESSION_UPDATED INTEGER NOT NULL,
                $COL_SESSION_LAST_MSG TEXT
            )
        \"\"\".trimIndent())

        db.execSQL(\"\"\"
            CREATE TABLE $TABLE_MESSAGES (
                $COL_MSG_ID TEXT PRIMARY KEY,
                $COL_MSG_SESSION_ID TEXT NOT NULL,
                $COL_MSG_ROLE TEXT NOT NULL,
                $COL_MSG_CONTENT TEXT NOT NULL,
                $COL_MSG_STATUS TEXT NOT NULL,
                $COL_MSG_TIMESTAMP INTEGER NOT NULL,
                FOREIGN KEY ($COL_MSG_SESSION_ID) REFERENCES $TABLE_SESSIONS($COL_SESSION_ID) ON DELETE CASCADE
            )
        \"\"\".trimIndent())"""

oncreate_replacement = """    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(\"\"\"
            CREATE TABLE $TABLE_SESSIONS (
                $COL_SESSION_ID TEXT PRIMARY KEY,
                $COL_SESSION_TITLE TEXT NOT NULL,
                $COL_SESSION_MODEL TEXT NOT NULL DEFAULT 'gemini-3.8-flash-high',
                $COL_SESSION_CREATED INTEGER NOT NULL,
                $COL_SESSION_UPDATED INTEGER NOT NULL,
                $COL_SESSION_LAST_MSG TEXT
            )
        \"\"\".trimIndent())

        db.execSQL(\"\"\"
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
        \"\"\".trimIndent())"""

assert oncreate_target in content, "oncreate_target not found"
content = content.replace(oncreate_target, oncreate_replacement, 1)

# 3. Update ChatModels.kt
models_target = """data class ChatSession(
    val id: String,
    val title: String,
    val createdAt: Long,
    val updatedAt: Long,
    val lastMessage: String? = null
)

data class ChatMessage(
    val id: String,
    val sessionId: String,
    val role: String, // "user" or "assistant"
    val content: String,
    val status: String, // "sending", "streaming", "completed", "error"
    val timestamp: Long
)"""

models_replacement = """data class ChatSession(
    val id: String,
    val title: String,
    val selectedModel: String = "gemini-3.8-flash-high",
    val createdAt: Long,
    val updatedAt: Long,
    val lastMessage: String? = null
)

data class ChatMessage(
    val id: String,
    val sessionId: String,
    val role: String, // "user" or "assistant"
    val content: String,
    val status: String, // "sending", "streaming", "completed", "error"
    val modelUsed: String = "gemini-3.8-flash-high",
    val timestamp: Long
)"""

assert models_target in content, "models_target not found"
content = content.replace(models_target, models_replacement, 1)

# 4. Update Phase-by-Phase plan
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
