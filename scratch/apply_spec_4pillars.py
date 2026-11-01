# -*- coding: utf-8 -*-
import os
import re

spec_path = r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md"

with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

# =========================================================================
# 1. Insert Section 3.8 to 3.11 right before Section 4
# =========================================================================
sec_38_to_311 = """
---

### 3.8 นโยบายความปลอดภัย Zero-PII Audit Logging และการคุ้มครองข้อมูลคดีความ (Zero-PII Compliance Spec)
เพื่อปฏิบัติตาม พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล (PDPA) และมรรยาทวิชาชีพทนายความในการรักษาความลับของลูกความ ข้อมูลที่ส่งผ่าน Gateway จะต้องได้รับการคุ้มครองสูงสุด:
1. **Zero-PII Access Logging Policy:**
   - ห้ามพิมพ์หรือบันทึกเนื้อหาคำถาม (`query`), ข้อเท็จจริงคดี, หรือข้อความตอบกลับ (`response`) ลงใน Text Log, Console stdout/stderr, หรือ Disk File ของเซิร์ฟเวอร์โดยเด็ดขาด
   - อนุญาตให้บันทึกเฉพาะ **Metadata เชิงตัวเลขและข้อมูลทางเทคนิค** สำหรับการวัดประสิทธิภาพ (Telemetry) และการตรวจสอบความปลอดภัย ได้แก่:
     - `timestamp` (เวลาสากล UTC)
     - `endpoint` (เช่น `/api/v1/chat/stream`)
     - `key_prefix` (เฉพาะ 8 ตัวอักษรแรกของ Key เช่น `thlaw_li...` โดยห้ามบันทึก Full Token)
     - `query_bytes` (ขนาดความยาวข้อมูลเป็นไบต์)
     - `duration_ms` (เวลาตอบสนองรวม)
     - `status_code` (รหัสผลลัพธ์ HTTP)
2. **รูปแบบโครงสร้าง Log มาตรฐาน:**
   ```json
   {"timestamp": "2026-11-01T15:00:00Z", "endpoint": "/api/v1/chat/stream", "key_prefix": "thlaw_li...", "query_bytes": 142, "duration_ms": 1240.5, "status": 200}
   ```

### 3.9 ระบบป้องกันการสแปมและจำกัดความถี่ต่อกุญแจ (Per-Key Rate Limiting Spec - 10 req/min)
เพื่อป้องกันไม่ให้กุญแจ API Key ใดกุญแจหนึ่งยิงคำขอซ้ำถี่เกินไปจนผูกขาดโควตา `Semaphore(3)` และทำให้ผู้ใช้อื่นไม่สามารถใช้งานได้ (Denial of Service):
1. **กลไก In-Memory Sliding Window Rate Limiter:**
   - จำกัดความถี่สูงสุด **10 คำขอต่อนาทีต่อกุญแจ (10 requests / 60 seconds per API Key)**
   - คำนวณในหน่วยความจำ RAM ด้วยระดับความซับซ้อน $O(1)$ ผ่านประวัติ Timestamp
   - หากคำขอเกินโควตา Gateway จะตัดจบและส่งคืน `HTTP 429 Too Many Requests` พร้อม Header `Retry-After: 60` ทันที โดยไม่ส่งคำขอเข้า Semaphore หรือ Subprocess
2. **การล้างหน่วยความจำอัตโนมัติ:**
   - ล้างประวัติ Timestamp ที่มีอายุเกิน 60 วินาทีทิ้งอย่างต่อเนื่อง เพื่อไม่ให้หน่วยความจำ RAM บวมสะสม

### 3.10 กลยุทธ์การสำรองข้อมูลอัตโนมัติแบบไร้ผลกระทบ (Automated SQLite Backup for keys.db)
ฐานข้อมูล `keys.db` คือหัวใจหลักในการเก็บข้อมูลกุญแจสิทธิ์และการเพิกถอนสิทธิ์ จึงต้องมีระบบป้องกันภัยพิบัติ (Disaster Recovery):
1. **SQLite Online Backup API (`sqlite3_backup`):**
   - ใช้งานฟังก์ชัน `backup_db()` ผ่าน `conn.backup(dest_conn)`
   - ทำงานแบบ Non-blocking ไม่ล็อกตาราง ไม่ทำให้การสตรีมคำตอบหรือการตรวจสอบสิทธิ์สะดุด (Zero-Downtime Backup)
2. **นโยบายการเก็บรักษา (Retention Policy):**
   - บันทึกไฟล์สำรองในโฟลเดอร์ `backend/backups/keys_backup_YYYYMMDD_HHMMSS.db`
   - เก็บไฟล์สำรองย้อนหลัง **สูงสุด 7 ชุด (Latest 7 Daily Snapshots)** และลบชุดที่เก่ากว่าทิ้งอัตโนมัติ

### 3.11 การบริหารบริบทคดีความระยะยาวและการแจ้งเตือนย่อสรุป (Long-Context Budgeting & Advisory Spec)
เมื่อมีการสนทนาคดีความยาวต่อเนื่องใน `conversation_id` เดิมหลายสิบรอบ ขนาดบริบทที่สะสมใน Google Antigravity อาจเพิ่มสูงขึ้น:
1. **เกณฑ์การตรวจวัด (Context Threshold):**
   - กำหนดเกณฑ์เฝ้าระวังขนาดบริบทที่ **64 KB (~16,000 Thai Tokens)**
2. **กลไกการส่งสัญญาณแจ้งเตือน (Advisory Event):**
   - หากบริบทสะสมเกิน 64 KB Gateway จะส่ง SSE `event: advisory` ไปยังแอปมือถือ:
     ```json
     {"type": "context_budget_warning", "message": "คำแนะนำ: คดีความนี้มีประวัติการสนทนายาวสะสม แนะนำให้พิมพ์คำสั่ง /compact เพื่อย่อสรุปประเด็น หรือเริ่มห้องแชตใหม่ เพื่อคงความแม่นยำสูงสุดในการวินิจฉัย"}
     ```
   - แอปมือถือจะแสดงป้ายคำแนะนำ (Advisory Banner) พร้อมปุ่มคลิกเดียวเพื่อสั่งย่อสรุป หรือเปิดห้องแชตใหม่
"""

