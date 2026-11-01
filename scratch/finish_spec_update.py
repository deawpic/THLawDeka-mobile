# -*- coding: utf-8 -*-
spec_path = r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md"

with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

target_delete_session = """    // 5. ลบห้องแชต (Delete Chat Session and All Its Messages)
    fun deleteSession(sessionId: String): Boolean {
        val db = writableDatabase
        val deletedRows = db.delete(TABLE_SESSIONS, "$COL_SESSION_ID = ?", arrayOf(sessionId))
        return deletedRows > 0
    }
}"""

replacement_delete_session = """    // 5. ลบห้องแชต (Delete Chat Session and All Its Messages)
    fun deleteSession(sessionId: String): Boolean {
        val db = writableDatabase
        val deletedRows = db.delete(TABLE_SESSIONS, "$COL_SESSION_ID = ?", arrayOf(sessionId))
        return deletedRows > 0
    }

    /**
     * ค้นหาข้อความคำพิพากษาหรือตัวบทกฎหมายแบบ Full-Text Search (FTS5) ออฟไลน์ 100%
     */
    fun searchMessages(keyword: String): List<ChatMessage> {
        val results = mutableListOf<ChatMessage>()
        val db = readableDatabase
        val sanitizedQuery = keyword.replace("\"", "\"\"")
        val cursor = db.rawQuery(
            \"\"\"
            SELECT m.$COL_MSG_ID, m.$COL_MSG_SESSION_ID, m.$COL_MSG_ROLE, m.$COL_MSG_CONTENT, m.$COL_MSG_STATUS, m.$COL_MSG_TIMESTAMP
            FROM $TABLE_MESSAGES m
            JOIN chat_messages_fts fts ON m.$COL_MSG_ID = fts.message_id
            WHERE chat_messages_fts MATCH ?
            ORDER BY m.$COL_MSG_TIMESTAMP DESC
            \"\"\".trimIndent(),
            arrayOf("\"$sanitizedQuery\"*")
        )
        cursor.use { c ->
            while (c.moveToNext()) {
                results.add(
                    ChatMessage(
                        id = c.getString(0),
                        sessionId = c.getString(1),
                        role = c.getString(2),
                        content = c.getString(3),
                        status = c.getString(4),
                        timestamp = c.getLong(5)
                    )
                )
            }
        }
        return results
    }
}"""

if target_delete_session in content:
    content = content.replace(target_delete_session, replacement_delete_session, 1)
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("ChatDatabaseHelper.kt searchMessages added successfully.")
else:
    print("target_delete_session not matched or already present.")
