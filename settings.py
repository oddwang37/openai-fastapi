from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_KEY: str
    OLLAMA_KEY: str
    SYSTEM_MESSAGE: str = (
        "You a helpful assistant who must answer only on questions about Naruto"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
