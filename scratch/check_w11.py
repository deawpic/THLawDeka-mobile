import sys
from pathlib import Path

qs_path = Path("QUICK_START.md")
content = qs_path.read_text(encoding="utf-8")

# Let's check how winget is described
print("Has winget:", "winget install" in content)
