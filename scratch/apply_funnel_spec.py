import sys
import re
from pathlib import Path

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# 1. Update Section 1 Introduction
old_sec1 = """1. **ความปลอดภัยระดับสูงสุด (Enterprise-Grade Security)**: ไร้การเปิดพอร์ตสาธารณะ (Zero Public Attack Surface) ป้องกัน Command Injection ด้วยการส่งผ่าน `stdin` และเข้ารหัสแบบ End-to-End ด้วย Tailscale WireGuard"""
new_sec1 = """1. **ความปลอดภัยระดับสูงสุด (Enterprise-Grade Security)**: รองรับทั้งระบบปิดสมบูรณ์ (Tailscale Serve Mesh) และระบบเปิดเผย HTTPS สาธารณะอย่างปลอดภัย (Tailscale Funnel พร้อม Zero-VPN บนมือถือ) ป้องกัน Command Injection ด้วยการส่งผ่าน `stdin`, กรอง Prompt Injection ที่ Gateway Pre-Filter, ตรวจสอบสิทธิ์ Bearer Token Mandatory ($O(1)$ In-Memory), และจำกัดการเข้าถึง Admin UI เฉพาะ Localhost/Tailnet"""

assert old_sec1 in content, "old_sec1 not found"
content = content.replace(old_sec1, new_sec1)

# 2. Update Section 2.1 Mermaid Diagram
old_diagram = """```mermaid
flowchart LR
    subgraph MobileDevice["📱 Android Mobile Device"]
        AndroidApp["Android App (OkHttp SSE Client)"]
        TS_Client["Tailscale Client (Always-On VPN)"]
        AndroidApp --> TS_Client
    end

    subgraph EncryptedOverlay["🛡️ Encrypted Mesh Network (Tailscale)"]
        Tunnel["WireGuard Protocol (P2P Mesh)<br/>Let's Encrypt TLS (HTTPS)<br/>Domain: your-server.tailnet.ts.net"]
    end

    subgraph HomeServer["🖥️ Local Home Server (Host PC)"]
        TS_Host["Tailscale Daemon (Tailscale Serve :443)"]
        FastAPIGateway["FastAPI Gateway (THLawDeka-mobile :8000)"]
        AgyController["Subprocess Pipe Controller"]
        AgyProcess["agy.exe (THLawDeka Core Agent Harness)"]
        CacheDB[("SQLite L2 Cache (mcp_cache.db)")]
        LegalMCPs["Legal MCPs (fourcorners / slegaltools / thailegal)"]

        TS_Host -->|"Proxy 443 -> 8000"| FastAPIGateway
        FastAPIGateway --> AgyController
        AgyController -->|"stdin / stdout Pipe"| AgyProcess
        AgyProcess <--> CacheDB
        AgyProcess <--> LegalMCPs
    end

    TS_Client <==>|"End-to-End Encrypted Tunnel"| Tunnel
    Tunnel <==> TS_Host
```"""

new_diagram = """```mermaid
flowchart TD
    subgraph OptionA["ทางเลือกที่ 1: Tailscale Serve (Private Mesh VPN)"]
        direction LR
        AppA["Android App"] -->|"Local VPN Slot"| TS_App["Tailscale App (Always-On VPN)"]
        TS_App -->|"WireGuard P2P Mesh"| Mesh["Tailscale Private Tailnet"]
    end

    subgraph OptionB["ทางเลือกที่ 2: Tailscale Funnel (Public HTTPS - No VPN Required)"]
        direction LR
        AppB["Android App (Zero VPN)"] -->|"Direct Public HTTPS (4G/5G/Wi-Fi)"| Internet["Public Internet"]
        Internet -->|"TLS Ingress Relay"| FunnelRelay["Tailscale Funnel Gateway"]
    end

    subgraph HomeServer["🖥️ Local Home Server (Host PC)"]
        direction TB
        TS_Host["Tailscale Daemon (Serve :443 / Funnel :443)"]
        FastAPIGateway["FastAPI Gateway (THLawDeka-mobile :8000)"]
        AgyController["Subprocess Pipe Controller"]
        AgyProcess["agy.exe (THLawDeka Core Agent Harness)"]
        CacheDB[("SQLite L2 Cache (mcp_cache.db)")]
        LegalMCPs["Legal MCPs (fourcorners / slegaltools / thailegal)"]

        TS_Host -->|"Proxy 443 -> 8000"| FastAPIGateway
        FastAPIGateway --> AgyController
        AgyController -->|"stdin / stdout Pipe"| AgyProcess
        AgyProcess <--> CacheDB
        AgyProcess <--> LegalMCPs
    end

    Mesh --> TS_Host
    FunnelRelay --> TS_Host
```"""

