# -*- coding: utf-8 -*-
import os

repo_root = r"c:\Ai_code\THLawDeka-mobile"
win_path = os.path.join(repo_root, "Quick_start_Windows.md")
linux_path = os.path.join(repo_root, "Quick_start_Linux.md")

# ==========================================
# Windows Section 7.1 Replacement
# ==========================================
win_old_71 = """### 🔹 7.1 เปิดเซิร์ฟเวอร์ Backend และสร้างรหัสกุญแจ (API Key)
1. เปิดเข้าไปในโฟลเดอร์ `backend` คลิกที่แถบที่อยู่ด้านบน พิมพ์ `powershell` แล้วกด Enter
2. รันคำสั่งเปิดเซิร์ฟเวอร์:
   ```powershell
   uv run uvicorn main:app --host 127.0.0.1 --port 8000
   ```
   *(หน้าจอจะขึ้นว่า `Uvicorn running on http://127.0.0.1:8000` แปลว่าเซิร์ฟเวอร์เปิดทำงานสำเร็จแล้ว **ห้ามปิดหน้าต่างนี้ทิ้งนะครับ**)*
3. เปิดเว็บเบราว์เซอร์ (Chrome หรือ Edge) ไปที่ลิงก์นี้:
   👉 **`http://127.0.0.1:8000/admin`**
4. ป้อนรหัสผ่าน Admin: `MySuperSecureAdminSecret2026` แล้วกด Enter (หรือกดปุ่มเข้าสู่ระบบ)
5. ในช่องระบุชื่อผู้ใช้ ให้พิมพ์ชื่อของคุณ (เช่น "นายสมชาย") แล้วกดปุ่มสีเขียว **`+ สร้าง Key ใหม่`**
6. คุณจะได้รับรหัสกุญแจยาว ๆ เช่น `thlaw_live_1a2b3c4d5e...` ให้คลิกปุ่ม 📋 **คัดลอกกุญแจนี้เก็บไว้**"""

win_new_71 = """### 🔹 7.1 การกำหนดรหัสผ่าน Admin และเปิดเซิร์ฟเวอร์ Backend (Admin Password Configuration)

เซิร์ฟเวอร์ Backend มีระบบป้องกันหน้าจอผู้ดูแลระบบ (`/admin`) ด้วย Master Secret โดยถูกควบคุมผ่านตัวแปรสภาพแวดล้อม (Environment Variable) ชื่อ **`ADMIN_SECRET`**:

#### 🔑 ข้อมูลรหัสผ่าน Admin:
* **รหัสผ่านเริ่มต้น (Default):** `admin_super_secret_pass_2026` (ใช้ได้ทันทีโดยไม่ต้องตั้งค่าเพิ่ม)
* **การเปลี่ยนรหัสผ่านเป็นของคุณเอง (Custom Password - แนะนำเพื่อความปลอดภัย):** คุณสามารถกำหนดรหัสผ่านใหม่ได้ทันทีในขั้นตอนรันเซิร์ฟเวอร์ด้านล่างนี้

---

#### 🚀 วิธีเปิดเซิร์ฟเวอร์ (เลือกได้ 2 แบบตามความสะดวก):
1. เปิดเข้าไปในโฟลเดอร์ `backend` คลิกที่แถบที่อยู่ด้านบน พิมพ์ `powershell` แล้วกด Enter
2. เลือกรันคำสั่งแบบใดแบบหนึ่ง:
   * **แบบที่ 1 (เปลี่ยนรหัสผ่าน Admin เป็นของตัวเองทันที - แนะนำ):**
     ```powershell
     $env:ADMIN_SECRET="ใส่รหัสผ่านใหม่ที่คุณต้องการตรงนี้"; uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```
   * **แบบที่ 2 (ใช้รหัสผ่านเริ่มต้นของระบบ: `admin_super_secret_pass_2026`):**
     ```powershell
     uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```
   *(เมื่อรันแล้ว หน้าจอจะขึ้นข้อความสีเขียวว่า `Uvicorn running on http://127.0.0.1:8000` แปลว่าเซิร์ฟเวอร์เปิดทำงานแล้ว **ห้ามปิดหน้าต่างนี้ทิ้งเด็ดขาดนะครับ**)*

---

#### 📋 เข้าหน้า Admin Web UI เพื่อสร้างกุญแจ API Key:
3. เปิดเว็บเบราว์เซอร์ (Chrome หรือ Edge) ไปที่ลิงก์:
   👉 **`http://127.0.0.1:8000/admin`**
4. ในช่อง **Master Admin Secret** ให้กรอกรหัสผ่านที่คุณตั้งไว้ในข้อ 2 (หรือกรอกรหัสเริ่มต้น: `admin_super_secret_pass_2026`) แล้วกดปุ่ม **โหลดข้อมูล / เข้าสู่ระบบ**
5. ในช่องระบุชื่อผู้ใช้ ให้พิมพ์ชื่อของคุณ (เช่น "นายสมชาย") แล้วกดปุ่มสีเขียว **`+ สร้าง Key ใหม่`**
6. คุณจะได้รับรหัสกุญแจยาว ๆ เช่น `thlaw_live_1a2b3c4d5e...` ให้คลิกปุ่ม 📋 **คัดลอกกุญแจนี้เก็บไว้** สำหรับนำไปใส่ในแอปมือถือ"""

