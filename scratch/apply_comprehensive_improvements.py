import sys
from pathlib import Path

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# 1. Update backend/main.py in Section 4.1:
# Add SelectiveGZipMiddleware and get_client_ip
old_sec41_middleware = """app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# เปิดใช้งาน GZipMiddleware สำหรับบีบอัดข้อมูลตอบกลับอัตโนมัติ (ลดแบนด์วิดท์ 70-85%)
app.add_middleware(GZipMiddleware, minimum_size=256)"""

new_sec41_middleware = """app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.types import ASGIApp, Receive, Scope, Send

class SelectiveGZipMiddleware:
    \"\"\"
    Middleware จัดการบีบอัดข้อมูลแบบชาญฉลาด (Selective Gzip):
    - บีบอัด Gzip บนทุกคำขอทั่วไป (JSON APIs, Admin UI, Direct Chat) เพื่อประหยัดแบนด์วิดท์ 70-85%
    - ยกเว้นเฉพาะเส้นทาง /stream (SSE text/event-stream) เพื่อไม่ให้ zlib บัฟเฟอร์โทเคน และคงความเร็ว Real-time TTFT สูงสุด
    \"\"\"
    def __init__(self, app: ASGIApp, minimum_size: int = 256):
        self.app = app
        self.minimum_size = minimum_size
        self.gzip_middleware = GZipMiddleware(app, minimum_size=minimum_size)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            path = scope.get("path", "")
            if path.endswith("/stream"):
                await self.app(scope, receive, send)
                return
        await self.gzip_middleware(scope, receive, send)

# เปิดใช้งาน SelectiveGZipMiddleware
app.add_middleware(SelectiveGZipMiddleware, minimum_size=256)"""

assert old_sec41_middleware in content, "old_sec41_middleware not found"
content = content.replace(old_sec41_middleware, new_sec41_middleware)

# Update get_client_ip in verify_admin
old_sec41_admin = """def is_tailnet_or_local_ip(ip: str) -> bool:
    \"\"\"ตรวจสอบว่าเป็น IP ภายในเครื่อง (127.0.0.1) หรือ IP ในวง Tailnet (100.64.0.0/10) หรือไม่\"\"\"
    if ip in ("127.0.0.1", "localhost", "::1", "testclient"):
        return True
    try:
        addr = ipaddress.ip_address(ip)
        tailnet_network = ipaddress.ip_network("100.64.0.0/10")
        return addr in tailnet_network
    except Exception:
        return False

async def verify_admin(request: Request, x_admin_secret: str = Header(None)):
    \"\"\"ตรวจสอบสิทธิ์ Admin พร้อมบล็อกคำขอจาก Public Funnel หากไม่ได้เปิด ALLOW_PUBLIC_ADMIN\"\"\"
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not ALLOW_PUBLIC_ADMIN and not is_tailnet_or_local_ip(client_ip):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access is restricted to Localhost and Private Tailnet Mesh only."
        )
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Admin")

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    \"\"\"ให้บริการหน้าจอ Web Admin UI สำหรับจัดการกุญแจ (บล็อก Public Funnel อัตโนมัติ)\"\"\"
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not ALLOW_PUBLIC_ADMIN and not is_tailnet_or_local_ip(client_ip):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin dashboard is restricted to Localhost and Private Tailnet Mesh only."
        )
    return templates.TemplateResponse("admin.html", {"request": request})"""

new_sec41_admin = """def is_tailnet_or_local_ip(ip: str) -> bool:
    \"\"\"ตรวจสอบว่าเป็น IP ภายในเครื่อง (127.0.0.1) หรือ IP ในวง Tailnet (100.64.0.0/10) หรือไม่\"\"\"
    if ip in ("127.0.0.1", "localhost", "::1", "testclient"):
        return True
    try:
        addr = ipaddress.ip_address(ip)
        tailnet_network = ipaddress.ip_network("100.64.0.0/10")
        return addr in tailnet_network
    except Exception:
        return False

def get_client_ip(request: Request) -> str:
    \"\"\"
    ดึง IP ต้นทางจริงของผู้ใช้ โดยอ่านจาก X-Forwarded-For ของ Tailscale Reverse Proxy / Funnel
    เพื่อป้องกันไม่ให้คำขอสาธารณะจาก Funnel ถูกมองเป็น 127.0.0.1
    \"\"\"
    forwarded = request.headers.get("x-forwarded-for") or request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

async def verify_admin(request: Request, x_admin_secret: str = Header(None)):
    \"\"\"ตรวจสอบสิทธิ์ Admin พร้อมบล็อกคำขอจาก Public Funnel หากไม่ได้เปิด ALLOW_PUBLIC_ADMIN\"\"\"
    client_ip = get_client_ip(request)
    if not ALLOW_PUBLIC_ADMIN and not is_tailnet_or_local_ip(client_ip):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access is restricted to Localhost and Private Tailnet Mesh only."
        )
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Admin")

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    \"\"\"ให้บริการหน้าจอ Web Admin UI สำหรับจัดการกุญแจ (บล็อก Public Funnel อัตโนมัติ)\"\"\"
    client_ip = get_client_ip(request)
    if not ALLOW_PUBLIC_ADMIN and not is_tailnet_or_local_ip(client_ip):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin dashboard is restricted to Localhost and Private Tailnet Mesh only."
        )
    return templates.TemplateResponse("admin.html", {"request": request})"""

assert old_sec41_admin in content, "old_sec41_admin not found"
content = content.replace(old_sec41_admin, new_sec41_admin)

