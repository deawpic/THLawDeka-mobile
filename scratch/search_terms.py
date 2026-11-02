import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("techdocs/system_spec_and_implementation_plan.md", "r", encoding="utf-8") as f:
    text = f.read()

for term in ["pii", "audit", "rate_limit", "backup", "fts5"]:
    count = text.lower().count(term)
    print(f"Term '{term}': {count} occurrences")
