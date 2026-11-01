import re
from pathlib import Path

# 1. Fix QUICK_START.md
qs_path = Path("QUICK_START.md")
qs_content = qs_path.read_text(encoding="utf-8")

# Replace file:///... with relative path
qs_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*techdocs/([^)]+)\)", r"[\1](techdocs/\2)", qs_content)
qs_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*THLawDeka/([^)]+)\)", r"[\1](THLawDeka/\2)", qs_content)
qs_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*AGENTS\.md\)", r"[\1](AGENTS.md)", qs_content)
qs_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*QUICK_START\.md\)", r"[\1](QUICK_START.md)", qs_content)
qs_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*scratch/([^)]+)\)", r"[\1](scratch/\2)", qs_content)

assert "file://" not in qs_content, "file:// still in QUICK_START.md"
qs_path.write_text(qs_content, encoding="utf-8")
print("Cleaned file:// from QUICK_START.md!")

# 2. Fix agent_enhancement_report.md
rep_path = Path(r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md")
if rep_path.exists():
    rep_content = rep_path.read_text(encoding="utf-8")
    rep_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*techdocs/([^)]+)\)", r"[\1](techdocs/\2)", rep_content)
    rep_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*THLawDeka/([^)]+)\)", r"[\1](THLawDeka/\2)", rep_content)
    rep_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*AGENTS\.md\)", r"[\1](AGENTS.md)", rep_content)
    rep_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*QUICK_START\.md\)", r"[\1](QUICK_START.md)", rep_content)
    rep_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*scratch/([^)]+)\)", r"[\1](scratch/\2)", rep_content)
    rep_content = re.sub(r"\[([^\]]+)\]\(file:///[^)]*agent_enhancement_report\.md([^)]*)\)", r"[\1](\2)", rep_content)
    rep_path.write_text(rep_content, encoding="utf-8")
    print("Cleaned file:// from agent_enhancement_report.md!")
