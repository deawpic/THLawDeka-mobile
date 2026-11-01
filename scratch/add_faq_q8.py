import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Update Quick_start_Windows.md
with open("Quick_start_Windows.md", "r", encoding="utf-8") as f:
    win_content = f.read()

target_win_header = "## ❓ 7 ปัญหาที่พบบ่อยและวิธีแก้ง่าย ๆ (Troubleshooting)"
replacement_win_header = "## ❓ 8 ปัญหาที่พบบ่อยและวิธีแก้ง่าย ๆ (Troubleshooting & FAQ)"

target_win_q7 = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** หากคุณไม่ได้ตั้งรหัสผ่านเอง สามารถเปิดดูรหัสผ่านสุ่มที่ระบบสร้างไว้ในไฟล์ `backend/.admin_secret` หรือหากต้องการเปลี่ยนรหัสผ่านใหม่ ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์เดิม แล้วสั่งเปิดใหม่พร้อมระบุรหัสผ่านใหม่ได้ทันที:
     ```powershell
     $env:ADMIN_SECRET="รหัสผ่านใหม่ของคุณ"; uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```"""

replacement_win_q7_and_q8 = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** หากคุณไม่ได้ตั้งรหัสผ่านเอง สามารถเปิดดูรหัสผ่านสุ่มที่ระบบสร้างไว้ในไฟล์ `backend/.admin_secret` หรือหากต้องการเปลี่ยนรหัสผ่านใหม่ ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์เดิม แล้วสั่งเปิดใหม่พร้อมระบุรหัสผ่านใหม่ได้ทันที:
     ```powershell
     $env:ADMIN_SECRET="รหัสผ่านใหม่ของคุณ"; uv run uvicorn main:app --host 127.0.0.1 --port 8000
     ```

8. **ถาม: เมื่อรีบูตคอมพิวเตอร์ (Reboot / Restart) หรือเปิดเครื่องใหม่ จะต้องคอยล็อกอินบัญชี Google (`agy`) ในเซิร์ฟเวอร์ใหม่หรือไม่? จะใช้งานได้ตลอดไปไหม?**
   * **ตอบ:** **ไม่ต้องล็อกอินใหม่แน่นอนครับ!** เมื่อคุณล็อกอินผ่าน Antigravity Desktop หรือ `agy` สำเร็จในครั้งแรก ระบบจะบันทึกกุญแจยืนยันตัวตนถาวร (OAuth 2.0 Refresh Token) เก็บไว้ในฮาร์ดดิสก์ของคุณ (`$env:USERPROFILE\\.gemini`) อย่างถาวร แม้คุณจะปิดคอมพิวเตอร์ สั่ง Restart หรือไฟดับแล้วเปิดใหม่ เมื่อมีคำถามส่งมาจากมือถือ ตัว `agy` จะอ่านกุญแจถาวรมาขอ Access Token ใหม่ในเบื้องหลังให้อัตโนมัติในเสี้ยววินาที (Silent Auto-Refresh) โดยไม่มีหน้าต่างเบราว์เซอร์เด้งกวนใจ คุณจึงสามารถตั้งค่าเซิร์ฟเวอร์ครั้งเดียวแล้วปล่อยรันยาว ๆ แบบ Set-and-Forget ได้เลยครับ
   *(กรณีเดียวที่อาจต้องแวะมาล็อกอินใหม่ คือเมื่อคุณมีการเปลี่ยนรหัสผ่าน Google Account ด้วยตนเอง หรือทิ้งเครื่องไว้โดยไม่มีการใช้งานเลยเกิน 6 เดือนเท่านั้นครับ)*"""

assert target_win_header in win_content, "target_win_header not found"
assert target_win_q7 in win_content, "target_win_q7 not found"

win_content = win_content.replace(target_win_header, replacement_win_header, 1)
win_content = win_content.replace(target_win_q7, replacement_win_q7_and_q8, 1)

