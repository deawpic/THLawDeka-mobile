import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

spec_path = Path(r"c:\Ai_code\THLawDeka-mobile\techdocs\system_spec_and_implementation_plan.md")
with open(spec_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Insert @app.get("/api/v1/models") after health check
health_target = """@app.get("/api/v1/health")
async def health_check_endpoint(authorization: str = Header(None)):
    \"\"\"ใช้สำหรับให้ Android Client ทดสอบการเชื่อมต่อและตรวจสอบความถูกต้องของ Auth Key\"\"\"
    await verify_auth(authorization)
    return {
        "status": "healthy",
        "service": "THLawDeka-mobile Gateway",
        "message": "พร้อมให้บริการวิเคราะห์คดีความ (Server-Side Zero-Disk-Write Policy)"
    }"""

models_endpoint_code = """@app.get("/api/v1/health")
async def health_check_endpoint(authorization: str = Header(None)):
    \"\"\"ใช้สำหรับให้ Android Client ทดสอบการเชื่อมต่อและตรวจสอบความถูกต้องของ Auth Key\"\"\"
    await verify_auth(authorization)
    return {
        "status": "healthy",
        "service": "THLawDeka-mobile Gateway",
        "message": "พร้อมให้บริการวิเคราะห์คดีความ (Server-Side Zero-Disk-Write Policy)"
    }

@app.get("/api/v1/models")
async def list_available_models(authorization: str = Header(None)):
    \"\"\"ดึงรายชื่อโมเดลปัญญาประดิษฐ์ที่รองรับในระบบ พร้อมจุดเด่นและคำอธิบายสำหรับแสดงผลบน Android\"\"\"
    await verify_auth(authorization)
    return {
        "status": "success",
        "default": "gemini-3.8-flash-high",
        "models": [
            {
                "id": "gemini-3.8-flash-high",
                "name": "Gemini 3.8 Flash (High)",
                "category": "Fast",
                "badge": "แนะนำ / เร็วสุด",
                "description": "ตอบรวดเร็ว แม่นยำสูง เหมาะสำหรับการค้นหาฎีกาเทียบเคียงและคำปรึกษาทั่วไป"
            },
            {
                "id": "claude-sonnet-4-6",
                "name": "Claude Sonnet 4.6 (Thinking)",
                "category": "Thinking",
                "badge": "วิเคราะห์ลึก",
                "description": "เน้นการคิดวิเคราะห์ ใช้เหตุผลซับซ้อน เหมาะกับการวางรูปคดีความและข้อต่อสู้"
            },
            {
                "id": "claude-opus-4-6-thinking",
                "name": "Claude Opus 4.6 (Thinking)",
                "category": "Thinking",
                "badge": "ปัญญาสูงสุด",
                "description": "โมเดลความฉลาดสูงสุดสำหรับการตีความข้อกฎหมายยากและคดีรัฐธรรมนูญ"
            },
            {
                "id": "gemini-3.8-flash-medium",
                "name": "Gemini 3.8 Flash (Medium)",
                "category": "Fast",
                "badge": "สมดุล",
                "description": "สมดุลระหว่างความเร็วและทรัพยากร สำหรับคดีความทั่วไป"
            },
            {
                "id": "gemini-3.8-flash-low",
                "name": "Gemini 3.8 Flash (Low)",
                "category": "Eco",
                "badge": "ประหยัดโควตา",
                "description": "ประหยัดพลังงานและโควตาสูงสุด เหมาะกับคำถามสั้นหรือตรวจเลขมาตรา"
            },
            {
                "id": "gpt-oss-120b-medium",
                "name": "GPT-OSS 120B (Medium)",
                "category": "OpenSource",
                "badge": "Open Weights",
                "description": "โมเดลโอเพ่นซอร์สประสิทธิภาพสูง สำหรับการค้นคว้ามุมมองเปรียบเทียบ"
            }
        ]
    }"""

assert health_target in content, "health_target not found"
content = content.replace(health_target, models_endpoint_code, 1)
print("✓ Added /api/v1/models endpoint to Section 4.1")

# 2. Insert fetchAvailableModels into Section 4.2
kt_target = """    /**
     * รับสตรีมคำปรึกษากฎหมายแบบ Gzip Compressed SSE
     * OkHttp จะทำ Transparent Gzip Decompression ให้อัตโนมัติเมื่อเซิร์ฟเวอร์ส่ง Content-Encoding: gzip
     */
    fun streamConsultation(
        serverUrl: String,
        apiKey: String,
        query: String,
        conversationId: String?,
        onStatus: (String) -> Unit,
        onToken: (String) -> Unit,
        onDone: () -> Unit,
        onError: (String) -> Unit
    ) {
        val payload = JSONObject().apply {
            put("query", query)
            if (!conversationId.isNullOrEmpty()) {
                put("conversation_id", conversationId)
            }
        }.toString()"""

kt_replacement = """    data class AiModelInfo(
        val id: String,
        val name: String,
        val category: String,
        val badge: String,
        val description: String
    )

    /**
     * ดึงรายการโมเดล AI ที่พร้อมใช้งานจาก Gateway (/api/v1/models)
     */
    fun fetchAvailableModels(
        serverUrl: String,
        apiKey: String,
        onSuccess: (List<AiModelInfo>) -> Unit,
        onError: (String) -> Unit
    ) {
        val url = if (serverUrl.endsWith("/api/v1/chat/stream")) {
            serverUrl.replace("/api/v1/chat/stream", "/api/v1/models")
        } else {
            "${serverUrl.trimEnd('/')}/api/v1/models"
        }
        val request = Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer $apiKey")
            .get()
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: java.io.IOException) {
                onError(e.localizedMessage ?: "Network failure")
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (!response.isSuccessful) {
                        onError("HTTP Error ${response.code}")
                        return
                    }
                    val body = response.body?.string() ?: ""
                    try {
                        val json = JSONObject(body)
                        val arr = json.getJSONArray("models")
                        val list = mutableListOf<AiModelInfo>()
                        for (i in 0 until arr.length()) {
                            val item = arr.getJSONObject(i)
                            list.add(
                                AiModelInfo(
                                    id = item.getString("id"),
                                    name = item.getString("name"),
                                    category = item.optString("category", "General"),
                                    badge = item.optString("badge", ""),
                                    description = item.optString("description", "")
                                )
                            )
                        }
                        onSuccess(list)
                    } catch (e: Exception) {
                        onError(e.localizedMessage ?: "JSON Parse error")
                    }
                }
            }
        })
    }

    /**
     * รับสตรีมคำปรึกษากฎหมายแบบ Gzip Compressed SSE พร้อมระบุโมเดลที่เลือก
     * OkHttp จะทำ Transparent Gzip Decompression ให้อัตโนมัติเมื่อเซิร์ฟเวอร์ส่ง Content-Encoding: gzip
     */
    fun streamConsultation(
        serverUrl: String,
        apiKey: String,
        query: String,
        conversationId: String?,
        model: String = "gemini-3.8-flash-high",
        onStatus: (String) -> Unit,
        onToken: (String) -> Unit,
        onDone: () -> Unit,
        onError: (String) -> Unit
    ) {
        val payload = JSONObject().apply {
            put("query", query)
            put("model", model)
            if (!conversationId.isNullOrEmpty()) {
                put("conversation_id", conversationId)
            }
        }.toString()"""

assert kt_target in content, "kt_target not found"
content = content.replace(kt_target, kt_replacement, 1)
print("✓ Added fetchAvailableModels and model param to Section 4.2")

with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("✓ Successfully updated spec with models endpoint and fetchAvailableModels!")
