import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Section 3.4.10
sec349_target = """  - เมื่อผู้ใช้แตะ Retry: แอปจะส่งคำขอเดิมอีกครั้งโดยแนบ `conversation_id` เดิมไปยัง Gateway ทำให้ Core Agent สามารถวิเคราะห์ต่อจากบริบทเดิมได้โดยไม่ต้องพิมพ์ข้อเท็จจริงคดีซ้ำ

---

### 3.5 โมดูลระบบจัดการกุญแจและหน้าจอผู้ดูแลระบบ (Admin Key Management & Web UI Spec)"""

sec3410_addition = """  - เมื่อผู้ใช้แตะ Retry: แอปจะส่งคำขอเดิมอีกครั้งโดยแนบ `conversation_id` เดิมไปยัง Gateway ทำให้ Core Agent สามารถวิเคราะห์ต่อจากบริบทเดิมได้โดยไม่ต้องพิมพ์ข้อเท็จจริงคดีซ้ำ

### 3.4.10 ข้อกำหนดการเลือกและสลับโมเดล AI บน Android (Top App Bar Model Switcher & BottomSheet Spec)
เพื่อมอบประสบการณ์การใช้งาน (Mobile UX) ระดับพรีเมียมเทียบชั้นแอปพลิเคชันอย่าง ChatGPT และ Claude ฝั่ง Android Client จะมีระบบจัดการโมเดลดังนี้:
1. **Top App Bar Quick Model Switcher**:
   - บน Header หน้าจอแชตหลัก (ใต้ชื่อห้องแชต) จะมี Component ปุ่ม Chip แสดงชื่อโมเดลปัจจุบัน เช่น `[ ⚡ Gemini 3.8 Flash ▾ ]`
   - เมื่อผู้ใช้แตะ จะเปิด **`ModelSelectionBottomSheet`** ลอยขึ้นมาจากขอบจอด้านล่าง แสดงรายการโมเดลทั้งหมดพร้อม Badge จุดเด่นและคำอธิบายสั้น ๆ
   - เมื่อแตะเลือกโมเดลใหม่ ตัวแอปจะอัปเดต State และใช้โมเดลนั้นสำหรับคำถามถัดไปทันที
2. **Dynamic Model Discovery & Offline Fallback**:
   - เมื่อเปิดแอปและเชื่อมต่อ Gateway สำเร็จ แอปจะเรียก `GET /api/v1/models` เพื่อดึงรายชื่อโมเดลล่าสุดมาแคชไว้ในเครื่อง
   - หากอยู่ในสถานะออฟไลน์ แอปจะมีชุด Fallback Models ฝังในโค้ด เพื่อให้ผู้ใช้ยังคงเปิดดูและเลือกโมเดลเตรียมไว้ได้
3. **การบันทึกประวัติโมเดลในฐานข้อมูล SQLite ในเครื่อง (`ChatDatabaseHelper.kt`)**:
   - ตาราง `chat_sessions` เพิ่มคอลัมน์ `selected_model TEXT DEFAULT 'gemini-3.8-flash-high'` เพื่อจำว่าห้องแชตนี้ใช้โมเดลใด
   - ตาราง `chat_messages` เพิ่มคอลัมน์ `model_used TEXT` เพื่อให้ในแต่ละบอลลูนคำตอบ สามารถแสดงป้ายกำกับขนาดเล็ก (Badge) เช่น *"ตอบโดย Claude Sonnet 4.6"* ช่วยให้ทนายความสามารถตรวจสอบย้อนหลังได้ว่าข้อกฎหมายนี้วิเคราะห์โดย AI ตัวใด

---

### 3.5 โมดูลระบบจัดการกุญแจและหน้าจอผู้ดูแลระบบ (Admin Key Management & Web UI Spec)"""

if "### 3.4.10" not in content:
    assert sec349_target in content, "sec349_target not found"
    content = content.replace(sec349_target, sec3410_addition, 1)
    print("✓ Added Section 3.4.10")

# 2. Add Section 3.8
sec375_target = """  - **ผลลัพธ์:** ประหยัดหน่วยความจำ RAM บนอุปกรณ์มือถือไป 50–80 MB ในห้องสนทนาทั่วไปที่ไม่มีแผนผังกระบวนการศาล

---

## 4. แหล่งโค้ดต้นแบบสำหรับการนำไปสร้างจริง (Reference Implementation Code)"""

