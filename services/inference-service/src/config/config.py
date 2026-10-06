from pydantic_settings import BaseSettings, SettingsConfigDict


class ENV_CONFIG_SCHEMA(BaseSettings):
    PYTHON_ENV: str
    PORT: int

    SENTRY_DSN: str

    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_HOST: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


ENV_CONFIG = ENV_CONFIG_SCHEMA()
