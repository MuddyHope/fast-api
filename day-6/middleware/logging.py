from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time

app = FastAPI()


async def _my_dispatch(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"Request: {request.method} {request.url.path} completed in {process_time:.4f}s"
    )
    response.headers["X-Process-Time"] = str(process_time)
    return response


class LoggingMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return await _my_dispatch(request, call_next)
