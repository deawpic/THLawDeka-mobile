import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path("techdocs/system_spec_and_implementation_plan.md")
content = spec_path.read_text(encoding="utf-8")

# Check for essential keywords
keywords = {
    "Target SDK 36": "targetSdk = 36",
    "Min SDK 26": "minSdk = 26",
    "Release signing debug key": 'signingConfig = signingConfigs.getByName("debug")',
    "Minimal APK size": "isMinifyEnabled = true",
    "Resource shrinking": "isShrinkResources = true",
    "Language filters": 'resourceConfigurations += listOf("th", "en")',
    "Multi-chat continue": "conversation_id",
    "Multi-chat create new": "chat_sessions",
    "Multi-chat delete": "CASCADE",
    "Stop generating": "cancelStream",
    "FileProvider": "androidx.core.content.FileProvider",
    "Sarabun A4 PDF": "Sarabun",
    "Network resilience": "interrupted",
    "Fast-path cache": "legal_cache",
    "In-memory token cache": "ACTIVE_KEYS_CACHE",
    "SQLite WAL Backend": "PRAGMA journal_mode=WAL;",
    "SQLite WAL Android": "enableWriteAheadLogging()",
    "Token Throttler 50ms": "50",
    "CLI Flag Injection regex": r"^[a-zA-Z0-9][a-zA-Z0-9_\-]{0,63}$",
    "File download regex": r"^[a-zA-Z0-9_\-\u0E00-\u0E7F]+\.md$",
    "Canonical Confinement": "is_relative_to",
    "safe_env isolation": "safe_env",
    "Windows auto-start": "setup_autostart_windows.ps1",
    "Linux systemd service": "thlaw-gateway.service",
}

print("=== Keyword Verification in System Spec ===")
all_found = True
for label, pattern in keywords.items():
    if pattern in content:
        print(f"  [OK] {label:30s} FOUND")
    else:
        print(f"  [MISSING] {label:30s} MISSING!")
        all_found = False

if all_found:
    print("\n>>> ALL 23 CORE CRITERIA FOUND IN SPEC! <<<")
else:
    print("\n>>> SOME CRITERIA MISSING! <<<")
