import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("THLawDeka/README.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Line 1:", repr(lines[0]))
print("Line 2:", repr(lines[1]))
print("Line 3:", repr(lines[2]))
print("Line 4:", repr(lines[3]))
