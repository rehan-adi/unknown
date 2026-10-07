from pydantic_settings import BaseSettings, SettingsConfigDict


class ENV_CONFIG_SCHEMA(BaseSettings):
    PYTHON_ENV: str
    PORT: int

    SENTRY_DSN: str | None = None

    OLLAMA_URL: str

    LANGFUSE_PUBLIC_KEY: str | None = None
    LANGFUSE_SECRET_KEY: str | None = None
    LANGFUSE_HOST: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


ENV_CONFIG = ENV_CONFIG_SCHEMA()
