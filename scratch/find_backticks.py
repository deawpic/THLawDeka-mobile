import sys
import re
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

matches = re.finditer(r"````|```mermaid", content)
for m in matches:
    start = max(0, m.start() - 30)
    end = min(len(content), m.end() + 30)
    snippet = content[start:end].replace("\n", "\\n")
    print(f"Pos {m.start()}: {snippet}")
