from fastapi import FastAPI
import uvicorn
from src.core.init_db import init_db
from src.infrastructure.controllers import (
    AuthController,
    CentralOfficeController,
    UserController,
    EventController,
    EventPhotoController,
)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="SCF API", version="1.0.0", lifespan=lifespan)

app.include_router(AuthController.router)
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
    uvicorn.run(app, host="127.0.0.1", port=8000)