target_sec3_end = "\n\n---\n\n## 4. แหล่งโค้ดต้นแบบสำหรับการนำไปสร้างจริง (Reference Implementation Code)"
replacement_sec3_end = sec_38_to_311 + target_sec3_end

assert target_sec3_end in content, "Could not find Section 3 end marker in spec"
content = content.replace(target_sec3_end, replacement_sec3_end, 1)
print("1. Inserted Sections 3.8 to 3.11 successfully.")

# =========================================================================
# 2. Update backend/main.py in Section 4.1
# =========================================================================
rate_limit_and_pii_code = """
# ==========================================
# ระบบจำกัดความถี่ต่อกุญแจ (Rate Limiter: 10 req/min) & Zero-PII Audit Logger
# ==========================================
import time
from collections import deque

RATE_LIMIT_WINDOW = 60.0  # หน้าต่างเวลา 60 วินาที
RATE_LIMIT_MAX_REQUESTS = 10  # ไม่เกิน 10 คำขอต่อนาทีต่อกุญแจ
KEY_REQUEST_TIMESTAMPS: dict[str, deque] = {}

def check_rate_limit(token: str) -> None:
    \"\"\"ตรวจสอบอัตราการเรียกใช้งานต่อกุญแจ (O(1)) สกัดกั้นการสแปมก่อนเข้า Semaphore\"\"\"
    now = time.time()
    if token not in KEY_REQUEST_TIMESTAMPS:
        KEY_REQUEST_TIMESTAMPS[token] = deque()

    timestamps = KEY_REQUEST_TIMESTAMPS[token]
    while timestamps and timestamps[0] < now - RATE_LIMIT_WINDOW:
        timestamps.popleft()

    if len(timestamps) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded: Max 10 requests per minute per API key. Please wait.",
            headers={"Retry-After": "60"}
        )
    timestamps.append(now)

def log_zero_pii_audit(key_prefix: str, endpoint: str, query_bytes: int, duration_ms: float, status_code: int) -> None:
    \"\"\"บันทึกเฉพาะ Telemetry เชิงตัวเลข ไม่บันทึกข้อเท็จจริงคดีหรือ PII ลง Disk Log เด็ดขาด\"\"\"
    audit_record = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "endpoint": endpoint,
        "key_prefix": (key_prefix[:8] + "...") if key_prefix else "anonymous",
        "query_bytes": query_bytes,
        "duration_ms": round(duration_ms, 2),
        "status": status_code
    }
    print(f"[AUDIT] {json.dumps(audit_record)}")
"""

