import sys
import re
import py_compile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

# -------------------------------------------------------------
# 1. Update cmd in chat_stream_endpoint in Section 4.1
# -------------------------------------------------------------
cmd_target = """                    cmd = [
                        "agy",
                        "--sandbox",                      # กักบริเวณห้ามแตะไฟล์นอก Workspace / ห้ามคำสั่ง OS อันตราย
                        "--dangerously-skip-permissions",  # อนุมัติรัน Legal MCPs แบบอัตโนมัติ
                        "--input-format", "text",
                        "--output-format", "stream-json",
                        "--print-timeout", "60s",         # Watchdog timeout ภายในตัว agy
                        "-p", "-"                         # บังคับรับข้อความจาก stdin เท่านั้น (ไม่มีข้อมูลคดีหลุดใน OS logs)
                    ]
                    
                    if req.conversation_id:"""

cmd_replacement = """                    cmd = [
                        "agy",
                        "--sandbox",                      # กักบริเวณห้ามแตะไฟล์นอก Workspace / ห้ามคำสั่ง OS อันตราย
                        "--dangerously-skip-permissions",  # อนุมัติรัน Legal MCPs แบบอัตโนมัติ
                        "--input-format", "text",
                        "--output-format", "stream-json",
                        "--print-timeout", "60s",         # Watchdog timeout ภายในตัว agy
                        "-p", "-"                         # บังคับรับข้อความจาก stdin เท่านั้น (ไม่มีข้อมูลคดีหลุดใน OS logs)
                    ]
                    
                    if req.model:
                        cmd.extend(["--model", req.model])
                    
                    if req.conversation_id:"""

assert cmd_target in content, "cmd_target not found"
content = content.replace(cmd_target, cmd_replacement, 1)
print("✓ Updated cmd array with --model flag")

# -------------------------------------------------------------
# 2. Update Section 4.2 LegalChatRepository.kt
# -------------------------------------------------------------
kt_target = """    /**
     * รับสตรีมคำปรึกษากฎหมายแบบ Gzip Compressed SSE
     * OkHttp จะทำ Transparent Gzip Decompression ให้อัตโนมัติเมื่อเซิร์ฟเวอร์ส่ง Content-Encoding: gzip
     */
    fun streamConsultation(
        serverUrl: String,
        apiKey: String,
        query: String,
        conversationId: String?,
        onStatus: (String) -> Unit,
        onToken: (String) -> Unit,
        onDone: () -> Unit,
        onError: (String) -> Unit
    ) {
        val payload = JSONObject().apply {
            put("query", query)
            if (!conversationId.isNullOrEmpty()) {
                put("conversation_id", conversationId)
            }
        }.toString()"""

kt_replacement = """    data class AiModelInfo(
        val id: String,
        val name: String,
        val category: String,
        val badge: String,
        val description: String
    )

    /**
     * ดึงรายการโมเดล AI ที่พร้อมใช้งานจาก Gateway (/api/v1/models)
     */
    fun fetchAvailableModels(
        serverUrl: String,
        apiKey: String,
        onSuccess: (List<AiModelInfo>) -> Unit,
        onError: (String) -> Unit
    ) {
        val url = if (serverUrl.endsWith("/api/v1/chat/stream")) {
            serverUrl.replace("/api/v1/chat/stream", "/api/v1/models")
        } else {
            "${serverUrl.trimEnd('/')}/api/v1/models"
        }
        val request = Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer $apiKey")
            .get()
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: java.io.IOException) {
                onError(e.localizedMessage ?: "Network failure")
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (!response.isSuccessful) {
                        onError("HTTP Error ${response.code}")
                        return
                    }
                    val body = response.body?.string() ?: ""
                    try {
                        val json = JSONObject(body)
                        val arr = json.getJSONArray("models")
                        val list = mutableListOf<AiModelInfo>()
                        for (i in 0 until arr.length()) {
                            val item = arr.getJSONObject(i)
                            list.add(
                                AiModelInfo(
                                    id = item.getString("id"),
                                    name = item.getString("name"),
                                    category = item.optString("category", "General"),
                                    badge = item.optString("badge", ""),
                                    description = item.optString("description", "")
                                )
                            )
                        }
                        onSuccess(list)
                    } catch (e: Exception) {
                        onError(e.localizedMessage ?: "JSON Parse error")
                    }
                }
            }
        })
    }

    /**
     * รับสตรีมคำปรึกษากฎหมายแบบ Gzip Compressed SSE พร้อมระบุโมเดลที่เลือก
     * OkHttp จะทำ Transparent Gzip Decompression ให้อัตโนมัติเมื่อเซิร์ฟเวอร์ส่ง Content-Encoding: gzip
     */
    fun streamConsultation(
        serverUrl: String,
        apiKey: String,
        query: String,
        conversationId: String?,
        model: String = "gemini-3.8-flash-high",
        onStatus: (String) -> Unit,
        onToken: (String) -> Unit,
        onDone: () -> Unit,
        onError: (String) -> Unit
    ) {
        val payload = JSONObject().apply {
            put("query", query)
            put("model", model)
            if (!conversationId.isNullOrEmpty()) {
                put("conversation_id", conversationId)
            }
        }.toString()"""

assert kt_target in content, "kt_target not found"
content = content.replace(kt_target, kt_replacement, 1)
print("✓ Updated LegalChatRepository.kt with fetchAvailableModels & model parameter")

# -------------------------------------------------------------
# 3. Update Section 4.10 ChatDatabaseHelper.kt & ChatModels.kt
# -------------------------------------------------------------
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
        const val COL_MSG_TIMESTAMP = "timestamp" """

assert db_cols_target in content, "db_cols_target not found"
content = content.replace(db_cols_target, db_cols_replacement, 1)

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

# -------------------------------------------------------------
# 4. Update Section 5 Phase-by-Phase plan
# -------------------------------------------------------------
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

# Save updated spec
with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("\n✓ Successfully updated techdocs/system_spec_and_implementation_plan.md!")
