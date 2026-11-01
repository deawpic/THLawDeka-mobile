import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("THLawDeka/README.md", "r", encoding="utf-8") as f:
    content = f.read()

target = """# Thai Legal Intelligence Advisor (AGY Project - Harness v3.0) ⚖️
**ผู้ช่วยผู้เชี่ยวชาญด้านกฎหมายไทยและทนายความผู้มีความรอบรู้ (Thai Legal Intelligence Advisor)**

**Ai Agent**  สำหรับคำปรึกษาทางกฎหมายไทยใช้งานกับ **Google Antigravity Desktop/CLI** ที่สมบูรณ์ พร้อมระบบ **Agent Harness v3.0 (Enterprise Caching & Resilience Edition)** ที่ผสาน:"""

replacement = """# Thai Legal Intelligence Advisor (AGY Project - Mobile Engine Edition) ⚖️📱
**ผู้ช่วยผู้เชี่ยวชาญด้านกฎหมายไทยและทนายความผู้มีความรอบรู้ (เวอร์ชันปรับแต่งพิเศษเฉพาะสำหรับ Mobile Client)**

> [!NOTE]
> **🌟 ข้อสังเกตสำคัญ (Dedicated Mobile Engine Edition):**
> โฟลเดอร์ `THLawDeka` ในโครงการนี้เป็น **เวอร์ชันปรับแต่งพิเศษเฉพาะสำหรับทำงานร่วมกับ Mobile Client และ FastAPI ASGI Gateway** ในโครงการ `THLawDeka-mobile` ซึ่งได้รับการแยกสายการพัฒนาจากเวอร์ชัน Standalone Desktop CLI โดยมีคุณลักษณะเฉพาะดังนี้:
> 1. **Server-Side Zero-Disk-Write Policy**: ปิดการสร้างหรือบันทึกไฟล์ลงบนดิสก์ของเซิร์ฟเวอร์ โดยส่งผลลัพธ์ผ่าน Standard Output (`stdout`) แบบสตรีมมิง เพื่อให้ Mobile Client นำไปบันทึกและเรนเดอร์เอกสาร A4 PDF บนตัวเครื่อง 100%
> 2. **Zero-Shell & RCE Immunity Gate**: ปฏิเสธการรันคำสั่ง OS/Shell ทุกชนิด และบล็อกคำสั่งสร้างไฟล์สคริปต์ เพื่อความปลอดภัยสูงสุดในการให้บริการผ่านระบบเครือข่าย
> 3. **Mobile-Optimized Output**: ปรับจูนการตอบกลับในรูปแบบ Markdown Table (GFM) และ Mermaid Flowchart เพื่อให้แสดงผลได้อย่างคมชัด สวยงาม บนหน้าจอสมาร์ตโฟนผ่าน Markwon และ Sandboxed WebView
> 4. **Safe Stdin Communication**: สื่อสารกับเกตเวย์ผ่านทางท่อ `stdin` อย่างรัดกุม ปราศจากช่องโหว่ Argument Injection

**Ai Agent**  สำหรับคำปรึกษาทางกฎหมายไทยใช้งานกับ **Google Antigravity Desktop/CLI** ที่สมบูรณ์ พร้อมระบบ **Agent Harness v3.0 (Enterprise Caching & Resilience Edition)** ที่ผสาน:"""

assert target in content, "Target not found!"
new_content = content.replace(target, replacement, 1)

with open("THLawDeka/README.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(new_content)

print("✓ Successfully updated THLawDeka/README.md!")
