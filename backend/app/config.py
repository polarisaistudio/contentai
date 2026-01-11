# backend/app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "ContentAI API"
    debug: bool = False

    # LLM
    openai_api_key: str
    default_model: str = "gpt-4o-mini"
    max_tokens_default: int = 1000

    # Database
    database_url: str = "postgresql://localhost/contentai"

    # Rate Limiting
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