sec38_addition = """  - **ผลลัพธ์:** ประหยัดหน่วยความจำ RAM บนอุปกรณ์มือถือไป 50–80 MB ในห้องสนทนาทั่วไปที่ไม่มีแผนผังกระบวนการศาล

---

### 3.8 ข้อกำหนดระบบเลือกโมเดลปัญญาประดิษฐ์ (Multi-Model Selection Architecture & Whitelist Spec)

ระบบ THLawDeka-mobile รองรับการเลือกและสลับโมเดล AI ในระดับเซสชันหรือคำขอ เพื่อให้ทนายความและผู้ใช้งานสามารถเลือกขุมพลังที่เหมาะสมกับลักษณะคดีความ (เช่น งานค้นหาฎีกาทั่วไปเน้นความเร็ว หรือ คดีซับซ้อนเน้นการคิดวิเคราะห์เชิงลึก) โดยมีสถาปัตยกรรมกำกับดังนี้:

#### 3.8.1 รายการโมเดลที่ผ่านการรับรอง (Supported Models Whitelist)
เกตเวย์จะควบคุมโมเดลผ่าน Whitelist ที่ตรวจสอบความถูกต้อง 100% ป้องกันการส่ง Flag หรือคำสั่งแปลกปลอมเข้า CLI:

| Model ID | ชื่อทางการ (Display Name) | ประเภท (Category) | ป้ายกำกับ (Badge) | คำอธิบายคุณสมบัติ (Capabilities) |
| :--- | :--- | :--- | :--- | :--- |
| **`gemini-3.8-flash-high`** | Gemini 3.8 Flash (High) | Fast | แนะนำ / เร็วสุด | ค่าเริ่มต้น (Default) ความเร็วสูง ความแม่นยำทางกฎหมายยอดเยี่ยม เหมาะสำหรับการค้นหาฎีกาเทียบเคียงทั่วไป |
| **`gemini-3.8-flash-medium`** | Gemini 3.8 Flash (Medium) | Fast | สมดุล | ประมวลผลรวดเร็ว สมดุลระหว่างทรัพยากรและคุณภาพ เหมาะกับคดีแพ่ง-อาญาทั่วไป |
| **`gemini-3.8-flash-low`** | Gemini 3.8 Flash (Low) | Eco | ประหยัดโควตา | ประหยัดทรัพยากรและโควตาสูงสุด เหมาะกับคำถามสั้นหรือตรวจเลขมาตรา |
| **`claude-sonnet-4-6`** | Claude Sonnet 4.6 (Thinking) | Thinking | วิเคราะห์ลึก | มีกระบวนการคิดวิเคราะห์ (Reasoning Process) เชิงลึก เหมาะกับการวางรูปคดีความซับซ้อนและการร่างข้อต่อสู้ |
| **`claude-opus-4-6-thinking`** | Claude Opus 4.6 (Thinking) | Thinking | ปัญญาสูงสุด | โมเดลปัญญาสูงสุดสำหรับการตีความข้อกฎหมายระดับสูง คดีรัฐธรรมนูญ และข้อพิพาททางธุรกิจมูลค่าสูง |
| **`gpt-oss-120b-medium`** | GPT-OSS 120B (Medium) | OpenSource | Open Weights | โมเดลแบบเปิดประสิทธิภาพสูง สำหรับการค้นคว้ามุมมองเปรียบเทียบและการประมวลผลอิสระ |

#### 3.8.2 มาตรการป้องกัน CLI Flag Injection สำหรับ Model ID
เพื่อป้องกันผู้ไม่ประสงค์ดีส่งค่าพารามิเตอร์แปลกปลอมเข้าคำสั่ง `agy --model <model>` ผ่านทาง Gateway:
1. **Regex Validation**: ต้องตรงตามนิพจน์ปกติ `^[a-zA-Z0-9][a-zA-Z0-9._\\-]{0,63}$` ห้ามมีช่องว่าง, อักขระพิเศษ, หรือเครื่องหมายขีดหน้าคู่ (`--`) เด็ดขาด
2. **Whitelist Membership**: ค่า Model ID ที่ส่งเข้ามาต้องอยู่ในชุด `VALID_MODELS` เท่านั้น หากไม่ระบุหรือส่งค่าว่าง ระบบจะกำหนดให้เป็น `gemini-3.8-flash-high` เสมอ
3. **Safe Subprocess Argument Array**: ส่งผ่านรายการอาร์กิวเมนต์แบบ `shell=False` โดยเพิ่ม `cmd.extend(["--model", req.model])` อย่างเคร่งครัด

---

## 4. แหล่งโค้ดต้นแบบสำหรับการนำไปสร้างจริง (Reference Implementation Code)"""

if "### 3.8" not in content:
    assert sec375_target in content, "sec375_target not found"
    content = content.replace(sec375_target, sec38_addition, 1)
    print("✓ Added Section 3.8")

with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("✓ Saved updated spec with Section 3.8 and Section 3.4.10!")
