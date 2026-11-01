from pathlib import Path

p = Path(r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md")
content = p.read_text(encoding="utf-8")

# Fix line 91
bad_line = """    alt ผู้ใช้แตะการ์ดไฟล์ หรือแตะ Markdown Link
        Android->>Gateway: GET /api/v1/files/<filename>.md (Bearer Token)
      - ป้องกัน Path Traversal Attack และ Windows Alternate Data Streams (ADS) ด้วย Strict Regex Whitelist `^[a-zA-Z0-9_\\-\\u0E00-\\u0E7F]+\\.md$` ร่วมกับ Canonical Path Confinement (`file_path.is_relative_to(OUTPUT_DIR.resolve())`)
        Gateway-->>Android: ส่งเนื้อหาไฟล์ (FileResponse - Content-Disposition: attachment)"""

good_line = """    alt ผู้ใช้แตะการ์ดไฟล์ หรือแตะ Markdown Link
        Android->>Gateway: GET /api/v1/files/<filename>.md (Bearer Token)
        Gateway->>Gateway: Regex Whitelist + ตรวจสอบ Path Confinement + Bearer Auth
        Gateway-->>Android: ส่งเนื้อหาไฟล์ (FileResponse - Content-Disposition: attachment)"""

content = content.replace(bad_line, good_line)

# Fix indentation at line 114
bad_indent = "     - ป้องกัน Path Traversal Attack และ Windows Alternate Data Streams (ADS)"
good_indent = "    - ให้บริการ Endpoint `GET /api/v1/files/{filename}`:\n      - ป้องกัน Path Traversal Attack และ Windows Alternate Data Streams (ADS)"

content = content.replace("   - ให้บริการ Endpoint `GET /api/v1/files/{filename}`:\n       - ป้องกัน Path Traversal Attack และ Windows Alternate Data Streams (ADS)", good_indent)

p.write_text(content, encoding="utf-8")
print("Fixed mermaid sequence diagram and indentation!")
