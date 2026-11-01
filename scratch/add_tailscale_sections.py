# -*- coding: utf-8 -*-
import os

repo_root = r"c:\Ai_code\THLawDeka-mobile"
win_path = os.path.join(repo_root, "Quick_start_Windows.md")
linux_path = os.path.join(repo_root, "Quick_start_Linux.md")

# ==========================================
# Windows Updates
# ==========================================
with open(win_path, "r", encoding="utf-8") as f:
    win_content = f.read()

# 1. Update diagram in Windows
win_content = win_content.replace(
    "[ขั้นตอนที่ 2] ติดตั้ง 3 โปรแกรมจำเป็นบน Windows 11 (uv, Python 3.12, Android Studio)",
    "[ขั้นตอนที่ 2] ติดตั้ง 4 โปรแกรมจำเป็นบน Windows 11 (uv, Python 3.12, Android Studio, Tailscale)"
)

# 2. Add Section 2.4 in Windows
win_sec_24 = """---

### 🔹 2.4 ติดตั้งและเข้าสู่ระบบ Tailscale (ระบบเครือข่ายความปลอดภัยสำหรับต่อมือถือ)
1. ในหน้าต่าง Terminal ให้คัดลอกคำสั่งนี้ไปวาง แล้วกด **Enter**:
   ```powershell
   winget install --id Tailscale.Tailscale
   ```
   *(หรือดาวน์โหลดตัวติดตั้งได้จากเว็บไซต์ทางการ: [https://tailscale.com/download/windows](https://tailscale.com/download/windows))*
2. เมื่อติดตั้งเสร็จ ให้กดปุ่ม **Windows (⊞)** แล้วพิมพ์ `tailscale` เพื่อเปิดโปรแกรมขึ้นมา
3. คลิกไอคอน Tailscale ที่มุมล่างขวาของจอ (System Tray) แล้วเลือก **Log in...**
4. หน้าต่างเว็บเบราว์เซอร์จะเปิดขึ้นมา ให้ล็อกอินด้วยบัญชี Google หรือ Microsoft ของคุณให้เรียบร้อย
5. โปรแกรมจะขึ้นสถานะเชื่อมต่อสำเร็จ แปลว่าคอมพิวเตอร์ของคุณพร้อมเชื่อมต่อกับมือถือแล้วครับ!
"""

# Insert after Section 2.3
if "### 🔹 2.4 ติดตั้งและเข้าสู่ระบบ Tailscale" not in win_content:
    marker_win_23 = """> 📱 *หมายเหตุ: คุณไม่จำเป็นต้องมีโทรศัพท์ Android จริงก็ได้ เพราะ Android Studio มีเครื่องจำลองมือถือ (Emulator) ให้ใช้งานบนจอคอมพิวเตอร์ได้ฟรีทันทีครับ*"""
    win_content = win_content.replace(marker_win_23, marker_win_23 + "\n" + win_sec_24)

# 3. Add Section 7.2 (Tailscale HTTPS Setup) in Windows and renumber old 7.2 to 7.3
win_sec_72 = """---

### 🔹 7.2 เปิดใช้งานอุโมงค์ความปลอดภัย Tailscale HTTPS (เลือก Serve หรือ Funnel)

หลังจากเซิร์ฟเวอร์ Backend รันอยู่ที่พอร์ต 8000 ในข้อ 7.1 ให้เปิด Terminal ใหม่อีก 1 หน้าต่าง เพื่อสั่งให้ Tailscale ทำการเข้ารหัสและสร้างที่อยู่ HTTPS สำหรับเชื่อมต่อกับโทรศัพท์มือถือ:

> 💡 **เลือกระหว่าง 2 ทางเลือกตามลักษณะการใช้งาน:**

#### ทางเลือกที่ 1: Tailscale Serve (ปลอดภัยสูงสุดสำหรับใช้ส่วนบุคคล - Private Tailnet Mesh)
* เหมาะสำหรับกรณีที่คุณติดตั้งแอป **Tailscale** บนโทรศัพท์มือถือด้วย และล็อกอินด้วยบัญชีเดียวกัน
* คำสั่งเปิดใช้งาน:
  ```powershell
  tailscale serve --bg https / http://127.0.0.1:8000
  ```
* **ผลลัพธ์:** ปิดการเข้าถึงจากสาธารณะ 100% มีเพียงอุปกรณ์ในวง Tailnet ของคุณเท่านั้นที่เข้าถึงได้ โดยมีที่อยู่เป็นชื่อคอมพิวเตอร์ของคุณ เช่น `https://my-pc.tailnet.ts.net`

#### ทางเลือกที่ 2: Tailscale Funnel (สะดวกที่สุด - ไม่ต้องเปิด VPN บนมือถือ / Public HTTPS)
* เหมาะสำหรับกรณีที่ต้องการแชร์ให้เพื่อนใช้ หรือต้องการใช้เน็ต 4G/5G นอกบ้านโดย **ไม่ต้องติดตั้ง/เปิดแอป Tailscale บนมือถือ**
* คำสั่งเปิดใช้งาน:
  ```powershell
  tailscale funnel --bg 443 on
  ```
* **ผลลัพธ์:** คุณจะได้รับลิงก์ HTTPS สาธารณะ (เช่น `https://my-pc.tailnet.ts.net`) นำลิงก์นี้ไปใส่ในแอปมือถือใช้งานได้ทันทีจากทุกที่ทั่วโลก
* 🛡️ **ความปลอดภัย:** ระบบมี **IP Shielding** สกัดกั้นคนแปลกหน้าไม่ให้เข้าถึงหน้า `/admin` โดยอัตโนมัติ และคำขอเข้าห้องแชตทั้งหมดต้องมี API Key ที่ถูกต้องเท่านั้น

> 🔍 **ตรวจสอบสถานะ Tailscale:** สามารถพิมพ์คำสั่ง `tailscale serve status` เพื่อดูลิงก์ HTTPS ปัจจุบันได้ตลอดเวลา"""

