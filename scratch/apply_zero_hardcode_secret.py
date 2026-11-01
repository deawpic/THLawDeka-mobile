# -*- coding: utf-8 -*-
import os

repo_root = r"c:\Ai_code\THLawDeka-mobile"
spec_path = os.path.join(repo_root, "techdocs", "system_spec_and_implementation_plan.md")
service_path = os.path.join(repo_root, "backend", "thlaw-gateway.service")
win_path = os.path.join(repo_root, "Quick_start_Windows.md")
linux_path = os.path.join(repo_root, "Quick_start_Linux.md")
agents_path = os.path.join(repo_root, "AGENTS.md")

# =========================================================================
# 1. Update spec main.py code
# =========================================================================
with open(spec_path, "r", encoding="utf-8") as f:
    spec_text = f.read()

target_spec_secret = 'ADMIN_SECRET = os.getenv("ADMIN_SECRET", "admin_super_secret_pass_2026")'
replacement_spec_secret = """import secrets

def get_admin_secret() -> str:
    \"\"\"
    ดึงรหัสผ่าน Admin โดยยึดหลัก Zero-Hardcoded Secret (CWE-798 Compliance):
    1. หากมีการกำหนดตัวแปรสภาพแวดล้อม ADMIN_SECRET ให้ใช้ค่านั้นทันที
    2. หากไม่ได้กำหนด ให้ตรวจสอบไฟล์ persistent secret ใน backend/.admin_secret
    3. หากยังไม่มีไฟล์ ให้สุ่มรหัสความปลอดภัยสูง (32 bytes urlsafe) บันทึกลงไฟล์ พร้อมแจ้งเตือนใน Console
    \"\"\"
    env_secret = os.getenv("ADMIN_SECRET")
    if env_secret and env_secret.strip():
        return env_secret.strip()

    secret_file = Path(__file__).resolve().parent / ".admin_secret"
    if secret_file.exists():
        try:
            return secret_file.read_text(encoding="utf-8").strip()
        except Exception:
            pass

    generated = f"thlaw_admin_{secrets.token_urlsafe(24)}"
    try:
        secret_file.write_text(generated, encoding="utf-8")
        if os.name == "posix":
            os.chmod(secret_file, 0o600)
    except Exception as e:
        print(f"[WARN] Failed to persist .admin_secret: {e}")

    print("=" * 70)
    print("🔒 [SECURITY NOTICE] ไม่พบการตั้งค่า ADMIN_SECRET ในระบบ")
    print(f"🔑 ระบบได้สร้างรหัสผ่านสุ่มอัตโนมัติ: {generated}")
    print(f"📁 บันทึกเก็บไว้ที่: {secret_file}")
    print("👉 ให้นำรหัสนี้ไปล็อกอินที่: http://127.0.0.1:8000/admin")
    print("=" * 70)
    return generated

ADMIN_SECRET = get_admin_secret()"""

assert target_spec_secret in spec_text, "Could not find target_spec_secret in spec"
spec_text = spec_text.replace(target_spec_secret, replacement_spec_secret, 1)

with open(spec_path, "w", encoding="utf-8") as f:
    f.write(spec_text)
print("1. Updated spec with get_admin_secret() successfully.")

# =========================================================================
# 2. Update backend/thlaw-gateway.service
# =========================================================================
with open(service_path, "r", encoding="utf-8") as f:
    service_text = f.read()

target_service_line = 'Environment="ADMIN_SECRET=admin_super_secret_pass_2026"'
replacement_service_line = '# กำหนดรหัสผ่านลับสำหรับ Admin (หรือปล่อยว่างเพื่อให้ระบบสุ่มสร้างและบันทึกลง backend/.admin_secret อัตโนมัติ)\n# Environment="ADMIN_SECRET=YOUR_CUSTOM_SECURE_SECRET_HERE"'

if target_service_line in service_text:
    service_text = service_text.replace(target_service_line, replacement_service_line, 1)
    with open(service_path, "w", encoding="utf-8") as f:
        f.write(service_text)
    print("2. Updated thlaw-gateway.service successfully.")

