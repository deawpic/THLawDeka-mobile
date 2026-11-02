import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("### 4.2")
pos_end = text.find("### 4.3", pos)
print(text[pos:pos_end])
