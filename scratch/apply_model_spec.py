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
# 1. Add Section 3.4.10 right after 3.4.9
# -------------------------------------------------------------
sec349_target = """  - เมื่อผู้ใช้แตะ Retry: แอปจะส่งคำขอเดิมอีกครั้งโดยแนบ `conversation_id` เดิมไปยัง Gateway ทำให้ Core Agent สามารถวิเคราะห์ต่อจากบริบทเดิมได้โดยไม่ต้องพิมพ์ข้อเท็จจริงคดีซ้ำ

---

### 3.5 โมดูลระบบจัดการกุญแจและหน้าจอผู้ดูแลระบบ (Admin Key Management & Web UI Spec)"""

sec3410_addition = """  - เมื่อผู้ใช้แตะ Retry: แอปจะส่งคำขอเดิมอีกครั้งโดยแนบ `conversation_id` เดิมไปยัง Gateway ทำให้ Core Agent สามารถวิเคราะห์ต่อจากบริบทเดิมได้โดยไม่ต้องพิมพ์ข้อเท็จจริงคดีซ้ำ

### 3.4.10 ข้อกำหนดการเลือกและสลับโมเดล AI บน Android (Top App Bar Model Switcher & BottomSheet Spec)
เพื่อมอบประสบการณ์การใช้งาน (Mobile UX) ระดับพรีเมียมเทียบชั้นแอปพลิเคชันอย่าง ChatGPT และ Claude ฝั่ง Android Client จะมีระบบจัดการโมเดลดังนี้:
1. **Top App Bar Quick Model Switcher**:
   - บน Header หน้าจอแชตหลัก (ใต้ชื่อห้องแชต) จะมี Component ปุ่ม Chip แสดงชื่อโมเดลปัจจุบัน เช่น `[ ⚡ Gemini 3.8 Flash ▾ ]`
   - เมื่อผู้ใช้แตะ จะเปิด **`ModelSelectionBottomSheet`** ลอยขึ้นมาจากขอบจอด้านล่าง แสดงรายการโมเดลทั้งหมดพร้อม Badge จุดเด่นและคำอธิบายสั้น ๆ
   - เมื่อแตะเลือกโมเดลใหม่ ตัวแอปจะอัปเดต State และใช้โมเดลนั้นสำหรับคำถามถัดไปทันที
2. **Dynamic Model Discovery & Offline Fallback**:
   - เมื่อเปิดแอปและเชื่อมต่อ Gateway สำเร็จ แอปจะเรียก `GET /api/v1/models` เพื่อดึงรายชื่อโมเดลล่าสุดมาแคชไว้ในเครื่อง
   - หากอยู่ในสถานะออฟไลน์ แอปจะมีชุด Fallback Models ฝังในโค้ด เพื่อให้ผู้ใช้ยังคงเปิดดูและเลือกโมเดลเตรียมไว้ได้
3. **การบันทึกประวัติโมเดลในฐานข้อมูล SQLite ในเครื่อง (`ChatDatabaseHelper.kt`)**:
   - ตาราง `chat_sessions` เพิ่มคอลัมน์ `selected_model TEXT DEFAULT 'gemini-3.8-flash-high'` เพื่อจำว่าห้องแชตนี้ใช้โมเดลใด
   - ตาราง `chat_messages` เพิ่มคอลัมน์ `model_used TEXT` เพื่อให้ในแต่ละบอลลูนคำตอบ สามารถแสดงป้ายกำกับขนาดเล็ก (Badge) เช่น *"ตอบโดย Claude Sonnet 4.6"* ช่วยให้ทนายความสามารถตรวจสอบย้อนหลังได้ว่าข้อกฎหมายนี้วิเคราะห์โดย AI ตัวใด

---

### 3.5 โมดูลระบบจัดการกุญแจและหน้าจอผู้ดูแลระบบ (Admin Key Management & Web UI Spec)"""

assert sec349_target in content, "sec349_target not found"
content = content.replace(sec349_target, sec3410_addition, 1)
print("✓ Added Section 3.4.10")

# -------------------------------------------------------------
# 2. Add Section 3.8 right after Section 3.7.5
# -------------------------------------------------------------
sec375_target = """  - **ผลลัพธ์:** ประหยัดหน่วยความจำ RAM บนอุปกรณ์มือถือไป 50–80 MB ในห้องสนทนาทั่วไปที่ไม่มีแผนผังกระบวนการศาล

---

## 4. แหล่งโค้ดต้นแบบสำหรับการนำไปสร้างจริง (Reference Implementation Code)"""

