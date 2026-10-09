import asyncio
import logging

import sentry_sdk

from config.config import ENV_CONFIG
from libs.rabbitmq.client import start_consumer
from processor.processor import process_job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if ENV_CONFIG.SENTRY_DSN:
    sentry_sdk.init(
        dsn=ENV_CONFIG.SENTRY_DSN,
        traces_sample_rate=1.0,
    )
    logger.info("Sentry initialized successfully.")


def run_worker():
    logger.info("Starting worker service...")
    try:
        asyncio.run(start_consumer(ENV_CONFIG.QUEUE_NAME, process_job))
    except KeyboardInterrupt:
        logger.info("Worker service stopped cleanly.")
