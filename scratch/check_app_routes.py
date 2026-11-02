import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r'@app\.\w+\([^)]+\)', text)
for m in matches:
    print(m)
