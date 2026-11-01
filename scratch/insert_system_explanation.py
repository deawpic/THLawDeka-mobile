# -*- coding: utf-8 -*-
import os

repo_root = r"c:\Ai_code\THLawDeka-mobile"
win_path = os.path.join(repo_root, "Quick_start_Windows.md")
linux_path = os.path.join(repo_root, "Quick_start_Linux.md")

system_explanation = """---

## 🧠 สถาปัตยกรรมและหลักการทำงานของระบบ (System Architecture & How It Works)

ระบบ **THLawDeka-mobile** คือแพลตฟอร์มผู้ช่วยทนายความและที่ปรึกษากฎหมายไทยอัจฉริยะแบบพกพา ซึ่งออกแบบภายใต้แนวคิด **"ความปลอดภัยสูงสุด ข้อมูลส่วนตัวไม่รั่วไหล และตอบคำถามได้แบบเรียลไทม์"** โดยแบ่งการทำงานออกเป็น **4 ส่วนหลัก** ประสานงานกันอย่างราบรื่น:

```mermaid
flowchart LR
    subgraph Mobile["📱 1. Android Mobile App"]
        direction TB
        UI["Chat UI & GFM Tables"]
        LocalDB[("SQLite ประวัติแชต")]
        PDF["DocumentExportManager<br/>(ส่งออก PDF สารบรรณ A4)"]
        UI --- LocalDB
        UI --- PDF
    end

    subgraph Network["🔒 2. เครือข่ายเข้ารหัส (Tailscale)"]
        Tunnel["WireGuard HTTPS Tunnel<br/>(Tailscale Serve / Funnel :443)"]
    end

    subgraph Gateway["⚙️ 3. เซิร์ฟเวอร์ประตูคัดกรอง (FastAPI Gateway)"]
        direction TB
        AuthGate["Bearer Token & IP Shielding"]
        PreFilter["Anti-Prompt Injection"]
        FastCache[("Legal Cache (SHA-256)")]
        Reaper["Process Reaper (ตัดสายใน 60s)"]
        AuthGate --> PreFilter --> FastCache
    end

    subgraph Brain["⚖️ 4. สมองกลกฎหมาย (THLawDeka Core Agent)"]
        direction TB
        AgyCLI["Google Antigravity (agy CLI)"]
        Skills["กฎหมายอาญา / แพ่ง / ฎีกา"]
        AgyCLI --- Skills
    end

    Mobile <== "SSE Stream (คำต่อคำ)" ==> Tunnel
    Tunnel <== "Reverse Proxy :8000" ==> Gateway
    Gateway <== "Safe Stdin/Stdout Pipe" ==> Brain
```

### 🔍 หน้าที่ของแต่ละส่วนประกอบ:

1. **📱 ส่วนที่ 1: แอปพลิเคชันบนมือถือ (Android Client - Kotlin Native)**
   * **หน้าจอสนทนา (Real-time SSE Chat UI):** รับและแสดงผลข้อความวิเคราะห์กฎหมายแบบสตรีมมิ่งคำต่อคำ (Streaming Tokens) นุ่มนวล เสมือนมีผู้ช่วยพิมพ์ตอบสด ๆ
   * **การแสดงผลทางกฎหมาย:** แสดงผลตารางเปรียบเทียบมาตรากฎหมาย (GFM Tables) และแผนผังขั้นตอนคดีความ (Mermaid Chart) ผ่านระบบตัดคำภาษาไทยความคมชัดสูง (`BREAK_STRATEGY_HIGH_QUALITY`)
   * **บันทึกข้อมูลแบบออฟไลน์ 100%:** จัดการห้องสนทนา (แชตต่อของเดิม / สร้างแชตใหม่ / ลบแชต) เก็บลงฐานข้อมูล SQLite ในเครื่องมือถือ ไม่มีการส่งประวัติคดีความไปเก็บที่เซิร์ฟเวอร์
   * **ส่งออกเอกสารบนเครื่อง (Zero-Disk-Write Server):** ฟังก์ชัน `DocumentExportManager` แปลงบทสนทนาเป็นเอกสาร **PDF ฟอนต์สารบรรณขนาด A4 มาตรฐานราชการ**, ไฟล์ Markdown (`.md`), หรือข้อความ (`.txt`) และสั่งพิมพ์หรือแชร์ทาง LINE ได้ทันทีจากมือถือ โดยไม่ต้องขอให้เซิร์ฟเวอร์สร้างไฟล์

2. **🔒 ส่วนที่ 2: เครือข่ายอุโมงค์เข้ารหัส (Tailscale HTTPS Tunnel)**
   * เชื่อมต่อระหว่างโทรศัพท์มือถือกับเครื่องคอมพิวเตอร์ผ่านเครือข่ายส่วนตัวเสมือน (WireGuard Mesh) หรือต่อผ่านอินเทอร์เน็ตสาธารณะด้วย Tailscale Funnel พร้อมใบรับรองความปลอดภัย HTTPS
   * สามารถใช้งานแอปจากนอกบ้านผ่านสัญญาณเน็ต 4G/5G ได้ทันที โดย **ไม่ต้องตั้งค่าเร้าเตอร์หรือเปิดพอร์ตบ้าน (No Port Forwarding)**

3. **⚙️ ส่วนที่ 3: เซิร์ฟเวอร์ประตูคัดกรองความปลอดภัย (FastAPI Gateway & Pipe Controller)**
   * **ตรวจสอบสิทธิ์ฉับไว ($O(1)$ Token Cache):** ตรวจสอบ API Key ของมือถือในหน่วยความจำ RAM อย่างรวดเร็ว ป้องกันการยิงสแปม
   * **ระบบแคชคำถามกฎหมายยอดฮิต (Fast-Path Legal Cache):** หากมีคำถามเดิมที่เคยตอบไว้แล้ว ระบบจะส่งคำตอบกลับทันทีใน 0.05 วินาที โดยไม่ต้องปลุก AI
   * **เกราะป้องกันการเจาะระบบ (Gateway Pre-Filter):** ตรวจจับและสกัดกั้นคำสั่งแฮกหรือ Prompt Injection ก่อนส่งไปยังตัวประมวลผล
   * **ระบบบีบอัดข้อมูลอัจฉริยะ (Selective Gzip):** บีบอัดข้อมูลหน้าเว็บ Admin ประหยัดแบนด์วิดท์ 70-85% แต่ปล่อยเส้นทางสตรีมมิ่งสดให้วิ่งตรงโดยไม่ติดค้างบัฟเฟอร์
   * **Zombie Process Reaper:** หากมือถือปิดจอหรือสัญญาณเน็ตหลุด เซิร์ฟเวอร์จะสั่งตัดโปรเซส AI ทันที ไม่ปล่อยให้ทำงานค้างกินทรัพยากรคอมพิวเตอร์

4. **⚖️ ส่วนที่ 4: สมองกลกฎหมายไทย (THLawDeka Core Agent - Google Antigravity)**
   * ทำงานผ่านคำสั่ง `agy` CLI ในโหมดความปลอดภัยสูง (`--sandbox`)
   * มีทักษะและความรู้ความเชี่ยวชาญเฉพาะทาง (Specialized Skills) เช่น ประมวลกฎหมายอาญา ประมวลกฎหมายแพ่งและพาณิชย์ พระราชบัญญัติเฉพาะทาง และคลังแนวคำพิพากษาศาลฎีกา
   * รับคำถามกฎหมายผ่านท่อส่งข้อมูลมาตรฐาน (`stdin`) และวิเคราะห์ส่งคืนผลลัพธ์ผ่านท่อข้อมูล (`stdout`) โดยไม่มีการเปิดช่องโหว่รันคำสั่งเชลล์ภายนอก (Zero-Shell Execution)

---

### ⏱️ วงจรการทำงานตั้งแต่พิมพ์ถามจนได้คำตอบ (5 ขั้นตอน):
```text
[1] ผู้ใช้พิมพ์คำถามบนมือถือ (เช่น ปรึกษาเรื่องคดีเช่าบ้าน หรือ ม.341)
     ↓
[2] มือถือส่งคำถามผ่าน HTTPS พร้อม API Key เข้าสู่ Gateway
     ↓
[3] Gateway ตรวจสอบความปลอดภัย ตรวจสิทธิ์ และเช็กแคชคำตอบ
     ↓
[4] Gateway ส่งคำถามเข้าสมอง AI (agy) ผ่านท่อ Safe Stdin แบบปลอดภัย
     ↓
[5] สมอง AI สตรีมคำตอบส่งคืนถึงหน้าจอมือถือแบบ Real-time และกดบันทึกเป็น PDF ทันที
```
"""

def insert_system_explanation(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    target_marker = "## 🗂️ ขั้นตอนที่ 1:"
    if target_marker in content and "## 🧠 สถาปัตยกรรมและหลักการทำงานของระบบ" not in content:
        parts = content.split(target_marker)
        new_content = parts[0] + system_explanation + "\n---\n\n" + target_marker + parts[1]
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Inserted system explanation into {os.path.basename(file_path)}")
    else:
        print(f"Skipped {os.path.basename(file_path)} (already present or marker not found)")

insert_system_explanation(win_path)
insert_system_explanation(linux_path)
