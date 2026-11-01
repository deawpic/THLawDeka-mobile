import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Check for file:// scheme
assert "file://" not in content, "Found file:// scheme in README.md"

# Check relative links
links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
for text, link in links:
    if link.startswith("http") or link.startswith("#"):
        continue
    target = link.split("#")[0]
    if target:
        assert os.path.exists(target), f"Broken relative link: {target} (from {link})"

print("✓ README.md passed all link and portability checks!")

# Check mermaid blocks
mermaid_blocks = re.findall(r"```mermaid\s+(.*?)\s+```", content, re.DOTALL)
print(f"✓ Found {len(mermaid_blocks)} valid Mermaid diagram(s) in README.md")
for i, block in enumerate(mermaid_blocks, 1):
    header = block.strip().splitlines()[0]
    assert header in ["flowchart TD", "flowchart LR", "graph TD", "graph LR", "sequenceDiagram"], f"Invalid mermaid header: {header}"
    print(f"  - Diagram {i}: {header} valid.")
