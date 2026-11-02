import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/verify_all.py", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("[Step 8]")
print(text[pos:])