sec38_addition = """  - **ผลลัพธ์:** ประหยัดหน่วยความจำ RAM บนอุปกรณ์มือถือไป 50–80 MB ในห้องสนทนาทั่วไปที่ไม่มีแผนผังกระบวนการศาล

---

### 3.8 ข้อกำหนดระบบเลือกโมเดลปัญญาประดิษฐ์ (Multi-Model Selection Architecture & Whitelist Spec)

ระบบ THLawDeka-mobile รองรับการเลือกและสลับโมเดล AI ในระดับเซสชันหรือคำขอ เพื่อให้ทนายความและผู้ใช้งานสามารถเลือกขุมพลังที่เหมาะสมกับลักษณะคดีความ (เช่น งานค้นหาฎีกาทั่วไปเน้นความเร็ว หรือ คดีซับซ้อนเน้นการคิดวิเคราะห์เชิงลึก) โดยมีสถาปัตยกรรมกำกับดังนี้:

#### 3.8.1 รายการโมเดลที่ผ่านการรับรอง (Supported Models Whitelist)
เกตเวย์จะควบคุมโมเดลผ่าน Whitelist ที่ตรวจสอบความถูกต้อง 100% ป้องกันการส่ง Flag หรือคำสั่งแปลกปลอมเข้า CLI:

| Model ID | ชื่อทางการ (Display Name) | ประเภท (Category) | ป้ายกำกับ (Badge) | คำอธิบายคุณสมบัติ (Capabilities) |
| :--- | :--- | :--- | :--- | :--- |
| **`gemini-3.8-flash-high`** | Gemini 3.8 Flash (High) | Fast | แนะนำ / เร็วสุด | ค่าเริ่มต้น (Default) ความเร็วสูง ความแม่นยำทางกฎหมายยอดเยี่ยม เหมาะสำหรับการค้นหาฎีกาเทียบเคียงทั่วไป |
| **`gemini-3.8-flash-medium`** | Gemini 3.8 Flash (Medium) | Fast | สมดุล | ประมวลผลรวดเร็ว สมดุลระหว่างทรัพยากรและคุณภาพ เหมาะกับคดีแพ่ง-อาญาทั่วไป |
| **`gemini-3.8-flash-low`** | Gemini 3.8 Flash (Low) | Eco | ประหยัดโควตา | ประหยัดทรัพยากรและโควตาสูงสุด เหมาะกับคำถามสั้นหรือตรวจเลขมาตรา |
| **`claude-sonnet-4-6`** | Claude Sonnet 4.6 (Thinking) | Thinking | วิเคราะห์ลึก | มีกระบวนการคิดวิเคราะห์ (Reasoning Process) เชิงลึก เหมาะกับการวางรูปคดีความซับซ้อนและการร่างข้อต่อสู้ |
| **`claude-opus-4-6-thinking`** | Claude Opus 4.6 (Thinking) | Thinking | ปัญญาสูงสุด | โมเดลปัญญาสูงสุดสำหรับการตีความข้อกฎหมายระดับสูง คดีรัฐธรรมนูญ และข้อพิพาททางธุรกิจมูลค่าสูง |
| **`gpt-oss-120b-medium`** | GPT-OSS 120B (Medium) | OpenSource | Open Weights | โมเดลแบบเปิดประสิทธิภาพสูง สำหรับการค้นคว้ามุมมองเปรียบเทียบและการประมวลผลอิสระ |

#### 3.8.2 มาตรการป้องกัน CLI Flag Injection สำหรับ Model ID
เพื่อป้องกันผู้ไม่ประสงค์ดีส่งค่าพารามิเตอร์แปลกปลอมเข้าคำสั่ง `agy --model <model>` ผ่านทาง Gateway:
1. **Regex Validation**: ต้องตรงตามนิพจน์ปกติ `^[a-zA-Z0-9][a-zA-Z0-9._\\-]{0,63}$` ห้ามมีช่องว่าง, อักขระพิเศษ, หรือเครื่องหมายขีดหน้าคู่ (`--`) เด็ดขาด
2. **Whitelist Membership**: ค่า Model ID ที่ส่งเข้ามาต้องอยู่ในชุด `VALID_MODELS` เท่านั้น หากไม่ระบุหรือส่งค่าว่าง ระบบจะกำหนดให้เป็น `gemini-3.8-flash-high` เสมอ
3. **Safe Subprocess Argument Array**: ส่งผ่านรายการอาร์กิวเมนต์แบบ `shell=False` โดยเพิ่ม `cmd.extend(["--model", req.model])` อย่างเคร่งครัด

---

## 4. แหล่งโค้ดต้นแบบสำหรับการนำไปสร้างจริง (Reference Implementation Code)"""

