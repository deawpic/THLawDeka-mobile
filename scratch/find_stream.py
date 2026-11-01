# -*- coding: utf-8 -*-
spec_path = r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md"
with open(spec_path, "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("def stream_chat")
if pos != -1:
    print(repr(text[pos:pos+400]))
else:
    print("def stream_chat not found")
