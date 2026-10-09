import json
import logging

import aio_pika

from config.config import ENV_CONFIG

logger = logging.getLogger(__name__)


async def publish_job(job_payload: dict):
    connection = await aio_pika.connect_robust(ENV_CONFIG.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        message = aio_pika.Message(
            body=json.dumps(job_payload).encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await channel.default_exchange.publish(message, routing_key=ENV_CONFIG.FANOUT_QUEUE_NAME)
