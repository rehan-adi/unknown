import asyncio
import logging
from typing import Awaitable, Callable

import aio_pika

from config.config import ENV_CONFIG

logger = logging.getLogger(__name__)


async def start_consumer(
    queue_name: str, callback: Callable[[aio_pika.abc.AbstractIncomingMessage], Awaitable[None]]
):
    logger.info("Connecting to RabbitMQ...")
    connection = await aio_pika.connect_robust(ENV_CONFIG.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        dlx = await channel.declare_exchange(ENV_CONFIG.DLX_NAME, aio_pika.ExchangeType.FANOUT)
        dlq = await channel.declare_queue(ENV_CONFIG.DLX_NAME + "_queue", durable=True)
        await dlq.bind(dlx)

        queue = await channel.declare_queue(
            queue_name, durable=True, arguments={"x-dead-letter-exchange": ENV_CONFIG.DLX_NAME}
        )

        await channel.set_qos(prefetch_count=1)

        logger.info(f"Worker successfully connected and listening on queue '{queue_name}'...")
        await queue.consume(callback)
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("Shutting down consumer...")
