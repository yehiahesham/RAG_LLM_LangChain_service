from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "local"

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    TOP_K: int = 5
    SIM_THRESHOLD: float = 0.1

    TEMPERATURE: float = 0.0
    MAX_RETRIES: int = 2

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    class Config:
        env_file = ".env"


settings = Settings()