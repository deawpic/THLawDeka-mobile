# -*- coding: utf-8 -*-
path = r"c:\Ai_code\THLawDeka-mobile\.agents\skills\frontend-development\SKILL.md"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

module_8 = """### Module 8: Offline FTS5 Full-Text Search & Partial Stream Recovery
- **Offline SQLite FTS5**: Enable `chat_messages_fts USING fts5(message_id UNINDEXED, session_id UNINDEXED, content, tokenize='unicode61')` in `ChatDatabaseHelper.kt` for instant offline keyword search across saved court precedents.
- **Partial Stream Recovery**: On premature connection drop, save accumulated tokens with `interrupted` status. Expose `continueInterruptedStream` to resume analysis without starting over.

"""

pos = text.find("## 2. Android Verification Checklist")
if pos != -1:
    text = text[:pos] + module_8 + text[pos:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Frontend skill updated with Module 8.")
else:
    print("Checkpoint not found in frontend skill.")
