---
name: anti-hallucination-guardian
description: >-
  Systematic protocols, verification gates, token optimization rules, and fact-checking workflows to eliminate AI hallucinations across code generation, API design, dependency resolution, and test execution.
---

# Anti-Hallucination Guardian Skill

Provides rigorous grounding protocols, token-optimized verification gates, and anti-fabrication procedures to ensure all agent outputs are tethered to ground truth while preventing token bloat.

---

## 1. The 4 Golden Rules of Anti-Hallucination & Verification

1. **The Grounding Rule (No Assumptions)**:
   - NEVER assume a file, class, method, column name, or API endpoint exists.
   - ALWAYS inspect the codebase using `find_by_name`, `grep_search`, or `view_file` before writing code that references it.

2. **The Verification Rule (Exit Codes > Self-Reports with Token Control)**:
   - NEVER trust an agent's self-proclaimed "All tests pass" or "Feature completed".
   - Ground truth verification must be deterministic (Exit code `0`).
   - **Token Optimization Protocol (Strict Zero-Test by Default)**:
     - By default, agents operate in **Implementation-Only Mode**: Do NOT write, execute, or read unit tests autonomously.
     - **Lightweight Verification Alternative**: Rely on fast static type checkers, syntax checkers, and linters (`tsc --noEmit`, `mypy --quick`, `ruff check`, `py_compile`). Stop once static analysis passes (exit code 0).
     - **Testing Mode (Opt-In Only)**: Run or write unit tests ONLY when explicitly triggered by the user prompt (`"write test"`, `"unit test"`, `"test this"`, `"run tests"`, `"generate test suite"`). When active, enforce minimal test scope, log suppression flags, and a strict maximum of 2 auto-fix attempts.

3. **The Package & API Grounding Rule (No Phantom Libraries)**:
   - NEVER import packages, NPM libraries, PyPI dependencies, or Android Gradle packages without verifying they are declared in `backend/requirements.txt`, `build.gradle.kts`, `package.json`, or officially supported in standard platform SDKs.
   - Ground all Android APIs strictly in the declared libraries (`com.squareup.okhttp3:okhttp:4.12.0`, `com.squareup.okhttp3:okhttp-sse:4.12.0`, `io.noties.markwon:core:4.6.2`, `androidx.security:security-crypto:1.1.0-alpha06`, `androidx.webkit:webkit:1.10.0`).
   - Ground all Backend APIs strictly in `backend/requirements.txt` (`fastapi>=0.110.0`, `uvicorn[standard]>=0.28.0`, `pydantic>=2.6.0`, `jinja2>=3.1.3`, `python-multipart>=0.0.9`).
   - Do not invent hypothetical framework functions or deprecated parameters.

4. **The Evidence Citation Rule**:
   - Every claim of a bug fix, system status, or test result MUST be accompanied by exact file paths, line references, or actual command terminal output.

---

## 2. Hallucination Detection & Prevention Workflows

### Workflow 1: Pre-Execution Codebase Grounding
Before writing any code or architecture specification:
1. Search for existing models and types (`grep_search` for interface/type/class definitions).
2. Check existing routes and endpoints to avoid duplicate or conflicting paths.
3. Check dependency manifests (`build.gradle.kts`, `backend/requirements.txt`) before importing third-party libraries.

### Workflow 2: Anti-Fabrication Code Review
When generating or reviewing code, actively scan for common hallucination patterns:
- **Phantom APIs**: Invoking methods that don't exist on third-party libraries (e.g. invented SDK methods).
- **Silent Exception Swallowing**: `try { ... } catch (e) {}` blocks that pretend operations succeed.
- **Mock Over-Fitting**: Writing tests that assert on hardcoded mock values instead of testing the actual business logic.
- **Fictional File References**: Linking to files or imports that were never created in the repository.

### Workflow 3: Ground-Truth Verification Gate (Pre-Handoff)
Before marking any task or milestone as complete, run this verification checklist:

| Verification Target | Ground Truth Verification Method | Gate Criteria |
| :--- | :--- | :--- |
| **Files Created/Edited** | `view_file` or `find_by_name` | File physically exists and contains valid syntax. |
| **Backend Syntax & Types (Default)** | Fast static check: `python -m py_compile`, `ruff check`, `mypy --quick` | 0 errors returned (Exit code 0). |
| **Android / Kotlin (Default)** | File existence & XML syntax check (`xml.etree.ElementTree`) | Valid file existence and XML/Kotlin structure. **Never run Gradle build CLI**. |
| **Business Logic (Default Mode)** | Static type checking + Pydantic schema validation | Type check passes with exit code 0. No test files created/run. |
| **Business Logic (Testing Mode Only)** | Targeted single-file test with log suppression (`pytest -q --tb=short --maxfail=1`, etc.) | Test exit code = 0 (strictly max 2 auto-fix attempts). |
| **API Endpoints** | Integration test / curl verification (if explicitly requested) | Expected HTTP status code and response envelope. |

---

## 3. Strict Token Optimization & Test Control Guardrails

When working in this repository or any agent harness governed by this skill:

### A. Zero-Test Policy by Default (Implementation-Only Mode)
- **DO NOT WRITE TESTS**: Do not create, update, mock, or touch test files (`*.test.*`, `*.spec.*`, `*Test.kt`, `tests/`, `__tests__/`).
- **DO NOT EXECUTE TESTS**: Do not run test runners (`pytest`, `vitest`, `jest`, `npm test`, `cargo test`, `gradle test`) autonomously.
- **DO NOT READ TEST CONTEXT**: Do not load test files into context unless a broken import in production code strictly breaks compilation.
- **ONLY CODE & CONTRACT**: Focus 100% of reasoning and output on production code, signatures, and interfaces.

### B. Testing Mode Trigger & Execution Guardrails
- **Trigger**: Transition into Testing Mode ONLY if user prompt explicitly contains trigger words: `"write test"`, `"unit test"`, `"test this"`, `"run tests"`, or `"generate test suite"`.
- **Target Single Scope**: Test ONLY the immediate requested function/module.
- **Log Suppression**: Always pass flags to suppress tracebacks:
  - Python: `pytest <path> -q --tb=short --maxfail=1`
  - Node/TS: `npx vitest run <path> --reporter=compact` or `npm test -- <path> --bail`
  - Android: *Never run gradle CLI; user tests manually in Android Studio*.
  - Go: `go test -v -run <TestName> <pkg>`
  - Rust: `cargo test <test_name> -- --nocapture`

### C. ⛔ Strict No-Gradle-Build Policy (User Builds Manually via Android Studio)
- **DO NOT RUN GRADLE / GRADLEW**:
  - NEVER execute `./gradlew`, `gradle`, `gradle build`, `gradle assembleDebug`, `gradle compileDebugKotlin`, or any Gradle build commands.
  - The user will build, compile, and run debug builds manually via **Android Studio**.
  - For Android code verification, verify file paths, file existence, and syntax statically without launching the Gradle daemon.

---

## 4. Self-Correction & Recovery Protocol (Max 2 Attempts)

If an agent discovers an error or a test fails (when in Testing Mode):
1. **Halt Execution Immediately**: Do not fabricate mock data or write workaround hacks.
2. **Read Concise Error**: Inspect only the concise error message or stack trace.
3. **Attempt 1 (Targeted Fix)**: Apply the direct, minimal fix to production code or test.
4. **Attempt 2 (Re-run Once)**: Re-run test once. If it still fails, **STOP IMMEDIATELY**.
5. **Revert & Escalate**: Revert broken test changes, report the exact error signature concisely (under 5 lines), and ask the user for direction. **NEVER loop beyond 2 attempts.**
