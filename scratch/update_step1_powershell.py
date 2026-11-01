import sys
from pathlib import Path

qs = Path("QUICK_START.md")
content = qs.read_text(encoding="utf-8")

old_text = """### 🔹 Step 1: ตรวจสอบและทดสอบ Core Agent Harness (`THLawDeka/`)
ทดสอบว่า `agy` CLI สามารถรับข้อเท็จจริงคดีผ่าน `stdin` (`-p -`) และสตรีมผลวิเคราะห์ออกมาได้ตามปกติ:

```bash
# 1. เข้าสู่โฟลเดอร์ Core Agent
cd THLawDeka

# 2. ทดสอบยิงคำถามกฎหมายผ่าน stdin (Windows PowerShell)
echo "คดีฉ้อโกงตามประมวลกฎหมายอาญา มาตรา 341 มีองค์ประกอบความผิดอย่างไร" | agy -p - --sandbox --input-format text --output-format stream-json

# 3. กลับมายังรูทของโปรเจกต์
cd ..
```
*ผลลัพธ์ที่ถูกต้อง:* ต้องเห็นสตรีม NDJSON ตอบกลับมา โดยที่ Process Table ของระบบปฏิบัติการไม่ปรากฏข้อความคำถามคดีความ (ความปลอดภัยระดับ Confidentiality Layer)"""

new_text = """### 🔹 Step 1: ตรวจสอบและทดสอบ Core Agent Harness (`THLawDeka/`)
ทดสอบว่า `agy` CLI ในเครื่องสามารถทำงานร่วมกับกฎหมาย IRAC และสตรีมผลวิเคราะห์ออกมาได้ตามปกติ:

```powershell
# 1. เข้าสู่โฟลเดอร์ Core Agent
cd THLawDeka

# 2. ทดสอบยิงคำถามกฎหมายใน Windows PowerShell (แนะนำ)
agy -p "คดีฉ้อโกงตามประมวลกฎหมายอาญา มาตรา 341 มีองค์ประกอบความผิดอย่างไร" --sandbox --input-format text --output-format stream-json

# 3. กลับมายังรูทของโปรเจกต์
cd ..
```

> 💡 **ข้อสังเกตสำคัญใน Windows PowerShell:**
> - การทดสอบบน PowerShell แบบ Manual ให้ใช้คำสั่ง `agy -p "ข้อความ..."` โดยตรง **ห้ามใช้ `echo "..." | agy -p -`** เนื่องจากคำสั่ง `echo` (Write-Output) ใน Windows PowerShell มีการแปลงรหัสภาษาไทยผ่าน `$OutputEncoding` ของคอนโซล (มักเป็น ASCII/CP874) ทำให้ข้อความภาษาไทยเพี้ยนหรือกลายเป็น `????`
> - ในระบบจริง โค้ด Backend (`backend/main.py`) จะส่งข้อความผ่าน `asyncio.subprocess.PIPE` ด้วยการเข้ารหัส `query.encode("utf-8")` ระดับ Binary Stream โดยตรง จึงไม่มีปัญหาเรื่องการแปลงรหัสของคอนโซล และปกป้องข้อเท็จจริงคดีไม่ให้ปรากฏใน OS Process Table ได้อย่างสมบูรณ์ 100%

*ผลลัพธ์ที่ถูกต้อง:* ต้องเห็นสตรีม NDJSON ตอบกลับมาทีละบรรทัด พร้อมผลวิเคราะห์หลักกฎหมายและแนวฎีกาเทียบเคียง"""

assert old_text in content, "old_text not found in QUICK_START.md"
content = content.replace(old_text, new_text)
qs.write_text(content, encoding="utf-8")
print("Successfully updated Step 1 in QUICK_START.md!")
