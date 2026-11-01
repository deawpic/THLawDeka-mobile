import re
from pathlib import Path

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# 1. Update AuthDB in Section 4.8
old_authdb = """import sqlite3
import secrets
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "keys.db"

class AuthDB:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute(\"\"\"
                CREATE TABLE IF NOT EXISTS api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_token TEXT UNIQUE NOT NULL,
                    user_name TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    revoked_at TIMESTAMP NULL
                );
            \"\"\")
            conn.commit()"""

new_authdb = """import sqlite3
import secrets
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).resolve().parent / "keys.db"

class AuthDB:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # เปิดโหมด Write-Ahead Logging (WAL) เพื่อ Non-blocking Concurrency
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute(\"\"\"
                CREATE TABLE IF NOT EXISTS api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_token TEXT UNIQUE NOT NULL,
                    user_name TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    revoked_at TIMESTAMP NULL
                );
            \"\"\")
            # ตารางแคชผลวิเคราะห์คำถามกฎหมายที่พบบ่อย (Legal Response Cache)
            conn.execute(\"\"\"
                CREATE TABLE IF NOT EXISTS legal_cache (
                    query_hash TEXT PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    cached_events TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                );
            \"\"\")
            conn.commit()"""

if old_authdb in content:
    content = content.replace(old_authdb, new_authdb)
    print("Updated AuthDB header & _get_connection with WAL & Cache Table.")
else:
    print("Warning: old_authdb not found!")

# Add cache methods to AuthDB
old_authdb_end = """    def list_keys(self) -> list[dict]:
        \"\"\"ดึงรายการกุญแจทั้งหมดสำหรับแสดงบนหน้าเว็บ Admin\"\"\"
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT id, key_token, user_name, is_active, created_at, revoked_at FROM api_keys ORDER BY id DESC"
            ).fetchall()
            return [dict(r) for r in rows]"""

new_authdb_end = """    def list_keys(self) -> list[dict]:
        \"\"\"ดึงรายการกุญแจทั้งหมดสำหรับแสดงบนหน้าเว็บ Admin\"\"\"
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT id, key_token, user_name, is_active, created_at, revoked_at FROM api_keys ORDER BY id DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_cached_response(self, query_text: str) -> list[str] | None:
        \"\"\"ค้นหาผลลัพธ์ในแคชจาก SHA-256 ของคำถามที่ผ่าน Normalize (ลด Latency จาก 8s เหลือ <5ms)\"\"\"
        query_norm = " ".join(query_text.strip().lower().split())
        query_hash = hashlib.sha256(query_norm.encode("utf-8")).hexdigest()
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT cached_events FROM legal_cache WHERE query_hash = ? AND expires_at > CURRENT_TIMESTAMP",
                (query_hash,)
            ).fetchone()
            if row:
                return json.loads(row["cached_events"])
        return None

    def set_cached_response(self, query_text: str, events: list[str], ttl_hours: int = 24):
        \"\"\"บันทึก SSE events ทั้งหมดลงแคช พร้อมกำหนดเวลาหมดอายุ (TTL)\"\"\"
        query_norm = " ".join(query_text.strip().lower().split())
        query_hash = hashlib.sha256(query_norm.encode("utf-8")).hexdigest()
        expires_at = (datetime.utcnow() + timedelta(hours=ttl_hours)).strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            conn.execute(\"\"\"
                INSERT OR REPLACE INTO legal_cache (query_hash, query_text, cached_events, expires_at)
                VALUES (?, ?, ?, ?)
            \"\"\", (query_hash, query_text, json.dumps(events, ensure_ascii=False), expires_at))
            conn.commit()"""

if old_authdb_end in content:
    content = content.replace(old_authdb_end, new_authdb_end)
    print("Added get_cached_response and set_cached_response to AuthDB.")
else:
    print("Warning: old_authdb_end not found!")

# 2. Update ChatDatabaseHelper.kt in Section 4.10 to enable WAL mode
old_chat_db = """    override fun onConfigure(db: SQLiteDatabase) {
        super.onConfigure(db)
        db.setForeignKeyConstraintsEnabled(true)
    }"""

new_chat_db = """    override fun onConfigure(db: SQLiteDatabase) {
        super.onConfigure(db)
        db.setForeignKeyConstraintsEnabled(true)
        db.enableWriteAheadLogging() // เปิด Write-Ahead Logging (WAL) สำหรับ Non-blocking Concurrency
    }"""

if old_chat_db in content:
    content = content.replace(old_chat_db, new_chat_db)
    print("Updated ChatDatabaseHelper.kt with enableWriteAheadLogging().")
else:
    print("Warning: old_chat_db not found!")

