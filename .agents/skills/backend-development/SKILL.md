---
name: backend-development
description: >-
  Backend engineering procedures for THLawDeka-mobile FastAPI ASGI Gateway, Server-Sent Events (SSE) streaming, Subprocess Pipe Controller with safe stdin/stdout, SQLite key management, and Admin Web UI.
---

# Backend Development Skill (THLawDeka-mobile Gateway)

Provides engineering standards, code structure guidelines, and token-optimized implementation workflows for Senior Backend Engineers implementing the **THLawDeka-mobile** FastAPI Gateway.

---

## ⚡ Token Optimization Note (Implementation-Only Mode)
By default, backend engineers operate in **Implementation-Only Mode**:
- Do not write, execute, or read unit test files (`test_*.py`, `tests/`) unless explicitly requested by the user (`"write test"`, `"unit test"`, etc.).
- Rely on Pydantic V2 schema validation and static syntax checks (`py_compile`, `ruff check`, `mypy --quick`) for deterministic baseline correctness.

---

## 📚 Scanned Skills & Playbooks Reference
When implementing async and security components, refer to the bundled playbooks:
- [FastAPI Pro Guidelines](references/fastapi-patterns.md) (Async endpoints, Pydantic V2, StreamingResponse, Middleware)
- [Async Python & Subprocess Playbook](references/async-subprocess-patterns.md) (Subprocess pipes, asyncio.gather, timeouts, Zombie Reaper)
- [AI Security Hardening Guide](references/ai-security-hardening.md) (Null-byte stripping, prompt injection heuristics, safe execution boundaries)

---

## 1. Core Modules & Implementation Workflows

### Module 0: Environment Setup & uv Runner (`backend/`)
- **Recommended Runner (`uv`)**:
  - Create venv & install: `uv venv && uv pip install -r requirements.txt`.
  - Run server directly: `uv run uvicorn main:app --host 127.0.0.1 --port 8000`.
  - Bypasses Windows PowerShell script execution policy (`Activate.ps1`) restrictions.
- **Fallback Runner**: `python -m venv .venv` and `pip install -r requirements.txt`.

### Module 1: Gateway Server & SSE Streaming (`backend/main.py`)
- **FastAPI ASGI Server** with CORS and Jinja2Templates.
- **Streaming Endpoint (`POST /api/v1/chat/stream`)**:
  - Validates `Authorization: Bearer <key_token>` against `auth_db.py`.
  - Enforces `asyncio.Semaphore(3)` for concurrency rate control.
  - Returns `StreamingResponse(stream_generator(), media_type="text/event-stream")`.
  - Sets anti-buffering headers:
    - `Cache-Control: no-cache`
    - `X-Accel-Buffering: no`
    - `Connection: keep-alive`
- **SSE Protocol Formatting**:
  - `event: status\ndata: {"text": "..."}\n\n`
  - `event: token\ndata: {"delta": "..."}\n\n`
  - `event: done\ndata: {"status": "completed", "conversation_id": "..."}\n\n`
  - `event: error\ndata: {"code": 500, "message": "..."}\n\n`

### Module 2: Subprocess Pipe Controller (`backend/main.py`)
- **Execution Mode**: `asyncio.create_subprocess_exec` with `shell=False` (never invoke shell interpreter).
- **CLI Flag Injection Prevention**:
  - Strictly validate `conversation_id` against `^[a-zA-Z0-9][a-zA-Z0-9_\-]{0,63}$` (must start with alphanumeric, never leading `-` or `--`).
- **Environment Isolation**:
  - Pass sanitized `safe_env` to `create_subprocess_exec` (strip `ADMIN_SECRET` and API keys to prevent secret dumping).
- **Safe Stdin/Stdout Boundary**:
  - Spawn `agy.exe` with arguments:
    `["agy", "-p", "-", "--sandbox", "--dangerously-skip-permissions", "--input-format", "text", "--output-format", "stream-json", "--print-timeout", "60s"]`
  - Pipe query text through `process.stdin.write(query.encode("utf-8"))` followed by `process.stdin.drain()` and `process.stdin.close()`.
  - Read lines from `process.stdout` asynchronously, parsing NDJSON frames and yielding SSE events.
