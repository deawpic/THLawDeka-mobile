from pathlib import Path

p = Path(r"c:\Ai_code\THLawDeka-mobile\.agents\skills\backend-development\SKILL.md")
content = p.read_text(encoding="utf-8")

old_sec3 = """### Module 3: Security Shield & Input Sanitization
- **Payload Size**: Reject queries > 32 KB immediately with HTTP `413 Payload Too Large`.
- **Null-Byte Sanitization**: Strip `\\x00` null bytes using regex `re.sub(r'[\\x00]', '', query)`.
- **Prompt Injection Defense**: Check for dangerous override tokens while strictly keeping shell execution disabled."""

new_sec3 = """### Module 3: Security Shield & Input Sanitization
- **Payload Size**: Reject queries > 32 KB immediately with HTTP `413 Payload Too Large`.
- **Null-Byte Sanitization**: Strip `\\x00` null bytes using regex `re.sub(r'[\\x00]', '', query)`.
- **Gateway Pre-Filter (Anti-Tamper & Injection Shield)**:
  - Validate incoming prompts using `INJECTION_BLACKLIST_PATTERNS` to catch override attempts ("ignore instructions", "system prompt", "DAN"), harness tampering ("modify AGENTS.md", "delete rules"), and OS command/script executions ("powershell", "bash", "curl", "rm -rf", "cat /etc/").
  - Immediately reject tampering attempts with HTTP `400 Bad Request` without invoking `agy` or consuming tokens.
- **Physical OS Lockdown Guideline**:
  - Advise setting OS permissions on `harness/`, `backend/`, and `THLawDeka/AGENTS.md` to Read-Only (`chmod 555` / `icacls /deny Everyone:(WD,AD)`), with Write permitted exclusively on `THLawDeka/output/`."""

if old_sec3 in content:
    content = content.replace(old_sec3, new_sec3)
    print("Replaced Module 3 in backend skill.")
else:
    # try normalized
    norm_content = content.replace("\r\n", "\n")
    norm_old = old_sec3.replace("\r\n", "\n")
    if norm_old in norm_content:
        content = norm_content.replace(norm_old, new_sec3)
        print("Replaced Module 3 with newline normalization.")
    else:
        print("Warning: old_sec3 not found!")

# Add checklist item
chk_old = "- [ ] Environment isolated: `safe_env` passed without `ADMIN_SECRET`."
chk_new = """- [ ] Gateway Pre-Filter checks for prompt injection, harness tampering, and shell patterns before invoking subprocess.
- [ ] Environment isolated: `safe_env` passed without `ADMIN_SECRET`."""

if chk_old in content:
    content = content.replace(chk_old, chk_new)
    print("Updated checklist in backend skill.")

p.write_text(content, encoding="utf-8")
print("Saved backend skill!")
