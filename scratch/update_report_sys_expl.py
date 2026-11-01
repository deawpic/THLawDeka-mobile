# -*- coding: utf-8 -*-
report_path = r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("และ `QUICK_START.md` ทันที", "และ `Quick_start_Windows.md` / `Quick_start_Linux.md` ทันที")

addition = """9. **แผนภาพและคำอธิบายสถาปัตยกรรมการทำงานของระบบ (System Architecture & How It Works):**
   - เพิ่มแผนผัง Mermaid แสดงการเชื่อมโยงของ 4 องค์ประกอบหลัก: Android Client, Tailscale Encrypted Tunnel, FastAPI Gateway, และ THLawDeka Core Agent
   - อธิบายหน้าที่และฟังก์ชันเชิงลึกของแต่ละส่วน (Offline SQLite, Zero-Disk-Write PDF, Selective Gzip, Safe Stdin Pipe, O(1) Token Cache, Fast-Path Cache)
   - สรุปวงจรการทำงานตั้งแต่พิมพ์คำถามกฎหมายจนได้รับเอกสาร PDF ใน 5 ขั้นตอนเข้าใจง่าย
"""

if "9. **แผนภาพและคำอธิบายสถาปัตยกรรม" not in text:
    target = "8. **6 ปัญหาที่พบบ่อยและวิธีแก้ง่าย ๆ (Newbie Troubleshooting Receipts):**\n   - ครอบคลุมเคส PATH ไม่ขึ้น, `agy` หาไม่เจอ, AI ค้างรอปุ่ม Proceed, มือถือต่อ USB ไม่ติด, Connection Refused, และการใช้งานนอกบ้านด้วย Tailscale Funnel"
    replacement = target + "\n" + addition
    text = text.replace(target, replacement)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Report updated with point 9.")
else:
    print("Already present.")
