from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    LLM_PROXY_URL: str
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"

    model_config = SettingsConfigDict(
        env_file='chatbot/config/.env',
        extra='ignore',
    )

settings = Settings()