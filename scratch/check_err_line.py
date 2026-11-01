from pathlib import Path

lines = Path("scratch/test_extracted_main.py").read_text(encoding="utf-8").splitlines()
for i in range(265, min(len(lines), 275)):
    print(f"{i+1}: {repr(lines[i])}")
