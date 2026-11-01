from pathlib import Path

report_path = Path(r"C:\Users\User\.gemini\antigravity\brain\87afe41b-53b3-4114-b562-1e2136717e1d\agent_enhancement_report.md")
if report_path.exists():
    content = report_path.read_text(encoding="utf-8")
    count = content.count("file://")
    print(f"agent_enhancement_report.md has {count} occurrences of file://")
    lines = content.splitlines()
    for i, l in enumerate(lines, 1):
        if "file://" in l:
            print(f"  Line {i}: {l[:100]}")
