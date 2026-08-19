import jwt
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.services.token_service import decode_access_token
from src.core.session import AsyncSessionLocal
from src.infrastructure.repositories.RevokedTokenRepository import RevokedTokenRepository

PUBLIC_PATHS = {
    "/auth/login",
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path in PUBLIC_PATHS or request.method == "OPTIONS":
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid Authorization header"},
            )

        token = auth_header.removeprefix("Bearer ").strip()

        try:
            payload = decode_access_token(token)
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        jti = payload.get("jti")
        if jti is not None:
            async with AsyncSessionLocal() as session:
                repository = RevokedTokenRepository(session)
                if await repository.is_revoked(jti):
                    return JSONResponse(
                        status_code=401, content={"detail": "Token has been revoked"}
                    )

        request.state.technician_code = payload.get("sub")
        request.state.role = payload.get("role")
        request.state.jti = payload.get("jti")
        request.state.token_exp = payload.get("exp")

        return await call_next(request)