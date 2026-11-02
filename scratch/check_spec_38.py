import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("3.8")
print(text[pos-10:pos+100])
