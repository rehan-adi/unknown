from pydantic_settings import BaseSettings, SettingsConfigDict


class ENV_CONFIG_SCHEMA(BaseSettings):
    DATABASE_URL: str

    INFERENCE_API_URL: str

    QDRANT_URL: str

    DLX_NAME: str
    QUEUE_NAME: str
    FANOUT_QUEUE_NAME: str
    RABBITMQ_URL: str

    R2_ACCOUNT_ID: str
    R2_BUCKET_NAME: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str

    SENTRY_DSN: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


ENV_CONFIG = ENV_CONFIG_SCHEMA()
