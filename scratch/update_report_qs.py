# -*- coding: utf-8 -*-
report_path = r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

old_sec = """## 15. การยกระดับ QUICK_START.md สู่คู่มือฉบับจับมือทำสำหรับมือใหม่ (Newbie-Proof Step-by-Step on Windows 11)

เพื่อขจัดอุปสรรคของผู้เริ่มต้นที่ไม่มีพื้นฐานการเขียนโปรแกรมมาก่อน ได้ทำการตรวจสอบและเสริมความละเอียดของ [QUICK_START.md](QUICK_START.md) ให้เป็นคู่มือแบบ Click-by-Click ที่ไม่มีจุดสะดุด โดยครอบคลุมประเด็นสำคัญดังนี้:"""

new_sec = """## 15. การจัดทำคู่มือ Quick Start แยกเฉพาะระบบปฏิบัติการ: Windows 11 และ Linux

เพื่อขจัดอุปสรรคของผู้เริ่มต้นที่ไม่มีพื้นฐานการเขียนโปรแกรมมาก่อน ได้ทำการปรับเปลี่ยนและจัดทำคู่มือเริ่มต้นฉบับจับมือทำ (Newbie-Proof Step-by-Step) แยกเฉพาะตามระบบปฏิบัติการเป็น 2 ฉบับอย่างชัดเจน ได้แก่ [Quick_start_Windows.md](Quick_start_Windows.md) และ [Quick_start_Linux.md](Quick_start_Linux.md) โดยมีรายละเอียดสำคัญดังนี้:"""

if old_sec in text:
    text = text.replace(old_sec, new_sec)
    text = text.replace("[QUICK_START.md](QUICK_START.md)", "[Quick_start_Windows.md](Quick_start_Windows.md)")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Report updated successfully.")
else:
    print("old_sec not found directly, checking...")
