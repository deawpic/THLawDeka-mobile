import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Update software-architecture/SKILL.md
p_arch = Path(".agents/skills/software-architecture/SKILL.md")
content_arch = p_arch.read_text(encoding="utf-8")

old_arch_block = """- **SSE Stream Contract (`POST /api/v1/chat/stream`)**:
  - Request Body: `{"query": "string", "conversation_id": "string | null"}` (Supports continuing previous chat)
  - `status`: Progress updates (`{"text": "..."}`)
  - `token`: Incremental answer text (`{"delta": "..."}`)
  - `file`: Artifact delivery notification (`{"filename": "...", "download_url": "/api/v1/files/...", "size_bytes": int}`)
  - `done`: Finalization (`{"status": "completed", "conversation_id": "..."}`)
  - `error`: Error envelope (`{"code": int, "message": "..."}`)
- **File Download Contract (`GET /api/v1/files/{filename}`)**:
  - Request: Header `Authorization: Bearer <token>`
  - Path traversal defense: `os.path.basename(filename)`, whitelisted `.md` extension
  - Response: `FileResponse` with `Content-Disposition: attachment; filename="..."`"""

new_arch_block = """- **SSE Stream Contract (`POST /api/v1/chat/stream`)**:
  - Request Header: `Accept-Encoding: gzip`
  - Request Body: `{"query": "string", "conversation_id": "string | null"}` (Supports continuing previous chat)
  - Response Header: `Content-Encoding: gzip` (SSE compressed stream reducing bandwidth by ~70-85%)
  - `status`: Progress updates (`{"text": "..."}`)
  - `token`: Incremental answer text (`{"delta": "..."}`)
  - `done`: Finalization (`{"status": "completed", "conversation_id": "..."}`)
  - `error`: Error envelope (`{"code": int, "message": "..."}`)
- **Server-Side Zero-Disk-Write Contract**:
  - Strictly enforces Read-Only operation: no client requests can create, write, or delete files on server disk.
  - 100% On-Device Local Export on Android Client: export to `.md`, `.pdf` (via A4 Sarabun `PrintManager`), and `.txt` locally."""

assert old_arch_block in content_arch, "old_arch_block not found"
content_arch = content_arch.replace(old_arch_block, new_arch_block)
p_arch.write_text(content_arch, encoding="utf-8")
print("Updated .agents/skills/software-architecture/SKILL.md successfully!")

# 2. Update product-management/SKILL.md
p_pm = Path(".agents/skills/product-management/SKILL.md")
content_pm = p_pm.read_text(encoding="utf-8")

old_pm_story1 = """  - *Given* user requests saving legal analysis to a file, *When* Core Agent writes to `output/<filename>.md` and emits artifact tag `<!-- ARTIFACT: output/<filename>.md -->`, *Then* Gateway intercepts the tag, fires SSE `event: file`, and Android app downloads `.md` via `GET /api/v1/files/{filename}` with Bearer auth for preview and PDF export."""
new_pm_story1 = """  - *Given* user requests saving legal analysis to a file, *When* Core Agent processes the request, *Then* it strictly enforces Server-Side Zero-Disk-Write Policy, streams the full Markdown answer directly through Gzip compression, and guides the user to export as `.md`, `.pdf`, or `.txt` directly on the Android app."""

old_pm_story2 = """  - *Given* user asks to save in formats other than .md (.pdf, .docx, .txt), *When* Core Agent processes the request, *Then* it soft-rejects by saving as .md and guiding user to use app PDF Export or Word, and hard-rejects scripts/system files without writing files."""
new_pm_story2 = """  - *Given* user asks to save files on the server or in unsafe formats, *When* Core Agent processes the request, *Then* it responds with the complete legal analysis in pure Markdown without server file creation, and informs user to use local on-device export."""

old_pm_story3 = """  - *Given* downloaded .md or generated PDF, *When* user taps Share, *Then* app launches Android Share Sheet via FileProvider to send files to LINE, Email, or Google Drive."""
new_pm_story3 = """  - *Given* locally exported .md, .pdf, or .txt file, *When* user taps Share, *Then* app launches Android Share Sheet via FileProvider to send files to LINE, Email, or Google Drive."""

assert old_pm_story1 in content_pm, "old_pm_story1 not found"
assert old_pm_story2 in content_pm, "old_pm_story2 not found"
assert old_pm_story3 in content_pm, "old_pm_story3 not found"

content_pm = content_pm.replace(old_pm_story1, new_pm_story1)
content_pm = content_pm.replace(old_pm_story2, new_pm_story2)
content_pm = content_pm.replace(old_pm_story3, new_pm_story3)
p_pm.write_text(content_pm, encoding="utf-8")
print("Updated .agents/skills/product-management/SKILL.md successfully!")
