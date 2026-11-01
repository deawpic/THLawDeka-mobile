# -*- coding: utf-8 -*-
verify_path = r"c:\Ai_code\THLawDeka-mobile\scratch\verify_all.py"
with open(verify_path, "r", encoding="utf-8") as f:
    text = f.read()

target = "print(\"\\n[Step 8] Deterministic Zero-PII, Rate Limit, Backup, FTS5 & Context Assertions...\")"
pos = text.find(target)
if pos != -1:
    text = text[:pos] + "import time\n" + text[pos:]
    with open(verify_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Added import time to verify_all.py")
else:
    print("Target not found")
