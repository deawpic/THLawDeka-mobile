import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
lines = spec_path.read_text(encoding="utf-8").splitlines()

print("=== Occurrences in system_spec_and_implementation_plan.md ===")
for i, line in enumerate(lines, 1):
    if any(k in line for k in ["ARTIFACT", "/api/v1/files", "event: file", "downloadArtifactFile", "Strict .md Whitelist", "Gateway Artifact Handshake"]):
        print(f"L{i:4d}: {line}")