with open("Quick_start_Windows.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(win_content)

print("✓ Successfully updated Quick_start_Windows.md with FAQ Q8!")

# 2. Update Quick_start_Linux.md
with open("Quick_start_Linux.md", "r", encoding="utf-8") as f:
    linux_content = f.read()

target_linux_header = "## ❓ 7 ปัญหาที่พบบ่อยบน Linux และวิธีแก้ง่าย ๆ (Troubleshooting)"
replacement_linux_header = "## ❓ 8 ปัญหาที่พบบ่อยบน Linux และวิธีแก้ง่าย ๆ (Troubleshooting & FAQ)"

target_linux_q7 = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** หากคุณไม่ได้ตั้งรหัสผ่านเอง สามารถเปิดดูรหัสผ่านสุ่มที่ระบบสร้างไว้ในไฟล์ `backend/.admin_secret` (หรือรัน `cat backend/.admin_secret`) หรือหากต้องการเปลี่ยนรหัสผ่านใหม่ ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์เดิม แล้วสั่งเปิดใหม่พร้อมระบุรหัสผ่านใหม่ได้ทันที:
     ```bash
     ADMIN_SECRET="รหัสผ่านใหม่ของคุณ" uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```"""

replacement_linux_q7_and_q8 = """7. **ถาม: ลืมรหัสผ่าน Admin หรืออยากเปลี่ยนรหัสผ่าน Backend Admin ต้องทำอย่างไร?**
   * **ตอบ:** หากคุณไม่ได้ตั้งรหัสผ่านเอง สามารถเปิดดูรหัสผ่านสุ่มที่ระบบสร้างไว้ในไฟล์ `backend/.admin_secret` (หรือรัน `cat backend/.admin_secret`) หรือหากต้องการเปลี่ยนรหัสผ่านใหม่ ให้กด `Ctrl + C` ปิดเซิร์ฟเวอร์เดิม แล้วสั่งเปิดใหม่พร้อมระบุรหัสผ่านใหม่ได้ทันที:
     ```bash
     ADMIN_SECRET="รหัสผ่านใหม่ของคุณ" uv run uvicorn main:app --host 0.0.0.0 --port 8000
     ```

8. **ถาม: เมื่อรีบูตเซิร์ฟเวอร์ Linux (Reboot / Restart) จะต้องคอยล็อกอินบัญชี Google (`agy`) ใหม่หรือไม่? จะใช้งานได้ตลอดไปไหม?**
   * **ตอบ:** **ไม่ต้องล็อกอินใหม่แน่นอนครับ!** เมื่อคุณล็อกอินผ่าน `agy` ในครั้งแรกสำเร็จ กุญแจยืนยันตัวตนถาวร (OAuth 2.0 Refresh Token) จะถูกบันทึกไว้ใน Home Directory ของคุณ (`~/.gemini`) อย่างถาวร เมื่อเซิร์ฟเวอร์บูตใหม่และเปิด Service `thlaw-gateway.service` (ซึ่งทำงานภายใต้สิทธิ์ User ของคุณ) ตัว `agy` จะอ่าน Refresh Token มาต่ออายุ Access Token ในเบื้องหลังให้อัตโนมัติ (Silent Auto-Refresh) ทันทีที่มีคำถามเข้ามา คุณจึงปล่อยเซิร์ฟเวอร์รันยาว ๆ แบบ Set-and-Forget ได้โดยไม่ต้องคอยรีโมตมาล็อกอินใหม่ครับ
   *(กรณีเดียวที่อาจต้องแวะมาล็อกอินใหม่ คือเมื่อคุณมีการเปลี่ยนรหัสผ่าน Google Account ด้วยตนเอง หรือไม่มีการเรียกใช้งานเลยเกิน 6 เดือนเท่านั้นครับ)*"""

assert target_linux_header in linux_content, "target_linux_header not found"
assert target_linux_q7 in linux_content, "target_linux_q7 not found"

linux_content = linux_content.replace(target_linux_header, replacement_linux_header, 1)
linux_content = linux_content.replace(target_linux_q7, replacement_linux_q7_and_q8, 1)

with open("Quick_start_Linux.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(linux_content)

print("✓ Successfully updated Quick_start_Linux.md with FAQ Q8!")