assert sec375_target in content, "sec375_target not found"
content = content.replace(sec375_target, sec38_addition, 1)
print("✓ Added Section 3.8")

# -------------------------------------------------------------
# 3. Update Section 4.1 backend/main.py
# -------------------------------------------------------------
chat_request_target = """class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=32768, description="ข้อเท็จจริงคดี ไม่เกิน 32KB")
    conversation_id: str | None = Field(None, max_length=128)

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        # 1. สกัดกั้น Null bytes ที่อาจทำให้ OS Subprocess เกิดพฤติกรรมไม่พึงประสงค์
        if "\\x00" in v:
            raise ValueError("ไม่อนุญาตให้อักขระ Null Byte ในข้อความ")
        # 2. เกราะชั้นที่ 1: สกัดกั้น Prompt Injection และคำสั่งดัดแปลง Core Agent Harness ทันที
        if contains_system_attack(v):
            raise ValueError("คำขอถูกปฏิเสธเนื่องจากมีรูปแบบคำสั่งที่อาจกระทบต่อความมั่นคงปลอดภัยของระบบ")
        return v.strip()"""

chat_request_replacement = """VALID_MODELS: set[str] = {
    "gemini-3.8-flash-high",
    "gemini-3.8-flash-medium",
    "gemini-3.8-flash-low",
    "claude-sonnet-4-6",
    "claude-opus-4-6-thinking",
    "gpt-oss-120b-medium"
}

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=32768, description="ข้อเท็จจริงคดี ไม่เกิน 32KB")
    conversation_id: str | None = Field(None, max_length=128)
    model: str | None = Field(default="gemini-3.8-flash-high", max_length=64, description="โมเดลปัญญาประดิษฐ์ที่เลือกใช้")

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        # 1. สกัดกั้น Null bytes ที่อาจทำให้ OS Subprocess เกิดพฤติกรรมไม่พึงประสงค์
        if "\\x00" in v:
            raise ValueError("ไม่อนุญาตให้อักขระ Null Byte ในข้อความ")
        # 2. เกราะชั้นที่ 1: สกัดกั้น Prompt Injection และคำสั่งดัดแปลง Core Agent Harness ทันที
        if contains_system_attack(v):
            raise ValueError("คำขอถูกปฏิเสธเนื่องจากมีรูปแบบคำสั่งที่อาจกระทบต่อความมั่นคงปลอดภัยของระบบ")
        return v.strip()

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str | None) -> str:
        if not v:
            return "gemini-3.8-flash-high"
        # 1. ป้องกัน CLI Flag Injection ด้วย Regex
        if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9._\\-]{0,63}$", v):
            raise ValueError("รูปแบบ Model ID ไม่ถูกต้อง")
        # 2. ตรวจสอบกับ Whitelist โมเดลที่รองรับ
        if v not in VALID_MODELS:
            raise ValueError(f"โมเดล {v} ไม่รองรับในระบบ")
        return v"""

assert chat_request_target in content, "chat_request_target not found"
content = content.replace(chat_request_target, chat_request_replacement, 1)
print("✓ Updated ChatRequest with model field and whitelist validation")

# Add endpoint /api/v1/models right after health check
health_target = """@app.get("/api/v1/health")
async def health_check_endpoint(authorization: str = Header(None)):
    \"\"\"ใช้สำหรับให้ Android Client ทดสอบการเชื่อมต่อและตรวจสอบความถูกต้องของ Auth Key\"\"\"
    await verify_auth(authorization)
    return {
        "status": "healthy",
        "service": "THLawDeka-mobile Gateway",
        "message": "พร้อมให้บริการวิเคราะห์คดีความ (Server-Side Zero-Disk-Write Policy)"
    }"""