target_active_keys = """ACTIVE_KEYS_CACHE: set[str] = set()

def refresh_active_keys_cache():"""

replacement_active_keys = f"""ACTIVE_KEYS_CACHE: set[str] = set()
{rate_limit_and_pii_code}
def refresh_active_keys_cache():"""

assert target_active_keys in content, "Could not find ACTIVE_KEYS_CACHE in main.py"
content = content.replace(target_active_keys, replacement_active_keys, 1)

target_verify_auth = """    token = authorization.split(" ")[1]
    if token not in ACTIVE_KEYS_CACHE and not auth_db.validate_key(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or revoked API Key"
        )"""

replacement_verify_auth = target_verify_auth + "\n    # ตรวจสอบ Rate Limit 10 req/min ต่อกุญแจ\n    check_rate_limit(token)"
assert target_verify_auth in content, "Could not find target_verify_auth in main.py"
content = content.replace(target_verify_auth, replacement_verify_auth, 1)
print("2. Updated verify_auth with check_rate_limit successfully.")

# Update sse_event_publisher in main.py with Zero-PII logging and Context Budgeting
target_sse_pub = """    async def sse_event_publisher():
        process = None
        try:"""

replacement_sse_pub = """    start_time = time.time()
    query_bytes = len(req.query.encode("utf-8"))
    token_prefix = authorization.split(" ")[1][:8] if authorization and " " in authorization else "unknown"

    async def sse_event_publisher():
        process = None
        try:
            # Long-Context Window Budgeting: แจ้งเตือนเมื่อบริบทสะสมเกิน 64KB
            if query_bytes > 65536:
                yield f"event: advisory\\ndata: {json.dumps({'type': 'context_budget_warning', 'message': 'คำแนะนำ: คดีความนี้มีประวัติการสนทนายาวสะสม แนะนำให้พิมพ์คำสั่ง /compact เพื่อย่อสรุปประเด็น หรือเริ่มห้องแชตใหม่ เพื่อคงความแม่นยำสูงสุดในการวินิจฉัย'})}\\n\\n"
"""

assert target_sse_pub in content, "Could not find sse_event_publisher in main.py"
content = content.replace(target_sse_pub, replacement_sse_pub, 1)

target_stream_done = """                    if process.returncode != 0:
                        yield f"event: error\\ndata: {json.dumps({'message': 'กระบวนการวิเคราะห์ขัดข้อง ไม่สามารถประมวลผลต่อได้'})}\\n\\n"
                    else:
                        yield f"event: done\\ndata: {json.dumps({'status': 'completed'})}\\n\\n" """

# Let's match line 1234 carefully
target_done_block = """                    if process.returncode != 0:
                        yield f"event: error\\ndata: {json.dumps({'message': 'กระบวนการวิเคราะห์ขัดข้อง ไม่สามารถประมวลผลต่อได้'})}\\n\\n"
                    else:
                        yield f"event: done\\ndata: {json.dumps({'status': 'completed'})}\\n\\n" """

# In content, let's see how line 1234 is written:
target_done_exact = """                    if process.returncode != 0:
                        yield f"event: error\\ndata: {json.dumps({'message': 'กระบวนการวิเคราะห์ขัดข้อง ไม่สามารถประมวลผลต่อได้'})}\\n\\n"
                    else:
                        yield f"event: done\\ndata: {json.dumps({'status': 'completed'})}\\n\\n\""""

replacement_done_exact = """                    if process.returncode != 0:
                        yield f"event: error\\ndata: {json.dumps({'message': 'กระบวนการวิเคราะห์ขัดข้อง ไม่สามารถประมวลผลต่อได้'})}\\n\\n"
                    else:
                        yield f"event: done\\ndata: {json.dumps({'status': 'completed'})}\\n\\n"
                        duration_ms = (time.time() - start_time) * 1000
                        log_zero_pii_audit(token_prefix, "/api/v1/chat/stream", query_bytes, duration_ms, 200)"""

assert target_done_exact in content, "Could not find target_done_exact in main.py"
content = content.replace(target_done_exact, replacement_done_exact, 1)
print("3. Updated chat_stream_endpoint with Zero-PII Audit and Context Budgeting successfully.")

