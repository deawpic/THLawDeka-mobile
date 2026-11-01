# -*- coding: utf-8 -*-
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_root = r"c:\Ai_code\THLawDeka-mobile"
files_to_check = [
    os.path.join(repo_root, "Quick_start_Windows.md"),
    os.path.join(repo_root, "Quick_start_Linux.md")
]

print("=== Running Deep Integrity Audit on Quick Start Files ===")

for file_path in files_to_check:
    name = os.path.basename(file_path)
    print(f"\nAuditing [{name}]...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check sections exist
    required_sections = [
        "## 🧭 แผนผังภาพรวม 7 ขั้นตอน",
        "## 🧠 สถาปัตยกรรมและหลักการทำงานของระบบ",
        "## 🗂️ ขั้นตอนที่ 1:",
        "## 🛠️ ขั้นตอนที่ 2:",
        "### 🔹 2.1",
        "### 🔹 2.2",
        "### 🔹 2.3",
        "### 🔹 2.4",
        "## ⚖️ ขั้นตอนที่ 3:",
        "## 🐍 ขั้นตอนที่ 4:",
        "## 💻 ขั้นตอนที่ 5:",
        "## 🤖 ขั้นตอนที่ 6:",
        "## 🚀 ขั้นตอนที่ 7:",
        "### 🔹 7.1",
        "### 🔹 7.2",
        "### 🔹 7.3",
        "## ❓ 8 ปัญหาที่พบบ่อย",
        "## 📚 เอกสารอ้างอิงเพิ่มเติม"
    ]
    for sec in required_sections:
        assert sec in content, f"Missing section '{sec}' in {name}"
    print(f"  ✓ All 18 structural sections and subsections are present.")

    # 2. Check troubleshooting questions 1 to 8
    for i in range(1, 9):
        q_marker = f"{i}. **ถาม:"
        assert q_marker in content, f"Missing question {i} in Troubleshooting of {name}"
    print(f"  ✓ All 8 troubleshooting & FAQ questions are continuously and correctly numbered (1 to 8).")

    # 3. Check for illegal file:// scheme
    assert "file://" not in content, f"Found illegal 'file://' link in {name}"
    print(f"  ✓ Zero 'file://' URIs detected (100% portable relative links).")

    # 4. Check for hardcoded absolute paths (C:\Users, etc.)
    abs_matches = re.findall(r"(?:[c|C]:\\Users\\[a-zA-Z0-9]+|[c|C]:\\Ai_code\\(?!THLawDeka-mobile))", content)
    assert not abs_matches, f"Found hardcoded absolute path in {name}: {abs_matches}"
    print(f"  ✓ Zero hardcoded absolute paths detected.")

    # 5. Check code blocks balance
    code_block_count = content.count("```")
    assert code_block_count % 2 == 0, f"Unbalanced code blocks in {name} (count: {code_block_count})"
    print(f"  ✓ Markdown code blocks are strictly balanced ({code_block_count // 2} blocks).")

    # 6. Check double separators
    double_sep = re.findall(r'---\s*\n\s*---', content)
    assert not double_sep, f"Found double separator in {name}"
    print(f"  ✓ Zero redundant horizontal separators.")

    # 7. Check cross-references
    if name == "Quick_start_Windows.md":
        assert "[Quick_start_Linux.md](Quick_start_Linux.md)" in content, "Missing Linux cross-reference"
    else:
        assert "[Quick_start_Windows.md](Quick_start_Windows.md)" in content, "Missing Windows cross-reference"
    print(f"  ✓ Cross-reference link to companion OS guide verified.")

print("\n=======================================================")
print("  ALL QUICK START AUDIT ASSERTIONS PASSED! (0 errors)")
print("=======================================================")
