import py_compile
import tempfile
from pathlib import Path

test_code = """
import asyncio
import json
import os
import re
import zlib
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from auth_db import AuthDB

app = FastAPI(
    title="THLawDeka-mobile Gateway",
    description="Secure ASGI SSE Gateway with Gzip Compression & Zero Server-Disk Writes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# เปิดใช้งาน GZipMiddleware สำหรับบีบอัดข้อมูลตอบกลับอัตโนมัติ (ลดแบนด์วิดท์ 70-85%)
app.add_middleware(GZipMiddleware, minimum_size=256)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "admin_super_secret_pass_2026")
auth_db = AuthDB()

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent

CANDIDATE_HARNESS = PROJECT_ROOT / "THLawDeka"
if (CANDIDATE_HARNESS / "AGENTS.md").exists():
    DEFAULT_WORKSPACE = CANDIDATE_HARNESS
elif (CURRENT_FILE.parent / "AGENTS.md").exists():
    DEFAULT_WORKSPACE = CURRENT_FILE.parent
else:
    DEFAULT_WORKSPACE = CANDIDATE_HARNESS

WORKSPACE_DIR = os.getenv("THLAW_WORKSPACE", str(DEFAULT_WORKSPACE))
VALID_API_KEY = os.getenv("GATEWAY_API_KEY", "thlaw_secret_dev_key_2026")

EXECUTION_SEMAPHORE = asyncio.Semaphore(3)

INJECTION_BLACKLIST_PATTERNS = [
    re.compile(r"(?i)ignore\s+(all\s+)?(previous|prior|above)\s+instructions"),
    re.compile(r"(?i)system\s+prompt"),
    re.compile(r"(?i)(modify|edit|overwrite|delete|update)\s+.*(agent|harness|rule|prompt|config|agents\.md)"),
    re.compile(r"(?i)(powershell|cmd\.exe|bash|sh\s+-c|curl\s+|wget\s+|chmod|rm\s+-rf|taskkill)"),
    re.compile(r"(?i)cat\s+/etc/"),
    re.compile(r"(?i)run\s+(command|terminal|script|shell)"),
    re.compile(r"(?i)(exec|eval|os\.system|subprocess)"),
]

def contains_system_attack(query: str) -> bool:
    for pattern in INJECTION_BLACKLIST_PATTERNS:
        if pattern.search(query):
            return True
    return False

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=32768, description="ข้อเท็จจริงคดี ไม่เกิน 32KB")
    conversation_id: str | None = Field(None, max_length=128)

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        if "\\x00" in v:
            raise ValueError("ไม่อนุญาตให้อักขระ Null Byte ในข้อความ")
        if contains_system_attack(v):
            raise ValueError("คำขอถูกปฏิเสธเนื่องจากมีรูปแบบคำสั่งที่อาจกระทบต่อความมั่นคงปลอดภัยของระบบ")
        return v.strip()

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
    if token not in ACTIVE_KEYS_CACHE and not auth_db.validate_key(token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or revoked API Key"
        )

class CreateKeyRequest(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=100)

async def verify_admin(x_admin_secret: str = Header(None)):
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Admin")

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/api/v1/admin/keys")
async def list_keys_endpoint(admin_auth: None = Depends(verify_admin)):
    return {"status": "success", "keys": auth_db.list_keys()}

@app.post("/api/v1/admin/keys")
async def generate_key_endpoint(req: CreateKeyRequest, admin_auth: None = Depends(verify_admin)):
    new_token = auth_db.generate_key(req.user_name)
    refresh_active_keys_cache()
    return {"status": "success", "token": new_token, "user_name": req.user_name}

@app.post("/api/v1/admin/keys/{key_id}/revoke")
async def revoke_key_endpoint(key_id: int, admin_auth: None = Depends(verify_admin)):
    success = auth_db.revoke_key(key_id)
    if not success:
        raise HTTPException(status_code=404, detail="Key ID not found")
    refresh_active_keys_cache()
    return {"status": "success", "message": f"Key {key_id} has been revoked"}

@app.get("/api/v1/health")
async def health_check_endpoint(authorization: str = Header(None)):
    await verify_auth(authorization)
    return {
        "status": "healthy",
        "service": "THLawDeka-mobile Gateway",
        "message": "พร้อมให้บริการวิเคราะห์คดีความ (Zero Server Disk Writes)"
    }

@app.post("/api/v1/chat/stream")
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
                    await asyncio.sleep(0.005)
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

    async def sse_event_publisher():
        process = None
        try:
            async with asyncio.timeout(10.0):
                async with EXECUTION_SEMAPHORE:
                    cmd = [
                        "agy",
                        "--sandbox",
                        "--dangerously-skip-permissions",
                        "--input-format", "text",
                        "--output-format", "stream-json",
                        "--print-timeout", "60s",
                        "-p", "-"
                    ]
                    
                    if req.conversation_id:
                        if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_\\-]{0,63}$", req.conversation_id):
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="รูปแบบ conversation_id ไม่ถูกต้อง"
                            )
                        cmd.extend(["--conversation", req.conversation_id])

                    safe_env = {
                        "PATH": os.getenv("PATH", ""),
                        "SYSTEMROOT": os.getenv("SYSTEMROOT", ""),
                        "TEMP": os.getenv("TEMP", ""),
                        "TMP": os.getenv("TMP", ""),
                        "HOME": os.getenv("HOME", ""),
                        "USERPROFILE": os.getenv("USERPROFILE", "")
                    }

                    yield f"event: status\\ndata: {json.dumps({'text': 'กำลังเตรียมการวิเคราะห์ข้อกฎหมาย...'})}\\n\\n"

                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=WORKSPACE_DIR,
                        env=safe_env
                    )

                    if process.stdin:
                        process.stdin.write(req.query.encode("utf-8"))
                        await process.stdin.drain()
                        process.stdin.close()
                        await process.stdin.wait_closed()

                    async for raw_line in process.stdout:
                        line = raw_line.decode("utf-8", errors="replace").strip()
                        if not line:
                            continue

                        try:
                            data = json.loads(line)
                            if data.get("type") == "token" or "delta" in data:
                                text_chunk = data.get("delta") or data.get("content", "")
                                yield f"event: token\\ndata: {json.dumps({'delta': text_chunk})}\\n\\n"
                            elif data.get("type") == "status":
                                yield f"event: status\\ndata: {json.dumps({'text': data.get('message', '')})}\\n\\n"
                            else:
                                yield f"event: token\\ndata: {json.dumps({'delta': line})}\\n\\n"
                        except json.JSONDecodeError:
                            yield f"event: token\\ndata: {json.dumps({'delta': line})}\\n\\n"

                    await process.wait()

                    if process.returncode != 0:
                        yield f"event: error\\ndata: {json.dumps({'message': 'กระบวนการวิเคราะห์ขัดข้อง ไม่สามารถประมวลผลต่อได้'})}\\n\\n"
                    else:
                        yield f"event: done\\ndata: {json.dumps({'status': 'completed'})}\\n\\n"

        except (TimeoutError, asyncio.CancelledError):
            yield f"event: error\\ndata: {json.dumps({'message': 'เซิร์ฟเวอร์กำลังให้บริการเต็ม หรือการประมวลผลหมดเวลา'})}\\n\\n"
        except Exception:
            yield f"event: error\\ndata: {json.dumps({'message': 'เกิดข้อผิดพลาดภายในระบบ'})}\\n\\n"
        finally:
            if process and process.returncode is None:
                try:
                    process.kill()
                    await process.wait()
                except Exception:
                    pass

    return StreamingResponse(
        sse_event_publisher(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
"""

test_p = Path("scratch/test_new_main_code.py")
test_p.write_text(test_code, encoding="utf-8")
py_compile.compile(str(test_p), doraise=True)
print("New main.py code compiles 100% cleanly!")
