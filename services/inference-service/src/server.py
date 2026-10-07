import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.config import ENV_CONFIG
from .routes.completions import completions_router
from .routes.health import health_router

if ENV_CONFIG.PYTHON_ENV != "development" and ENV_CONFIG.SENTRY_DSN:
    sentry_sdk.init(
        dsn=ENV_CONFIG.SENTRY_DSN,
        environment=ENV_CONFIG.PYTHON_ENV,
        traces_sample_rate=1.0,
    )
    print("Sentry initialized successfully")

app = FastAPI(
    title="Unknown Inference Service",
    description="Inference API serving local and hosted models.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1/health")
app.include_router(completions_router, prefix="/api/v1/chat")