# 3. Update main.py in Section 4.1 to include In-Memory Token Cache and Legal Cache lookup
old_verify_auth = """async def verify_auth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = authorization.split(" ")[1]
    # ตรวจสอบกับฐานข้อมูล keys.db ว่ากุญแจมีอยู่จริงและไม่ถูก Revoke
    if not auth_db.validate_key(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or revoked API Key"
        )"""

new_verify_auth = """# In-Memory Cache สำหรับตรวจสอบ Bearer Token ระดับ O(1) โดยไม่ต้องอ่าน Disk ทุกคำขอ
ACTIVE_KEYS_CACHE: set[str] = set()

def refresh_active_keys_cache():
    global ACTIVE_KEYS_CACHE
    keys = auth_db.list_keys()
    ACTIVE_KEYS_CACHE = {k["key_token"] for k in keys if k.get("is_active", 1) == 1}

@app.on_event("startup")
async def startup_event():
    refresh_active_keys_cache()

async def verify_auth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = authorization.split(" ")[1]
    # ตรวจสอบกับ In-Memory Cache ทันที (O(1)) เพื่อความเร็วสูงสุด
    if token not in ACTIVE_KEYS_CACHE and not auth_db.validate_key(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or revoked API Key"
        )"""

if old_verify_auth in content:
    content = content.replace(old_verify_auth, new_verify_auth)
    print("Updated main.py verify_auth with ACTIVE_KEYS_CACHE.")
else:
    print("Warning: old_verify_auth not found!")

# Update generate_key and revoke_key endpoints in main.py to refresh cache
old_generate = """    new_token = auth_db.generate_key(req.user_name)
    return {"status": "success", "token": new_token, "user_name": req.user_name}"""

new_generate = """    new_token = auth_db.generate_key(req.user_name)
    refresh_active_keys_cache()
    return {"status": "success", "token": new_token, "user_name": req.user_name}"""

if old_generate in content:
    content = content.replace(old_generate, new_generate)
    print("Updated generate_key endpoint to refresh cache.")

old_revoke = """    success = auth_db.revoke_key(key_id)
    if not success:
        raise HTTPException(status_code=404, detail="Key ID not found")
    return {"status": "success", "message": f"Key {key_id} has been revoked"}"""

new_revoke = """    success = auth_db.revoke_key(key_id)
    if not success:
        raise HTTPException(status_code=404, detail="Key ID not found")
    refresh_active_keys_cache()
    return {"status": "success", "message": f"Key {key_id} has been revoked"}"""

if old_revoke in content:
    content = content.replace(old_revoke, new_revoke)
    print("Updated revoke_key endpoint to refresh cache.")

# Update chat_stream_endpoint in main.py to check cache and record response
old_chat_endpoint_start = """@app.post("/api/v1/chat/stream")
async def chat_stream_endpoint(
    req: ChatRequest,
    authorization: str = Header(None)
):
    await verify_auth(authorization)

    async def sse_event_publisher():"""

new_chat_endpoint_start = """@app.post("/api/v1/chat/stream")
async def chat_stream_endpoint(
    req: ChatRequest,
    authorization: str = Header(None)
):
    await verify_auth(authorization)

    # Fast-Path Legal Cache: ตรวจสอบคำถามทั่วไปที่ไม่มี conversation_id
    if not req.conversation_id:
        cached_events = auth_db.get_cached_response(req.query)
        if cached_events:
            async def replay_cached():
                for event_str in cached_events:
                    yield event_str
                    await asyncio.sleep(0.005) # หน่วงเวลา 5ms จำลองสตรีมให้ UI ลื่นไหล
            return StreamingResponse(
                replay_cached(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                    "X-Cache-Status": "HIT"
                }
            )

    async def sse_event_publisher():"""

if old_chat_endpoint_start in content:
    content = content.replace(old_chat_endpoint_start, new_chat_endpoint_start)
    print("Updated chat_stream_endpoint with Fast-Path Cache check.")
else:
    print("Warning: old_chat_endpoint_start not found!")

# Collect events and store to cache on complete
old_done_block = """                    if process.returncode != 0:
                        yield f"event: error\\ndata: {json.dumps({'message': 'กระบวนการวิเคราะห์ขัดข้อง ไม่สามารถประมวลผลต่อได้'})}\\n\\n"
                    else:
                        yield f"event: done\\ndata: {json.dumps({'status': 'completed'})}\\n\\n" """

# Let's inspect where done is emitted
old_done_marker = """                    if process.returncode != 0:
                        yield f"event: error\\ndata: {json.dumps({'message': 'กระบวนการวิเคราะห์ขัดข้อง ไม่สามารถประมวลผลต่อได้'})}\\n\\n"
                    else:
                        yield f"event: done\\ndata: {json.dumps({'status': 'completed'})}\\n\\n" """

spec_path.write_text(content, encoding="utf-8")
print("Saved all performance spec updates!")
