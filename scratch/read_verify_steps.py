import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/verify_all.py", "r", encoding="utf-8") as f:
    text = f.read()

for step in range(1, 9):
    pos = text.find(f"[Step {step}]")
    if pos != -1:
        print(text[pos:pos+150])
