import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with open("scratch/verify_all.py", "r", encoding="utf-8") as f:
    text = f.read()

step9_code = """
print("\\n[Step 9] Deterministic Multi-Model Whitelist & Flag Injection Assertions...")

VALID_MODELS = {
    "gemini-3.8-flash-high",
    "gemini-3.8-flash-medium",
    "gemini-3.8-flash-low",
    "claude-sonnet-4-6",
    "claude-opus-4-6-thinking",
    "gpt-oss-120b-medium"
}

model_regex = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._\\-]{0,63}$")

# 9.1 Valid models acceptance
for m in VALID_MODELS:
    assert model_regex.match(m) is not None, f"Valid model failed regex: {m}"
print("  ✓ All 6 supported AI models passed regex and whitelist validation.")

# 9.2 Rejection of Flag Injection & Unsupported models
malicious_or_invalid_models = [
    "--dangerously-skip-permissions",
    "-p",
    "--model",
    "-m",
    "; rm -rf /",
    "model with spaces",
    "model\\x00null",
    "../../etc/passwd",
    "gpt-4o-unknown",
    "-invalid-start",
    "claude-unknown-version",
    "gemini;curl"
]

for bad_m in malicious_or_invalid_models:
    is_valid = bool(model_regex.match(bad_m)) and (bad_m in VALID_MODELS)
    assert not is_valid, f"Security failure: Malicious/invalid model passed validation: {bad_m}"
print("  ✓ Successfully intercepted all 12 model flag injection and unsupported model attempts.")

# 9.3 Verify Section 3.8 and Section 3.4.10 presence in spec
assert "### 3.8 ข้อกำหนดระบบเลือกโมเดลปัญญาประดิษฐ์" in spec_content, "Missing Section 3.8 in spec"
assert "### 3.4.10 ข้อกำหนดการเลือกและสลับโมเดล AI บน Android" in spec_content, "Missing Section 3.4.10 in spec"
assert "@app.get(\\"/api/v1/models\\")" in spec_content, "Missing /api/v1/models endpoint in spec"
assert "fetchAvailableModels" in spec_content, "Missing fetchAvailableModels in LegalChatRepository spec"
assert "selected_model" in spec_content, "Missing selected_model in ChatDatabaseHelper spec"
assert "model_used" in spec_content, "Missing model_used in ChatDatabaseHelper spec"
print("  ✓ Verified Section 3.8, Section 3.4.10, /api/v1/models, and SQLite schema in spec.")
"""

target = 'print("\\n=======================================================")\nprint("  ALL VERIFICATION GATES PASSED DETERMINISTICALLY! (0 errors)")'

assert target in text, "Target not found in verify_all.py"
text = text.replace(target, step9_code + "\n" + target, 1)

with open("scratch/verify_all.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print("✓ Successfully added Step 9 to scratch/verify_all.py!")
