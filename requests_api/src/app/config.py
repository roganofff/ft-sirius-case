from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    CLICKHOUSE_DB: str
    SIMILARITY_THRESHOLD: float
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"

    class Config:
        env_file = "requests_api/.env"

settings = Settings()