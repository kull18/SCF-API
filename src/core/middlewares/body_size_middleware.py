from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

MAX_BODY_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB, suficiente para JSON de texto; las fotos van por S3, no por aquí


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        content_length = request.headers.get("content-length")

        if content_length is not None and int(content_length) > MAX_BODY_SIZE_BYTES:
            return JSONResponse(
                status_code=413,
                content={"detail": "Request body too large"},
            )

        return await call_next(request)