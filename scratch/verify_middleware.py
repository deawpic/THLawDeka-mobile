import py_compile
from pathlib import Path

test_code = """
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi.middleware.gzip import GZipMiddleware

class SelectiveGZipMiddleware:
    def __init__(self, app: ASGIApp, minimum_size: int = 256):
        self.app = app
        self.minimum_size = minimum_size
        self.gzip_middleware = GZipMiddleware(app, minimum_size=minimum_size)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            path = scope.get("path", "")
            if path.endswith("/stream"):
                await self.app(scope, receive, send)
                return
        await self.gzip_middleware(scope, receive, send)
"""
p = Path("scratch/test_selective_gzip.py")
p.write_text(test_code, encoding="utf-8")
py_compile.compile(str(p), doraise=True)
print("SelectiveGZipMiddleware compiled with 0 errors!")
