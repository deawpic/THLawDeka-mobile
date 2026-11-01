from pathlib import Path

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# Let's inspect around char 47518
start_pos = max(0, 47518 - 300)
end_pos = min(len(content), 47518 + 500)
snippet = content[start_pos:end_pos]
print("=== Snippet around char 47518 ===")
print(snippet)
