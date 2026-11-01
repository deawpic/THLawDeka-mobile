from pathlib import Path

p = Path(r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md")
lines = p.read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines[110:118], 111):
    print(i, repr(l))

for idx, line in enumerate(lines):
    if "os.path.basename" in line:
        print(f"Found at line {idx+1}: {repr(line)}")
        lines[idx] = "      - ป้องกัน Path Traversal Attack และ Windows Alternate Data Streams (ADS) ด้วย Strict Regex Whitelist `^[a-zA-Z0-9_\\-\\u0E00-\\u0E7F]+\\.md$` ร่วมกับ Canonical Path Confinement (`file_path.is_relative_to(OUTPUT_DIR.resolve())`)"

p.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Done writing!")
