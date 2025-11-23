from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None,
    OPENAI_MODEL: str = "gpt-4o-mini"
    CHIRON_LOG_LEVEL: str = "INFO"
    LLM_ENABLE_FALLBACK: bool = False
    PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
