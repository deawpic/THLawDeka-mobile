---
name: frontend-development
description: >-
  Mobile and Android frontend engineering workflows for THLawDeka-mobile, specializing in Kotlin native development, OkHttp SSE streaming, Markwon GFM rendering, sandboxed WebView Mermaid diagrams, Jetpack Security, and Android PrintManager PDF export.
---

# Android Frontend Development Skill (THLawDeka-mobile)

Provides engineering standards, architectural patterns, and token-optimized implementation workflows for Android Mobile Engineers developing the **THLawDeka-mobile** Android Client.

---

## ⛔ Strict No-Gradle-Build Policy (User Builds Manually via Android Studio)
- **DO NOT RUN GRADLE / GRADLEW**:
  - NEVER execute `./gradlew`, `gradle`, `gradle build`, `gradle assembleDebug`, `gradle compileDebugKotlin`, or any Gradle build commands under any circumstances.
  - The user will build, compile, install, and run debug builds manually via **Android Studio**.
  - Do not spawn Gradle daemons or background build processes.
- **Focus strictly on Code & Contract**:
  - Focus 100% on writing and maintaining clean production Kotlin code, XML layouts/manifests, and Gradle dependency scripts (`build.gradle.kts`).
  - Verification for Android artifacts is strictly static: physical file existence checks and structural validation without running Gradle.

---

## ⚡ Token Optimization Note (Implementation-Only Mode)
By default, mobile frontend engineers operate in **Implementation-Only Mode**:
- Do not write, execute, or read unit test files (`*.test.*`, `*Test.kt`) unless explicitly requested by the user (`"write test"`, `"test this"`, etc.).
- Rely on static structural inspection and contract validations against `techdocs/system_spec_and_implementation_plan.md` for deterministic verification.

---

## 📚 Scanned Skills & Playbooks Reference
When deep reference patterns are required, refer to the bundled playbooks:
- [Android Native Patterns](references/android-native.md) (Architecture, MVVM, Lifecycle, Repository)
- [Kotlin Coroutines & Flow Expert](references/kotlin-coroutines.md) (Structured concurrency, StateFlow, CoroutineExceptionHandler)
- [Mobile Security Coder](references/mobile-security.md) (Encrypted storage, WebView sandboxing, TLS enforcement)

---

## 1. Core Modules & Implementation Workflows

### Module 0: Android SDK, Build Configuration & Minimal APK Optimization (`app/build.gradle.kts`)
- **SDK Versions**:
  - `compileSdk = 36`
  - `minSdk = 26`
  - `targetSdk = 36`
- **Minimal APK Size Directives (รีดขนาด APK ให้เล็กที่สุด)**:
  1. **R8 Minification**: `isMinifyEnabled = true` with `proguard-android-optimize.txt` (Dead-code elimination & Method inlining)
  2. **Resource Shrinking**: `isShrinkResources = true` (ตัด Drawables/Layouts ที่ไม่ได้ใช้จริง)
  3. **Language Filtering**: `resourceConfigurations += listOf("th", "en")` (ลบ 70+ ภาษาที่ไม่จำเป็น)
  4. **Packaging Exclusions**: ตัด License/Notices และ `META-INF/*.kotlin_module`
  5. **Vector Drawables**: `vectorDrawables.useSupportLibrary = true` (ไม่ใช้ Bitmap PNG หลายความละเอียด)
- **Build Release Signing with Debug Key**:
  - In `buildTypes.release`:
    ```kotlin
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            // บังคับ sign release ด้วย debug key ตาม spec เพื่อให้ทดสอบ build release ได้ทันที
            signingConfig = signingConfigs.getByName("debug")
        }
        debug {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("debug")
        }
    }
    ```
- **Java / Kotlin Compatibility & Packaging**:
  - `JavaVersion.VERSION_17` and `jvmTarget = "17"`
  - `packaging { resources { excludes += setOf("META-INF/DEPENDENCIES", "META-INF/LICENSE", "META-INF/NOTICE", "META-INF/*.kotlin_module") } }`

### Module 1: Networking & SSE Stream Client (`data/LegalChatRepository.kt`)
- Use **OkHttp 4.12.0** and **okhttp-sse**:
  - Request to `https://<tailnet-node>.ts.net/api/v1/chat/stream` with `Accept: text/event-stream`.
  - Header `Authorization: Bearer <authen_key>`.
  - Handle SSE event types:
    - `event: status` -> update UI thought/status chips (e.g., "กำลังตรวจแคช L2", "กำลังค้นหาฎีกาเทียบเคียง").
    - `event: token` -> append delta text to streaming legal answer.
    - `event: done` -> mark completion, persist conversation state.
    - `event: error` -> emit actionable error event.
