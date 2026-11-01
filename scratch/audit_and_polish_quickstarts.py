# -*- coding: utf-8 -*-
import os
import re

repo_root = r"c:\Ai_code\THLawDeka-mobile"
win_path = os.path.join(repo_root, "Quick_start_Windows.md")
linux_path = os.path.join(repo_root, "Quick_start_Linux.md")

def polish_file(file_path, is_linux=False):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Clean double horizontal rules (--- \n\n ---)
    content = re.sub(r'---\s*\n\s*---\s*\n', '---\n\n', content)
    content = re.sub(r'---\s*\n\s*\n\s*---\s*\n', '---\n\n', content)

    # 2. Fix dangling separator between Question 6 and Question 7 in Troubleshooting
    content = re.sub(r'(6\.\s+\*\*ถาม:[\s\S]*?\n\n)---\s*\n\s*(7\.\s+\*\*ถาม:)', r'\1\2', content)

    # 3. Polish Step 7 in the overview diagram
    old_step7_win = "[ขั้นตอนที่ 7] เปิดรันเซิร์ฟเวอร์ และเปิดแอปในมือถือ (หรือ Emulator) เพื่อเริ่มใช้งานจริง!"
    new_step7_win = "[ขั้นตอนที่ 7] รันเซิร์ฟเวอร์, เปิดอุโมงค์ Tailscale HTTPS, และเปิดแอปเพื่อใช้งานจริง!"
    content = content.replace(old_step7_win, new_step7_win)

    old_step7_linux = "[ขั้นตอนที่ 7] เปิดรันเซิร์ฟเวอร์ และเปิดแอปใน Android Studio (Emulator หรือมือถือจริง)"
    new_step7_linux = "[ขั้นตอนที่ 7] รันเซิร์ฟเวอร์, เปิดอุโมงค์ Tailscale HTTPS, และเปิดแอปเพื่อใช้งานจริง!"
    content = content.replace(old_step7_linux, new_step7_linux)

    # 4. Ensure trailing clean single newline
    content = content.strip() + "\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Polished {os.path.basename(file_path)}")

polish_file(win_path, is_linux=False)
polish_file(linux_path, is_linux=True)
