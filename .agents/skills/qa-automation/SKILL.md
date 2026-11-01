---
name: qa-automation
description: >-
  Quality assurance, test automation, token optimization guardrails, and anti-hallucination verification protocols for THLawDeka-mobile across Android Kotlin, FastAPI SSE, and Tailscale mesh boundaries.
---

# QA Automation Skill (THLawDeka-mobile Verification Oracle)

Provides token-optimized quality assurance standards, static verification gates, and anti-hallucination protocols for QA Automation Engineers and Verification Gatekeepers in **THLawDeka-mobile**.

---

## ⛔ Strict No-Gradle-Build Policy (User Builds Manually via Android Studio)
- **DO NOT RUN GRADLE / GRADLEW**:
  - NEVER execute `./gradlew`, `gradle`, `gradle build`, `gradle assembleDebug`, `gradle compileDebugKotlin`, or any Gradle test commands (`testDebugUnitTest`).
  - The user will build, compile, and run debug builds manually via **Android Studio**.
  - For Android client verification, QA inspects physical file existence, XML syntax validity, and source code contracts statically without spawning Gradle processes.

---

## ⚡ Strict Token Optimization & Test Control Directive (Core Invariant)

This skill strictly enforces the **Zero-Test Policy by Default** to prevent context window bloat and excessive token consumption.

### 1. Default Behavior: Strict Zero-Test Policy (Implementation-Only Mode)
By default, the QA Agent and all peer agents operate in **Implementation-Only Mode**:
- **DO NOT WRITE TESTS**: Do not create, update, mock, or touch any test files (`*.test.*`, `*Test.kt`, `tests/`, `__tests__/`).
- **DO NOT EXECUTE TESTS**: Do not execute test runners (`pytest`, `vitest`, `gradle test`, `adb test`, etc.) autonomously under any circumstances.
- **DO NOT READ TEST CONTEXT**: Do not load or read existing test files into context unless a broken import strictly breaks compilation.
- **ONLY CODE & CONTRACT**: Focus 100% of reasoning and verification output on production code, schema models, and interfaces.

### 2. Exception Trigger (Explicit Opt-In Only)
Transition into **Testing Mode** ONLY if the user prompt explicitly uses trigger words:
`"write test"`, `"unit test"`, `"test this"`, `"run tests"`, or `"generate test suite"`.

### 3. Guardrails When Testing Mode is Activated
- **Minimal Context & Scope**: Test ONLY the immediate function or endpoint requested.
- **Log Suppression**: Suppress tracebacks (`pytest <path> -q --tb=short --maxfail=1`).
- **Android Policy**: Do NOT run gradle CLI test runners; user tests manually via Android Studio.
- **Strict Auto-Fix Loop Limit (Max 2 Attempts)**:
  - Iteration 1: Targeted fix.
  - Iteration 2: Re-run once. If still failing, STOP IMMEDIATELY and report under 5 lines.

### 4. Lightweight Verification Alternative (Default Baseline Truth)
- Python: `python -m py_compile <path>`, `ruff check <path>`.
- Kotlin/Android: Static file existence check, XML syntax validity (`xml.etree.ElementTree`).
- Stop once static analysis passes with exit code `0`.

---

## 📚 Scanned Skills & Playbooks Reference
When instrumenting UI inspection or inspecting device states on Android emulators:
- [Android ADB Verification Playbook](references/android-adb-verification.md) (Device calibration, UIAutomator XML dumps, click/tap commands, screencaps, and logcat monitoring)

---

## 1. Phase-by-Phase Verification Protocols

### Phase 1: Local Harness Pipe Verification
- Run `python test_pipe.py`.
- Verify: Subprocess executes `agy.exe`, streams valid NDJSON frames, and leaves 0 query strings in OS process arguments (`ps aux` / Task Manager).

### Phase 2: FastAPI Gateway & SSE Protocol Verification
- Run static syntax compilation on backend files:
  `python -m py_compile backend/main.py backend/auth_db.py backend/manage_keys.py`
- Verify SSE stream headers: `Content-Type: text/event-stream`, `Cache-Control: no-cache`, `X-Accel-Buffering: no`.
- Verify SQLite auth handling: HTTP 403 on invalid key, HTTP 200 on active key.

### Phase 3: Tailscale HTTPS Mesh Verification
- Verify Tailscale status: `tailscale status`.
- Verify reverse proxy binding: `tailscale serve status` indicates port 443 routes to port 8000.
- Verify TLS certificate validity without SSL warnings.

### Phase 4: Android Client Architecture & Layout Verification
- **DO NOT RUN GRADLE BUILDS**: User compiles and tests manually in Android Studio.
- Verify physical existence of all specified Kotlin files:
  - `AppConfigManager.kt`, `LegalChatRepository.kt`, `ChatModels.kt`, `ChatDatabaseHelper.kt`, `MarkdownViewManager.kt`, `MermaidRendererView.kt`, `ConnectionSettingsManager.kt`, `PdfExportManager.kt`.
- Verify XML assets and manifests are well-formed.
- If Android emulator is running and UI inspection is requested:
  - Dump view hierarchy: `adb shell uiautomator dump /sdcard/view.xml && adb pull /sdcard/view.xml`
  - Capture screen: `adb shell screencap -p /sdcard/screen.png`
  - Inspect logcat: `adb logcat -d | findstr /i "THLawDeka"`

### Phase 5: Resiliency & Security Hardening Verification
- **Timeout Test**: Assert subprocess is terminated (`process.kill()`) when execution exceeds 60 seconds.
- **Injection Prevention Test**: Send strings with single quotes, semicolons, shell pipes (`|`), and null bytes (`\x00`). Verify gateway strips null bytes and subprocess executes cleanly with `shell=False`.
- **Markdown Table Test**: Verify GFM tables parse without crashing.