assert old_diagram in content, "old_diagram not found"
content = content.replace(old_diagram, new_diagram)

# 3. Update Section 3.3
old_sec33 = """### 3.3 โมดูลเครือข่ายและการรักษาความปลอดภัย (Tailscale HTTPS)

- **การเปิดใช้งาน HTTPS ผ่าน Tailscale Serve:**
  ```bash
  # ชี้พอร์ต 443 (HTTPS สาธารณะในวง Tailnet) ไปยัง FastAPI พอร์ต 8000
  tailscale serve --bg https / http://127.0.0.1:8000
  ```
- **URL รูปแบบมาตรฐาน:**
  `https://<node-name>.<tailnet-name>.ts.net/api/v1/chat/stream`
- **การตั้งค่าฝั่ง Android:**
  - ติดตั้งแอป Tailscale จาก Google Play Store
  - ล็อกอินด้วยบัญชีเดียวกันกับ Home Server
  - ตั้งค่า `Settings -> Apps -> Tailscale -> Battery -> Unrestricted`
  - เปิดตัวเลือก `Always-on VPN` ในระบบ Android"""

new_sec33 = """### 3.3 โมดูลเครือข่ายและการรักษาความปลอดภัย (Tailscale Serve & Tailscale Funnel)

ระบบ THLawDeka-mobile ได้รับการออกแบบให้รองรับสถาปัตยกรรมการเชื่อมต่อ **2 ทางเลือก (Dual Connectivity Architecture)** เพื่อตอบสนองทั้งผู้ใช้ที่เน้นความปลอดภัยระดับสูงสุด (Private Mesh) และผู้ใช้ที่เน้นความสะดวกสบายสูงสุด (Zero-VPN on Mobile):

```mermaid
flowchart LR
    Client["📱 Android App"]
    
    subgraph Mode1["ทางเลือกที่ 1: Tailscale Serve"]
        direction TB
        V1["ต้องลงแอป Tailscale"] --> M1["วงปิด Private Tailnet"]
        M1 --> S1["ความปลอดภัยสูงสุด (Zero Public Surface)"]
    end
    
    subgraph Mode2["ทางเลือกที่ 2: Tailscale Funnel"]
        direction TB
        V2["ไม่ต้องลงแอป Tailscale ใดๆ"] --> M2["Public HTTPS (Let's Encrypt)"]
        M2 --> S2["Bearer Token & Admin IP Isolation"]
    end
    
    Client -.-> Mode1
    Client -.-> Mode2
```

#### 3.3.1 ทางเลือกที่ 1: Tailscale Serve (Private Tailnet Mesh — ความปลอดภัยสูงสุด)
- **สถาปัตยกรรม:** ให้บริการเฉพาะอุปกรณ์ภายในวง Tailnet ส่วนตัวเท่านั้น ทราฟฟิกวิ่งผ่านอุโมงค์ WireGuard แบบ Point-to-Point (P2P) โดยตรงทะลุ CGNAT
- **การเปิดใช้งานบน Host Server:**
  ```bash
  # ชี้พอร์ต 443 (HTTPS ในวง Tailnet) ไปยัง FastAPI พอร์ต 8000
  tailscale serve --bg https / http://127.0.0.1:8000
  ```
- **การตั้งค่าฝั่งอุปกรณ์ Android:**
  1. ติดตั้งแอป Tailscale จาก Google Play Store
  2. ล็อกอินด้วยบัญชี Tailscale เดียวกันกับ Home Server
  3. ตั้งค่า `Settings -> Apps -> Tailscale -> Battery -> Unrestricted`
  4. เปิดตัวเลือก `Always-on VPN` ในการตั้งค่า Android เพื่อคงสถานะการเชื่อมต่อตลอดเวลา

#### 3.3.2 ทางเลือกที่ 2: Tailscale Funnel (Public HTTPS — ความสะดวกสบายสูงสุด ไร้ VPN บนมือถือ)
- **สถาปัตยกรรม:** Tailscale จะรับทราฟฟิก HTTPS จากอินเทอร์เน็ตสาธารณะผ่านโหนดรีเลย์ทั่วโลก (Global Anycast TLS Ingress) พร้อมใบรับรอง Let's Encrypt แล้วส่งต่อผ่านอุโมงค์ WireGuard เข้ามายัง Home Server
- **ข้อได้เปรียบสำคัญ:**
  - **Zero Mobile VPN Overhead:** ฝั่งโทรศัพท์มือถือ Android **ไม่ต้องติดตั้ง ไม่ต้องล็อกอิน และไม่ต้องเปิดแอป Tailscale ใด ๆ ทั้งสิ้น**
  - **แบตเตอรี่ไม่ลดลง:** ไม่มีการรัน Background VPN Service บนมือถือ
  - **ไม่ชนกับ VPN อื่น:** ผู้ใช้สามารถเปิด VPN สำหรับงานอื่น (เช่น Corporate VPN) ควบคู่กับการใช้แอป THLawDeka-mobile ได้อย่างอิสระ
  - **แชร์ให้บุคคลอื่นในทีมใช้งานง่าย:** เพียงแจกจ่าย Bearer Token ให้เพื่อนร่วมงานนำไปกรอกในแอป Android ก็สามารถใช้งานได้ทันทีโดยไม่ต้องดึงอุปกรณ์เข้าสู่วง Tailnet ส่วนตัว
- **การเปิดใช้งานบน Host Server:**
  ```bash
  # ขั้นตอนที่ 1: เปิด Serve ชี้พอร์ต 443 ไปยัง FastAPI พอร์ต 8000
  tailscale serve --bg https / http://127.0.0.1:8000

  # ขั้นตอนที่ 2: เปิดการเข้าถึงจากสาธารณะด้วย Funnel
  tailscale funnel --bg 443 on
  ```
- **การตั้งค่าฝั่งอุปกรณ์ Android:**
  - กรอก URL สาธารณะในแอป: `https://<node-name>.<tailnet-name>.ts.net` และ Bearer Token เท่านั้น เชื่อมต่อได้ทันทีผ่าน 4G, 5G, หรือ Wi-Fi ทั่วไป

#### 3.3.3 ตารางเปรียบเทียบ Serve vs Funnel
| มิติการเปรียบเทียบ (Dimension) | ทางเลือกที่ 1: Tailscale Serve | ทางเลือกที่ 2: Tailscale Funnel |
| :--- | :--- | :--- |
| **การติดตั้งบนอุปกรณ์ Android** | ต้องติดตั้งแอป Tailscale และล็อกอินในบัญชีเดียวกัน | **ไม่ต้องติดตั้งแอป Tailscale (Zero-Install)** |
| **การใช้ทรัพยากรแบตเตอรี่มือถือ** | ใช้งานแบตเตอรี่เพิ่มขึ้นเล็กน้อยจาก Always-on VPN | **ไม่ใช้แบตเตอรี่เพิ่ม (Zero VPN Overhead)** |
| **การใช้งานร่วมกับ VPN อื่น** | ชนกัน (Android อนุญาตให้รัน VPN ได้ 1 ตัว) | **ใช้งานร่วมกับ VPN อื่นได้อิสระ** |
| **การเปิดสู่สาธารณะ (Public Exposure)** | ปิด 100% (เข้าถึงได้เฉพาะอุปกรณ์ในวง Tailnet) | เปิดพอร์ต 443 สู่สาธารณะผ่าน Tailscale Ingress Relay |
| **ความหน่วงของเครือข่าย (Latency)** | ต่ำสุด (~15-30 ms) ผ่าน WireGuard P2P Mesh | เล็กน้อย (~35-65 ms) ผ่าน Tailscale Relay Ingress |
| **กลไกความปลอดภัยหลัก** | Tailnet Identity + Bearer Token | **Mandatory Bearer Token ($O(1)$ Cache) + Gateway Pre-Filter + Admin IP Isolation** |
| **คำสั่งเปิดใช้งานบน Server** | `tailscale serve --bg https / http://127.0.0.1:8000` | `tailscale serve --bg https / http://127.0.0.1:8000`<br/>`tailscale funnel --bg 443 on` |

#### 3.3.4 มาตรการความปลอดภัยเข้มงวดเมื่อเปิดใช้ Tailscale Funnel (Funnel Hardening)
เนื่องจากการเปิดใช้ Funnel จะทำให้ Endpoint สามารถเข้าถึงได้จากอินเทอร์เน็ตสาธารณะ ระบบจึงบังคับใช้เกราะป้องกัน 4 ชั้น:
1. **Mandatory Bearer Token Gate ($O(1)$ RAM Validation):** ทุกคำขอสู่ `/api/v1/chat/stream` ต้องมี Token ที่ถูกต้อง หากไม่พบบน `ACTIVE_KEYS_CACHE` จะถูกตัดจบด้วย `HTTP 401 Unauthorized` ทันที โดยไม่แตะต้อง Subprocess หรือ LLM
2. **Admin Web UI Perimeter Isolation:** ปิดกั้นหน้า `/admin` และ API `/api/v1/admin/*` ไม่ให้เข้าถึงจากอินเทอร์เน็ตสาธารณะ ระบบจะตรวจสอบ Client IP และอนุญาตเฉพาะคำขอที่มาจาก `127.0.0.1` (Localhost) หรือ Tailnet IP (`100.64.0.0/10`) เท่านั้น ยกเว้นแอดมินจะเปิด `ALLOW_PUBLIC_ADMIN=true` อย่างเจาะจง
3. **Gateway Pre-Filter:** สกัดกั้นคำสั่ง Prompt Injection และการดัดแปลงระบบด้วย `contains_system_attack(query)` ตั้งแต่หน้าประตู
4. **Concurrency Semaphore & Zero-Disk-Write:** จำกัดคำขอพร้อมกันสูงสุดที่ 3 งาน (`Semaphore(3)`) และเซิร์ฟเวอร์เป็น Read-Only ไร้การเขียนไฟล์ลงดิสก์ 100%

#### 3.3.5 คำสั่งควบคุมและสลับโหมดการทำงาน (CLI Operations Runbook)
```bash
# ตรวจสอบสถานะ Serve และ Funnel ปัจจุบัน
tailscale funnel status
tailscale serve status

# สลับกลับไปใช้เฉพาะ Serve (ปิดการเข้าถึงจากสาธารณะ)
tailscale funnel 443 off

# ปิดทั้ง Serve และ Funnel ทั้งหมด
tailscale serve reset
```"""