# ==========================================
# Linux Section 7.1 Replacement
# ==========================================
linux_old_71 = """### 🔹 7.1 เปิดเซิร์ฟเวอร์ Backend และสร้างรหัสกุญแจ (API Key)
1. เปิด Terminal ใหม่เข้าไปที่โฟลเดอร์ `backend`:
   ```bash
   cd ~/THLawDeka-mobile/backend
   uv run uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   *(หน้าจอจะขึ้นว่า `Uvicorn running on http://0.0.0.0:8000` แปลว่าเซิร์ฟเวอร์เปิดทำงานแล้ว **ห้ามปิด Terminal นี้ทิ้งนะครับ**)*
2. เปิดเว็บเบราว์เซอร์ไปที่ลิงก์นี้:
   👉 **`http://127.0.0.1:8000/admin`**
3. ป้อนรหัสผ่าน Admin: `MySuperSecureAdminSecret2026` แล้วกด Enter
4. ในช่องระบุชื่อผู้ใช้ ให้พิมพ์ชื่อของคุณ (เช่น "สมชาย") แล้วกดปุ่มสีเขียว **`+ สร้าง Key ใหม่`**
5. คุณจะได้รับรหัสกุญแจยาว ๆ เช่น `thlaw_live_1a2b3c4d5e...` ให้คลิกปุ่ม 📋 **คัดลอกกุญแจนี้เก็บไว้**"""

linux_new_71 = """### 🔹 7.1 การกำหนดรหัสผ่าน Admin และเปิดเซิร์ฟเวอร์ Backend (Admin Password Configuration)

เซิร์ฟเวอร์ Backend มีระบบป้องกันหน้าจอผู้ดูแลระบบ (`/admin`) ด้วย Master Secret โดยถูกควบคุมผ่านตัวแปรสภาพแวดล้อม (Environment Variable) ชื่อ **`ADMIN_SECRET`**:

#### 🔑 ข้อมูลรหัสผ่าน Admin:
* **รหัสผ่านเริ่มต้น (Default):** `admin_super_secret_pass_2026` (ใช้ได้ทันทีโดยไม่ต้องตั้งค่าเพิ่ม)
* **การเปลี่ยนรหัสผ่านเป็นของคุณเอง (Custom Password - แนะนำเพื่อความปลอดภัย):** คุณสามารถกำหนดรหัสผ่านใหม่ได้ทันทีในขั้นตอนรันเซิร์ฟเวอร์ด้านล่างนี้

---

#### 🚀 วิธีเปิดเซิร์ฟเวอร์ (เลือกได้ 2 แบบตามความสะดวก):
1. เปิด Terminal เข้าไปที่โฟลเดอร์ `backend`:
   ```bash
   cd ~/THLawDeka-mobile/backend
   ```
2. เลือกรันคำสั่งแบบใดแบบหนึ่ง:
   * **แบบที่ 1 (เปลี่ยนรหัสผ่าน Admin เป็นของตัวเองทันที - แนะนำ):**
     ```bash
     ADMIN_SECRET="ใส่รหัสผ่านใหม่ที่คุณต้องการตรงนี้" uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```
   * **แบบที่ 2 (ใช้รหัสผ่านเริ่มต้นของระบบ: `admin_super_secret_pass_2026`):**
     ```bash
     uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```
   *(เมื่อรันแล้ว หน้าจอจะขึ้นข้อความว่า `Uvicorn running on http://0.0.0.0:8000` แปลว่าเซิร์ฟเวอร์เปิดทำงานแล้ว **ห้ามปิดหน้าต่างนี้ทิ้งเด็ดขาดนะครับ**)*
   > 💡 *สำหรับโหมด Background Service (Systemd):* สามารถระบุรหัสผ่านในไฟล์ `/etc/systemd/system/thlaw-gateway.service` ที่บรรทัด `Environment="ADMIN_SECRET=รหัสผ่านของคุณ"` ได้เช่นกัน

---

#### 📋 เข้าหน้า Admin Web UI เพื่อสร้างกุญแจ API Key:
3. เปิดเว็บเบราว์เซอร์ไปที่ลิงก์:
   👉 **`http://127.0.0.1:8000/admin`**
4. ในช่อง **Master Admin Secret** ให้กรอกรหัสผ่านที่คุณตั้งไว้ในข้อ 2 (หรือกรอกรหัสเริ่มต้น: `admin_super_secret_pass_2026`) แล้วกดปุ่ม **โหลดข้อมูล / เข้าสู่ระบบ**
5. ในช่องระบุชื่อผู้ใช้ ให้พิมพ์ชื่อของคุณ (เช่น "สมชาย") แล้วกดปุ่มสีเขียว **`+ สร้าง Key ใหม่`**
6. คุณจะได้รับรหัสกุญแจยาว ๆ เช่น `thlaw_live_1a2b3c4d5e...` ให้คลิกปุ่ม 📋 **คัดลอกกุญแจนี้เก็บไว้** สำหรับนำไปใส่ในแอปมือถือ"""

