# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE chat_messages (id TEXT PRIMARY KEY, session_id TEXT, role TEXT, content TEXT, status TEXT, timestamp INTEGER)")
conn.execute("CREATE VIRTUAL TABLE chat_messages_fts USING fts5(message_id UNINDEXED, session_id UNINDEXED, content, tokenize='unicode61')")
conn.execute("""
    CREATE TRIGGER trg_msg_ai AFTER INSERT ON chat_messages BEGIN
        INSERT INTO chat_messages_fts(message_id, session_id, content) VALUES (new.id, new.session_id, new.content);
    END;
""")

conn.execute("INSERT INTO chat_messages VALUES ('m1', 's1', 'model', 'คำพิพากษาศาลฎีกา 1234/2565 ข้อหา ฉ้อโกง มาตรา 341', 'completed', 1000)")
conn.commit()

row = conn.execute("SELECT m.content FROM chat_messages m JOIN chat_messages_fts fts ON m.id = fts.message_id WHERE chat_messages_fts MATCH 'ฉ้อโกง*'").fetchone()
print(f"Match result: {row}")
conn.close()
