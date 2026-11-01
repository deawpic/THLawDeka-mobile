# -*- coding: utf-8 -*-
spec_path = r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md"
with open(spec_path, "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("class ChatDatabaseHelper")
if pos != -1:
    end_pos = text.find("class ChatSessionRepository", pos)
    print(repr(text[pos+800:end_pos]))
