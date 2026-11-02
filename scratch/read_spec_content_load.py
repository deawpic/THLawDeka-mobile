import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/verify_all.py", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("spec_content =")
print(text[pos:pos+300])
