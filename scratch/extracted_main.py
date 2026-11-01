import asyncio
import json
import os
import re
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from auth_db import AuthDB

app = FastAPI(
    title="THLawDeka-mobile Gateway",
    description="Secure ASGI SSE Gateway for THLawDeka Core Agent via agy Stdin Pipe",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ติดตั้ง Jinja2 สำหรับเรนเดอร์หน้า Admin Dashboard
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# รหัสผ่านลับสำหรับผู้ดูแลระบบเข้าหน้า /admin
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "admin_super_secret_pass_2026")
auth_db = AuthDB()

# ค้นหาตำแหน่งโฟลเดอร์ Root ของโปรเจกต์ Core Harness แบบ Relative อัตโนมัติ
# โครงสร้าง: THLawDeka-mobile/backend/main.py -> ถอย 1 ระดับไป Root -> เข้าโฟลเดอร์ THLawDeka/
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent  # โฟลเดอร์ THLawDeka-mobile

# ตรวจสอบหาตำแหน่ง Core Agent Workspace (THLawDeka-mobile/THLawDeka)
CANDIDATE_HARNESS = PROJECT_ROOT / "THLawDeka"
if (CANDIDATE_HARNESS / "AGENTS.md").exists():
    DEFAULT_WORKSPACE = CANDIDATE_HARNESS
elif (CURRENT_FILE.parent / "AGENTS.md").exists():
    DEFAULT_WORKSPACE = CURRENT_FILE.parent
else:
    DEFAULT_WORKSPACE = CANDIDATE_HARNESS

WORKSPACE_DIR = os.getenv("THLAW_WORKSPACE", str(DEFAULT_WORKSPACE))
OUTPUT_DIR = Path(WORKSPACE_DIR) / "output"
VALID_API_KEY = os.getenv("GATEWAY_API_KEY", "thlaw_secret_dev_key_2026")

# ตรวจจับแท็ก <!-- ARTIFACT: output/<filename>.md --> จาก Core Agent
ARTIFACT_REGEX = re.compile(r"<!--\s*ARTIFACT:\s*output/([a-zA-Z0-9_\-\.\u0E00-\u0E7F]+)\s*-->")

# จำกัดคำขอที่เข้าประมวลผลพร้อมกันไม่เกิน 3 คิว เพื่อรักษาทรัพยากร CPU
EXECUTION_SEMAPHORE = asyncio.Semaphore(3)

# รูปแบบ Regular Expression สำหรับสกัดกั้น Prompt Injection, System Tampering และคำสั่ง Shell ก่อนเข้า Subprocess
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
    """ตรวจสอบว่าคำถามมีเจตนาทำลายระบบหรือหลอกล่อให้แก้ไข Core Harness หรือไม่"""
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
        # 1. สกัดกั้น Null bytes ที่อาจทำให้ OS Subprocess เกิดพฤติกรรมไม่พึงประสงค์
        if "\x00" in v:
            raise ValueError("ไม่อนุญาตให้อักขระ Null Byte ในข้อความ")
        # 2. เกราะชั้นที่ 1: สกัดกั้น Prompt Injection และคำสั่งดัดแปลง Core Agent Harness ทันที
        if contains_system_attack(v):
            raise ValueError("คำขอถูกปฏิเสธเนื่องจากมีรูปแบบคำสั่งที่อาจกระทบต่อความมั่นคงปลอดภัยของระบบ")
        return v.strip()

# In-Memory Cache สำหรับตรวจสอบ Bearer Token ระดับ O(1) โดยไม่ต้องอ่าน Disk ทุกคำขอ
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
        )

# ==========================================
# ส่วนงาน Admin UI และ API จัดการกุญแจ
# ==========================================

class CreateKeyRequest(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=100)

async def verify_admin(x_admin_secret: str = Header(None)):
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Admin")

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    """ให้บริการหน้าจอ Web Admin UI สำหรับจัดการกุญแจ"""
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/api/v1/admin/keys")
async def list_keys_endpoint(admin_auth: None = Depends(verify_admin)):
    """ดึงรายชื่อกุญแจทั้งหมดจาก keys.db"""
    return {"status": "success", "keys": auth_db.list_keys()}