health_and_models_replacement = """@app.get("/api/v1/health")
async def health_check_endpoint(authorization: str = Header(None)):
    \"\"\"ใช้สำหรับให้ Android Client ทดสอบการเชื่อมต่อและตรวจสอบความถูกต้องของ Auth Key\"\"\"
    await verify_auth(authorization)
    return {
        "status": "healthy",
        "service": "THLawDeka-mobile Gateway",
        "message": "พร้อมให้บริการวิเคราะห์คดีความ (Server-Side Zero-Disk-Write Policy)"
    }

@app.get("/api/v1/models")
async def list_available_models(authorization: str = Header(None)):
    \"\"\"ดึงรายชื่อโมเดลปัญญาประดิษฐ์ที่รองรับในระบบ พร้อมจุดเด่นและคำอธิบายสำหรับแสดงผลบน Android\"\"\"
    await verify_auth(authorization)
    return {
        "status": "success",
        "default": "gemini-3.8-flash-high",
        "models": [
            {
                "id": "gemini-3.8-flash-high",
                "name": "Gemini 3.8 Flash (High)",
                "category": "Fast",
                "badge": "แนะนำ / เร็วสุด",
                "description": "ตอบรวดเร็ว แม่นยำสูง เหมาะสำหรับการค้นหาฎีกาเทียบเคียงและคำปรึกษาทั่วไป"
            },
            {
                "id": "claude-sonnet-4-6",
                "name": "Claude Sonnet 4.6 (Thinking)",
                "category": "Thinking",
                "badge": "วิเคราะห์ลึก",
                "description": "เน้นการคิดวิเคราะห์ ใช้เหตุผลซับซ้อน เหมาะกับการวางรูปคดีความและข้อต่อสู้"
            },
            {
                "id": "claude-opus-4-6-thinking",
                "name": "Claude Opus 4.6 (Thinking)",
                "category": "Thinking",
                "badge": "ปัญญาสูงสุด",
                "description": "โมเดลความฉลาดสูงสุดสำหรับการตีความข้อกฎหมายยากและคดีรัฐธรรมนูญ"
            },
            {
                "id": "gemini-3.8-flash-medium",
                "name": "Gemini 3.8 Flash (Medium)",
                "category": "Fast",
                "badge": "สมดุล",
                "description": "สมดุลระหว่างความเร็วและทรัพยากร สำหรับคดีความทั่วไป"
            },
            {
                "id": "gemini-3.8-flash-low",
                "name": "Gemini 3.8 Flash (Low)",
                "category": "Eco",
                "badge": "ประหยัดโควตา",
                "description": "ประหยัดพลังงานและโควตาสูงสุด เหมาะกับคำถามสั้นหรือตรวจเลขมาตรา"
            },
            {
                "id": "gpt-oss-120b-medium",
                "name": "GPT-OSS 120B (Medium)",
                "category": "OpenSource",
                "badge": "Open Weights",
                "description": "โมเดลโอเพ่นซอร์สประสิทธิภาพสูง สำหรับการค้นคว้ามุมมองเปรียบเทียบ"
            }
        ]
    }"""

assert health_target in content, "health_target not found"
content = content.replace(health_target, health_and_models_replacement, 1)
print("✓ Added /api/v1/models endpoint")