win_content = win_content.replace(
    "### 🔹 7.2 เปิดแอปใน Android Studio และเริ่มใช้งานบนมือถือ",
    win_sec_72 + "\n\n---\n\n### 🔹 7.3 เปิดแอปใน Android Studio และเริ่มใช้งานบนมือถือ"
)

# Update reference in Settings step
win_content = win_content.replace(
    "- *หากต่อจากนอกบ้านผ่าน 4G/5G:* ให้ใส่ลิงก์ HTTPS ของ Tailscale Funnel (เช่น `https://my-pc.tailnet.ts.net`)",
    "- *หากต่อผ่าน Tailscale (Serve หรือ Funnel ในข้อ 7.2):* ให้ใส่ลิงก์ HTTPS ของคุณ เช่น `https://my-pc.tailnet.ts.net`"
)

with open(win_path, "w", encoding="utf-8") as f:
    f.write(win_content)
print("Updated Quick_start_Windows.md with Tailscale sections.")


# ==========================================
# Linux Updates
# ==========================================
with open(linux_path, "r", encoding="utf-8") as f:
    linux_content = f.read()

# 1. Update diagram in Linux
linux_content = linux_content.replace(
    "[ขั้นตอนที่ 2] ติดตั้งเครื่องมือจำเป็นบน Linux (curl, uv, Python 3.12, Android Studio)",
    "[ขั้นตอนที่ 2] ติดตั้งเครื่องมือจำเป็นบน Linux (curl, uv, Python 3.12, Android Studio, Tailscale)"
)

# 2. Add Section 2.4 in Linux
linux_sec_24 = """---

### 🔹 2.4 ติดตั้งและเข้าสู่ระบบ Tailscale (ระบบเครือข่ายความปลอดภัยสำหรับต่อมือถือ)
1. ใน Terminal ให้ติดตั้ง Tailscale ด้วยสคริปต์ทางการ:
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   ```
2. เริ่มต้นและเปิดการทำงานของ Service:
   ```bash
   sudo systemctl enable --now tailscaled
   ```
3. รันคำสั่งล็อกอินเข้าสู่ระบบ Tailscale:
   ```bash
   sudo tailscale up
   ```
   *(หน้าจอจะแสดงลิงก์ยืนยันตัวตน เช่น `https://login.tailscale.com/a/...` ให้คัดลอกไปเปิดในเว็บเบราว์เซอร์ แล้วล็อกอินด้วยบัญชี Google หรือ Microsoft ของคุณ)*
4. ตรวจสอบสถานะการเชื่อมต่อด้วยคำสั่ง:
   ```bash
   tailscale status
   ```
   *(จะเห็นชื่อเครื่อง Linux ของคุณและไอพีในวง Tailnet เป็นอันเสร็จสิ้นเรียบร้อย)*
"""

