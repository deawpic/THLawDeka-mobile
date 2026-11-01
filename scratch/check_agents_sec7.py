import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

agents_path = Path("THLawDeka/AGENTS.md")
content = agents_path.read_text(encoding="utf-8")

# Let's inspect Section 7 in THLawDeka/AGENTS.md
target_header = "## 7. การบันทึกไฟล์และส่งออกข้อมูล (File Saving & Data Export)"
target_end = "## 8. กฎการสร้างแผนภาพและตาราง (Diagram & Table Guardrails - Mermaid & Markdown Table Only)"

idx_start = content.find(target_header)
idx_end = content.find(target_end)

assert idx_start != -1, "Section 7 header not found"
assert idx_end != -1, "Section 8 header not found"

print(f"Section 7 found from {idx_start} to {idx_end} ({idx_end - idx_start} chars)")
print("Current Section 7 content preview:")
print(content[idx_start:idx_start+300])
