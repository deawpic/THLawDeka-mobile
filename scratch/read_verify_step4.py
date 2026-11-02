import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/verify_all.py", "r", encoding="utf-8") as f:
    text = f.read()

print("verify_all.py length:", len(text))
pos = text.find("[Step 4]")
print(text[pos:pos+1000])