if "### 🔹 2.4 ติดตั้งและเข้าสู่ระบบ Tailscale" not in linux_content:
    marker_linux_23 = """> 📱 *หมายเหตุ: หากคุณไม่มีโทรศัพท์มือถือจริง คุณสามารถเปิดใช้งานเครื่องจำลอง **Android Emulator (Virtual Device)** บนหน้าจอคอมพิวเตอร์ผ่าน Android Studio ได้ฟรีทันทีโดยไม่ต้องตั้งค่าสาย USB ใด ๆ ครับ*"""
    linux_content = linux_content.replace(marker_linux_23, marker_linux_23 + "\n" + linux_sec_24)

# 3. Add Section 7.2 (Tailscale HTTPS Setup) in Linux and renumber old 7.2 to 7.3
linux_sec_72 = """---

### 🔹 7.2 เปิดใช้งานอุโมงค์ความปลอดภัย Tailscale HTTPS (เลือก Serve หรือ Funnel)

หลังจากเซิร์ฟเวอร์ Backend รันอยู่ที่พอร์ต 8000 ในข้อ 7.1 ให้เปิด Terminal ใหม่อีก 1 หน้าต่าง เพื่อสั่งให้ Tailscale ทำการเข้ารหัสและสร้างที่อยู่ HTTPS สำหรับเชื่อมต่อกับโทรศัพท์มือถือ:

> 💡 **เลือกระหว่าง 2 ทางเลือกตามลักษณะการใช้งาน:**

#### ทางเลือกที่ 1: Tailscale Serve (ปลอดภัยสูงสุดสำหรับใช้ส่วนบุคคล - Private Tailnet Mesh)
* เหมาะสำหรับกรณีที่คุณติดตั้งแอป **Tailscale** บนโทรศัพท์มือถือด้วย และล็อกอินด้วยบัญชีเดียวกัน
* คำสั่งเปิดใช้งาน:
  ```bash
  sudo tailscale serve --bg https / http://127.0.0.1:8000
  ```
* **ผลลัพธ์:** ปิดการเข้าถึงจากสาธารณะ 100% มีเพียงอุปกรณ์ในวง Tailnet ของคุณเท่านั้นที่เข้าถึงได้ โดยมีที่อยู่เป็นชื่อคอมพิวเตอร์ของคุณ เช่น `https://my-linux-pc.tailnet.ts.net`

#### ทางเลือกที่ 2: Tailscale Funnel (สะดวกที่สุด - ไม่ต้องเปิด VPN บนมือถือ / Public HTTPS)
* เหมาะสำหรับกรณีที่ต้องการแชร์ให้เพื่อนใช้ หรือต้องการใช้เน็ต 4G/5G นอกบ้านโดย **ไม่ต้องติดตั้ง/เปิดแอป Tailscale บนมือถือ**
* คำสั่งเปิดใช้งาน:
  ```bash
  sudo tailscale funnel --bg 443 on
  ```
* **ผลลัพธ์:** คุณจะได้รับลิงก์ HTTPS สาธารณะ (เช่น `https://my-linux-pc.tailnet.ts.net`) นำลิงก์นี้ไปใส่ในแอปมือถือใช้งานได้ทันทีจากทุกที่ทั่วโลก
* 🛡️ **ความปลอดภัย:** ระบบมี **IP Shielding** สกัดกั้นคนแปลกหน้าไม่ให้เข้าถึงหน้า `/admin` โดยอัตโนมัติ และคำขอเข้าห้องแชตทั้งหมดต้องมี API Key ที่ถูกต้องเท่านั้น

> 🔍 **ตรวจสอบสถานะ Tailscale:** สามารถพิมพ์คำสั่ง `sudo tailscale serve status` เพื่อดูลิงก์ HTTPS ปัจจุบันได้ตลอดเวลา"""

linux_content = linux_content.replace(
    "### 🔹 7.2 เปิดแอปใน Android Studio และเริ่มใช้งานบนมือถือ",
    linux_sec_72 + "\n\n---\n\n### 🔹 7.3 เปิดแอปใน Android Studio และเริ่มใช้งานบนมือถือ"
)

# Update reference in Settings step
linux_content = linux_content.replace(
    "- *หากต่อจากนอกบ้านผ่านเน็ต 4G/5G:* ให้ใส่ลิงก์ HTTPS ของ Tailscale Funnel (เช่น `https://my-linux-pc.tailnet.ts.net`)",
    "- *หากต่อผ่าน Tailscale (Serve หรือ Funnel ในข้อ 7.2):* ให้ใส่ลิงก์ HTTPS ของคุณ เช่น `https://my-linux-pc.tailnet.ts.net`"
)

with open(linux_path, "w", encoding="utf-8") as f:
    f.write(linux_content)
print("Updated Quick_start_Linux.md with Tailscale sections.")
