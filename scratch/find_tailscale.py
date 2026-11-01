import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
lines = spec_path.read_text(encoding="utf-8").splitlines()

for i, l in enumerate(lines, 1):
    if any(k in l.lower() for k in ["tailscale serve", "phase 3", "2.1 แผนผัง", "3.3 tailscale"]):
        print(f"Line {i}: {l[:120]}")
