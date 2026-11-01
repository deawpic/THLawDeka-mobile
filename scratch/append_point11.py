# -*- coding: utf-8 -*-
report_path = r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md"

addition = """11. **การติดตั้งและตั้งค่าเครือข่ายความปลอดภัย Tailscale (Tailscale Installation & Dual Topology Configuration):**
    - เพิ่มขั้นตอนที่ 2.4: ติดตั้งและล็อกอิน Tailscale ผ่าน Winget (Windows) และสคริปต์ทางการ `curl -fsSL https://tailscale.com/install.sh | sh` พร้อมคำสั่ง `sudo tailscale up` (Linux)
    - เพิ่มขั้นตอนที่ 7.2: คำสั่งเปิดใช้งานอุโมงค์เข้ารหัส HTTPS แบบแยก 2 ทางเลือก:
      * **Tailscale Serve:** สำหรับ Private Tailnet Mesh ปลอดภัยสูงสุด 0 Public Exposure
      * **Tailscale Funnel:** สำหรับ Public HTTPS ไม่ต้องเปิด VPN บนมือถือ พร้อมระบบ IP Shielding กั้นหน้า Admin
    - ปรับปรุงขั้นตอนที่ 7.3 ในแอปมือถือให้นำลิงก์ Tailscale HTTPS ไปใส่ในช่อง Server URL ใช้งานได้จริงจากนอกบ้านผ่าน 4G/5G
"""

with open(report_path, "a", encoding="utf-8") as f:
    f.write(addition)

print("Added point 11 to agent_enhancement_report.md.")
