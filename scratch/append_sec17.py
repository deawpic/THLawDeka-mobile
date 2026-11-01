# -*- coding: utf-8 -*-
report_path = r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md"

sec17 = """

---

## 17. การกำจัดรหัสผ่าน Hardcoded และการยกระดับสู่ Zero-Hardcoded Secrets Policy (CWE-798 Elimination)

ตามข้อสังเกตเชิงลึกของผู้ใช้งานเรื่องความปลอดภัยของ `ADMIN_SECRET` ที่ไม่ควรมีค่าเริ่มต้น Hardcoded ในโค้ด ได้ดำเนินการยกระดับระบบความปลอดภัยเพื่อขจัดช่องโหว่ **CWE-798 (Use of Hard-coded Credentials)** อย่างเด็ดขาด 100%:

### 17.1 สถาปัตยกรรม Zero-Hardcoded Secrets ผ่าน `get_admin_secret()`:
1. **ลำดับการดึงรหัสผ่าน (Hierarchical Secret Resolution):**
   - **ลำดับที่ 1 (Environment Variable):** ตรวจสอบตัวแปร `os.getenv("ADMIN_SECRET")` หากผู้ใช้กำหนดไว้จะนำมาใช้ทันที
   - **ลำดับที่ 2 (Persistent Secret File):** ตรวจสอบไฟล์ `backend/.admin_secret` หากมีอยู่แล้วจะอ่านรหัสเดิมมาใช้ (คงค่าเดิมข้ามการรีสตาร์ทเซิร์ฟเวอร์)
   - **ลำดับที่ 3 (Auto-Generated Cryptographic Secret):** หากไม่พบทั้งสองทาง ระบบจะสร้างรหัสผ่านสุ่มความปลอดภัยสูงอัตโนมัติด้วย `secrets.token_urlsafe(24)` (เช่น `thlaw_admin_x9K...`) บันทึกลงในไฟล์ `backend/.admin_secret` (กำหนดสิทธิ์ POSIX 0600) และพิมพ์แสดงเด่นชัดบน Terminal เพียงครั้งเดียวตอนเริ่มระบบ
2. **การป้องกันรหัสผ่านหลุดสู่ Git (.gitignore Enforcement):**
   - สร้างไฟล์ `.gitignore` ใน Root Directory ระบุไม่ให้นำไฟล์ `backend/.admin_secret`, `*.db`, และ `backend/backups/` ขึ้นสู่ Git Repo โดยเด็ดขาด
3. **การปรับปรุงเอกสารและ Service:**
   - ปรับปรุง [system_spec_and_implementation_plan.md](techdocs/system_spec_and_implementation_plan.md) ใน Section 4.1 ให้ใช้ฟังก์ชัน `get_admin_secret()`
   - ปรับปรุง [Quick_start_Windows.md](Quick_start_Windows.md) และ [Quick_start_Linux.md](Quick_start_Linux.md) ในขั้นตอนที่ 7.1 และ Troubleshooting ให้สอดคล้องกับพฤติกรรมของระบบ
   - ปรับปรุง `backend/thlaw-gateway.service` ลบค่าเริ่มต้นที่ฮาร์ดโค้ดออก
"""

with open(report_path, "a", encoding="utf-8") as f:
    f.write(sec17)

print("Section 17 appended to agent_enhancement_report.md successfully.")
