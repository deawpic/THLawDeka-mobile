# -*- coding: utf-8 -*-
report_path = r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md"

addition = """

---

## 15. การยกระดับ QUICK_START.md สู่คู่มือฉบับจับมือทำสำหรับมือใหม่ (Newbie-Proof Step-by-Step on Windows 11)

เพื่อขจัดอุปสรรคของผู้เริ่มต้นที่ไม่มีพื้นฐานการเขียนโปรแกรมมาก่อน ได้ทำการตรวจสอบและเสริมความละเอียดของ [QUICK_START.md](QUICK_START.md) ให้เป็นคู่มือแบบ Click-by-Click ที่ไม่มีจุดสะดุด โดยครอบคลุมประเด็นสำคัญดังนี้:

### 15.1 องค์ประกอบที่เสริมความละเอียดเป็นพิเศษ:
1. **คำแนะนำสำหรับผู้ส่งไฟล์ (Pre-Zip Checklist):**
   - เตือนให้ลบโฟลเดอร์ `backend/.venv` และ `__pycache__` ก่อนบีบอัดไฟล์ เพื่อให้ไฟล์ Zip มีขนาดเพียง 1–2 MB แทนที่จะเป็น 200+ MB
2. **การแตกไฟล์และตรวจสอบโฟลเดอร์ซ้อน (Anti-Nesting Inspection):**
   - ระบุจุดตรวจเช็กชัดเจนว่าเมื่อแตกไฟล์แล้วต้องเห็น `backend/`, `THLawDeka/`, `techdocs/`, และ `QUICK_START.md` ทันที หากพบโฟลเดอร์ชื่อเดียวกันซ้อนอีกชั้น ให้ใช้โฟลเดอร์ชั้นใน
3. **การติดตั้งเครื่องมือบน Windows 11 แบบไร้รอยต่อ (Zero-Friction Windows 11 Setup):**
   - คำสั่ง `winget install --id astral-sh.uv` พร้อมคำสั่งสำรองผ่าน PowerShell
   - การรีสตาร์ท Terminal เพื่อโหลด PATH
   - คำสั่ง `uv python install 3.12` อธิบายเหตุผลที่ไม่ต้องง้อ Microsoft Store และตัดปัญหาความไม่เข้ากันของแพ็กเกจ
4. **ทริคเปิด Terminal ในโฟลเดอร์ทันที (Address Bar Trick):**
   - คลิกพื้นที่ว่างบนแถบที่อยู่ด้านบน พิมพ์ `powershell` แล้วกด Enter ไม่ต้องเสียเวลาจำหรือพิมพ์คำสั่ง `cd`
5. **การทดสอบ `agy` CLI กฎหมาย:**
   - ใช้รูปแบบ `agy -p "..."` ขจัดปัญหา Encoding ภาษาไทยใน Windows PowerShell
6. **คำเตือนสำคัญสำหรับหน้าต่างขออนุมัติ AI (The "Proceed / Allow" Trap):**
   - ระบุชัดเจนว่าระหว่างที่ AI Agent กำลังทำงาน หากมีปุ่ม **"Proceed"**, **"Allow"**, หรือ **"Always Allow"** เด้งขึ้นมา ให้ผู้ใช้คลิกอนุมัติทันที เพื่อไม่ให้ AI หยุดค้างรอ
7. **คู่มือ Android Studio แบบ 2 ทางเลือก (Emulator vs มือถือจริง):**
   - **ทางเลือก A (Emulator):** รันบนจอคอมพิวเตอร์ผ่าน Virtual Device โดยใช้ Server URL `http://10.0.2.2:8000` (อธิบายความหมายของไอพี 10.0.2.2)
   - **ทางเลือก B (มือถือจริง):** แนะนำวิธีเปิดโหมดนักพัฒนา (แตะ Build Number 7 ครั้ง) และเปิด USB Debugging พร้อมวิธีหา IP ในบ้านด้วย `ipconfig`
8. **6 ปัญหาที่พบบ่อยและวิธีแก้ง่าย ๆ (Newbie Troubleshooting Receipts):**
   - ครอบคลุมเคส PATH ไม่ขึ้น, `agy` หาไม่เจอ, AI ค้างรอปุ่ม Proceed, มือถือต่อ USB ไม่ติด, Connection Refused, และการใช้งานนอกบ้านด้วย Tailscale Funnel
"""

with open(report_path, "a", encoding="utf-8") as f:
    f.write(addition)

print("Section 15 appended to agent_enhancement_report.md successfully.")