# Windows troubleshooting addition
win_trouble_q7 = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** รหัสผ่าน Admin ถูกควบคุมผ่านตัวแปร `ADMIN_SECRET` หากไม่ได้ระบุไว้ รหัสเริ่มต้นคือ `admin_super_secret_pass_2026` หากต้องการเปลี่ยนรหัสผ่าน ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์ uvicorn เดิม แล้วรันใหม่ด้วยคำสั่ง:
     ```powershell
     $env:ADMIN_SECRET="รหัสผ่านใหม่ของคุณ"; uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```
"""

linux_trouble_q7 = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** รหัสผ่าน Admin ถูกควบคุมผ่านตัวแปร `ADMIN_SECRET` หากไม่ได้ระบุไว้ รหัสเริ่มต้นคือ `admin_super_secret_pass_2026` หากต้องการเปลี่ยนรหัสผ่าน ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์ uvicorn เดิม แล้วรันใหม่ด้วยคำสั่ง:
     ```bash
     ADMIN_SECRET="รหัสผ่านใหม่ของคุณ" uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```
"""

# Apply to Windows
with open(win_path, "r", encoding="utf-8") as f:
    win_text = f.read()

if win_old_71 in win_text:
    win_text = win_text.replace(win_old_71, win_new_71)
    if "7. **ถาม: ลืมรหัสผ่าน Admin" not in win_text:
        win_text = win_text.replace(
            "## ❓ 6 ปัญหาที่พบบ่อยและวิธีแก้ง่าย ๆ (Troubleshooting)",
            "## ❓ 7 ปัญหาที่พบบ่อยและวิธีแก้ง่าย ๆ (Troubleshooting)"
        )
        # Append before reference
        win_text = win_text.replace(
            "## 📚 เอกสารอ้างอิงเพิ่มเติม",
            win_trouble_q7 + "\n---\n\n## 📚 เอกสารอ้างอิงเพิ่มเติม"
        )
    with open(win_path, "w", encoding="utf-8") as f:
        f.write(win_text)
    print("Updated Quick_start_Windows.md with Admin Password section.")
else:
    print("win_old_71 not matched in Quick_start_Windows.md")

# Apply to Linux
with open(linux_path, "r", encoding="utf-8") as f:
    linux_text = f.read()

if linux_old_71 in linux_text:
    linux_text = linux_text.replace(linux_old_71, linux_new_71)
    if "7. **ถาม: ลืมรหัสผ่าน Admin" not in linux_text:
        linux_text = linux_text.replace(
            "## ❓ 6 ปัญหาที่พบบ่อยบน Linux และวิธีแก้ง่าย ๆ (Troubleshooting)",
            "## ❓ 7 ปัญหาที่พบบ่อยบน Linux และวิธีแก้ง่าย ๆ (Troubleshooting)"
        )
        linux_text = linux_text.replace(
            "## 📚 เอกสารอ้างอิงเพิ่มเติม",
            linux_trouble_q7 + "\n---\n\n## 📚 เอกสารอ้างอิงเพิ่มเติม"
        )
    with open(linux_path, "w", encoding="utf-8") as f:
        f.write(linux_text)
    print("Updated Quick_start_Linux.md with Admin Password section.")
else:
    print("linux_old_71 not matched in Quick_start_Linux.md")