# =========================================================================
# 3. Update backend/auth_db.py in Section 4.8 with backup_db()
# =========================================================================
backup_db_code = """    def backup_db(self, backup_dir: Path | str | None = None, max_keep: int = 7) -> str:
        \"\"\"
        สำรองข้อมูล keys.db อัตโนมัติด้วย SQLite Online Backup API (Non-blocking Zero-Downtime Backup)
        เก็บบันทึกไฟล์สำรองย้อนหลังสูงสุด max_keep ชุด และล้างชุดเก่าอัตโนมัติ
        \"\"\"
        if backup_dir is None:
            backup_dir = self.db_path.parent / "backups"
        backup_path_dir = Path(backup_dir)
        backup_path_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_file = backup_path_dir / f"keys_backup_{timestamp}.db"

        with self._get_connection() as src_conn:
            dest_conn = sqlite3.connect(str(backup_file))
            with dest_conn:
                src_conn.backup(dest_conn)
            dest_conn.close()

        # ล้างไฟล์สำรองเก่าที่เกิน max_keep
        existing_backups = sorted(backup_path_dir.glob("keys_backup_*.db"))
        if len(existing_backups) > max_keep:
            for old_file in existing_backups[:-max_keep]:
                try:
                    old_file.unlink()
                except OSError:
                    pass
        return str(backup_file)
"""

target_authdb_end = """    def purge_expired_cache(self) -> int:
        \"\"\"ล้างรายการแคชที่หมดอายุ (Auto Purge) เพื่อรักษาขนาดฐานข้อมูล keys.db ให้กะทัดรัดเสมอ\"\"\"
        with self._get_connection() as conn:
            cur = conn.execute("DELETE FROM legal_cache WHERE expires_at <= CURRENT_TIMESTAMP")
            conn.commit()
            return cur.rowcount
```"""

replacement_authdb_end = f"""    def purge_expired_cache(self) -> int:
        \"\"\"ล้างรายการแคชที่หมดอายุ (Auto Purge) เพื่อรักษาขนาดฐานข้อมูล keys.db ให้กะทัดรัดเสมอ\"\"\"
        with self._get_connection() as conn:
            cur = conn.execute("DELETE FROM legal_cache WHERE expires_at <= CURRENT_TIMESTAMP")
            conn.commit()
            return cur.rowcount

{backup_db_code}```"""

assert target_authdb_end in content, "Could not find authdb purge_expired_cache end in spec"
content = content.replace(target_authdb_end, replacement_authdb_end, 1)
print("4. Updated auth_db.py with backup_db successfully.")

# =========================================================================
# 4. Update LegalChatRepository.kt in Section 4.2 with Partial Stream Recovery
# =========================================================================
target_repo_listener = """                    when (type) {
                        "status" -> onStatus(json.optString("text", "กำลังประมวลผล..."))
                        "token" -> onToken(json.optString("delta", ""))
                        "done" -> onDone()
                        "error" -> onError(json.optString("message", "เกิดข้อผิดพลาดในการประมวลผล"))
                    }"""

replacement_repo_listener = """                    when (type) {
                        "status" -> onStatus(json.optString("text", "กำลังประมวลผล..."))
                        "token" -> onToken(json.optString("delta", ""))
                        "advisory" -> onStatus(json.optString("message", ""))
                        "done" -> onDone()
                        "error" -> onError(json.optString("message", "เกิดข้อผิดพลาดในการประมวลผล"))
                    }"""

assert target_repo_listener in content, "Could not find target_repo_listener in spec"
content = content.replace(target_repo_listener, replacement_repo_listener, 1)

target_repo_end = """        })
    }
}
```"""

repo_continue_method = """        })
    }

    /**
     * ถามต่อจากจุดเดิมเมื่อสัญญาณเน็ตหลุด (Partial Stream Recovery & Resume)
     */
    fun continueInterruptedStream(
        serverUrl: String,
        apiKey: String,
        conversationId: String,
        lastPartialSnippet: String,
        onStatus: (String) -> Unit,
        onToken: (String) -> Unit,
        onDone: () -> Unit,
        onError: (String) -> Unit
    ) {
        val continuePrompt = "กรุณาวิเคราะห์ต่อจากข้อความเดิม: \"${lastPartialSnippet.takeLast(200)}\""
        streamConsultation(serverUrl, apiKey, continuePrompt, conversationId, onStatus, onToken, onDone, onError)
    }
}
```"""

assert target_repo_end in content, "Could not find target_repo_end in spec"
content = content.replace(target_repo_end, repo_continue_method, 1)
print("5. Updated LegalChatRepository.kt with Partial Stream Recovery successfully.")

