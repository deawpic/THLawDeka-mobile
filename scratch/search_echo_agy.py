import os

for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith((".md", ".py", ".sh", ".bat", ".ps1")):
            p = os.path.join(root, f)
            try:
                content = open(p, encoding="utf-8").read()
                if "| agy" in content or "echo " in content and "agy" in content:
                    lines = content.splitlines()
                    for i, l in enumerate(lines, 1):
                        if "agy" in l and ("|" in l or "-p" in l):
                            print(f"{p} line {i}: {l}")
            except Exception:
                pass
