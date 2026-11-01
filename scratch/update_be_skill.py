import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(".agents/skills/backend-development/SKILL.md")
content = p.read_text(encoding="utf-8")

old_mod6 = """### Module 6: Artifact Handshake & File Download (`backend/main.py`)
- **Real-Time Stream Interceptor**:
  - Regular expression `<!--\\s*ARTIFACT:\\s*output/([a-zA-Z0-9_\\-\\.\\u0E00-\\u0E7F]+)\\s*-->` scans tokens/chunks from `process.stdout`.
  - When detected, checks file existence and size in `OUTPUT_DIR = Path(WORKSPACE_DIR) / "output"`.
  - Immediately emits `event: file\\ndata: {"filename": "...", "download_url": "/api/v1/files/...", "size_bytes": ...}\\n\\n`.
- **Secure File Serving Endpoint (`GET /api/v1/files/{filename}`)**:
  - Enforces `Authorization: Bearer <key>` authenticated against `keys.db`.
  - Path traversal defense: Strict regex whitelist `^[a-zA-Z0-9_\\-\\u0E00-\\u0E7F]+\\.md$` (rejects `/`, `\\`, `..`, `:`, `%00`).
  - Canonical Confinement: Enforce `(OUTPUT_DIR / filename).resolve().is_relative_to(OUTPUT_DIR.resolve())`.
  - Serves file via `FileResponse` with `media_type="text/markdown; charset=utf-8"` and `Content-Disposition: attachment`."""

new_mod6 = """### Module 6: Server-Side Zero-Disk-Write & Gzip Compressed Markdown Streaming (`backend/main.py`)
- **Server-Side Zero-Disk-Write Policy**:
  - The server strictly enforces Read-Only operation for client requests. Under NO circumstances does the server create, modify, or delete files on the server disk for user requests.
  - No client-directed file creation in `output/` and no `/api/v1/files/` download endpoint on the server.
  - Completely eliminates server-side file write vulnerabilities, directory traversal, Alternate Data Streams (ADS), and disk exhaustion.
- **Gzip Compressed Markdown Streaming**:
  - Integrate Gzip compression on SSE stream (`Content-Encoding: gzip`).
  - Achieves ~70–85% bandwidth reduction over Tailscale WireGuard mesh for Thai legal text, GFM tables, and Mermaid blocks.
  - Emits pure Markdown text stream chunks (`event: token`) directly to the client."""

old_chk = """- [ ] Artifact Handshake regex detects `<!-- ARTIFACT: output/<filename>.md -->` and emits `event: file`.
- [ ] `GET /api/v1/files/{filename}` strictly validated with Regex Whitelist and `is_relative_to` path confinement."""

new_chk = """- [ ] Server-Side Zero-Disk-Write Policy enforced: zero server files written or stored for client queries.
- [ ] Gzip compression configured on Markdown stream (`Content-Encoding: gzip`) for bandwidth optimization."""

assert old_mod6 in content, "old_mod6 not found"
assert old_chk in content, "old_chk not found"

content = content.replace(old_mod6, new_mod6)
content = content.replace(old_chk, new_chk)

p.write_text(content, encoding="utf-8")
print("Updated .agents/skills/backend-development/SKILL.md successfully!")
