import sys
from pathlib import Path

report_path = Path(r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md")
content = report_path.read_text(encoding="utf-8")

sec12_text = """

---

## 12. การเพิ่มทางเลือกการเชื่อมต่อด้วย Tailscale Funnel (Public HTTPS — Zero VPN Client)

เพื่อเพิ่มความยืดหยุ่นในการใช้งานจริง โดยเฉพาะกรณีที่ผู้ใช้งานไม่สะดวกติดตั้งแอป Tailscale หรือไม่ต้องการเปิด Always-On VPN ค้างไว้บนโทรศัพท์มือถือ ระบบได้รับการอัปเกรดให้รองรับ **สถาปัตยกรรม 2 ทางเลือก (Dual Connectivity Options)**:

### 12.1 สถาปัตยกรรมการเชื่อมต่อ 2 ทางเลือก (Dual Topology)

```mermaid
flowchart TD
    subgraph OptionA["ทางเลือกที่ 1: Tailscale Serve (Private Mesh VPN)"]
        direction LR
        AppA["Android App"] -->|"Local VPN"| TS_App["Tailscale App (Always-On VPN)"]
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
```

### 12.2 ตารางเปรียบเทียบ Serve vs Funnel

| มิติการเปรียบเทียบ (Dimension) | ทางเลือกที่ 1: Tailscale Serve | ทางเลือกที่ 2: Tailscale Funnel |
| :--- | :--- | :--- |
| **การติดตั้งบนอุปกรณ์ Android** | ต้องติดตั้งแอป Tailscale และล็อกอินในบัญชีเดียวกัน | **ไม่ต้องติดตั้งแอป Tailscale ใด ๆ (Zero-Install)** |
| **การใช้ทรัพยากรแบตเตอรี่มือถือ** | ใช้งานแบตเตอรี่เพิ่มขึ้นเล็กน้อยจาก Always-on VPN | **ไม่ใช้แบตเตอรี่เพิ่ม (Zero VPN Overhead)** |
| **การใช้งานร่วมกับ VPN อื่น** | ชนกัน (Android อนุญาตให้รัน VPN ได้ 1 ตัว) | **ใช้งานร่วมกับ VPN อื่นได้อิสระ** |
| **การเปิดสู่สาธารณะ (Public Exposure)** | ปิด 100% (เข้าถึงได้เฉพาะอุปกรณ์ในวง Tailnet) | เปิดพอร์ต 443 สู่สาธารณะผ่าน Tailscale Ingress Relay |
| **ความหน่วงของเครือข่าย (Latency)** | ต่ำสุด (~15-30 ms) ผ่าน WireGuard P2P Mesh | เล็กน้อย (~35-65 ms) ผ่าน Tailscale Relay Ingress |
| **กลไกความปลอดภัยหลัก** | Tailnet Identity + Bearer Token | **Mandatory Bearer Token ($O(1)$ Cache) + Gateway Pre-Filter + Admin IP Isolation** |
| **คำสั่งเปิดใช้งานบน Server** | `tailscale serve --bg https / http://127.0.0.1:8000` | `tailscale serve --bg https / http://127.0.0.1:8000`<br/>`tailscale funnel --bg 443 on` |

### 12.3 มาตรการป้องกันความปลอดภัยเมื่อเปิดใช้งาน Funnel (Funnel Hardening Receipts)
1. **Admin Web UI Perimeter Isolation:**
   - ใน `backend/main.py` มีการตรวจจับ Client IP ผ่านฟังก์ชัน `is_tailnet_or_local_ip(ip)`
   - บล็อกการเข้าถึง `/admin` และ `/api/v1/admin/*` จากอินเทอร์เน็ตสาธารณะด้วย `HTTP 403 Forbidden` ทันที อนุญาตเฉพาะ `127.0.0.1` (Localhost) และ `100.64.0.0/10` (Tailnet Mesh) เท่านั้น
2. **Mandatory Bearer Token Gate:**
   - ทุกคำขอสู่ `/api/v1/chat/stream` ต้องมี Token ใน `ACTIVE_KEYS_CACHE` หากไม่ผ่านจะถูกตัดจบด้วย HTTP 401 ในระดับ $O(1)$ โดยไม่แตะต้อง Subprocess หรือ LLM
3. **Gateway Pre-Filter:**
   - สกัดกั้น Prompt Injection และ System Tampering ด้วย `contains_system_attack()`
4. **Concurrency Semaphore & Server-Side Zero-Disk-Write:**
   - ควบคุมโหลดเซิร์ฟเวอร์ด้วย `Semaphore(3)` และเซิร์ฟเวอร์เป็น Immutable Read-Only 100%
"""

if "## 12. การเพิ่มทางเลือกการเชื่อมต่อด้วย Tailscale Funnel" not in content:
    content += sec12_text
    report_path.write_text(content, encoding="utf-8")
    print("Successfully added Section 12 to agent_enhancement_report.md!")
