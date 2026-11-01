# -*- coding: utf-8 -*-
import os

repo_root = r"c:\Ai_code\THLawDeka-mobile"
win_path = os.path.join(repo_root, "Quick_start_Windows.md")
linux_path = os.path.join(repo_root, "Quick_start_Linux.md")

for p in [win_path, linux_path]:
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()

    # Enhance Part 1
    target_part1 = "   * **ส่งออกเอกสารบนเครื่อง (Zero-Disk-Write Server):** ฟังก์ชัน `DocumentExportManager` แปลงบทสนทนาเป็นเอกสาร **PDF ฟอนต์สารบรรณขนาด A4 มาตรฐานราชการ**, ไฟล์ Markdown (`.md`), หรือข้อความ (`.txt`) และสั่งพิมพ์หรือแชร์ทาง LINE ได้ทันทีจากมือถือ โดยไม่ต้องขอให้เซิร์ฟเวอร์สร้างไฟล์"
    replacement_part1 = target_part1 + "\n   * **ค้นหาคดีความออฟไลน์และกู้คืนสตรีม:** รองรับ **SQLite FTS5 Full-Text Search** ค้นหาคำสำคัญในฎีกาเก่าได้ทันทีแม้อยู่ในห้องพิจารณาคดีที่ไม่มีสัญญาณเน็ต พร้อมระบบ **Partial Stream Recovery** บันทึกคำตอบบางส่วนและถามต่อได้ทันทีหากสัญญาณหลุด"

    if target_part1 in text and "SQLite FTS5 Full-Text Search" not in text:
        text = text.replace(target_part1, replacement_part1, 1)

    # Enhance Part 3
    target_part3 = "   * **Zombie Process Reaper:** หากมือถือปิดจอหรือสัญญาณเน็ตหลุด เซิร์ฟเวอร์จะสั่งตัดโปรเซส AI ทันที ไม่ปล่อยให้ทำงานค้างกินทรัพยากรคอมพิวเตอร์"
    replacement_part3 = target_part3 + """\n   * **Zero-PII Audit Logging:** บันทึกเฉพาะเมทริกซ์เชิงตัวเลข (เวลา, ขนาดไบต์, รหัสสถานะ) **ห้ามบันทึกข้อเท็จจริงคดีหรือคำถาม/คำตอบลง Disk Log เด็ดขาด** เพื่อจรรยาบรรณวิชาชีพและ PDPA\n   * **Per-Key Rate Limiting:** จำกัดความถี่ไม่เกิน 10 คำขอ/นาทีต่อกุญแจ ป้องกันการสแปมคิว AI (Semaphore)\n   * **Automated SQLite Backup:** สำรองข้อมูล `keys.db` อัตโนมัติแบบ Online Backup ย้อนหลัง 7 ชุด\n   * **Long-Context Budgeting:** ส่งสัญญาณเตือนเมื่อบริบทคดีสะสมเกิน 64KB เพื่อแนะนำให้ย่อสรุปด้วย `/compact` หรือเปิดห้องแชตใหม่"""

    if target_part3 in text and "Zero-PII Audit Logging" not in text:
        text = text.replace(target_part3, replacement_part3, 1)

    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated highlights in {os.path.basename(p)}")
