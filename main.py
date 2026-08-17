from fastapi import FastAPI
import uvicorn
from src.core.init_db import init_db
from src.infrastructure.controllers import (
    AuthController,
    CentralOfficeController,
    UserController,
    EventController,
    EventPhotoController,
    EventCommentController,
)
from contextlib import asynccontextmanager
from src.core.middlewares.auth_middleware import AuthMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="SCF API", version="1.0.0", lifespan=lifespan)

app.add_middleware(AuthMiddleware)

app.include_router(AuthController.router)
app.include_router(EventCommentController.router)
app.include_router(CentralOfficeController.router)
app.include_router(UserController.router)
app.include_router(EventController.router)
app.include_router(EventPhotoController.router)

@app.get("/")
def health():
    return {
        "status": "ok",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)