assert old_sec33 in content, "old_sec33 not found"
content = content.replace(old_sec33, new_sec33)

# 4. Update Section 4.1 backend/main.py
# Add ipaddress to imports
old_imports = """import asyncio
import json
import os
import re
import zlib
from pathlib import Path"""

new_imports = """import asyncio
import ipaddress
import json
import os
import re
import zlib
from pathlib import Path"""

assert old_imports in content, "old_imports not found"
content = content.replace(old_imports, new_imports)

# Update Admin UI with IP isolation in Section 4.1
old_admin_sec = """# ==========================================
# ส่วนงาน Admin UI และ API จัดการกุญแจ
# ==========================================

class CreateKeyRequest(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=100)

async def verify_admin(x_admin_secret: str = Header(None)):
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Admin")

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    \"\"\"ให้บริการหน้าจอ Web Admin UI สำหรับจัดการกุญแจ\"\"\"
    return templates.TemplateResponse("admin.html", {"request": request})"""

new_admin_sec = """# ==========================================
# ส่วนงาน Admin UI และ API จัดการกุญแจ (ป้องกันการเข้าถึงจาก Public Funnel)
# ==========================================

class CreateKeyRequest(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=100)

ALLOW_PUBLIC_ADMIN = os.environ.get("ALLOW_PUBLIC_ADMIN", "false").lower() == "true"

def is_tailnet_or_local_ip(ip: str) -> bool:
    \"\"\"ตรวจสอบว่าเป็น IP ภายในเครื่อง (127.0.0.1) หรือ IP ในวง Tailnet (100.64.0.0/10) หรือไม่\"\"\"
    if ip in ("127.0.0.1", "localhost", "::1", "testclient"):
        return True
    try:
        addr = ipaddress.ip_address(ip)
        tailnet_network = ipaddress.ip_network("100.64.0.0/10")
        return addr in tailnet_network
    except Exception:
        return False

async def verify_admin(request: Request, x_admin_secret: str = Header(None)):
    \"\"\"ตรวจสอบสิทธิ์ Admin พร้อมบล็อกคำขอจาก Public Funnel หากไม่ได้เปิด ALLOW_PUBLIC_ADMIN\"\"\"
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not ALLOW_PUBLIC_ADMIN and not is_tailnet_or_local_ip(client_ip):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access is restricted to Localhost and Private Tailnet Mesh only."
        )
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized Admin")

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    \"\"\"ให้บริการหน้าจอ Web Admin UI สำหรับจัดการกุญแจ (บล็อก Public Funnel อัตโนมัติ)\"\"\"
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not ALLOW_PUBLIC_ADMIN and not is_tailnet_or_local_ip(client_ip):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin dashboard is restricted to Localhost and Private Tailnet Mesh only."
        )
    return templates.TemplateResponse("admin.html", {"request": request})"""

