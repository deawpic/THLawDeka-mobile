import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
pos = text.find("@app.post(\"/api/chat/stream\")")
if pos != -1:
    print(text[pos:pos+1200])
else:
    pos = text.find("/api/chat/stream")
    print(text[pos:pos+1200])
