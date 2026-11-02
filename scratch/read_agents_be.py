import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("AGENTS.md", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("Backend Developer")
print(text[pos:pos+900])