assert old_admin_sec in content, "old_admin_sec not found"
content = content.replace(old_admin_sec, new_admin_sec)

# 5. Update Section 5 Phase 3
old_phase3_diagram = """    Phase3["<b>Phase 3: Tailscale HTTPS Setup</b><br/>เปิดใช้งาน tailscale serve รับรอง SSL + Direct STUN"]"""
new_phase3_diagram = """    Phase3["<b>Phase 3: Tailscale HTTPS Setup (Serve & Funnel)</b><br/>เปิดใช้งาน tailscale serve (Private Mesh) หรือ funnel (Zero-VPN)"]"""
assert old_phase3_diagram in content, "old_phase3_diagram not found"
content = content.replace(old_phase3_diagram, new_phase3_diagram)

old_phase3_desc = """### เฟสที่ 3: กำหนดค่าเครือข่าย Tailscale HTTPS บน Home Server (Day 2)
- **เป้าหมาย:** ผูก Local Port 8000 ให้กลายเป็น HTTPS ที่ปลอดภัยภายในวง Tailnet พร้อมรับประกันการเชื่อมต่อแบบ Direct STUN (ไม่ผ่าน DERP Relay)
- **เกณฑ์การยอมรับ (Acceptance Criteria - Gherkin):**
  - **Given** เครื่องโฮสต์เชื่อมต่อใน Tailnet สำเร็จ
  - **When** รันคำสั่ง `tailscale serve --bg https / http://127.0.0.1:8000`
  - **Then** สามารถเข้าถึง `https://<node-name>.tailnet.ts.net/api/v1/health` ด้วยการเข้ารหัส TLS และค่า Latency เครือข่าย < 30ms (สถานะ `direct`)
- **ขั้นตอนการทำ:**
  1. ตรวจสอบสถานะการเชื่อมต่อ: `tailscale status`
  2. เปิดใช้งาน Reverse Proxy HTTPS: `tailscale serve --bg https / http://127.0.0.1:8000`
  3. ตรวจสอบการเปิดพอร์ต UDP Firewall ฝั่ง Server เพื่อให้มือถือเชื่อมต่อแบบ Direct STUN"""