# Update SSE headers in backend/main.py: Cache-Control: no-cache, no-transform
old_sse_headers = """            return StreamingResponse(
                replay_cached(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                    "X-Cache-Status": "HIT"
                }
            )"""

new_sse_headers = """            return StreamingResponse(
                replay_cached(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache, no-transform",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                    "X-Cache-Status": "HIT"
                }
            )"""

assert old_sse_headers in content, "old_sse_headers not found"
content = content.replace(old_sse_headers, new_sse_headers)

old_sse_live_headers = """    return StreamingResponse(
        sse_event_publisher(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )"""

new_sse_live_headers = """    return StreamingResponse(
        sse_event_publisher(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )"""

assert old_sse_live_headers in content, "old_sse_live_headers not found"
content = content.replace(old_sse_live_headers, new_sse_live_headers)

# 2. Update Section 4.2 LegalChatRepository.kt: remove manual Accept-Encoding gzip
old_okhttp_request = """        val request = Request.Builder()
            .url(serverUrl)
            .addHeader("Authorization", "Bearer $apiKey")
            .addHeader("Accept", "text/event-stream")
            .addHeader("Accept-Encoding", "gzip")
            .post(payload.toRequestBody("application/json; charset=utf-8".toMediaType()))
            .build()"""

new_okhttp_request = """        val request = Request.Builder()
            .url(serverUrl)
            .addHeader("Authorization", "Bearer $apiKey")
            .addHeader("Accept", "text/event-stream")
            // ปล่อยให้ OkHttp BridgeInterceptor จัดการ Transparent Decompression อัตโนมัติ (ไม่เซ็ตซ้ำเพื่อป้องกันปัญหา EventSource binary parsing)
            .post(payload.toRequestBody("application/json; charset=utf-8".toMediaType()))
            .build()"""

assert old_okhttp_request in content, "old_okhttp_request not found"
content = content.replace(old_okhttp_request, new_okhttp_request)

# 3. Update Section 4.3 MarkdownViewManager.kt: add setupTextView for Thai typography
old_md_manager = """    /**
     * เรนเดอร์ข้อความ Markdown ลงบน TextView ทันทีที่ Token ไหลเข้ามา
     */
    fun render(textView: TextView, markdownContent: String) {
        markwon.setMarkdown(textView, markdownContent)
    }"""

new_md_manager = """    /**
     * กำหนดการตัดคำภาษาไทยให้สวยงามและถูกต้องตามสรีระภาษา (Thai Typography & Line Breaking)
     */
    fun setupTextView(textView: TextView) {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
            textView.breakStrategy = android.graphics.text.LineBreaker.BREAK_STRATEGY_HIGH_QUALITY
            textView.hyphenationFrequency = android.text.Layout.HYPHENATION_FREQUENCY_FULL
        }
    }

    /**
     * เรนเดอร์ข้อความ Markdown ลงบน TextView ทันทีที่ Token ไหลเข้ามา
     */
    fun render(textView: TextView, markdownContent: String) {
        setupTextView(textView)
        markwon.setMarkdown(textView, markdownContent)
    }"""

assert old_md_manager in content, "old_md_manager not found"
content = content.replace(old_md_manager, new_md_manager)

# 4. Update Section 4.8 backend/auth_db.py: modernize datetime and add purge_expired_cache
old_authdb_imports = """import sqlite3
import secrets
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta"""

new_authdb_imports = """import sqlite3
import secrets
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone"""

assert old_authdb_imports in content, "old_authdb_imports not found"
content = content.replace(old_authdb_imports, new_authdb_imports)

old_authdb_revoke = """            cur = conn.execute(
                "UPDATE api_keys SET is_active = 0, revoked_at = ? WHERE id = ?",
                (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), key_id)
            )"""

new_authdb_revoke = """            cur = conn.execute(
                "UPDATE api_keys SET is_active = 0, revoked_at = ? WHERE id = ?",
                (datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), key_id)
            )"""

assert old_authdb_revoke in content, "old_authdb_revoke not found"
content = content.replace(old_authdb_revoke, new_authdb_revoke)

old_authdb_set_cache = """        expires_at = (datetime.utcnow() + timedelta(hours=ttl_hours)).strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            conn.execute(\"\"\"
                INSERT OR REPLACE INTO legal_cache (query_hash, query_text, cached_events, expires_at)
                VALUES (?, ?, ?, ?)
            \"\"\", (query_hash, query_text, json.dumps(events, ensure_ascii=False), expires_at))
            conn.commit()"""

new_authdb_set_cache = """        expires_at = (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            conn.execute(\"\"\"
                INSERT OR REPLACE INTO legal_cache (query_hash, query_text, cached_events, expires_at)
                VALUES (?, ?, ?, ?)
            \"\"\", (query_hash, query_text, json.dumps(events, ensure_ascii=False), expires_at))
            conn.commit()

    def purge_expired_cache(self) -> int:
        \"\"\"ล้างรายการแคชที่หมดอายุ (Auto Purge) เพื่อรักษาขนาดฐานข้อมูล keys.db ให้กะทัดรัดเสมอ\"\"\"
        with self._get_connection() as conn:
            cur = conn.execute("DELETE FROM legal_cache WHERE expires_at <= CURRENT_TIMESTAMP")
            conn.commit()
            return cur.rowcount"""

assert old_authdb_set_cache in content, "old_authdb_set_cache not found"
content = content.replace(old_authdb_set_cache, new_authdb_set_cache)

spec_path.write_text(content, encoding="utf-8")
print("Successfully applied comprehensive improvements to system_spec_and_implementation_plan.md!")
