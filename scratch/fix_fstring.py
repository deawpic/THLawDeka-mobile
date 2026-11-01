from pathlib import Path

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

bad_str = """        except Exception:
            # ป้องกันการพ่น Internal System Path หรือ Stack Trace ให้ Client เห็น
            yield f"event: error\\ndata: {json.dumps({'message': 'เกิดข้อผิดพลาดภายในระบบ'})}

\""""

# Let's search for the exact lines in content
lines = content.splitlines()
for i, line in enumerate(lines):
    if "เกิดข้อผิดพลาดภายในระบบ" in line:
        print(f"Line {i+1}: {repr(line)}")
        if i + 1 < len(lines):
            print(f"Line {i+2}: {repr(lines[i+1])}")
        if i + 2 < len(lines):
            print(f"Line {i+3}: {repr(lines[i+2])}")
        
        # fix it
        lines[i] = '            yield f"event: error\\ndata: {json.dumps({\'message\': \'เกิดข้อผิดพลาดภายในระบบ\'})}\\n\\n"'
        # remove the empty lines if they were leftover
        if lines[i+1] == '' and lines[i+2] == '"':
            del lines[i+2]
            del lines[i+1]
        break

spec_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Fixed f-string in spec!")