- **Zombie Reaper & Timeout**:
  - Wrap process execution with `asyncio.wait_for(timeout=65.0)`.
  - On timeout or client disconnect (`asyncio.CancelledError`), trigger immediate `process.kill()` to prevent dangling zombie processes.

### Module 3: Security Shield & Input Sanitization
- **Payload Size**: Reject queries > 32 KB immediately with HTTP `413 Payload Too Large`.
- **Null-Byte Sanitization**: Strip `\x00` null bytes using regex `re.sub(r'[\x00]', '', query)`.
- **Gateway Pre-Filter (Anti-Tamper & Injection Shield)**:
  - Validate incoming prompts using `INJECTION_BLACKLIST_PATTERNS` to catch override attempts ("ignore instructions", "system prompt", "DAN"), harness tampering ("modify AGENTS.md", "delete rules"), and OS command/script executions ("powershell", "bash", "curl", "rm -rf", "cat /etc/").
  - Immediately reject tampering attempts with HTTP `400 Bad Request` without invoking `agy` or consuming tokens.
- **Physical OS Lockdown Guideline**:
  - Advise setting OS permissions on `harness/`, `backend/`, and `THLawDeka/AGENTS.md` to Read-Only (`chmod 555` / `icacls /deny Everyone:(WD,AD)`), with the entire workspace being 100% Immutable Read-Only (Server-Side Zero-Disk-Write Policy).

### Module 4: Authentication & Key Management (`backend/auth_db.py` & `backend/manage_keys.py`)
- **Database (`backend/keys.db`)**: SQLite table `api_keys`:
  - `id INTEGER PRIMARY KEY`
  - `key_token TEXT UNIQUE NOT NULL` (`thlaw_live_<hex32>`)
  - `user_name TEXT NOT NULL`
  - `is_active INTEGER DEFAULT 1`
  - `created_at TIMESTAMP`
  - `revoked_at TIMESTAMP NULL`
- Methods: `validate_key(token) -> bool`, `create_key(user_name) -> str`, `revoke_key(token) -> bool`, `list_keys() -> list`.
- **CLI Utility (`backend/manage_keys.py`)**: Subcommands `add`, `revoke`, `list` for terminal management.

### Module 5: Admin Web UI (`backend/templates/admin.html`) & Tailscale Funnel Shielding
- Served at `GET /admin` via Jinja2 template.
- Protected by master `ADMIN_SECRET` environment variable.
- **Tailscale Funnel Admin Shielding**: When Tailscale Funnel is enabled to allow public Android clients to stream, restrict `/admin` and `/api/v1/admin/*` to Localhost (`127.0.0.1`) and Tailnet IPs (`100.64.0.0/10`) unless `ALLOW_PUBLIC_ADMIN=true`.
- Features: View all issued keys, single-click copy key, Instant Revoke button, and Generate New Key modal.

### Module 6: Server-Side Zero-Disk-Write & Gzip Compressed Markdown Streaming (`backend/main.py`)
- **Server-Side Zero-Disk-Write Policy**:
  - The server strictly enforces Read-Only operation for client requests. Under NO circumstances does the server create, modify, or delete files on the server disk for user requests.
  - No client-directed file creation in `output/` and no `/api/v1/files/` download endpoint on the server.
  - Completely eliminates server-side file write vulnerabilities, directory traversal, Alternate Data Streams (ADS), and disk exhaustion.
- **Gzip Compressed Markdown Streaming**:
  - Integrate Gzip compression on SSE stream (`Content-Encoding: gzip`).
  - Achieves ~70–85% bandwidth reduction over Tailscale WireGuard mesh for Thai legal text, GFM tables, and Mermaid blocks.
  - Emits pure Markdown text stream chunks (`event: token`) directly to the client.

### Module 7: Daemon & Auto-Start Service (`backend/`)
- **Windows**: Deploy `backend/start_gateway.bat` + `backend/run_hidden.vbs` via Task Scheduler (`setup_autostart_windows.ps1`) for headless auto-start on logon.
- **Linux**: Deploy `backend/thlaw-gateway.service` to `/etc/systemd/system/` with `Restart=always` and `systemctl enable --now thlaw-gateway`.
- **Tailscale Serve & Funnel Persistence**: Ensure Tailscale serves with `--bg` (`tailscale serve --bg https / http://127.0.0.1:8000`) and Funnel with `--bg` (`tailscale funnel --bg 443 on`) so proxying survives reboot without manual intervention.

