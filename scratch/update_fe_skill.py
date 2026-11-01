import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(".agents/skills/frontend-development/SKILL.md")
content = p.read_text(encoding="utf-8")

# 1. Update lines 83 and 93-95
old_m1_snippet = """    - `event: status` -> update UI thought/status chips (e.g., "กำลังตรวจแคช L2", "กำลังค้นหาฎีกาเทียบเคียง").
    - `event: token` -> append delta text to streaming legal answer.
    - `event: file` -> parse `filename`, `download_url`, `size_bytes`, render file download card in chat UI.
    - `event: done` -> mark completion, persist conversation state.
    - `event: error` -> emit actionable error event.
- Expose response as reactive Kotlin `Flow<SseEvent>` collected in `ViewModelScope` on `Dispatchers.IO`.
- **Stream Cancellation (Stop Generating)**:
  - Provide `cancelStream()` method on repository calling `EventSource.cancel()`.
  - Canceling drops HTTP connection -> triggers `asyncio.CancelledError` on Gateway -> invokes `process.kill()` on `agy` subprocess to free up `Semaphore(3)` and CPU.
- **Resilient Chunk Buffering & Network Reconnect**:
  - Buffer tokens in ViewModel state; on unexpected disconnect, save message with `status = 'interrupted'` in SQLite.
  - Surface a "ลองใหม่ (Retry)" action that resends prompt with original `conversation_id`.
- **Artifact File Downloader**:
  - Provide `downloadArtifactFile(baseUrl, apiKey, relativeDownloadUrl, destinationFile, onSuccess, onError)`.
  - Stream downloaded bytes to internal cache (`context.cacheDir/artifacts/` or `context.filesDir/documents/`)."""

new_m1_snippet = """    - `event: status` -> update UI thought/status chips (e.g., "กำลังตรวจแคช L2", "กำลังค้นหาฎีกาเทียบเคียง").
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
  - Surface a "ลองใหม่ (Retry)" action that resends prompt with original `conversation_id`."""

assert old_m1_snippet in content, "old_m1_snippet not found"
content = content.replace(old_m1_snippet, new_m1_snippet)

# 2. Update Module 5
old_m5_snippet = """### Module 5: Official A4 Legal PDF Export & Sharing (`export/PdfExportManager.kt`)
- Use Android native `PrintManager` and `WebView.createPrintDocumentAdapter()`.
- Zero heavy 3rd-party PDF dependencies.
- **Thai Court Document Standards**:
  - Inject `@page { size: A4; margin: 20mm 15mm 20mm 20mm; }`.
  - Use `font-family: 'Sarabun', 'TH Sarabun New', sans-serif; font-size: 16pt; line-height: 1.6;` with bundled `Sarabun-Regular.ttf` (~120KB) in `assets/fonts/`.
  - Inject `@media print` CSS for precise page breaks (`page-break-inside: avoid;`).
- **FileProvider Sharing Integration**:
  - Implement `shareDocumentFile(file, mimeType)` using `androidx.core.content.FileProvider.getUriForFile()`.
  - Launch `Intent.ACTION_SEND` with `FLAG_GRANT_READ_URI_PERMISSION` for sharing `.md` or `.pdf` directly to LINE, Email, or Drive."""

new_m5_snippet = """### Module 5: 100% Client-Side Document Export & Sharing (`export/DocumentExportManager.kt`)
- Zero server file generation: client handles all file exports on device storage.
- **Multi-Format Local Export**:
  - **Export `.md`**: Writes raw markdown text directly to local device storage (`context.filesDir` or `cacheDir`) or Storage Access Framework.
  - **Export `.pdf`**: Uses Android native `PrintManager` and `WebView.createPrintDocumentAdapter()` with Thai Court Document Standards (`@page { size: A4; margin: 20mm 15mm 20mm 20mm; }` and Sarabun font).
  - **Export `.txt`**: Exports plain text (.txt) directly on device.
- **FileProvider Sharing Integration**:
  - Implement `shareDocumentFile(file, mimeType)` using `androidx.core.content.FileProvider.getUriForFile()`.
  - Launch `Intent.ACTION_SEND` with `FLAG_GRANT_READ_URI_PERMISSION` for sharing `.md`, `.pdf`, or `.txt` directly to LINE, Email, or Drive."""

assert old_m5_snippet in content, "old_m5_snippet not found"
content = content.replace(old_m5_snippet, new_m5_snippet)

# 3. Update Checklist
old_fe_chk = """- [ ] FileProvider configured: allows native sharing of `.md` and `.pdf` files via Android Share Sheet.
- [ ] Official PDF Layout verified: A4 margins and Sarabun typography applied in `PdfExportManager.kt`.
- [ ] Artifact/File Download handled: `event: file` and markdown link `/api/v1/files/<filename>.md` trigger secure OkHttp download and allow PDF export."""

new_fe_chk = """- [ ] FileProvider configured: allows native sharing of `.md`, `.pdf`, and `.txt` files via Android Share Sheet.
- [ ] Official PDF Layout verified: A4 margins and Sarabun typography applied in `DocumentExportManager.kt`.
- [ ] 100% On-device local export to `.md`, `.pdf`, and `.txt` supported without server-side file creation."""

assert old_fe_chk in content, "old_fe_chk not found"
content = content.replace(old_fe_chk, new_fe_chk)

p.write_text(content, encoding="utf-8")
print("Updated .agents/skills/frontend-development/SKILL.md successfully!")
