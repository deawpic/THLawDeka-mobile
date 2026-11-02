import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/verify_all.py", "rb") as f:
    raw = f.read()

# Let's see lines around line 485
lines = raw.decode("utf-8", errors="replace").splitlines()
for i, l in enumerate(lines[480:495], 481):
    print(f"{i}: {l}")
