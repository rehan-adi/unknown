import asyncio
import logging
import random

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


# Resilience: If the server returns a 502/503 error, wait exponentially
# (2s, 4s, 8s) and retry up to 3 times before crashing the job.
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def fetch_url(url: str) -> str:
    # Polite Crawler Delay: To avoid getting IP-Banned by websites during Fan-Out,
    # we wait a random time (0.5s - 2.0s)
    delay = random.uniform(0.5, 2.0)
    logger.info(f"Polite crawler waiting {delay:.2f}s before fetching: {url}")
    await asyncio.sleep(delay)

    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.text
    except httpx.HTTPError as e:
        logger.warning(f"HTTP request failed for {url}, retrying if applicable. Error: {str(e)}")
        raise e
