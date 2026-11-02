import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [(m.start(), m.group()) for m in re.finditer(r'Zero-PII|Rate Limiting|SQLite Backup|Context Budgeting', text)]
for pos, match in matches[:10]:
    line_no = text[:pos].count('\n') + 1
    print(f"Line {line_no}: {match}")
