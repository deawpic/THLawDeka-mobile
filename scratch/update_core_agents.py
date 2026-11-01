import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

agents_path = Path("THLawDeka/AGENTS.md")
content = agents_path.read_text(encoding="utf-8")

target_header = "## 7. การบันทึกไฟล์และส่งออกข้อมูล (File Saving & Data Export)"
target_end = "## 8. กฎการสร้างแผนภาพและตาราง (Diagram & Table Guardrails - Mermaid & Markdown Table Only)"

idx_start = content.find(target_header)
idx_end = content.find(target_end)

assert idx_start != -1, "Section 7 header not found"
assert idx_end != -1, "Section 8 header not found"

new_sec7 = """## 7. กฎเหล็กห้ามสร้างไฟล์บนเซิร์ฟเวอร์และการส่งผลลัพธ์เป็น Markdown Text (Server-Side Zero-Disk-Write & Pure Markdown Response Gate)
- **กฎเหล็กห้ามสร้าง, เขียน หรือบันทึกไฟล์ใดๆ ลงในดิสก์ของเซิร์ฟเวอร์ (Strict Server-Side Zero-Disk-Write Policy)**:
  - Agent ทำงานในโหมด Read-Only บนเครื่องเซิร์ฟเวอร์อย่างเด็ดขาด **ห้าม Agent สร้าง, เขียน หรือบันทึกไฟล์ใดๆ ลงในไดเรกทอรี `./output` หรือโฟลเดอร์ใดๆ ของเซิร์ฟเวอร์สำหรับคำขอของผู้ใช้งานโดยเด็ดขาด**
  - ระบบจะส่งออกผลลัพธ์การวิเคราะห์ทั้งหมดเป็น **Markdown Text** ผ่าน Standard Output (`stdout`) แบบเรียลไทม์เท่านั้น เพื่อให้ Gateway บีบอัด Gzip และส่งต่อไปยัง Android Client
- **การจัดการเมื่อผู้ใช้ขอให้บันทึกไฟล์และการแนะนำฟังก์ชันส่งออกในเครื่อง (Zero-Server-File Rejection & Client Export Guidance)**:
  - หากผู้ใช้มีคำสั่ง เช่น *"บันทึกไฟล์ให้ด้วย"*, *"สร้างไฟล์สรุปคดี"*, *"เซฟลงเครื่องเซิร์ฟเวอร์"*, หรือขอไฟล์นามสกุลใดๆ เช่น `.md`, `.pdf`, `.txt`, `.docx`:
    - **ห้ามสร้างไฟล์บนเครื่องเซิร์ฟเวอร์เด็ดขาด**
    - ให้ Agent ส่งเนื้อหาบทวิเคราะห์ข้อกฎหมายฉบับสมบูรณ์ในรูปแบบ Markdown Text (พร้อมตาราง GFM และบล็อก Mermaid) ผ่านข้อความแชตโดยตรงตามปกติ
    - และระบุข้อความแนะนำสั้นๆ ท้ายคำตอบ:
      > *"📄 **หมายเหตุการส่งออกเอกสาร:** ระบบได้ส่งมอบบทวิเคราะห์ข้อกฎหมายฉบับสมบูรณ์ในข้อความนี้เรียบร้อยแล้ว โดยท่านสามารถแตะที่เมนูส่งออกเอกสารบนแอปพลิเคชัน Android เพื่อสั่งบันทึกหรือแชร์เป็นไฟล์ **Markdown (.md)**, **เอกสารทางการศาล A4 (.pdf)**, หรือ **ข้อความธรรมดา (.txt)** ลงในอุปกรณ์ของท่านได้ทันทีโดยตรงครับ"*
  - **กรณีผู้ใช้ขอให้บันทึกเป็นไฟล์โค้ด, สคริปต์ หรือไฟล์ระบบ (`.bat`, `.cmd`, `.sh`, `.ps1`, `.exe`, `.py`, `.json`, `.env`, `.db`) (Strict Security Hard Reject)**:
    - **ปฏิเสธทันที (Hard Reject)**: แจ้งเตือนผู้ใช้ว่าระบบความปลอดภัยไม่อนุญาตให้สร้างหรือส่งออกไฟล์สคริปต์/ไฟล์ระบบ
- **กฎเหล็กแผนภาพและตารางในคำตอบ (Mermaid & Markdown Table Gate)**:
  - ส่วนที่เป็นแผนภาพ ต้องใช้บล็อกโค้ด Mermaid (` ```mermaid ... ``` `) เท่านั้น
  - ส่วนที่เป็นตาราง ต้องใช้ Markdown Table (`| คอลัมน์ 1 | คอลัมน์ 2 |`) ตามมาตรฐาน GitHub Flavored Markdown (GFM) เท่านั้น
  - ห้ามใช้อักขระหรือเส้น ASCII Text ทำแผนภาพหรือตารางโดยเด็ดขาด

---

"""

updated_content = content[:idx_start] + new_sec7 + content[idx_end:]
agents_path.write_text(updated_content, encoding="utf-8")
print("Updated THLawDeka/AGENTS.md Section 7 successfully!")