# =========================================================================
# 3. Update Quick_start_Windows.md
# =========================================================================
with open(win_path, "r", encoding="utf-8") as f:
    win_text = f.read()

win_old_sec = """#### 🔑 ข้อมูลรหัสผ่าน Admin:
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
4. ในช่อง **Master Admin Secret** ให้กรอกรหัสผ่านที่คุณตั้งไว้ในข้อ 2 (หรือกรอกรหัสเริ่มต้น: `admin_super_secret_pass_2026`) แล้วกดปุ่ม **โหลดข้อมูล / เข้าสู่ระบบ**"""

win_new_sec = """#### 🔑 ข้อมูลรหัสผ่าน Admin (Zero-Hardcoded Secrets Policy):
เพื่อความมั่นคงปลอดภัยสูงสุด ระบบ **ไม่มีการฮาร์ดโค้ดรหัสผ่านไว้ในซอร์สโค้ด (Zero-Hardcoded Secrets)** เพื่อป้องกันช่องโหว่ CWE-798:
* **วิธีที่ 1 (แนะนำ - กำหนดรหัสผ่านของคุณเอง):** ระบุรหัสผ่านที่ต้องการผ่านตัวแปร `$env:ADMIN_SECRET` ในคำสั่งรัน
* **วิธีที่ 2 (สะดวก ปลอดภัยสูง):** หากไม่ได้กำหนดรหัสผ่านไว้ ระบบจะ **สุ่มสร้างรหัสผ่านความปลอดภัยสูงให้อัตโนมัติ (เช่น `thlaw_admin_x9K...`)** โดยจะพิมพ์แสดงเด่นชัดบนหน้าต่าง Terminal ทันทีที่เซิร์ฟเวอร์เปิด และบันทึกเก็บไว้ในไฟล์ `backend/.admin_secret` (ไม่ถูกส่งขึ้น Git)

---

#### 🚀 วิธีเปิดเซิร์ฟเวอร์ (เลือกได้ 2 แบบตามความสะดวก):
1. เปิดเข้าไปในโฟลเดอร์ `backend` คลิกที่แถบที่อยู่ด้านบน พิมพ์ `powershell` แล้วกด Enter
2. เลือกรันคำสั่งแบบใดแบบหนึ่ง:
   * **แบบที่ 1 (กำหนดรหัสผ่าน Admin ด้วยตนเอง - แนะนำ):**
     ```powershell
     $env:ADMIN_SECRET="ใส่รหัสผ่านใหม่ที่คุณต้องการตรงนี้"; uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```
   * **แบบที่ 2 (ให้ระบบสุ่มสร้างรหัสผ่านอัตโนมัติ):**
     ```powershell
     uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```
     *(ระบบจะพิมพ์รหัสผ่านสุ่ม เช่น `thlaw_admin_...` บนหน้าจอ Terminal ให้คุณคัดลอกไปใช้งานได้ทันที)*
   *(เมื่อรันแล้ว หน้าจอจะขึ้นข้อความว่า `Uvicorn running on http://127.0.0.1:8000` แปลว่าเซิร์ฟเวอร์เปิดทำงานแล้ว **ห้ามปิดหน้าต่างนี้ทิ้งนะครับ**)*

---

#### 📋 เข้าหน้า Admin Web UI เพื่อสร้างกุญแจ API Key:
3. เปิดเว็บเบราว์เซอร์ (Chrome หรือ Edge) ไปที่ลิงก์:
   👉 **`http://127.0.0.1:8000/admin`**
4. ในช่อง **Master Admin Secret** ให้กรอกรหัสผ่านที่คุณตั้งไว้ (หรือคัดลอกรหัสผ่านสุ่มที่ระบบพิมพ์แสดงบนหน้าต่าง Terminal / ไฟล์ `backend/.admin_secret`) แล้วกดปุ่ม **โหลดข้อมูล / เข้าสู่ระบบ**"""

assert win_old_sec in win_text, "Could not find win_old_sec in Quick_start_Windows.md"
win_text = win_text.replace(win_old_sec, win_new_sec, 1)

