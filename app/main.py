from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import settings
from .routes import router

app = FastAPI(title="User CRUD API", version="1.0.0")
app.include_router(router)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
