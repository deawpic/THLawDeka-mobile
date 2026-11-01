from pathlib import Path

# 1. Update backend-development/SKILL.md
backend_skill_path = Path(r"c:\Ai_code\THLawDeka-mobile\.agents\skills\backend-development\SKILL.md")
backend_content = backend_skill_path.read_text(encoding="utf-8")

mod8_text = """### Module 8: Performance & Latency Optimization (`backend/main.py` & `backend/auth_db.py`)
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

"""

if "### Module 8: Performance & Latency Optimization" not in backend_content:
    backend_content = backend_content.replace("--- \n\n## 2. Backend Verification Checklist", mod8_text + "---\n\n## 2. Backend Verification Checklist")
    backend_content = backend_content.replace("---\n\n## 2. Backend Verification Checklist", mod8_text + "---\n\n## 2. Backend Verification Checklist")
    
    # Also add checklist items
    chk_target = "- [ ] Python syntax compiles without errors (`python -m py_compile backend/main.py`)."
    new_chk = """- [ ] SQLite WAL mode and in-memory bearer token cache implemented for sub-millisecond auth.
- [ ] Fast-Path Legal Cache configured with SHA-256 query hash and 24h TTL replay.
- [ ] Python syntax compiles without errors (`python -m py_compile backend/main.py`)."""
    if chk_target in backend_content:
        backend_content = backend_content.replace(chk_target, new_chk)
    
    backend_skill_path.write_text(backend_content, encoding="utf-8")
    print("Updated backend-development/SKILL.md successfully!")
else:
    print("backend-development/SKILL.md already has Module 8.")

# 2. Update frontend-development/SKILL.md
frontend_skill_path = Path(r"c:\Ai_code\THLawDeka-mobile\.agents\skills\frontend-development\SKILL.md")
frontend_content = frontend_skill_path.read_text(encoding="utf-8")

mod7_fe_text = """### Module 7: Performance & Latency Optimization (Android Client)
- **Stream Token Batching Buffer (50ms Throttler)**:
  - Do NOT recalculate Markwon Spannable layout on the Main Thread for every incoming SSE token.
  - Implement a Coroutine Throttling Buffer (`StreamTokenThrottler`) collecting tokens and flushing to the UI every 50–80 ms or on `\\n`.
  - Keeps UI rendering smoothly at 60–120 fps without frame drops.
- **SQLite WAL Mode & Batch Write**:
  - In `ChatDatabaseHelper.kt`, enable Write-Ahead Logging via `db.enableWriteAheadLogging()`.
  - Buffer message deltas in ViewModel RAM; persist to SQLite in batch upon `event: done`, `event: error`, or cancellation.
- **Mermaid WebView Lazy Loading**:
  - Defer initializing `MermaidRendererView` until a ```mermaid block is detected in the response text, saving 50–80 MB of RAM.

"""

if "### Module 7: Performance & Latency Optimization" not in frontend_content:
    fe_target = "---\n\n## 2. Mobile Verification Checklist"
    if fe_target in frontend_content:
        frontend_content = frontend_content.replace(fe_target, mod7_fe_text + fe_target)
    
    fe_chk_target = "- [ ] Markwon renders GFM tables and handles Thai line breaks with `breakStrategy=\"high_quality\"`."
    new_fe_chk = """- [ ] Stream Token Batching Buffer (50ms) implemented to eliminate UI jank during high-throughput SSE.
- [ ] SQLite WAL mode (`enableWriteAheadLogging()`) and RAM-based stream batch write enabled.
- [ ] Markwon renders GFM tables and handles Thai line breaks with `breakStrategy=\"high_quality\"`."""
    if fe_chk_target in frontend_content:
        frontend_content = frontend_content.replace(fe_chk_target, new_fe_chk)
        
    frontend_skill_path.write_text(frontend_content, encoding="utf-8")
    print("Updated frontend-development/SKILL.md successfully!")
else:
    print("frontend-development/SKILL.md already has Module 7.")
