# -*- coding: utf-8 -*-
report_path = r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md"

addition = """10. **การกำหนดรหัสผ่าน Backend Admin (ADMIN_SECRET Configuration):**
    - อธิบายค่ารหัสผ่านเริ่มต้นของระบบ (`admin_super_secret_pass_2026`) ที่เชื่อมตรงกับ `backend/main.py`
    - เพิ่มคำแนะนำและคำสั่งการตั้งรหัสผ่านใหม่ (Custom Secret) ผ่าน Environment Variable ทั้งบน Windows PowerShell (`$env:ADMIN_SECRET="..."`) และ Linux Bash (`ADMIN_SECRET="..."`)
    - เพิ่มข้อแนะนำการตั้งค่าในไฟล์ Systemd Service สำหรับรันเป็น Background Service บน Linux
    - เพิ่มข้อคำถาม-คำตอบที่ 7 ในหัวข้อ Troubleshooting สำหรับกรณีลืมรหัสผ่านหรือต้องการเปลี่ยนรหัสผ่านใหม่
"""

with open(report_path, "a", encoding="utf-8") as f:
    f.write(addition)

print("Added point 10 to agent_enhancement_report.md.")
