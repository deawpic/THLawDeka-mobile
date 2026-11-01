import sys
import re
import py_compile
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

main_match = re.search(r"### 4\.1 โค้ดฝั่ง Backend Gateway \(`backend/main\.py`\).*?```python\s*(.*?)\s*```", content, re.DOTALL)
assert main_match, "Failed to match main.py"
test_main = Path("scratch/test_extracted_main.py")
test_main.write_text(main_match.group(1), encoding="utf-8")
py_compile.compile(str(test_main), doraise=True)
print("Section 4.1 (main.py) compiles with 0 errors!")

authdb_match = re.search(r"### 4\.8 โค้ดฝั่ง Backend สำหรับฐานข้อมูลกุญแจ \(`backend/auth_db\.py`\).*?```python\s*(.*?)\s*```", content, re.DOTALL)
assert authdb_match, "Failed to match auth_db.py"
test_authdb = Path("scratch/test_extracted_authdb.py")
test_authdb.write_text(authdb_match.group(1), encoding="utf-8")
py_compile.compile(str(test_authdb), doraise=True)
print("Section 4.8 (auth_db.py) compiles with 0 errors!")

mermaid_blocks = re.findall(r"```mermaid\s*(.*?)\s*```", content, re.DOTALL)
print(f"Exactly {len(mermaid_blocks)} valid Mermaid diagrams found:")
for i, mb in enumerate(mermaid_blocks, 1):
    first_line = mb.strip().splitlines()[0]
    print(f"  Diagram {i}: {first_line}")
    assert any(first_line.startswith(x) for x in ["flowchart", "sequenceDiagram", "graph", "classDiagram", "erDiagram"]), f"Invalid mermaid type: {first_line}"
print("All Mermaid diagrams are valid!")
