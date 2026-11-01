import sys
from pathlib import Path

qs_path = Path("QUICK_START.md")
content = qs_path.read_text(encoding="utf-8")

old_sec4 = """## 🛠️ 4. สิ่งที่ต้องติดตั้งบนเครื่องก่อนเริ่มงาน (Prerequisites)

| ซอฟต์แวร์ / เครื่องมือ | เวอร์ชันที่ต้องการ | วัตถุประสงค์และการนำไปใช้ |
| :--- | :--- | :--- |
| **Python** | 3.10 – 3.13 | สำหรับรัน FastAPI Gateway และ Harness Engine |
| **`uv` (แนะนำอย่างยิ่ง)** | เวอร์ชันล่าสุด | Package Manager ความเร็วสูงของ Python (ข้ามปัญหา ExecutionPolicy ของ Windows PowerShell ได้ 100%) ติดตั้งผ่าน `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex" หรือ `winget install --id astral-sh.uv`` |
| **Google Antigravity CLI (`agy`)** | เวอร์ชันล่าสุด | Core Agent CLI สำหรับรันโมเดลกฎหมาย ติดตั้งและล็อกอินตาม [Google Antigravity Documentation](https://antigravity.google/docs/overview) |
| **Tailscale** | เวอร์ชันล่าสุด | ติดตั้งบนเครื่องคอมพิวเตอร์เพื่อทำ HTTPS Reverse Proxy ข้าม CGNAT ด้วยพอร์ต 443 |
| **Android Studio** | Ladybug / Koala ขึ้นไป | สำหรับเปิดและบิลด์แอป Android (ติดตั้ง Android SDK 36 และ OpenJDK 17) |

---"""

new_sec4 = """## 🛠️ 4. สิ่งที่ต้องติดตั้งบนเครื่องก่อนเริ่มงาน (Prerequisites)

| ซอฟต์แวร์ / เครื่องมือ | เวอร์ชันที่ต้องการ | วัตถุประสงค์และการนำไปใช้ |
| :--- | :--- | :--- |
| **Python** | 3.10 – 3.13 | สำหรับรัน FastAPI Gateway และ Harness Engine |
| **`uv` (แนะนำอย่างยิ่ง)** | เวอร์ชันล่าสุด | Package Manager ความเร็วสูงของ Python (สร้าง venv เร็วขึ้น 10-100 เท่า และข้ามปัญหา Script Execution Policy ของ Windows PowerShell ได้ 100%) |
| **Google Antigravity CLI (`agy`)** | เวอร์ชันล่าสุด | Core Agent CLI สำหรับรันโมเดลกฎหมาย ติดตั้งและล็อกอินตาม [Google Antigravity Documentation](https://antigravity.google/docs/overview) |
| **Tailscale** | เวอร์ชันล่าสุด | ติดตั้งบนเครื่องคอมพิวเตอร์เพื่อทำ HTTPS Reverse Proxy ข้าม CGNAT ด้วยพอร์ต 443 |
| **Android Studio** | Ladybug / Koala ขึ้นไป | สำหรับเปิดและบิลด์แอป Android (ติดตั้ง Android SDK 36 และ OpenJDK 17) |

### 📌 คำสั่งติดตั้ง `uv` สำหรับ Windows (เลือกวิธีใดวิธีหนึ่ง):

* **วิธีที่ 1: ผ่าน Official PowerShell Script (แนะนำที่สุด — ติดตั้งและเซ็ต PATH อัตโนมัติ):**
  เปิด PowerShell แล้วคัดลอกคำสั่งนี้ไปรัน:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
* **วิธีที่ 2: ผ่าน Windows Package Manager (`winget`):**
  ```powershell
  winget install --id astral-sh.uv
  ```
* **วิธีที่ 3: ผ่าน `pip` (กรณีมี Python ติดตั้งอยู่แล้ว):**
  ```powershell
  pip install uv
  ```

> 💡 **การตรวจสอบหลังติดตั้ง:** ปิดหน้าต่าง PowerShell เดิมแล้วเปิดใหม่ เพื่อให้ระบบโหลด PATH จากนั้นรัน:
> ```powershell
> uv --version
> ```

---"""

assert old_sec4 in content, "old_sec4 not found in QUICK_START.md"
content = content.replace(old_sec4, new_sec4)
qs_path.write_text(content, encoding="utf-8")
print("Successfully inserted uv for Windows installation commands into QUICK_START.md!")
