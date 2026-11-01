import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# Let's read lines of spec and modify systematically
lines = content.splitlines()

# 1. Update lines around 207-238 (Section 3.1.3)
for idx, line in enumerate(lines):
    if 'P2["อนุญาตสิทธิ์เขียนเฉพาะ' in line:
        lines[idx] = '        P2["บังคับใช้นโยบาย <b>Server-Side Zero-Disk-Write</b> ไม่มีการเขียนไฟล์ใดๆ บนเซิร์ฟเวอร์"]'
    elif 'และเครื่องมือสร้างไฟล์บทวิเคราะห์ `.md` ในโฟลเดอร์ `output/`' in line:
        lines[idx] = '   - ให้สิทธิ์เฉพาะเครื่องมือค้นหาข้อกฎหมายและฎีกา (Read-Only) และตัดเครื่องมือเขียนไฟล์หรือแก้ไขดิสก์ทิ้งทั้งหมด'
    elif 'อนุญาตสิทธิ์เขียนเฉพาะไดเรกทอรี `THLawDeka/output/` แห่งเดียวเท่านั้น' in line:
        lines[idx] = '   - กำหนดให้โฟลเดอร์ทั้งหมดบนเซิร์ฟเวอร์เป็น Read-Only โดยไม่มีการเปิดสิทธิ์เขียนในโฟลเดอร์ใดๆ เพื่อรองรับ Server-Side Zero-Disk-Write Policy 100%'

# 2. Update Section 6.1 Runbook line
for idx, line in enumerate(lines):
    if "ดาวน์โหลดไฟล์ไม่ผ่าน" in line:
        lines[idx] = '| **ส่งออกหรือแชร์ไฟล์ในเครื่อง Android ไม่สำเร็จ** | ขาดการกำหนดค่า FileProvider หรือไม่มีสิทธิ์เข้าถึง Cache/Documents | ตรวจสอบว่ากำหนด `grantUriPermissions="true"` ใน `AndroidManifest.xml` และระบุ `<cache-path>` ใน `res/xml/file_paths.xml` ถูกต้อง |'

# 3. Update Section 6.3 Windows & Linux ACL instructions
for idx, line in enumerate(lines):
    if '# 2. ปลดล็อกสิทธิ์เขียนเฉพาะโฟลเดอร์ output เพื่อให้ออกบทวิเคราะห์คดีความได้' in line:
        lines[idx] = '# (ไม่ต้องเปิดสิทธิ์เขียนในโฟลเดอร์ output เนื่องจากระบบใช้ Server-Side Zero-Disk-Write Policy)'
        if idx + 1 < len(lines) and 'icacls "THLawDeka\\output"' in lines[idx + 1]:
            lines[idx + 1] = '# icacls "THLawDeka\\output" /grant "Everyone":(OI)(CI)(M) [DEPRECATED: Zero disk write enforced]'
    elif '# 2. เปิดสิทธิ์เขียนเฉพาะโฟลเดอร์ output สำหรับผู้ใช้ที่รันเซอร์วิส' in line:
        lines[idx] = '# (ไม่ต้องเปิดสิทธิ์เขียนในโฟลเดอร์ output เนื่องจากระบบใช้ Server-Side Zero-Disk-Write Policy)'
        if idx + 1 < len(lines) and 'sudo chmod -R 775 THLawDeka/output/' in lines[idx + 1]:
            lines[idx + 1] = '# sudo chmod -R 775 THLawDeka/output/ [DEPRECATED: Zero disk write enforced]'
        if idx + 2 < len(lines) and 'sudo chown -R thlaw:thlaw THLawDeka/output/' in lines[idx + 2]:
            lines[idx + 2] = '# sudo chown -R thlaw:thlaw THLawDeka/output/ [DEPRECATED]'

spec_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Applied Section 3.1.3 and Section 6 line edits successfully!")
