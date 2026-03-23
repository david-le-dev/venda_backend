from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    app_name: str = "VedaTwin AI"
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"
    api_cors_origins: str = "*"

    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-pro"
    gemini_vision_model: str = "gemini-2.5-pro"

    chroma_persist_dir: str = "./chromadb"
    rag_collection_name: str = "vedic_knowledge"
    enable_rag: bool = True
    enable_face_analysis: bool = True
    enable_palm_analysis: bool = True
    enable_pdf_export: bool = True

    default_language: str = "en"
    stream_heartbeat_seconds: int = 10
    stream_chunk_size: int = 260
    max_image_bytes: int = 5_000_000

    model_config = SettingsConfigDict(
        env_file=(str(BACKEND_DIR / ".env"), str(ROOT_DIR / ".env")),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
