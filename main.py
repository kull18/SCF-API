from fastapi import FastAPI
import uvicorn
from src.core.exceptions import ConflictError, ForbiddenError, NotFoundError, ValidationError
from src.core.init_db import init_db
from src.core.config import settings
from src.infrastructure.controllers import (
    AuthController,
    CentralOfficeController,
    UserController,
    EventController,
    EventPhotoController,
    EventCommentController,
    NotificationController,
) 
from contextlib import asynccontextmanager
from src.core.middlewares.auth_middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from src.core.middlewares.body_size_middleware import BodySizeLimitMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.core.middlewares.rate_limiter import limiter
from src.core.exception_handlers import (
    not_found_handler,
    conflict_handler,
    forbidden_handler,
    validation_handler,
    unhandled_exception_handler
)
from src.core.middlewares.error_handling_middleware import ErrorHandlingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="SCF API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.add_middleware(BodySizeLimitMiddleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(ConflictError, conflict_handler)
app.add_exception_handler(ForbiddenError, forbidden_handler)
app.add_exception_handler(ValidationError, validation_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(AuthMiddleware)

app.include_router(AuthController.router)
app.include_router(NotificationController.router)
app.include_router(EventCommentController.router)
app.include_router(CentralOfficeController.router)
app.include_router(UserController.router)
app.include_router(EventController.router)
app.include_router(EventPhotoController.router)

@app.get("/health", tags=["health"])
def health():
    return {
        "status": "ok",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)