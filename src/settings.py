import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    GROQ_API_KEY:str
    ELEVENLABS_API_KEY: str
    ELEVENLABS_VOICE_ID: str
    TOGETHER_API_KEY: str

    QDRANT_API_KEY:str | None
    QDRANT_URL:str

    TEXT_MODEL_NAME:str ="llama-3.3-70b-versatile"
    SMALL_TEXT_MODEL_NAME: str = "gemma2-9b-it"
    TTS_MODEL_NAME: str = "eleven_flash_v2_5"
    STT_MODEL_NAME: str = "whisper-large-v3-turbo"
    ITT_MODEL_NAME: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    TTI_MODEL_NAME: str = "black-forest-labs/FLUX.1-schnell-Free"

    ROUTER_MESSAGES_TO_ANALYZE: int = 3
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 5
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 20
    MEMORY_TOP_K: int = 3

    SHORT_TERM_MEMORY_DB_PATH: str = "memory.db"

settings=Settings()