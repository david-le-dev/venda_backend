from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import analyze, export, health


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Bilingual reflective Vedic astrology API with streaming support.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api_cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(analyze.router, tags=["analyze"])
app.include_router(export.router, tags=["export"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "VedaTwin AI backend is running."}
