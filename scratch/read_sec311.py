import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("### 3.11")
print(text[pos:pos+1500])
