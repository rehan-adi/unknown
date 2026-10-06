import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.config import ENV_CONFIG
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


def start():
    print(
        f"Starting inference service on port {ENV_CONFIG.PORT} in {ENV_CONFIG.PYTHON_ENV} mode..."
    )
    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=ENV_CONFIG.PORT,
        reload=(ENV_CONFIG.PYTHON_ENV == "development"),
    )


if __name__ == "__main__":
    start()