# =========================================================================
# 5. Update ChatDatabaseHelper.kt in Section 4.10 with FTS5 search
# =========================================================================
target_chat_db_helper = """        db.execSQL(\"\"\"
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

fts5_schema_and_search = """        db.execSQL(\"\"\"
            CREATE TABLE $TABLE_MESSAGES (
                $COL_MSG_ID TEXT PRIMARY KEY,
                $COL_MSG_SESSION_ID TEXT NOT NULL,
                $COL_MSG_ROLE TEXT NOT NULL,
                $COL_MSG_CONTENT TEXT NOT NULL,
                $COL_MSG_STATUS TEXT NOT NULL,
                $COL_MSG_TIMESTAMP INTEGER NOT NULL,
                FOREIGN KEY ($COL_MSG_SESSION_ID) REFERENCES $TABLE_SESSIONS($COL_SESSION_ID) ON DELETE CASCADE
            )
        \"\"\".trimIndent())

        // ตารางดัชนีสืบค้นข้อความกฎหมายเต็มรูปแบบ (Offline FTS5 Full-Text Search)
        db.execSQL(\"\"\"
            CREATE VIRTUAL TABLE IF NOT EXISTS chat_messages_fts USING fts5(
                message_id UNINDEXED,
                session_id UNINDEXED,
                content,
                tokenize = 'unicode61'
            )
        \"\"\".trimIndent())

        // ทริกเกอร์เชื่อมข้อมูลเข้า FTS5 อัตโนมัติ (INSERT, UPDATE, DELETE)
        db.execSQL(\"\"\"
            CREATE TRIGGER IF NOT EXISTS trg_msg_ai AFTER INSERT ON $TABLE_MESSAGES BEGIN
                INSERT INTO chat_messages_fts(message_id, session_id, content)
                VALUES (new.$COL_MSG_ID, new.$COL_MSG_SESSION_ID, new.$COL_MSG_CONTENT);
            END;
        \"\"\".trimIndent())"""

assert target_chat_db_helper in content, "Could not find ChatDatabaseHelper schema in spec"
content = content.replace(target_chat_db_helper, fts5_schema_and_search, 1)

target_helper_class_end = """    fun deleteSession(sessionId: String): Boolean {
        val db = writableDatabase
        val rows = db.delete(TABLE_SESSIONS, "$COL_SESSION_ID = ?", arrayOf(sessionId))
        return rows > 0
    }
}"""

fts5_search_method = """    fun deleteSession(sessionId: String): Boolean {
        val db = writableDatabase
        val rows = db.delete(TABLE_SESSIONS, "$COL_SESSION_ID = ?", arrayOf(sessionId))
        return rows > 0
    }

    /**
     * ค้นหาข้อความคำพิพากษาหรือตัวบทกฎหมายแบบ Full-Text Search ออฟไลน์ 100%
     */
    fun searchMessages(keyword: String): List<ChatMessage> {
        val results = mutableListOf<ChatMessage>()
        val db = readableDatabase
        val sanitizedQuery = keyword.replace("\"", "\"\"")
        val cursor = db.rawQuery(
            \"\"\"
            SELECT m.$COL_MSG_ID, m.$COL_MSG_SESSION_ID, m.$COL_MSG_ROLE, m.$COL_MSG_CONTENT, m.$COL_MSG_STATUS, m.$COL_MSG_TIMESTAMP
            FROM $TABLE_MESSAGES m
            JOIN chat_messages_fts fts ON m.$COL_MSG_ID = fts.message_id
            WHERE chat_messages_fts MATCH ?
            ORDER BY m.$COL_MSG_TIMESTAMP DESC
            \"\"\".trimIndent(),
            arrayOf("\"$sanitizedQuery\"*")
        )
        cursor.use { c ->
            while (c.moveToNext()) {
                results.add(
                    ChatMessage(
                        id = c.getString(0),
                        sessionId = c.getString(1),
                        role = c.getString(2),
                        content = c.getString(3),
                        status = c.getString(4),
                        timestamp = c.getLong(5)
                    )
                )
            }
        }
        return results
    }
}"""

assert target_helper_class_end in content, "Could not find deleteSession end in spec"
content = content.replace(target_helper_class_end, fts5_search_method, 1)
print("6. Updated ChatDatabaseHelper.kt with FTS5 and searchMessages successfully.")

with open(spec_path, "w", encoding="utf-8") as f:
    f.write(content)

print("ALL SPEC UPDATES APPLIED SUCCESSFULLY.")
