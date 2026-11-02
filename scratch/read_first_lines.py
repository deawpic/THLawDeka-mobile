import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/verify_all.py", "r", encoding="utf-8") as f:
    first_lines = [f.readline() for _ in range(5)]

print(first_lines)
