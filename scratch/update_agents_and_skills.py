# -*- coding: utf-8 -*-
import os

repo_root = r"c:\Ai_code\THLawDeka-mobile"
agents_md_path = os.path.join(repo_root, "AGENTS.md")
backend_skill_path = os.path.join(repo_root, ".agents", "skills", "backend-development", "SKILL.md")
frontend_skill_path = os.path.join(repo_root, ".agents", "skills", "frontend-development", "SKILL.md")

# 1. Update AGENTS.md
with open(agents_md_path, "r", encoding="utf-8") as f:
    agents_text = f.read()

target_backend_guard = "Enforce performance optimizations: SQLite WAL mode, in-memory Bearer token cache ($O(1)$ lookup), and Fast-Path Legal Cache (`legal_cache` table) with SHA-256 query hash replay. Default to Implementation-Only Mode (verify via `python -m py_compile`)."
replacement_backend_guard = target_backend_guard + " Enforce Zero-PII Audit Logging (never log client query or response text to disk). Enforce Per-Key Rate Limiting (10 req/min per key with HTTP 429). Implement Automated SQLite Backup (`backup_db` with 7-day retention). Implement Long-Context Window Budgeting (emit SSE advisory on >64KB context recommending `/compact`)."

assert target_backend_guard in agents_text, "Could not find target_backend_guard in AGENTS.md"
agents_text = agents_text.replace(target_backend_guard, replacement_backend_guard, 1)

target_frontend_guard = "Render Mermaid charts in local sandboxed WebView with bundled `mermaid.min.js`. Implement 100% Client-Side Local Export (`DocumentExportManager.kt`):"
replacement_frontend_guard = "Render Mermaid charts in local sandboxed WebView with bundled `mermaid.min.js`. Implement SQLite FTS5 Full-Text Search for offline legal queries across saved messages. Implement Partial Stream Recovery (`continueInterruptedStream`) allowing users to resume interrupted queries seamlessly. Implement 100% Client-Side Local Export (`DocumentExportManager.kt`):"

assert target_frontend_guard in agents_text, "Could not find target_frontend_guard in AGENTS.md"
agents_text = agents_text.replace(target_frontend_guard, replacement_frontend_guard, 1)

with open(agents_md_path, "w", encoding="utf-8") as f:
    f.write(agents_text)
print("Updated AGENTS.md successfully.")

# 2. Update backend SKILL.md
with open(backend_skill_path, "r", encoding="utf-8") as f:
    backend_skill = f.read()

module_9_backend = """### Module 9: Zero-PII Audit, Per-Key Rate Limiting, Automated Backup & Context Budgeting
- **Zero-PII Audit Logging**: Log only telemetry JSON `{timestamp, endpoint, key_prefix, query_bytes, duration_ms, status}`. NEVER log raw client queries or responses to disk logs.
- **Per-Key Rate Limiting**: Limit to 10 requests / 60 seconds per key in RAM ($O(1)$). Return HTTP 429 Too Many Requests with `Retry-After: 60`.
- **Automated SQLite Backup**: Implement `backup_db(backup_dir, max_keep=7)` using `conn.backup(dest_conn)` for non-blocking online backup with 7-day retention.
- **Long-Context Budgeting**: If context exceeds 64KB, emit SSE `event: advisory` recommending `/compact` or starting a new session.

"""

target_backend_skill_end = "### Module 8: Performance & Latency Optimization (`backend/main.py` & `backend/auth_db.py`)"
assert target_backend_skill_end in backend_skill, "Could not find Module 8 in backend skill"
pos = backend_skill.find("\n## 2. Backend Verification Checklist")
assert pos != -1, "Could not find Section 2 in backend skill"
backend_skill = backend_skill[:pos] + "\n" + module_9_backend + backend_skill[pos:]

with open(backend_skill_path, "w", encoding="utf-8") as f:
    f.write(backend_skill)
print("Updated backend SKILL.md successfully.")

# 3. Update frontend SKILL.md
with open(frontend_skill_path, "r", encoding="utf-8") as f:
    frontend_skill = f.read()

module_8_frontend = """### Module 8: Offline FTS5 Full-Text Search & Partial Stream Recovery
- **Offline SQLite FTS5**: Enable `chat_messages_fts USING fts5(message_id UNINDEXED, session_id UNINDEXED, content, tokenize='unicode61')` in `ChatDatabaseHelper.kt` for instant offline keyword search across saved court precedents.
- **Partial Stream Recovery**: On premature connection drop, save accumulated tokens with `interrupted` status. Expose `continueInterruptedStream` to resume analysis without starting over.

"""

pos_front = frontend_skill.find("\n## 2. Mobile Verification Checklist")
assert pos_front != -1, "Could not find Section 2 in frontend skill"
frontend_skill = frontend_skill[:pos_front] + "\n" + module_8_frontend + frontend_skill[pos_front:]

with open(frontend_skill_path, "w", encoding="utf-8") as f:
    f.write(frontend_skill)
print("Updated frontend SKILL.md successfully.")