win_old_trouble = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** รหัสผ่าน Admin ถูกควบคุมผ่านตัวแปร `ADMIN_SECRET` หากไม่ได้ระบุไว้ รหัสเริ่มต้นคือ `admin_super_secret_pass_2026` หากต้องการเปลี่ยนรหัสผ่าน ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์ uvicorn เดิม แล้วรันใหม่ด้วยคำสั่ง:
     ```powershell
     $env:ADMIN_SECRET="รหัสผ่านใหม่ของคุณ"; uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```"""

win_new_trouble = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** หากคุณไม่ได้ตั้งรหัสผ่านเอง สามารถเปิดดูรหัสผ่านสุ่มที่ระบบสร้างไว้ในไฟล์ `backend/.admin_secret` หรือหากต้องการเปลี่ยนรหัสผ่านใหม่ ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์เดิม แล้วสั่งเปิดใหม่พร้อมระบุรหัสผ่านใหม่ได้ทันที:
     ```powershell
     $env:ADMIN_SECRET="รหัสผ่านใหม่ของคุณ"; uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```"""

assert win_old_trouble in win_text, "Could not find win_old_trouble in Quick_start_Windows.md"
win_text = win_text.replace(win_old_trouble, win_new_trouble, 1)

with open(win_path, "w", encoding="utf-8") as f:
    f.write(win_text)
print("3. Updated Quick_start_Windows.md successfully.")

# =========================================================================
# 4. Update Quick_start_Linux.md
# =========================================================================
with open(linux_path, "r", encoding="utf-8") as f:
    linux_text = f.read()

linux_old_sec = """#### 🔑 ข้อมูลรหัสผ่าน Admin:
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
4. ในช่อง **Master Admin Secret** ให้กรอกรหัสผ่านที่คุณตั้งไว้ในข้อ 2 (หรือกรอกรหัสเริ่มต้น: `admin_super_secret_pass_2026`) แล้วกดปุ่ม **โหลดข้อมูล / เข้าสู่ระบบ**"""

linux_new_sec = """#### 🔑 ข้อมูลรหัสผ่าน Admin (Zero-Hardcoded Secrets Policy):
เพื่อความมั่นคงปลอดภัยสูงสุด ระบบ **ไม่มีการฮาร์ดโค้ดรหัสผ่านไว้ในซอร์สโค้ด (Zero-Hardcoded Secrets)** เพื่อป้องกันช่องโหว่ CWE-798:
* **วิธีที่ 1 (แนะนำ - กำหนดรหัสผ่านของคุณเอง):** ระบุรหัสผ่านที่ต้องการผ่านตัวแปร `ADMIN_SECRET` ในคำสั่งรัน
* **วิธีที่ 2 (สะดวก ปลอดภัยสูง):** หากไม่ได้กำหนดรหัสผ่านไว้ ระบบจะ **สุ่มสร้างรหัสผ่านความปลอดภัยสูงให้อัตโนมัติ (เช่น `thlaw_admin_x9K...`)** โดยจะพิมพ์แสดงเด่นชัดบน Terminal ทันทีที่เซิร์ฟเวอร์เปิด และบันทึกเก็บไว้ในไฟล์ `backend/.admin_secret` (สิทธิ์ 600)

---

#### 🚀 วิธีเปิดเซิร์ฟเวอร์ (เลือกได้ 2 แบบตามความสะดวก):
1. เปิด Terminal เข้าไปที่โฟลเดอร์ `backend`:
   ```bash
   cd ~/THLawDeka-mobile/backend
   ```
2. เลือกรันคำสั่งแบบใดแบบหนึ่ง:
   * **แบบที่ 1 (กำหนดรหัสผ่าน Admin ด้วยตนเอง - แนะนำ):**
     ```bash
     ADMIN_SECRET="ใส่รหัสผ่านใหม่ที่คุณต้องการตรงนี้" uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```
   * **แบบที่ 2 (ให้ระบบสุ่มสร้างรหัสผ่านอัตโนมัติ):**
     ```bash
     uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```
     *(ระบบจะพิมพ์รหัสผ่านสุ่ม เช่น `thlaw_admin_...` บน Terminal ให้คุณคัดลอกไปใช้งานได้ทันที)*
   *(เมื่อรันแล้ว หน้าจอจะขึ้นข้อความว่า `Uvicorn running on http://0.0.0.0:8000` แปลว่าเซิร์ฟเวอร์เปิดทำงานแล้ว **ห้ามปิดหน้าต่างนี้ทิ้งนะครับ**)*
   > 💡 *สำหรับโหมด Background Service (Systemd):* สามารถระบุรหัสผ่านในไฟล์ `/etc/systemd/system/thlaw-gateway.service` ที่บรรทัด `Environment="ADMIN_SECRET=รหัสผ่านของคุณ"` ได้เช่นกัน

---

#### 📋 เข้าหน้า Admin Web UI เพื่อสร้างกุญแจ API Key:
3. เปิดเว็บเบราว์เซอร์ไปที่ลิงก์:
   👉 **`http://127.0.0.1:8000/admin`**
4. ในช่อง **Master Admin Secret** ให้กรอกรหัสผ่านที่คุณตั้งไว้ (หรือคัดลอกรหัสผ่านสุ่มที่ระบบพิมพ์แสดงบน Terminal / ไฟล์ `backend/.admin_secret`) แล้วกดปุ่ม **โหลดข้อมูล / เข้าสู่ระบบ**"""

