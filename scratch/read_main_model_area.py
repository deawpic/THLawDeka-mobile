import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

pos1 = text.find('class ChatRequest(BaseModel):')
pos2 = text.find('async def chat_stream_endpoint(', pos1)
pos3 = text.find('cmd = [', pos2)
print("=== ChatRequest ===")
print(text[pos1:pos2])
print("=== cmd = [ ===")
print(text[pos3:pos3+300])
