import sys
from pathlib import Path

qs_path = Path("QUICK_START.md")
content = qs_path.read_text(encoding="utf-8")

old_sec4_end = """> 💡 **การตรวจสอบหลังติดตั้ง:** ปิดหน้าต่าง PowerShell เดิมแล้วเปิดใหม่ เพื่อให้ระบบโหลด PATH จากนั้นรัน:
> ```powershell
> uv --version
> ```

---"""

new_sec4_end = """> 💡 **การตรวจสอบหลังติดตั้ง:** ปิดหน้าต่าง PowerShell เดิมแล้วเปิดใหม่ เพื่อให้ระบบโหลด PATH จากนั้นรัน:
> ```powershell
> uv --version
> ```

### 🐍 ติดตั้ง Python อัตโนมัติผ่าน `uv` (แนะนำอย่างยิ่ง — ไม่ต้องดาวน์โหลดจาก python.org เอง):
หากในเครื่องยังไม่มี Python หรือต้องการเวอร์ชันที่เสถียรและตรงตามข้อกำหนดระบบ (แนะนำ Python 3.12) สามารถสั่งให้ `uv` ติดตั้ง Python แบบ Standalone ได้ทันทีในคำสั่งเดียว:
```powershell
# สั่งให้ uv ดาวน์โหลดและติดตั้ง Python 3.12 ให้อัตโนมัติ
uv python install 3.12
```
*ข้อดี:* ไม่ต้องเปิดเบราว์เซอร์ดาวน์โหลดตัวติดตั้ง ไม่ต้องจัดการเรื่องสิทธิ์ Admin หรือการติ๊กเลือก Add to PATH และไม่ทำให้สภาพแวดล้อม Python อื่นในเครื่องสับสน

---"""

assert old_sec4_end in content, "old_sec4_end not found"
content = content.replace(old_sec4_end, new_sec4_end)

# Also update Step 2 in Section 5:
old_step2 = """1. **สร้าง Virtual Environment และติดตั้ง Dependencies:**
   ```bash
   cd backend
   
   # ติดตั้งผ่าน uv (แนะนำ เร็วที่สุด):
   uv venv
   uv pip install -r requirements.txt"""

new_step2 = """1. **สร้าง Virtual Environment และติดตั้ง Dependencies:**
   ```bash
   cd backend
   
   # สร้าง venv ด้วย Python 3.12 ที่ uv ติดตั้งไว้ และลง Dependencies:
   uv venv --python 3.12
   uv pip install -r requirements.txt"""

assert old_step2 in content, "old_step2 not found"
content = content.replace(old_step2, new_step2)

qs_path.write_text(content, encoding="utf-8")
print("Successfully added uv python install to QUICK_START.md!")
