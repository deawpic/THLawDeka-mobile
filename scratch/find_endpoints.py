# -*- coding: utf-8 -*-
spec_path = r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md"
with open(spec_path, "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = re.findall(r"@app\.(?:post|get)\([^\)]+\)\s*\nasync def [^\(]+\([^\)]*\):", text)
for m in matches:
    print(m)
    print("-" * 40)
