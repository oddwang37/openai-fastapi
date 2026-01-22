from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LLM_MODEL: str = "chatgpt-4o"
    LLM_API_KEY: str = "No key provided"
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    SYSTEM_MESSAGE: str = "You a helpful assistant"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
