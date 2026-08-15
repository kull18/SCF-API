from fastapi import FastAPI
import uvicorn
from src.core.init_db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="SCF API", version="1.0.0", lifespan=lifespan)

@app.get("/")
def health():
    return {
        "status": "ok",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)