# Update cmd in chat_stream_endpoint
cmd_target = """                    cmd = [
                        "agy",
                        "--sandbox",                      # กักบริเวณห้ามแตะไฟล์นอก Workspace / ห้ามคำสั่ง OS อันตราย
                        "--dangerously-skip-permissions",  # อนุมัติรัน Legal MCPs แบบอัตโนมัติ
                        "--input-format", "text",
                        "--output-format", "stream-json",
                        "--print-timeout", "60s",         # Watchdog timeout ภายในตัว agy
                        "-p", "-"                         # บังคับรับข้อความจาก stdin เท่านั้น (ไม่มีข้อมูลคดีหลุดใน OS logs)
                    ]
                    if req.conversation_id:
                        cmd.extend(["--conversation", req.conversation_id])"""

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
                    if req.conversation_id:
                        cmd.extend(["--conversation", req.conversation_id])"""

assert cmd_target in content, "cmd_target not found"
content = content.replace(cmd_target, cmd_replacement, 1)
print("✓ Updated cmd to extend --model req.model")

# -------------------------------------------------------------
# 4. Update Section 4.2 LegalChatRepository.kt
# -------------------------------------------------------------
kt_target = """    /**
     * สตรีมการวิเคราะห์ข้อกฎหมายจาก FastAPI Gateway
     */
    fun streamChat(query: String, conversationId: String? = null): Flow<StreamEvent> = callbackFlow {"""

kt_replacement = """    data class AiModelInfo(
        val id: String,
        val name: String,
        val category: String,
        val badge: String,
        val description: String
    )

    data class ModelsResponse(
        val status: String,
        val default: String,
        val models: List<AiModelInfo>
    )

    /**
     * ดึงรายการโมเดล AI ที่พร้อมใช้งานจาก Gateway
     */
    suspend fun getAvailableModels(): Result<List<AiModelInfo>> = withContext(Dispatchers.IO) {
        val serverUrl = appConfig.getServerUrl().trimEnd('/')
        val token = appConfig.getAuthToken()
        val request = Request.Builder()
            .url("$serverUrl/api/v1/models")
            .header("Authorization", "Bearer $token")
            .get()
            .build()
        try {
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) return@withContext Result.failure(IOException("HTTP ${response.code}"))
                val body = response.body?.string() ?: return@withContext Result.failure(IOException("Empty body"))
                val parsed = org.json.JSONObject(body)
                val arr = parsed.getJSONArray("models")
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
                Result.success(list)
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * สตรีมการวิเคราะห์ข้อกฎหมายจาก FastAPI Gateway พร้อมระบุโมเดลที่เลือก
     */
    fun streamChat(query: String, conversationId: String? = null, model: String = "gemini-3.8-flash-high"): Flow<StreamEvent> = callbackFlow {"""

assert kt_target in content, "kt_target not found"
content = content.replace(kt_target, kt_replacement, 1)

kt_json_target = """        val jsonPayload = org.json.JSONObject().apply {
            put("query", query)
            if (conversationId != null) {
                put("conversation_id", conversationId)
            }
        }.toString()"""

kt_json_replacement = """        val jsonPayload = org.json.JSONObject().apply {
            put("query", query)
            put("model", model)
            if (conversationId != null) {
                put("conversation_id", conversationId)
            }
        }.toString()"""

assert kt_json_target in content, "kt_json_target not found"
content = content.replace(kt_json_target, kt_json_replacement, 1)
print("✓ Updated LegalChatRepository.kt with models API & model param")

# -------------------------------------------------------------
# 5. Update Section 4.10 ChatDatabaseHelper.kt schema
# -------------------------------------------------------------
schema_target = """        val createSessionsTable = \"\"\"
            CREATE TABLE chat_sessions (
                session_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            );
        \"\"\".trimIndent()

        val createMessagesTable = \"\"\"
            CREATE TABLE chat_messages (
                message_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                content TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                FOREIGN KEY(session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
            );
        \"\"\".trimIndent()"""

schema_replacement = """        val createSessionsTable = \"\"\"
            CREATE TABLE chat_sessions (
                session_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                selected_model TEXT NOT NULL DEFAULT 'gemini-3.8-flash-high',
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            );
        \"\"\".trimIndent()

        val createMessagesTable = \"\"\"
            CREATE TABLE chat_messages (
                message_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                sender TEXT NOT NULL,
                content TEXT NOT NULL,
                status TEXT NOT NULL,
                model_used TEXT NOT NULL DEFAULT 'gemini-3.8-flash-high',
                timestamp INTEGER NOT NULL,
                FOREIGN KEY(session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
            );
        \"\"\".trimIndent()"""

assert schema_target in content, "schema_target not found"
content = content.replace(schema_target, schema_replacement, 1)
print("✓ Updated ChatDatabaseHelper.kt with selected_model and model_used columns")

# -------------------------------------------------------------
# 6. Update Section 5 Phase-by-Phase plan
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

assert phase2_target in content, "phase2_target not found"
content = content.replace(phase2_target, phase2_replacement, 1)

phase4_target = """- **งานที่ต้องส่งมอบ:**
  - `android/` source code ทั้งหมด
  - ทดสอบการเชื่อมต่อ SSE, Decompress Gzip อัตโนมัติ, ทดสอบส่งออกเอกสาร `.pdf` ทางการศาล, `.md`, `.txt`, ทดสอบแชร์ผ่าน `FileProvider`, สลับห้องแชต, ปิด Main Thread Jank ด้วย Token Batching Buffer, และค้นหาคดีออฟไลน์ผ่าน SQLite FTS5"""

phase4_replacement = """- **งานที่ต้องส่งมอบ:**
  - `android/` source code ทั้งหมด
  - ทดสอบการเชื่อมต่อ SSE, Decompress Gzip อัตโนมัติ, ทดสอบระบบเลือกโมเดล (Top App Bar Switcher & ModelSelectionBottomSheet), ทดสอบส่งออกเอกสาร `.pdf` ทางการศาล, `.md`, `.txt`, ทดสอบแชร์ผ่าน `FileProvider`, สลับห้องแชต, ปิด Main Thread Jank ด้วย Token Batching Buffer, และค้นหาคดีออฟไลน์ผ่าน SQLite FTS5"""

assert phase4_target in content, "phase4_target not found"
content = content.replace(phase4_target, phase4_replacement, 1)
print("✓ Updated Section 5 Phase 2 and Phase 4 plans")

# Write updated spec
with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("\n✓ Successfully updated techdocs/system_spec_and_implementation_plan.md!")