- Expose response as reactive Kotlin `Flow<SseEvent>` collected in `ViewModelScope` on `Dispatchers.IO`.
- **Automatic Gzip Decompression**:
  - Include `Accept-Encoding: gzip` in OkHttp requests (handled transparently by OkHttp's `BridgeInterceptor` or decoded via `GZIPInputStream`).
  - Saves ~70–85% network bandwidth over Tailscale WireGuard mesh.
- **Stream Cancellation (Stop Generating)**:
  - Provide `cancelStream()` method on repository calling `EventSource.cancel()`.
  - Canceling drops HTTP connection -> triggers `asyncio.CancelledError` on Gateway -> invokes `process.kill()` on `agy` subprocess to free up `Semaphore(3)` and CPU.
- **Resilient Chunk Buffering & Network Reconnect**:
  - Buffer tokens in ViewModel state; on unexpected disconnect, save message with `status = 'interrupted'` in SQLite.
  - Surface a "ลองใหม่ (Retry)" action that resends prompt with original `conversation_id`.

### Module 2: Secure Storage & Settings (`config/AppConfigManager.kt` & `ui/ConnectionSettingsManager.kt`)
- **Jetpack Security Crypto (`androidx.security:security-crypto:1.1.0-alpha06`)**:
  - Use `MasterKey.Builder` with `MasterKey.KeyScheme.AES256_GCM`.
  - Initialize `EncryptedSharedPreferences` for storing:
    1. `tailscale_gateway_url` (must validate starts with `https://`).
    2. `authen_key` (API Bearer token).
  - NEVER store tokens or URLs in unencrypted SharedPreferences.
- **Connection Test (Pre-save Health Check)**:
  - Send `GET /api/v1/health` with `Bearer <authen_key>` before persisting settings. Show visual connection feedback.

### Module 3: Thai Typography & Markdown GFM Rendering (`ui/MarkdownViewManager.kt`)
- **Engine**: `io.noties.markwon:core:4.6.2` + `ext-tables` + `ext-strikethrough` + `linkify` + `html`.
- **GFM Tables**: Enable `TablePlugin` for rendering legal comparison tables (e.g. IRAC steps 3, 6, 7).
- **Thai Word Breaking**: Configure in `TextView`:
  - `android:hyphenationFrequency="normal"`
  - `android:breakStrategy="high_quality"`

### Module 4: Offline Sandboxed Mermaid Diagram Rendering (`ui/MermaidRendererView.kt`)
- Local embedded `WebView` rendering legal procedural flowcharts (`assets/mermaid_template.html` and bundled `assets/mermaid.min.js`).
- **Security Sandboxing**:
  - Do NOT load external scripts from CDNs.
  - Set `settings.javaScriptEnabled = true`.
  - Set `settings.allowFileAccessFromFileURLs = false` and `settings.allowUniversalAccessFromFileURLs = false`.
  - Disable geolocation, file access, and content access.
- Support pinch-to-zoom with viewport `width=device-width, initial-scale=1.0, user-scalable=yes`.

### Module 5: 100% Client-Side Document Export & Sharing (`export/DocumentExportManager.kt`)
- Zero server file generation: client handles all file exports on device storage.
- **Multi-Format Local Export**:
  - **Export `.md`**: Writes raw markdown text directly to local device storage (`context.filesDir` or `cacheDir`) or Storage Access Framework.
  - **Export `.pdf`**: Uses Android native `PrintManager` and `WebView.createPrintDocumentAdapter()` with Thai Court Document Standards (`@page { size: A4; margin: 20mm 15mm 20mm 20mm; }` and Sarabun font).
  - **Export `.txt`**: Exports plain text (.txt) directly on device.
- **FileProvider Sharing Integration**:
  - Implement `shareDocumentFile(file, mimeType)` using `androidx.core.content.FileProvider.getUriForFile()`.
  - Launch `Intent.ACTION_SEND` with `FLAG_GRANT_READ_URI_PERMISSION` for sharing `.md`, `.pdf`, or `.txt` directly to LINE, Email, or Drive.

### Module 6: Multi-Chat Session Management (`data/local/ChatDatabaseHelper.kt` & `ui/session/ChatHistoryManager.kt`)
- **Built-in Android SQLite (`SQLiteOpenHelper`)**:
  - Pure Android SDK `android.database.sqlite.*` (Zero external library bloat, 0 KB added to APK).
  - Foreign key constraints enabled (`db.setForeignKeyConstraintsEnabled(true)`).
  - Indexing on `session_id` in `chat_messages` table.
- **3 Core Capabilities**:
  1. **แชตต่อของเดิม (Continue Existing Chat)**:
     - Load conversation history from `chat_messages` where `session_id = ?`.
     - Pass `conversation_id = sessionId` in `LegalChatRepository.sendStreamRequest(query, conversationId)` payload.
     - Backend forwards `--conversation <sessionId>` to preserve continuous legal case context.
  2. **สร้างแชตใหม่ (Create New Chat)**:
     - Clear active chat viewport, generate new session UUID (`UUID.randomUUID().toString()`).
     - Auto-generate session title from first prompt text (up to 40 chars).
  3. **ลบแชต (Delete Chat)**:
     - Trash icon / swipe action with confirmation dialog (*"ต้องการลบประวัติการปรึกษานี้หรือไม่?"*).
     - Cascade delete session and all messages from SQLite.
     - If deleted session was active, reset immediately to new chat view.

### Module 7: Performance & Latency Optimization (Android Client)
- **Stream Token Batching Buffer (50ms Throttler)**:
  - Do NOT recalculate Markwon Spannable layout on the Main Thread for every incoming SSE token.
  - Implement a Coroutine Throttling Buffer (`StreamTokenThrottler`) collecting tokens and flushing to the UI every 50–80 ms or on `\n`.
  - Keeps UI rendering smoothly at 60–120 fps without frame drops.
- **SQLite WAL Mode & Batch Write**:
  - In `ChatDatabaseHelper.kt`, enable Write-Ahead Logging via `db.enableWriteAheadLogging()`.
  - Buffer message deltas in ViewModel RAM; persist to SQLite in batch upon `event: done`, `event: error`, or cancellation.
- **Mermaid WebView Lazy Loading**:
  - Defer initializing `MermaidRendererView` until a ```mermaid block is detected in the response text, saving 50–80 MB of RAM.

---

### Module 8: Offline FTS5 Full-Text Search & Partial Stream Recovery
- **Offline SQLite FTS5**: Enable `chat_messages_fts USING fts5(message_id UNINDEXED, session_id UNINDEXED, content, tokenize='unicode61')` in `ChatDatabaseHelper.kt` for instant offline keyword search across saved court precedents.
- **Partial Stream Recovery**: On premature connection drop, save accumulated tokens with `interrupted` status. Expose `continueInterruptedStream` to resume analysis without starting over.

## 2. Android Verification Checklist
Before completing mobile implementation tasks, verify:
- [ ] Android SDK spec adhered: `compileSdk = 36`, `targetSdk = 36`, `minSdk = 26`.
- [ ] Release build configured with `signingConfig = signingConfigs.getByName("debug")`.
- [ ] Minimal APK size spec implemented: `isMinifyEnabled = true`, `isShrinkResources = true`, `resourceConfigurations += listOf("th", "en")`, and `packaging` excludes.
- [ ] Multi-chat session management supported: continue previous chat (`conversation_id`), create new chat (`+ แชตใหม่`), and delete chat with confirmation dialog.
- [ ] Stop Generating supported: UI displays stop button during streaming calling `cancelStream()` to terminate subprocess.
- [ ] Network resilience implemented: buffers incoming stream, sets `interrupted` status on drops, and offers Retry action.
- [ ] FileProvider configured: allows native sharing of `.md`, `.pdf`, and `.txt` files via Android Share Sheet.
- [ ] Official PDF Layout verified: A4 margins and Sarabun typography applied in `DocumentExportManager.kt`.
- [ ] 100% On-device local export to `.md`, `.pdf`, and `.txt` supported without server-side file creation.
- [ ] Local storage implemented via built-in `SQLiteOpenHelper` (Zero 3rd-party database library bloat).
- [ ] Dependencies match `techdocs/system_spec_and_implementation_plan.md` exactly in `build.gradle.kts`.
- [ ] No unencrypted credentials stored in plaintext.
- [ ] WebView security flags properly set (`allowFileAccessFromFileURLs = false`).
- [ ] Thai text views configured with `breakStrategy="high_quality"`.
- [ ] Stream Token Batching Buffer (50ms) implemented to eliminate UI jank during high-throughput SSE.
- [ ] SQLite WAL mode (`enableWriteAheadLogging()`) and RAM-based stream batch write enabled.
- [ ] Strict Zero-Test Policy observed: unit/instrumented tests run ONLY if explicitly requested by user prompt.
- [ ] ⛔ No Gradle build execution: Never run `./gradlew` or `gradle build`; user builds manually in Android Studio.
- [ ] Files physically exist at designated paths in `android/app/src/main/`.
