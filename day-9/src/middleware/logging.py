import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.requests import Request


class LoggingMiddleWare(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(
            f"Request: {request.method} {request.url.path} completed in {process_time:.4f}s"
        )
        response.headers["X-Process-Time"] = str(process_time)
        return response