@app.post("/api/v1/admin/keys")
async def generate_key_endpoint(req: CreateKeyRequest, admin_auth: None = Depends(verify_admin)):
    """สร้างกุญแจใหม่และบันทึกลง keys.db"""
    new_token = auth_db.generate_key(req.user_name)
    refresh_active_keys_cache()
    return {"status": "success", "token": new_token, "user_name": req.user_name}

@app.post("/api/v1/admin/keys/{key_id}/revoke")
async def revoke_key_endpoint(key_id: int, admin_auth: None = Depends(verify_admin)):
    """สั่งระงับ (Revoke) กุญแจทันที มีผลแบบ Real-time"""
    success = auth_db.revoke_key(key_id)
    if not success:
        raise HTTPException(status_code=404, detail="Key ID not found")
    refresh_active_keys_cache()
    return {"status": "success", "message": f"Key {key_id} has been revoked"}

# ==========================================
# ส่วนงาน Mobile Client API
# ==========================================

@app.get("/api/v1/health")
async def health_check_endpoint(authorization: str = Header(None)):
    """ใช้สำหรับให้ Android Client ทดสอบการเชื่อมต่อและตรวจสอบความถูกต้องของ Auth Key"""
    await verify_auth(authorization)
    return {
        "status": "healthy",
        "service": "THLawDeka-mobile Gateway",
        "message": "พร้อมให้บริการวิเคราะห์คดีความ"
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

    async def sse_event_publisher():
        process = None
        try:
            # รอคิวว่างไม่เกิน 10 วินาที
            async with asyncio.timeout(10.0):
                async with EXECUTION_SEMAPHORE:
                    cmd = [
                        "agy",
                        "--sandbox",                      # กักบริเวณห้ามแตะไฟล์นอก Workspace / ห้ามคำสั่ง OS อันตราย
                        "--dangerously-skip-permissions",  # อนุมัติรัน Legal MCPs แบบอัตโนมัติ
                        "--input-format", "text",
                        "--output-format", "stream-json",
                        "--print-timeout", "60s",         # Watchdog timeout ภายในตัว agy
                        "-p", "-"                         # บังคับรับข้อความจาก stdin เท่านั้น (ไม่มีข้อมูลคดีหลุดใน OS logs)
                    ]
                    
                    if req.conversation_id:
                        # ป้องกัน CLI Flag Injection โดยบังคับขึ้นต้นด้วยตัวอักษร/ตัวเลขเท่านั้น (ห้ามมีขีด - นำหน้า)
                        if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_\-]{0,63}$", req.conversation_id):
                            raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail="รูปแบบ conversation_id ไม่ถูกต้อง (ต้องขึ้นต้นด้วยตัวอักษรหรือตัวเลขเท่านั้น)"
                            )
                        cmd.extend(["--conversation", req.conversation_id])

                    # กรอง Environment ปลอดภัย ไม่ส่งต่อ ADMIN_SECRET หรือ API Keys ลับเข้า Subprocess
                    safe_env = {
                        "PATH": os.getenv("PATH", ""),
                        "SYSTEMROOT": os.getenv("SYSTEMROOT", ""),
                        "TEMP": os.getenv("TEMP", ""),
                        "TMP": os.getenv("TMP", ""),
                        "HOME": os.getenv("HOME", ""),
                        "USERPROFILE": os.getenv("USERPROFILE", "")
                    }

                    yield f"event: status\ndata: {json.dumps({'text': 'กำลังเตรียมการวิเคราะห์ข้อกฎหมาย...'})}\n\n"

                    # เปิด subprocess โดยไม่ผ่าน Shell Interpreter (shell=False) พร้อมสภาพแวดล้อมที่จำกัดสิทธิ์
                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=WORKSPACE_DIR,
                        env=safe_env
                    )

                    # ส่งข้อความคดีความผ่าน stdin Pipe แล้วปิดท่อเขียนทันที
                    if process.stdin:
                        process.stdin.write(req.query.encode("utf-8"))
                        await process.stdin.drain()
                        process.stdin.close()
                        await process.stdin.wait_closed()

                    # ฟังก์ชันตรวจสอบและส่ง event: file หากพบ Artifact Handshake Tag
                    def check_artifact(text: str):
                        match = ARTIFACT_REGEX.search(text)
                        if match:
                            filename = match.group(1)
                            target_file = OUTPUT_DIR / filename
                            size_bytes = target_file.stat().st_size if target_file.is_file() else 0
                            return f"event: file\ndata: {json.dumps({'filename': filename, 'download_url': f'/api/v1/files/{filename}', 'size_bytes': size_bytes})}\n\n"
                        return None

                    # อ่านคำตอบทีละบรรทัดจาก stdout แบบ Streaming
                    async for raw_line in process.stdout:
                        line = raw_line.decode("utf-8", errors="replace").strip()
                        if not line:
                            continue

                        try:
                            data = json.loads(line)
                            if data.get("type") == "token" or "delta" in data:
                                text_chunk = data.get("delta") or data.get("content", "")
                                artifact_event = check_artifact(text_chunk)
                                if artifact_event:
                                    yield artifact_event
                                yield f"event: token\ndata: {json.dumps({'delta': text_chunk})}\n\n"
                            elif data.get("type") == "status":
                                yield f"event: status\ndata: {json.dumps({'text': data.get('message', '')})}\n\n"
                            else:
                                artifact_event = check_artifact(line)
                                if artifact_event:
                                    yield artifact_event
                                yield f"event: token\ndata: {json.dumps({'delta': line})}\n\n"
                        except json.JSONDecodeError:
                            artifact_event = check_artifact(line)
                            if artifact_event:
                                yield artifact_event
                            yield f"event: token\ndata: {json.dumps({'delta': line})}\n\n"

                    # รอ process ทำงานเสร็จ
                    await process.wait()

                    if process.returncode != 0:
                        yield f"event: error\ndata: {json.dumps({'message': 'กระบวนการวิเคราะห์ขัดข้อง ไม่สามารถประมวลผลต่อได้'})}\n\n"
                    else:
                        yield f"event: done\ndata: {json.dumps({'status': 'completed'})}\n\n"

        except (TimeoutError, asyncio.CancelledError):
            yield f"event: error\ndata: {json.dumps({'message': 'เซิร์ฟเวอร์กำลังให้บริการเต็ม หรือการประมวลผลหมดเวลา'})}\n\n"
        except Exception as e:
            # ป้องกันการพ่น Internal System Path หรือ Stack Trace ให้ Client เห็น
            yield f"event: error\ndata: {json.dumps({'message': 'เกิดข้อผิดพลาดภายในระบบ'})}\n\n"
        finally:
            # Zombie Process Reaper: รับประกันการฆ่า Subprocess ไม่ให้ตกค้างเป็น Process ผีในเครื่อง
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

