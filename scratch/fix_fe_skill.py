from pathlib import Path

frontend_skill_path = Path(r"c:\Ai_code\THLawDeka-mobile\.agents\skills\frontend-development\SKILL.md")
content = frontend_skill_path.read_text(encoding="utf-8")

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

target = "---\n\n## 2. Android Verification Checklist"
if target in content:
    content = content.replace(target, mod7_fe_text + target)
    print("Inserted Module 7 into frontend-development/SKILL.md")

# Add checklist item
chk_target = "- [ ] Thai text views configured with `breakStrategy=\"high_quality\"`."
new_chk = """- [ ] Thai text views configured with `breakStrategy=\"high_quality\"`.
- [ ] Stream Token Batching Buffer (50ms) implemented to eliminate UI jank during high-throughput SSE.
- [ ] SQLite WAL mode (`enableWriteAheadLogging()`) and RAM-based stream batch write enabled."""

if chk_target in content:
    content = content.replace(chk_target, new_chk)
    print("Added checklist items.")

frontend_skill_path.write_text(content, encoding="utf-8")
print("Saved frontend-development/SKILL.md!")