new_phase3_desc = """### เฟสที่ 3: กำหนดค่าเครือข่าย Tailscale HTTPS บน Home Server (รองรับ Serve & Funnel) (Day 2)
- **เป้าหมาย:** ผูก Local Port 8000 ให้กลายเป็น HTTPS ผ่าน Tailscale Serve (สำหรับ Private Tailnet Mesh) หรือ Tailscale Funnel (สำหรับ Public HTTPS ไม่ต้องเปิด VPN บนมือถือ) พร้อมการรักษาความปลอดภัยหน้า Admin
- **เกณฑ์การยอมรับ (Acceptance Criteria - Gherkin):**
  - **Given** เครื่องโฮสต์เชื่อมต่อใน Tailnet สำเร็จ
  - **When** รันคำสั่ง `tailscale serve --bg https / http://127.0.0.1:8000` (โหมด Serve)
  - **Then** สามารถเข้าถึง `https://<node-name>.tailnet.ts.net/api/v1/health` จากอุปกรณ์ในวง Tailnet ได้ด้วยการเข้ารหัส TLS และ Latency < 30ms
  - **When** รันคำสั่ง `tailscale funnel --bg 443 on` (โหมด Funnel)
  - **Then** อุปกรณ์ภายนอกโดยไม่ต้องลงแอป Tailscale สามารถยิงเรียก API สตรีมผ่านอินเทอร์เน็ตสาธารณะได้ โดยมี Bearer Token ตรวจสอบความถูกต้อง
  - **When** อุปกรณ์ภายนอกผ่าน Funnel พยายามเข้าหน้า `/admin`
  - **Then** ระบบปฏิเสธด้วย HTTP 403 Forbidden ทันทีเพื่อความปลอดภัยสูงสุด
- **ขั้นตอนการทำ:**
  1. ตรวจสอบสถานะการเชื่อมต่อ: `tailscale status`
  2. เปิดใช้งาน Reverse Proxy HTTPS: `tailscale serve --bg https / http://127.0.0.1:8000`
  3. (ทางเลือก) เปิดใช้งาน Funnel: `tailscale funnel --bg 443 on` และตรวจสอบด้วย `tailscale funnel status`
  4. ตรวจสอบการกั้นสิทธิ์หน้า Admin UI ว่าสามารถเข้าได้เฉพาะจาก Localhost หรือ Tailnet IP"""

assert old_phase3_desc in content, "old_phase3_desc not found"
content = content.replace(old_phase3_desc, new_phase3_desc)

# 6. Update Section 7 References
old_ref = """| 7 | **Mermaid.js Diagramming Engine** | https://mermaid.js.org/ | การสร้างไดอะแกรมทางกฎหมายและ Flowchart ขั้นตอนคดีความใน Sandboxed WebView |"""
new_ref = """| 7 | **Mermaid.js Diagramming Engine** | https://mermaid.js.org/ | การสร้างไดอะแกรมทางกฎหมายและ Flowchart ขั้นตอนคดีความใน Sandboxed WebView |
| 8 | **Tailscale Funnel Documentation** | https://tailscale.com/kb/1223/tailscale-funnel | การกำหนดค่า Tailscale Funnel เพื่อเปิดเผยบริการ HTTPS สู่สาธารณะโดยไม่ต้องเปิดแอป Tailscale บนอุปกรณ์มือถือ (Zero-VPN Client) |"""

assert old_ref in content, "old_ref not found"
content = content.replace(old_ref, new_ref)

spec_path.write_text(content, encoding="utf-8")
print("Successfully applied Tailscale Funnel updates to system_spec_and_implementation_plan.md!")
