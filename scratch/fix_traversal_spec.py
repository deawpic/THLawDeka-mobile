from pathlib import Path

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
lines = spec_path.read_text(encoding="utf-8").splitlines()

for idx, line in enumerate(lines):
    if "os.path.basename" in line:
        if "Gateway->>Gateway:" in line:
            lines[idx] = "        Gateway->>Gateway: Regex Whitelist + ตรวจขอบเขต Confinement + ตรวจสิทธิ์ keys.db"
            print(f"Updated line {idx+1}")
        elif "Path Traversal Shield:" in line:
            lines[idx] = "   - **Path Traversal & ADS Shield:** ตรวจสอบชื่อไฟล์ด้วย Regex Whitelist `^[a-zA-Z0-9_\\-\\u0E00-\\u0E7F]+\\.md$` และตรวจสอบการกักขังไดเรกทอรีด้วย `file_path.is_relative_to(OUTPUT_DIR.resolve())` ป้องกันการเจาะอ่านไฟล์ระบบนอกไดเรกทอรี `output/` และ Alternate Data Streams"
            print(f"Updated line {idx+1}")

spec_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Saved spec updates!")