@app.get("/api/v1/files/{filename}")
async def download_file_endpoint(
    filename: str,
    authorization: str = Header(None)
):
    """ให้บริการดาวน์โหลดไฟล์ผลลัพธ์ (.md) ที่ Core Agent บันทึกไว้ พร้อมระบบป้องกัน Directory Traversal ขั้นสูงสุด"""
    await verify_auth(authorization)

    # 1. Regex Whitelist ป้องกัน Path Traversal, Null Bytes, และ Windows Alternate Data Streams (ADS)
    if not re.match(r"^[a-zA-Z0-9_\-\u0E00-\u0E7F]+\.md$", filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ชื่อไฟล์ไม่ถูกต้อง อนุญาตเฉพาะอักขระมาตรฐานและนามสกุล .md เท่านั้น"
        )

    # 2. Canonical Confinement Check (รับประกัน 100% ว่าไฟล์ต้องอยู่ใต้ไดเรกทอรี OUTPUT_DIR จริงๆ ป้องกัน Symlink Attack)
    file_path = (OUTPUT_DIR / filename).resolve()
    if not file_path.is_relative_to(OUTPUT_DIR.resolve()) or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ไม่พบไฟล์เอกสารที่ร้องขอ"
        )

    # 3. ส่งไฟล์กลับให้ Mobile Client บันทึกและประมวลผลต่อ
    return FileResponse(
        path=str(file_path),
        media_type="text/markdown; charset=utf-8",
        filename=filename,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Content-Type-Options": "nosniff"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)