assert linux_old_sec in linux_text, "Could not find linux_old_sec in Quick_start_Linux.md"
linux_text = linux_text.replace(linux_old_sec, linux_new_sec, 1)

linux_old_trouble = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** รหัสผ่าน Admin ถูกควบคุมผ่านตัวแปร `ADMIN_SECRET` หากไม่ได้ระบุไว้ รหัสเริ่มต้นคือ `admin_super_secret_pass_2026` หากต้องการเปลี่ยนรหัสผ่าน ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์ uvicorn เดิม แล้วรันใหม่ด้วยคำสั่ง:
     ```bash
     ADMIN_SECRET="รหัสผ่านใหม่ของคุณ" uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```"""

linux_new_trouble = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** หากคุณไม่ได้ตั้งรหัสผ่านเอง สามารถเปิดดูรหัสผ่านสุ่มที่ระบบสร้างไว้ในไฟล์ `backend/.admin_secret` (หรือรัน `cat backend/.admin_secret`) หรือหากต้องการเปลี่ยนรหัสผ่านใหม่ ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์เดิม แล้วสั่งเปิดใหม่พร้อมระบุรหัสผ่านใหม่ได้ทันที:
     ```bash
     ADMIN_SECRET="รหัสผ่านใหม่ของคุณ" uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```"""

assert linux_old_trouble in linux_text, "Could not find linux_old_trouble in Quick_start_Linux.md"
linux_text = linux_text.replace(linux_old_trouble, linux_new_trouble, 1)

with open(linux_path, "w", encoding="utf-8") as f:
    f.write(linux_text)
print("4. Updated Quick_start_Linux.md successfully.")

# =========================================================================
# 5. Update AGENTS.md with Zero-Hardcoded Secrets policy
# =========================================================================
with open(agents_path, "r", encoding="utf-8") as f:
    agents_text = f.read()

target_backend_agent = "SQLite keys.db auth, Fast-Path Legal Cache, and Admin Web UI."
replacement_backend_agent = "SQLite keys.db auth, Zero-Hardcoded Admin Secret Policy (CWE-798 compliance via get_admin_secret() and persistent .admin_secret fallback), Fast-Path Legal Cache, and Admin Web UI."

if target_backend_agent in agents_text and "Zero-Hardcoded Admin Secret Policy" not in agents_text:
    agents_text = agents_text.replace(target_backend_agent, replacement_backend_agent, 1)
    with open(agents_path, "w", encoding="utf-8") as f:
        f.write(agents_text)
    print("5. Updated AGENTS.md successfully.")

print("ALL ZERO-HARDCODE UPDATES COMPLETED SUCCESSFULLY.")
