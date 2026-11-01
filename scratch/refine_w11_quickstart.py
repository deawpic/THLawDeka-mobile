import sys
from pathlib import Path

qs_path = Path("QUICK_START.md")
content = qs_path.read_text(encoding="utf-8")

old_sec4_table = """| **Python** | 3.10 – 3.13 | สำหรับรัน FastAPI Gateway และ Harness Engine |
| **`uv` (แนะนำอย่างยิ่ง)** | เวอร์ชันล่าสุด | Package Manager ความเร็วสูงของ Python (สร้าง venv เร็วขึ้น 10-100 เท่า และข้ามปัญหา Script Execution Policy ของ Windows PowerShell ได้ 100%) |"""

new_sec4_table = """| **ระบบปฏิบัติการ** | Windows 11 (หรือ Windows 10) | รองรับ Windows Terminal และ UTF-8 เต็มรูปแบบ |
| **Python** | 3.12 (แนะนำอย่างยิ่ง) | สำหรับรัน FastAPI Gateway และ Harness Engine (มี Pre-built Wheel ครบ 100%) |
| **`uv` (แนะนำอย่างยิ่ง)** | เวอร์ชันล่าสุด | Package Manager ความเร็วสูงของ Python (ติดตั้งผ่าน `winget` บน Windows 11 ได้ทันที และข้ามปัญหา Microsoft Store Redirect) |"""

if old_sec4_table in content:
    content = content.replace(old_sec4_table, new_sec4_table)

old_winget = """* **วิธีที่ 2: ผ่าน Windows Package Manager (`winget`):**
  ```powershell
  winget install --id astral-sh.uv
  ```"""

new_winget = """* **วิธีที่ 2: ผ่าน Windows Package Manager (`winget` — สำหรับ Windows 11 มีติดเครื่องมาอยู่แล้ว รันได้ทันที):**
  ```powershell
  winget install --id astral-sh.uv
  ```"""

if old_winget in content:
    content = content.replace(old_winget, new_winget)

# Add Windows 11 benefit tip
old_py_install = """*ข้อดี:* ไม่ต้องเปิดเบราว์เซอร์ดาวน์โหลดตัวติดตั้ง ไม่ต้องจัดการเรื่องสิทธิ์ Admin หรือการติ๊กเลือก Add to PATH และไม่ทำให้สภาพแวดล้อม Python อื่นในเครื่องสับสน"""

new_py_install = """*ข้อดีบน Windows 11:* 
  1. ไม่ต้องเปิดเบราว์เซอร์ดาวน์โหลดตัวติดตั้ง และไม่ต้องมีสิทธิ์ Admin
  2. แก้ปัญหาคลาสสิกของ Windows 11 ที่ชอบเด้งหน้าต่าง **Microsoft Store** ขึ้นมาเมื่อพิมพ์คำสั่ง `python`
  3. ไม่ทำให้ PATH หรือ Python ตัวอื่นในเครื่องตีกัน"""

if old_py_install in content:
    content = content.replace(old_py_install, new_py_install)

qs_path.write_text(content, encoding="utf-8")
print("Successfully refined QUICK_START.md for Windows 11!")
