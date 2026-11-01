# -*- coding: utf-8 -*-
import os
import shutil

repo_root = r"c:\Ai_code\THLawDeka-mobile"
qs_old = os.path.join(repo_root, "QUICK_START.md")
qs_win = os.path.join(repo_root, "Quick_start_Windows.md")
qs_linux = os.path.join(repo_root, "Quick_start_Linux.md")

# 1. Read existing QUICK_START.md
with open(qs_old, "r", encoding="utf-8") as f:
    win_content = f.read()

# Update header and references in Quick_start_Windows.md
win_content = win_content.replace(
    "# 🚀 THLawDeka-mobile: คู่มือเริ่มต้นฉบับจับมือทำสำหรับมือใหม่ (Newbie-Proof Step-by-Step Guide)",
    "# 🚀 THLawDeka-mobile: คู่มือเริ่มต้นฉบับจับมือทำสำหรับ Windows 11 (Newbie-Proof Step-by-Step Guide for Windows 11)"
)
win_content = win_content.replace(
    "`QUICK_START.md`",
    "`Quick_start_Windows.md`"
)

# Add notice at the top for Linux users
top_notice_win = """
> 🐧 **สำหรับผู้ใช้ระบบปฏิบัติการ Linux (Ubuntu / Debian / Fedora / Arch):**
> โปรดอ่านคู่มือฉบับเฉพาะของระบบ Linux ได้ที่: [Quick_start_Linux.md](Quick_start_Linux.md)
"""
win_content = win_content.replace(
    "คู่มือนี้เขียนขึ้นสำหรับผู้เริ่มต้นที่ **ไม่มีพื้นฐานการเขียนโปรแกรมมาก่อน** โดยอธิบายแบบ **\"จับมือทำทีละคลิก (Click-by-Click)\"** ครบทุกขั้นตอน ตั้งแต่การแตกไฟล์ ติดตั้งโปรแกรม ทดสอบคำสั่ง สั่ง AI พัฒนา ไปจนถึงเปิดใช้งานแอปจริงบนมือถือ พร้อมวิธีรับมือกับปัญหาที่พบบ่อย (Troubleshooting) อย่างละเอียดที่สุดครับ\n",
    "คู่มือนี้เขียนขึ้นสำหรับผู้เริ่มต้นที่ **ไม่มีพื้นฐานการเขียนโปรแกรมมาก่อน** โดยอธิบายแบบ **\"จับมือทำทีละคลิก (Click-by-Click)\"** ครบทุกขั้นตอน ตั้งแต่การแตกไฟล์ ติดตั้งโปรแกรม ทดสอบคำสั่ง สั่ง AI พัฒนา ไปจนถึงเปิดใช้งานแอปจริงบนมือถือ พร้อมวิธีรับมือกับปัญหาที่พบบ่อย (Troubleshooting) อย่างละเอียดที่สุดครับ\n" + top_notice_win
)

# Write Quick_start_Windows.md
with open(qs_win, "w", encoding="utf-8") as f:
    f.write(win_content)

# Remove old QUICK_START.md
if os.path.exists(qs_old):
    os.remove(qs_old)
print("Created Quick_start_Windows.md and removed QUICK_START.md")

