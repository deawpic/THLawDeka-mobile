import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Target for Section 3.8
sec37_end_target = """### 3.7.5 การปรับแต่ง Tailscale Direct Connection & WebView Lazy Loading
1. **Tailscale Direct Mesh Connection**: ตรวจสอบสถานะ `tailscale ping <node-ip>` ให้เป็น DERP: direct เสมอ เพื่อลด Latency เหลือต่ำกว่า 15ms
2. **WebView Lazy Initialization**: ฝั่ง Android ให้โหลด WebView และไลบรารี `mermaid.min.js` ล่วงหน้าแบบ Background Pre-warming เพื่อให้เมื่อผู้ใช้เปิดอ่านชาร์ต ไม่เกิดอาการค้างหรือจอดำแม้แต่เสี้ยววินาที"""

sec38_content = """### 3.7.5 การปรับแต่ง Tailscale Direct Connection & WebView Lazy Loading
1. **Tailscale Direct Mesh Connection**: ตรวจสอบสถานะ `tailscale ping <node-ip>` ให้เป็น DERP: direct เสมอ เพื่อลด Latency เหลือต่ำกว่า 15ms
2. **WebView Lazy Initialization**: ฝั่ง Android ให้โหลด WebView และไลบรารี `mermaid.min.js` ล่วงหน้าแบบ Background Pre-warming เพื่อให้เมื่อผู้ใช้เปิดอ่านชาร์ต ไม่เกิดอาการค้างหรือจอดำแม้แต่เสี้ยววินาที

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
3. **Safe Subprocess Argument Array**: ส่งผ่านรายการอาร์กิวเมนต์แบบ `shell=False` โดยเพิ่ม `cmd.extend(["--model", req.model])` อย่างเคร่งครัด"""

assert sec37_end_target in content, "sec37_end_target not found"
print("✓ Found sec37_end_target")
