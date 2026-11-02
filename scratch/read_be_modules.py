import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open(".agents/skills/backend-development/SKILL.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'### Module \d+.*', text)
for m in matches:
    print(m)
