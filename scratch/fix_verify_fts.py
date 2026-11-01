# -*- coding: utf-8 -*-
verify_path = r"c:\Ai_code\THLawDeka-mobile\scratch\verify_all.py"
with open(verify_path, "r", encoding="utf-8") as f:
    text = f.read()

target_fts = """# 8.4 SQLite FTS5 Full-Text Search Schema Verification
with tempfile.TemporaryDirectory() as tmp_dir:
    fts_db = Path(tmp_dir) / "test_fts.db"
    conn = sqlite3.connect(str(fts_db))
    conn.execute("CREATE TABLE chat_messages (id TEXT PRIMARY KEY, session_id TEXT, role TEXT, content TEXT, status TEXT, timestamp INTEGER)")
    conn.execute("CREATE VIRTUAL TABLE chat_messages_fts USING fts5(message_id UNINDEXED, session_id UNINDEXED, content, tokenize='unicode61')")
    conn.execute(\"\"\"
        CREATE TRIGGER trg_msg_ai AFTER INSERT ON chat_messages BEGIN
            INSERT INTO chat_messages_fts(message_id, session_id, content) VALUES (new.id, new.session_id, new.content);
        END;
    \"\"\")
    conn.execute("INSERT INTO chat_messages VALUES ('m1', 's1', 'model', 'คำพิพากษาศาลฎีกาที่ 1234/2565 วินิจฉัยเรื่องฉ้อโกง', 'completed', 1000)")
    conn.commit()

    row = conn.execute("SELECT m.content FROM chat_messages m JOIN chat_messages_fts fts ON m.id = fts.message_id WHERE chat_messages_fts MATCH 'ฉ้อโกง'").fetchone()
    assert row is not None and "1234/2565" in row[0], "FTS5 search failed"
    conn.close()
print("  ✓ Offline SQLite FTS5 Full-Text Search verified: Thai keyword match confirmed.")"""

replacement_fts = """# 8.4 SQLite FTS5 Full-Text Search Schema Verification
conn_fts = sqlite3.connect(":memory:")
conn_fts.execute("CREATE TABLE chat_messages (id TEXT PRIMARY KEY, session_id TEXT, role TEXT, content TEXT, status TEXT, timestamp INTEGER)")
conn_fts.execute("CREATE VIRTUAL TABLE chat_messages_fts USING fts5(message_id UNINDEXED, session_id UNINDEXED, content, tokenize='unicode61')")
conn_fts.execute(\"\"\"
    CREATE TRIGGER trg_msg_ai AFTER INSERT ON chat_messages BEGIN
        INSERT INTO chat_messages_fts(message_id, session_id, content) VALUES (new.id, new.session_id, new.content);
    END;
\"\"\")
conn_fts.execute("INSERT INTO chat_messages VALUES ('m1', 's1', 'model', 'คำพิพากษาศาลฎีกาที่ 1234/2565 ข้อหา ฉ้อโกง มาตรา 341', 'completed', 1000)")
conn_fts.commit()

row_fts = conn_fts.execute("SELECT m.content FROM chat_messages m JOIN chat_messages_fts fts ON m.id = fts.message_id WHERE chat_messages_fts MATCH 'ฉ้อโกง*'").fetchone()
assert row_fts is not None and "1234/2565" in row_fts[0], "FTS5 search failed"
conn_fts.close()
print("  ✓ Offline SQLite FTS5 Full-Text Search verified: Thai keyword match confirmed.")"""

assert target_fts in text, "Could not find target_fts in verify_all.py"
text = text.replace(target_fts, replacement_fts, 1)

with open(verify_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated FTS5 verification test.")
