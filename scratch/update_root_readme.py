import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

target = """1. **Core Legal AI Intelligence ([`THLawDeka/`](THLawDeka/))**: เอเจนต์ปัญญาประดิษฐ์บน **Google Antigravity CLI / Python SDK** พร้อมทักษะการดึงข้อเท็จจริง (Legal Fact Elicitation), ตัวตรวจสอบเลขฎีกาป้องกันข้อมูลหลอน (Anti-Hallucination Citation Verifier), และระบบแคชแบบ L1/L2 Memory-to-Disk Compression"""

replacement = """1. **Core Legal AI Intelligence — Mobile Engine Edition ([`THLawDeka/`](THLawDeka/))**: ปัญญาประดิษฐ์วิเคราะห์ข้อกฎหมายเวอร์ชันปรับแต่งพิเศษเฉพาะสำหรับทำงานร่วมกับ Mobile Client Gateway (สื่อสารผ่าน Safe stdin, ปฏิเสธการรันคำสั่ง OS/Shell ตามกฎ Zero-Shell, และปฏิบัติตามนโยบาย Server-Side Zero-Disk-Write โดยส่งผลลัพธ์ผ่านสตรีมเพื่อให้แอปพลิเคชันมือถือนำไปเรนเดอร์และส่งออกไฟล์บนตัวเครื่อง 100%) แยกสายการพัฒนาเป็นเอกเทศจากเวอร์ชัน Desktop CLI"""

assert target in content, "Target not found in root README.md"
new_content = content.replace(target, replacement, 1)

with open("README.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(new_content)

print("✓ Successfully updated root README.md!")
