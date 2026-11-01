
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
