import asyncio
import time
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import StreamingResponse
from starlette.testclient import TestClient

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=256)

@app.get("/stream")
async def stream():
    async def event_generator():
        for i in range(3):
            await asyncio.sleep(0.05)
            # Make sure it's long enough or test behavior
            yield f"event: token\ndata: {{'chunk': {i}, 'text': '{'ก'*100}'}}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")

client = TestClient(app)

print("--- Testing without Accept-Encoding ---")
t0 = time.time()
with client.stream("GET", "/stream") as response:
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    for line in response.iter_lines():
        if line:
            print(f"[{time.time()-t0:.2f}s] Received: {line[:50]}...")

print("\n--- Testing with Accept-Encoding: gzip ---")
t0 = time.time()
with client.stream("GET", "/stream", headers={"Accept-Encoding": "gzip"}) as response:
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    for line in response.iter_lines():
        if line:
            print(f"[{time.time()-t0:.2f}s] Received: {line[:50]}...")
