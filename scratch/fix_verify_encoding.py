import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/verify_all.py", "r", encoding="utf-8") as f:
    code = f.read()

if not code.startswith("# -*- coding: utf-8 -*-"):
    code = "# -*- coding: utf-8 -*-\n" + code

with open("scratch/verify_all.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(code)

print("Added encoding declaration to scratch/verify_all.py")
