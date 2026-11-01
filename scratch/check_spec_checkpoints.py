# -*- coding: utf-8 -*-
import os

spec_path = r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md"

with open(spec_path, "r", encoding="utf-8") as f:
    spec_content = f.read()

# Verify that insertion points exist
assert "#### 3.7.5 การปรับแต่ง Tailscale Direct Connection" in spec_content
assert "## 4. แหล่งโค้ดต้นแบบสำหรับการนำไปสร้างจริง" in spec_content
assert "def purge_expired_cache(self) -> int:" in spec_content

print("All assertion checkpoints found in spec.")