# 2. Build Quick_start_Linux.md
linux_content = """# 🚀 THLawDeka-mobile: คู่มือเริ่มต้นฉบับจับมือทำสำหรับ Linux (Newbie-Proof Step-by-Step Guide for Linux)
## สำหรับผู้ใช้งาน Ubuntu, Debian, Fedora, Arch Linux หรือ WSL2 ตั้งแต่ศูนย์จนใช้งานได้จริง 100%

> 🪟 **สำหรับผู้ใช้งานระบบปฏิบัติการ Windows 11:**
> โปรดอ่านคู่มือฉบับเฉพาะของ Windows ได้ที่: [Quick_start_Windows.md](Quick_start_Windows.md)

คู่มือนี้เขียนขึ้นสำหรับผู้ใช้งานระบบปฏิบัติการ Linux ทุกระดับ ครอบคลุม **Ubuntu 22.04/24.04 LTS, Debian, Fedora, Arch Linux รวมถึง WSL2 (Windows Subsystem for Linux)** โดยอธิบายแบบทีละขั้นตอน (Step-by-Step) ตั้งแต่การแตกไฟล์ ติดตั้งโปรแกรม จัดการสิทธิ์ USB (udev rules) สั่ง AI Agent พัฒนา ไปจนถึงรันแอปบนมือถือหรือ Emulator จริง พร้อมหัวข้อแก้ปัญหาที่พบบ่อย (Troubleshooting) อย่างครบถ้วนครับ

---

### 📦 สำหรับ "ผู้ส่งไฟล์" (ทำก่อน Zip ส่งให้เพื่อน):
ก่อนกดบีบอัดเป็นไฟล์ `THLawDeka-mobile.zip` ให้ตรวจเช็ก 2 ข้อนี้ เพื่อให้ไฟล์มีขนาดเล็กกะทัดรัด (เพียง 1-2 MB แทนที่จะเป็น 200+ MB):
1. ลบโฟลเดอร์ `backend/.venv` (หากเคยสร้างไว้) ทิ้งก่อน
2. ลบโฟลเดอร์แคช `__pycache__` ต่างๆ ทิ้งก่อน
*(เพื่อนของคุณจะสร้างสภาพแวดล้อมใหม่ที่สะอาดบนเครื่องของเขาเองตามคู่มือนี้ในเวลาเพียงไม่กี่วินาทีครับ)*

---

## 🧭 แผนผังภาพรวม 7 ขั้นตอนบน Linux (ทำตามลำดับนี้ได้เลย):
```text
[ขั้นตอนที่ 1] แตกไฟล์ Zip ในโฟลเดอร์ Home (~/THLawDeka-mobile)
      ↓
[ขั้นตอนที่ 2] ติดตั้งเครื่องมือจำเป็นบน Linux (curl, uv, Python 3.12, Android Studio)
      ↓
[ขั้นตอนที่ 3] ทดสอบเครื่องมือ AI (agy CLI) ในโฟลเดอร์ THLawDeka
      ↓
[ขั้นตอนที่ 4] สร้างสภาพแวดล้อม (.venv) และลงแพ็กเกจในโฟลเดอร์ backend
      ↓
[ขั้นตอนที่ 5] เปิดโปรเจกต์ใน Antigravity Desktop
      ↓
[ขั้นตอนที่ 6] คัดลอกคำสั่ง Master Prompt สั่ง AI เริ่มพัฒนา Phase 1 ถึง Phase 5
      ↓
[ขั้นตอนที่ 7] เปิดรันเซิร์ฟเวอร์ และเปิดแอปใน Android Studio (Emulator หรือมือถือจริง)
```

---

## 🗂️ ขั้นตอนที่ 1: การแตกไฟล์ Zip บน Linux

1. เมื่อได้รับไฟล์ `THLawDeka-mobile.zip` ให้บันทึกไว้ใน Home Directory ของคุณ (`~/Downloads` หรือ `~/`)
2. เปิดโปรแกรม **Terminal** (`Ctrl + Alt + T` บน Ubuntu/Debian)
3. รันคำสั่งแตกไฟล์ไปยังโฟลเดอร์ `~/THLawDeka-mobile`:
   ```bash
   mkdir -p ~/THLawDeka-mobile
   unzip ~/Downloads/THLawDeka-mobile.zip -d ~/THLawDeka-mobile
   ```
   *(หรือคลิกขวาที่ไฟล์ zip ในโปรแกรม Files/Nautilus แล้วเลือก **Extract Here**)*
4. ⚠️ **จุดตรวจเช็กสำคัญ (ป้องกันโฟลเดอร์ซ้อน):**
   - รันคำสั่งตรวจสอบ:
     ```bash
     cd ~/THLawDeka-mobile && ls -la
     ```
   - **จะต้องเห็นโฟลเดอร์ชื่อ `backend`, `THLawDeka`, `techdocs` และไฟล์ `Quick_start_Linux.md` ทันที**
   - *หาก `ls` แล้วเจอโฟลเดอร์ชื่อ `THLawDeka-mobile` ซ้อนอยู่อีกชั้นหนึ่ง ให้ย้ายเข้าไปทำงานในโฟลเดอร์ชั้นในนั้นด้วยคำสั่ง `cd THLawDeka-mobile` ครับ*

---

## 🛠️ ขั้นตอนที่ 2: ติดตั้งเครื่องมือจำเป็นบน Linux (ทำครั้งเดียว ใช้ได้ตลอดไป)

### 🔹 2.1 ติดตั้ง `curl`, `uv` และ `Python 3.12`
1. ใน Terminal ให้ติดตั้ง `curl` ก่อน (หากยังไม่มี):
   * **Ubuntu / Debian:** `sudo apt update && sudo apt install -y curl unzip build-essential`
   * **Fedora:** `sudo dnf install -y curl unzip gcc`
   * **Arch Linux:** `sudo pacman -S --needed curl unzip base-devel`
2. ติดตั้งเครื่องมือจัดการ Python ความเร็วสูง **`uv`**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. โหลดค่า PATH ให้ระบบรู้จักคำสั่ง `uv`:
   ```bash
   source ~/.bashrc  # หากใช้ zsh ให้รัน source ~/.zshrc
   ```
4. ติดตั้ง **Python 3.12** แบบแยกส่วน (Standalone) ผ่าน `uv`:
   ```bash
   uv python install 3.12
   ```
   *(รอประมาณ 5-10 วินาที ระบบจะดาวน์โหลดและติดตั้ง Python 3.12 ให้เสร็จสมบูรณ์ โดยไม่กระทบกับ Python ประจำเครื่องของ Linux)*

---

### 🔹 2.2 ติดตั้ง Google Antigravity Desktop (โปรแกรมควบคุม AI Agent)
1. ดาวน์โหลดโปรแกรม **Antigravity Desktop** สำหรับ Linux (.deb / .tar.gz / AppImage) จากเว็บไซต์ทางการ: [https://antigravity.google](https://antigravity.google)
2. ติดตั้งตามประเภทไฟล์:
   * **กรณี .deb (Ubuntu/Debian):**
     ```bash
     sudo dpkg -i antigravity_*.deb || sudo apt --fix-broken install -y
     ```
   * **กรณี AppImage:** คลิกขวา -> Properties -> Permissions -> ติ๊กถูกที่ "Allow executing file as program" แล้วดับเบิลคลิกเปิดใช้งาน
3. เปิดโปรแกรม Antigravity ขึ้นมา ล็อกอินด้วยบัญชี Google ของคุณให้เรียบร้อย (ตัวโปรแกรมจะติดตั้งคำสั่ง `agy` CLI ลงในเครื่องให้อัตโนมัติ)
4. ตรวจสอบว่าคำสั่ง `agy` ใช้งานได้ด้วยคำสั่ง:
   ```bash
   agy --version
   ```

---

### 🔹 2.3 ติดตั้ง Android Studio บน Linux
1. ติดตั้ง Android Studio ผ่านช่องทางที่สะดวกที่สุด:
   * **Ubuntu (ผ่าน Snap - แนะนำง่ายที่สุด):**
     ```bash
     sudo snap install android-studio --classic
     ```
   * **หรือดาวน์โหลดจากเว็บทางการ:** [https://developer.android.com/studio](https://developer.android.com/studio) แตกไฟล์ tar.gz แล้วรัน `./android-studio/bin/studio.sh`
2. **ตั้งค่าสิทธิ์ USB สำหรับต่อมือถือจริง (เฉพาะระบบ Linux):**
   * ระบบ Linux ต้องติดตั้ง udev rules เพื่อให้มองเห็นมือถือ Android ผ่านสาย USB:
     ```bash
     sudo apt install -y android-sdk-platform-tools-common adb  # สำหรับ Ubuntu/Debian
     ```
   > 📱 *หมายเหตุ: หากคุณไม่มีโทรศัพท์มือถือจริง คุณสามารถเปิดใช้งานเครื่องจำลอง **Android Emulator (Virtual Device)** บนหน้าจอคอมพิวเตอร์ผ่าน Android Studio ได้ฟรีทันทีโดยไม่ต้องตั้งค่าสาย USB ใด ๆ ครับ*

---

## ⚖️ ขั้นตอนที่ 3: ทดสอบการทำงานของ `agy` CLI ในโฟลเดอร์ `THLawDeka`

ขั้นตอนนี้ทำเพื่อ **ทดสอบว่าระบบ AI ผู้เชี่ยวชาญกฎหมายในเครื่อง Linux พร้อมทำงานจริง 100%**:

1. ใน Terminal ให้เข้าไปที่โฟลเดอร์ `THLawDeka`:
   ```bash
   cd ~/THLawDeka-mobile/THLawDeka
   ```
2. รันคำสั่งทดสอบยิงคำถามกฎหมายไทย:
   ```bash
   agy -p "คดีฉ้อโกงตามประมวลกฎหมายอาญา มาตรา 341 มีองค์ประกอบความผิดอย่างไร" --sandbox --input-format text --output-format stream-json
   ```
3. **ผลลัพธ์ที่ถูกต้อง:** หน้าจอจะเริ่มสตรีมข้อความวิเคราะห์กฎหมายตอบกลับมาทีละบรรทัด พร้อมระบุข้อกฎหมายและคำพิพากษาศาลฎีกา แปลว่า AI พร้อมทำงานสมบูรณ์แบบแล้วครับ!

---

## 🐍 ขั้นตอนที่ 4: สร้างสภาพแวดล้อม (`.venv`) และลงแพ็กเกจในโฟลเดอร์ `backend`

1. สลับเข้าไปที่โฟลเดอร์ `backend`:
   ```bash
   cd ~/THLawDeka-mobile/backend
   ```
2. รันคำสั่งสร้าง Virtual Environment ด้วย Python 3.12:
   ```bash
   uv venv --python 3.12
   ```
   *(โฟลเดอร์ `.venv` จะถูกสร้างขึ้นมาทันที)*
3. รันคำสั่งติดตั้งแพ็กเกจเซิร์ฟเวอร์ทั้งหมด:
   ```bash
   uv pip install -r requirements.txt
   ```
   *(หน้าจอจะขึ้น `Installed 5 packages in ...` เสร็จสิ้นใน 1 วินาที)*

---

## 💻 ขั้นตอนที่ 5: เปิดโปรเจกต์ใน Antigravity Desktop

1. เปิดโปรแกรม **Antigravity Desktop** (พิมพ์ `antigravity` ใน Terminal หรือเปิดจาก App Launcher)
2. คลิกที่เมนูมุมซ้ายบน **File -> Open Folder...**
3. เลือกโฟลเดอร์ `~/THLawDeka-mobile` แล้วกดปุ่ม **Open**
4. หากมีหน้าต่างขึ้นมาถามว่า *"Do you trust the authors of the files in this folder?"* ให้คลิกเลือก **Yes, I trust the authors**
5. หน้าจอจะพร้อมใช้งาน:
   - ด้านซ้ายมือ: โครงสร้างไฟล์ทั้งหมด
   - ด้านขวามือ: **หน้าต่างแชต (Chat Panel)** สำหรับสั่งงาน AI Agent (หรือกดคีย์ลัด `Ctrl + L`)

---

## 🤖 ขั้นตอนที่ 6: สั่งให้ AI Agent พัฒนาตั้งแต่ Phase 1 ถึง Phase 5 (Copy & Paste คำสั่งเดียว!)

ในหน้าต่างแชตของ **Antigravity Desktop** ทางขวามือ ให้ **คัดลอกข้อความในกรอบด้านล่างนี้ทั้งหมด** ไปวางในช่องพิมพ์ แล้วกดปุ่ม **Enter (ส่งข้อความ)**:

```text
สวัสดีทีมงาน Antigravity ให้เริ่มดำเนินการพัฒนาโปรเจกต์ THLawDeka-mobile ตามแผนปฏิบัติการ 5 เฟสที่ระบุไว้ในเอกสาร techdocs/system_spec_and_implementation_plan.md โดยยึดถือกฎเหล็กใน AGENTS.md อย่างเคร่งครัด:

1. ดำเนินการตามลำดับทีละเฟส:
   - Phase 1: Local Harness Pipe Test (ทดสอบ safe stdin pipe ของ agy CLI ใน THLawDeka/)
   - Phase 2: FastAPI Gateway & SSE (สร้าง backend/main.py, auth_db.py, Selective Gzip, และ Admin UI)
   - Phase 3: Tailscale HTTPS Setup (จัดเตรียมคำสั่ง Serve และ Funnel พร้อม Admin Reverse Proxy IP Shielding)
   - Phase 4: Android App Integration (สร้างโค้ด Kotlin ใน android/ สำหรับ OkHttp SSE, Markwon, Mermaid WebView, และ 100% Client-side DocumentExportManager)
   - Phase 5: E2E Verification & Hardening (ทดสอบ Zombie Reaper, CLI Flag Regex, และรัน scratch/verify_all.py)

2. กฎเหล็กที่ต้องปฏิบัติอย่างเข้มงวด:
   - Zero-Test by Default: ห้ามสร้างหรือรัน unit tests เอง เว้นแต่จะได้รับคำสั่งเฉพาะเจาะจง ให้ตรวจสอบโค้ดผ่าน python -m py_compile เท่านั้น
   - No Gradle Build: ห้ามรันคำสั่ง ./gradlew หรือ gradle ในเทอร์มินัลเด็ดขาด (ฉันจะเปิดบิลด์ผ่าน Android Studio ด้วยตัวเอง)
   - Server-Side Zero-Disk-Write: เซิร์ฟเวอร์ทำงานแบบ Read-Only ห้ามเขียนไฟล์ลงดิสก์เซิร์ฟเวอร์
   - 100% Portability: ใช้เฉพาะ Relative Paths ห้ามมี Hardcoded Absolute Path

ให้เริ่มดำเนินการจาก Phase 1 ทันที และรายงานความคืบหน้าเชิงประจักษ์เมื่อแต่ละเฟสสำเร็จ!
```

> ⚠️ **ข้อควรระวังสำคัญที่สุดในขั้นตอนนี้ (สำหรับมือใหม่):**
> - ระหว่างที่ AI กำลังสร้างโค้ดและรันสคริปต์ ระบบจะมีหน้าต่างถามขออนุมัติการทำงาน เช่น **"Proceed"**, **"Allow"**, หรือ **"Run Command"**
> - **ให้คลิกปุ่ม Proceed หรือ Always Allow ได้เลยครับ** หากไม่คลิก AI จะหยุดรอคำอนุมัติจากคุณ
> - นั่งดู AI ทำงานประมาณ 2-3 นาที จนกระทั่ง AI แจ้งว่า **"พัฒนาเสร็จสมบูรณ์ครบทั้ง 5 เฟส และผ่านการตรวจสอบ 0 errors"** ครับ

---

## 🚀 ขั้นตอนที่ 7: การเปิดใช้งานจริงเมื่อ AI พัฒนาเสร็จ

### 🔹 7.1 เปิดเซิร์ฟเวอร์ Backend และสร้างรหัสกุญแจ (API Key)
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
5. คุณจะได้รับรหัสกุญแจยาว ๆ เช่น `thlaw_live_1a2b3c4d5e...` ให้คลิกปุ่ม 📋 **คัดลอกกุญแจนี้เก็บไว้**

---

### 🔹 7.2 เปิดแอปใน Android Studio และเริ่มใช้งานบนมือถือ
1. เปิดโปรแกรม **Android Studio**
2. เลือกเมนู **File -> Open...** แล้วเลือกโฟลเดอร์ **`~/THLawDeka-mobile/android`**
3. รอสักครู่ให้แถบสถานะ Gradle Sync ด้านล่างขวาโหลดเสร็จสิ้น (ประมาณ 1-2 นาที)
4. เลือกว่าจะทดสอบด้วยวิธีใด:
   * **ทางเลือก A (เครื่องจำลอง Emulator บนหน้าจอ Linux):**
     - คลิกที่เมนูเลือกอุปกรณ์ด้านบน เลือก **Pixel 8 Pro** (หรือสร้างใหม่ใน Device Manager)
     - กดปุ่ม **Run (รูปสามเหลี่ยมสีเขียว ▶️)**
     - หน้าต่างโทรศัพท์จำลองจะเปิดขึ้นมาบนหน้าจอ Linux
   * **ทางเลือก B (โทรศัพท์ Android จริงผ่านสาย USB):**
     - เปิดโหมดนักพัฒนา: เข้าไปที่ **Settings -> About Phone** แตะที่ **Build Number** 7 ครั้ง
     - เข้าไปที่ **Developer Options -> เปิดสวิตช์ USB Debugging**
     - เสียบสาย USB ต่อโทรศัพท์เข้าคอมพิวเตอร์ Linux
     - รันคำสั่ง `adb devices` ใน Terminal เพื่อเช็กว่าเครื่องขึ้นสถานะ `device` (หากขึ้น `unauthorized` ให้ดูที่จอมือถือและแตะ "Allow Always")
     - ใน Android Studio จะเห็นชื่อรุ่นมือถือของคุณปรากฏขึ้นมา ให้กดปุ่ม **Run (▶️)**
5. เมื่อแอปพลิเคชัน THLawDeka ติดตั้งและเปิดขึ้นมาบนหน้าจอ:
   - แตะที่เมนู **Settings (ไอคอนรูปฟันเฟือง ⚙️)** ที่มุมบนขวา
   - ในช่อง **API Key:** นำรหัสกุญแจ `thlaw_live_...` ที่คัดลอกไว้ในข้อ 7.1 มาวาง
   - ในช่อง **Server URL:**
     - *หากใช้เครื่องจำลอง (Emulator):* ให้ใส่ `http://10.0.2.2:8000` (ไอพีพิเศษของแอนดรอยด์สำหรับต่อคอมพิวเตอร์)
     - *หากใช้มือถือจริงต่อ Wi-Fi ในบ้าน:* ให้ใส่ไอพีเครื่อง Linux เช่น `http://192.168.1.50:8000` (ดูไอพีเครื่องได้ด้วยคำสั่ง `ip addr show` หรือ `hostname -I`)
     - *หากต่อจากนอกบ้านผ่านเน็ต 4G/5G:* ให้ใส่ลิงก์ HTTPS ของ Tailscale Funnel (เช่น `https://my-linux-pc.tailnet.ts.net`)
   - กดปุ่ม **Save (บันทึก)**
6. แตะกลับมาที่หน้าแชตหลัก แล้วพิมพ์ปรึกษากฎหมายได้ทันที เช่น:
   > *"ผู้เช่าค้างค่าเช่า 3 เดือน เจ้าของบ้านมีสิทธิตัดน้ำตัดไฟและล็อกกุญแจห้องเช่าได้หรือไม่"*
7. คุณจะเห็นตัวอักษรพิมพ์ตอบออกมาสด ๆ แบบสตรีมมิ่งคำต่อคำ พร้อมตารางมาตรากฎหมาย และสามารถแตะปุ่ม **Export** ด้านบน เพื่อแปลงคำตอบเป็นเอกสาร **PDF ฟอนต์สารบรรณขนาด A4** บันทึกเก็บไว้หรือส่งต่อได้ทันทีครับ!

---

## ❓ 6 ปัญหาที่พบบ่อยบน Linux และวิธีแก้ง่าย ๆ (Troubleshooting)

1. **ถาม: พิมพ์คำสั่ง `uv` แล้วขึ้นว่า `bash: uv: command not found`?**
   * **ตอบ:** รันคำสั่ง `source ~/.bashrc` (หรือ `source ~/.zshrc`) เพื่อให้เชลล์โหลด PATH ของ uv หรือตรวจสอบว่ามีโฟลเดอร์ `~/.local/bin` ใน PATH หรือไม่

2. **ถาม: พิมพ์ `agy` แล้วระบบหาไม่เจอ?**
   * **ตอบ:** ตรวจดูว่าได้เปิดโปรแกรม **Antigravity Desktop** ขึ้นมาล็อกอินแล้วหรือยัง หรือตรวจเช็กว่าโฟลเดอร์ binary ของ Antigravity อยู่ใน PATH หรือเปิด Terminal ใหม่

3. **ถาม: สั่ง AI ใน Antigravity Desktop แล้วทำไมนิ่งไป ไม่ยอมพิมพ์โค้ดต่อ?**
   * **ตอบ:** มองไปที่หน้าต่างแชต มักจะมีปุ่มถามขออนุญาตสีฟ้าหรือสีเขียว เช่น **"Proceed"** หรือ **"Allow"** รอให้คุณคลิกอยู่ ให้คลิกอนุมัติ AI ก็จะทำงานต่อทันทีครับ

4. **ถาม: เสียบสายโทรศัพท์ Android เข้าคอม Linux แล้ว `adb devices` ขึ้นว่า `no permissions`?**
   * **ตอบ:** เกิดจากสิทธิ์ udev rules ให้รันคำสั่ง:
     ```bash
     sudo apt install -y android-sdk-platform-tools-common
     sudo adb kill-server && sudo adb start-server
     ```
     แล้วถอดสาย USB เสียบใหม่ จากนั้นแตะ "Allow Always" บนจอมือถือครับ

5. **ถาม: รัน `uv run uvicorn ...` แล้วขึ้นว่า Address already in use (พอร์ต 8000 ชน)?**
   * **ตอบ:** ค้นหาและปิดโปรเซสเก่าที่ค้างอยู่ด้วยคำสั่ง:
     ```bash
     fuser -k 8000/tcp
     ```
     แล้วรันคำสั่งเปิด uvicorn ใหม่อีกครั้ง

6. **ถาม: ถ้าอยากเชื่อมต่อจากมือถือภายนอกบ้านผ่านอินเทอร์เน็ต 4G/5G ต้องทำอย่างไร?**
   * **ตอบ:** เปิด Terminal บน Linux แล้วรันคำสั่ง:
     ```bash
     sudo tailscale funnel --bg 443 on
     ```
     เครื่องคอมของคุณจะได้รับลิงก์ HTTPS สาธารณะมา 1 ลิงก์ (เช่น `https://my-linux-pc.tailnet.ts.net`) ให้นำลิงก์นี้ไปใส่ในช่อง Server URL ของแอปมือถือ ก็จะใช้งานได้จากทั่วโลกอย่างปลอดภัย 100% ครับ!

---

## 📚 เอกสารอ้างอิงเพิ่มเติม
- คู่มือเริ่มต้นสำหรับ Windows 11: [Quick_start_Windows.md](Quick_start_Windows.md)
- เอกสารข้อกำหนดระบบฉบับเต็ม: [techdocs/system_spec_and_implementation_plan.md](techdocs/system_spec_and_implementation_plan.md)
- กฎการทำงานของทีม Agent: [AGENTS.md](AGENTS.md)
"""

with open(qs_linux, "w", encoding="utf-8") as f:
    f.write(linux_content)

print(f"Created Quick_start_Linux.md successfully ({len(linux_content)} chars).")
