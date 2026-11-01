import sys
import re
import py_compile
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

print("=== Deep Multi-Dimensional Specification Audit ===")

# 1. Extract and Compile backend/main.py from Section 4.1
main_match = re.search(r"### 4\.1 โค้ดฝั่ง Backend Gateway \(`backend/main\.py`\)\s*```python\s*(.*?)\s*```", content, re.DOTALL)
if main_match:
    main_code = main_match.group(1)
    test_main_path = Path("scratch/extracted_main.py")
    test_main_path.write_text(main_code, encoding="utf-8")
    try:
        py_compile.compile(str(test_main_path), doraise=True)
        print("  ✓ Section 4.1 (main.py) code block compiles cleanly!")
    except Exception as e:
        print(f"  ✗ Section 4.1 code syntax error: {e}")
else:
    print("  ✗ Could not extract Section 4.1 code block!")

# 2. Extract and Compile backend/auth_db.py from Section 4.8
authdb_match = re.search(r"### 4\.8 โค้ดฝั่ง Backend สำหรับฐานข้อมูลกุญแจ \(`backend/auth_db\.py`\)\s*```python\s*(.*?)\s*```", content, re.DOTALL)
if authdb_match:
    authdb_code = authdb_match.group(1)
    test_authdb_path = Path("scratch/extracted_authdb.py")
    test_authdb_path.write_text(authdb_code, encoding="utf-8")
    try:
        py_compile.compile(str(test_authdb_path), doraise=True)
        print("  ✓ Section 4.8 (auth_db.py) code block compiles cleanly!")
    except Exception as e:
        print(f"  ✗ Section 4.8 code syntax error: {e}")
else:
    print("  ✗ Could not extract Section 4.8 code block!")

# 3. Check for any unresolved TODOs, FIXMEs, or placeholders
todos = re.findall(r"(?i)\b(todo|fixme|xxx|tbd|placeholder)\b", content)
print(f"  ✓ Unresolved placeholders/TODOs count: {len(todos)}")

# 4. Check Mermaid Diagrams Syntax (all closed properly)
mermaid_blocks = re.findall(r"```mermaid\s*(.*?)\s*```", content, re.DOTALL)
print(f"  ✓ Found {len(mermaid_blocks)} Mermaid architecture diagrams.")
for i, m in enumerate(mermaid_blocks, 1):
    first_line = m.strip().splitlines()[0]
    print(f"    - Diagram {i}: {first_line}")

# 5. Check Section Hierarchy and Numbering
headers = [line.strip() for line in content.splitlines() if line.strip().startswith("##")]
print(f"  ✓ Document sections ({len(headers)} total):")
for h in headers[:15]:
    print(f"    - {h}")

print("\n>>> AUDIT SCAN FINISHED <<<")
