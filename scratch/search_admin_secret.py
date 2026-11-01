# -*- coding: utf-8 -*-
spec_path = r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md"
with open(spec_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "admin_super_secret_pass_2026" in line:
        print(f"Line {i+1}: {line.strip()}")
