import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

repo_root = Path(".")
py_and_md = list(repo_root.glob("**/*.md"))

for p in py_and_md:
    if ".git" in str(p) or "brain" in str(p):
        continue
    txt = p.read_text(encoding="utf-8")
    if "downloadArtifactFile" in txt:
        print(f"Found downloadArtifactFile in: {p}")