### Module 8: Performance & Latency Optimization (`backend/main.py` & `backend/auth_db.py`)
- **SQLite WAL Mode**:
  - Invoke `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;` in `AuthDB._get_connection()`.
  - Enables concurrent non-blocking reads while writing keys or cache entries.
- **In-Memory Bearer Token Cache**:
  - Maintain `ACTIVE_KEYS_CACHE = set()` loaded at startup and updated on key creation/revocation.
  - Grants $O(1)$ token verification without reading the SQLite file on every HTTP request.
- **Fast-Path Legal Cache**:
  - Maintain `legal_cache` table in `keys.db` (SHA-256 normalized query hash -> JSON SSE events array).
  - Bypass cache if `conversation_id` is present (ensuring tailored multi-turn context).
  - On Cache Hit: replay events with 5ms delays per chunk (reduces response time from 8s to <5ms).
  - On Stream Completion: save full event sequence with 24h TTL.

---

### Module 9: Zero-PII Audit, Per-Key Rate Limiting, Automated Backup & Context Budgeting
- **Zero-PII Audit Logging**: Log only telemetry JSON `{timestamp, endpoint, key_prefix, query_bytes, duration_ms, status}`. NEVER log raw client queries or responses to disk logs.
- **Per-Key Rate Limiting**: Limit to 10 requests / 60 seconds per key in RAM ($O(1)$). Return HTTP 429 Too Many Requests with `Retry-After: 60`.
- **Automated SQLite Backup**: Implement `backup_db(backup_dir, max_keep=7)` using `conn.backup(dest_conn)` for non-blocking online backup with 7-day retention.
- **Long-Context Budgeting**: If context exceeds 64KB, emit SSE `event: advisory` recommending `/compact` or starting a new session.


## 2. Backend Verification Checklist
Before completing backend implementation tasks, verify:
- [ ] Dependencies declared in `backend/requirements.txt` (`fastapi`, `uvicorn[standard]`, `pydantic`, `python-multipart`, `jinja2`).
- [ ] Subprocess executes with `shell=False` and query passed via `stdin` only.
- [ ] CLI Flag Injection prevented: `conversation_id` validated with `^[a-zA-Z0-9][a-zA-Z0-9_\-]{0,63}$`.
- [ ] Gateway Pre-Filter checks for prompt injection, harness tampering, and shell patterns before invoking subprocess.
- [ ] Environment isolated: `safe_env` passed without `ADMIN_SECRET`.
- [ ] Zombie reaper handles process termination on timeout or cancellation.
- [ ] Server-Side Zero-Disk-Write Policy enforced: zero server files written or stored for client queries.
- [ ] Gzip compression configured on Markdown stream (`Content-Encoding: gzip`) for bandwidth optimization.
- [ ] Auto-start scripts verified: `start_gateway.bat`, `run_hidden.vbs`, and `thlaw-gateway.service` exist in `backend/`.
- [ ] SQLite WAL mode and in-memory bearer token cache implemented for sub-millisecond auth.
- [ ] Fast-Path Legal Cache configured with SHA-256 query hash and 24h TTL replay.
- [ ] Python syntax compiles without errors (`python -m py_compile backend/main.py`).
- [ ] Strict Zero-Test Policy observed: unit tests run ONLY if explicitly requested by user prompt.
- [ ] No local secret keys or absolute paths hardcoded.
---

### Module 10: Multi-Model Discovery & Security Whitelist (`GET /api/v1/models`)

1. **Supported Model Whitelist**:
   - `gemini-3.8-flash-high` (Default, Fast, High Accuracy)
   - `gemini-3.8-flash-medium` (Fast, Balanced)
   - `gemini-3.8-flash-low` (Eco, Token-Saver)
   - `claude-sonnet-4-6` (Thinking, Deep Reasoning, Legal Analysis)
   - `claude-opus-4-6-thinking` (Thinking, Top Intelligence, High-Complexity Cases)
   - `gpt-oss-120b-medium` (Open Weights, Comparative Law)

2. **Security & Injection Guardrail**:
   - Validate model input with regex: `^[a-zA-Z0-9][a-zA-Z0-9._\-]{0,63}$`
   - Hard Reject any input not in `VALID_MODELS`
   - Pass safely to subprocess: `cmd.extend(["--model", req.model])` with `shell=False`
